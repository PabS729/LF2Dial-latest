from openai import OpenAI
from contradict_app.def_logical_fallacy import *
import json
import copy
from prompts_toulmin import * 
import argparse
import pandas as pd
from persona_roleplay.prompts_roleplay import *
from persona_roleplay.respond_role import *
from strategy_handle import * 
from Intent_prompts import *
from fsm_prompts import *
import random


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_to_annotate", type=str, default='pos_train_set.csv')
    parser.add_argument("--components_to_read", type=str, default='decomposed_sentences_toulmin.xlsx')
    parser.add_argument("--definition", type=str, default='proposed')
    parser.add_argument("--use_banks", type=bool, default=True)
    parser.add_argument("--use_toulmin", type=bool, default=False)
    parser.add_argument("--use_FSM", type=bool, default=True)
    parser.add_argument("--save_fn", type=str, default='results/fsm_0127_89_all_3con')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=0)
    
    args = parser.parse_args()

    df_to_argue = pd.read_csv(args.file_to_annotate)
    sampled_df = df_to_argue.groupby('Label').sample(n=3, random_state=89)
    
    # df_lf = pd.read_csv
    # df_components = pd.read_excel(args.components_to_read)
    # sampled_df = df_to_argue.loc[df_to_argue["updated_label"] == "ad populum"].sample(n=1, random_state=15)
    # strategy = strategy_dc_commonsense["fallacy of credibility"]
    # strategy = emo_alt
    sentences = sampled_df["Context"].values.tolist()
    labels = sampled_df["Label"].values.tolist()
    # sentences = ["In fact, it's starting to fall apart not because of lawsuits -- though they are a problem, and John Edwards and I are committed to fixing them -- but because of the larger issue that we don't cover Americans."]
    # labels =["false causality"]
    model_student = "gpt-4o"
    model_teacher = "gpt-4o"
    model_agent = model_teacher
    sampled_sentence = []
    sampled_labels = []

    conversation_teacher = []
    conversation_student = []
    sums = []
    anas = []
    pfs = []
    chats = []
    reles = []
    coll_agr = []
    coll_bank = []
    lm_thought = []
    STS = ["1", "2", "3", "4"]
    following = []
    all_states = []
    rs = []
    
    

    def appends(a, b, c, d, e, f, g, h, i, j, k):
        conversation_teacher.append(a)
        conversation_student.append(b)
        anas.append(c)
        lm_thought.append(d)
        sums.append(e)
        reles.append(f)
        cp_agr = copy.deepcopy(g)
        cp_disagr = copy.deepcopy(h)
        coll_bank.append(cp_disagr)
        coll_agr.append(cp_agr)
        following.append(i)
        all_states.append(j)
        rs.append(k)

    def construct_context(conv_t, conv_s, start, stop):
        context_history = ''
        for j in range(start, stop):
            context_history += "teacher: " + conv_t[j] + "\n" + "student: " + conv_s[j] + "\n"
        return context_history

    for j in range(len(sentences)):
        example_sentence = sentences[j]
        example_label = labels[j]
        agreement_bank = []
        print(example_sentence)

        #Generates toulmin Decomposition of sentence.
        if args.use_toulmin:
            toulmin_res = await generate_res("gen_strategy", model_student, example_sentence, 
                                                    None, None, None, None, None, PROMPT_DECOMPOSE_TOULMIN, 0)
            toulmin = json.loads(toulmin_res.choices[0].message.content)
            print(toulmin)

            opening_res = await generate_res("conv", model_teacher, example_sentence, 
                                                    None, None, None, None, None, PROMPT_OPENING, 0)
            appends(opening_res.choices[0].message.content, STUDENT_RESPONDS, "", "", "", "", [], [], '0', '0', '0')

        rounds = 10
        chat_history = ""
        full_chat = ""
        summary = ""
        agr_bank = []

        #Check if student agrees with the components. Ideally, the student should agree with all of them.
        
        # for k in toulmin.keys():
        if True:
            conv_teacher = []
            conv_student =[]
            count_states = {"1":0,"2":0,"3":0,"4":0,"5":0}
            if args.use_toulmin:
                # decomp = toulmin[k]
                # print(decomp)
            # teacher_res = await generate_res("t", model_teacher, example_sentence, "["+ k + ": " + decomp + "]", None, None, conv_teacher, conv_student, PROMPT_JUDGEMENT, 0)
            
            #Teacher check the logical validity of sentence, and ask the student if they agree with the judgement
                teacher_res = await generate_res("", model_teacher, example_sentence, toulmin, None, None, conv_teacher, conv_student, PROMPT_JUDGEMENT, 0)
                teacher_r = json.loads(teacher_res.choices[0].message.content)
                flaw_part = teacher_r["2"]
                teacher_res = teacher_r["1"]
            else:
                teacher_res = await generate_res("teacher", model_teacher, example_sentence, None, None, None, conv_teacher, conv_student, PROMPT_TEACHER_ARGUE_No_CoT, 0)
                teacher_res = teacher_res.choices[0].message.content
            conv_teacher.append(teacher_res)
            utterance_teacher = teacher_res
            print(utterance_teacher)
            # student_res = await generate_res("student_bio", model_teacher, example_sentence, "["+ k + ": " + decomp + "]", None, None, conv_teacher, conv_student, PROMPT_STUDENT_RESPOND, 0)
            
            #student responds. 
            if args.use_toulmin:
                student_res = await generate_res("student_bio", model_teacher, example_sentence, toulmin, None, None, conv_teacher, conv_student, PROMPT_STUDENT_RESPOND, 0)
            else:
                student_res = await generate_res("student", model_teacher, example_sentence, None, None, None, conv_teacher, conv_student, PROMPT_STUDENT_STUBBORN, 0)
            utterance_student = student_res.choices[0].message.content
            conv_student.append(utterance_student)
            
            print(utterance_student)
            appends(utterance_teacher, utterance_student, "", "", "", "", [], [], '0', '0', '0')
            # agr_bank.append()

            #If yes, end conversation
            if "yes" in student_res.choices[0].message.content.lower():
                print("initial agreement")
                if args.use_banks:
                    agr_bank.append(conv_teacher[-1])
                continue

            # if no, enter debate
            else: 
                tmp = conv_teacher[-1]
                disagr_bank = []
                #if the student disagrees, enter discussion
                #starts at state 3 since it is a neutral state
                curr_state = "3"
                FSM_STATES = [curr_state]
                start_student_strategy = "None"
                cs = {"1": "no", "2": "no"}
                context_history = ''
                
                for i in range(0, rounds):
                    # print(i)
                    if i == 0:
                        sampled_sentence.append(example_sentence)
                        sampled_labels.append(example_label)

                        thought = "D"
                        reles.append("")
                        coll_bank.append([])
                        # coll_agr.append([])
                    else: 
                        
                        sampled_sentence.append("")
                        sampled_labels.append("")

                        #checks the relevance and potential repetition of the student's response
                        thought = 0
                        if args.use_banks:
                            relevance_res = await generate_res("check", model_teacher, example_sentence, disagr_bank, 
                                                               utterance_student, agr_bank, None, None, PROMPT_CHECK_DISAGREEMENT, 0)
                            relevance = json.loads(relevance_res.choices[0].message.content)
                            print(relevance)
                            reles.append(relevance)

                            if "yes" in relevance["Q2"].lower(): 
                                disagr_bank.append(relevance["Q2"])

                                confirm_disagreement = "It seems that our current disagreement lies on this point:" + relevance["Q2"][4:].lower()+ ", do you agree? If yes, then we can focus our discussion on this part." 
                                print(confirm_disagreement)
                                student_res = await generate_res("ag", model_teacher, relevance["Q2"][4:].lower(), chat_history, None, None, None, None, PROMPT_STUDENT_CONFIRM, 0)
                                student_res = student_res.choices[0].message.content
                                
                                print(student_res)
                                
                                # conv_teacher.append(confirm_disagreement)
                                # conv_student.append(student_res)
                                appends(confirm_disagreement, student_res, "", "", "", "", agr_bank, disagr_bank, '0', '0', '0')
                                
                                if "yes" in student_res.lower():
                                    a = 0
                                else:
                                    ta = "Can you tell me which point you don't agree with?"
                                    conv_teacher.append(ta)
                                    student_utterance = await generate_res("stu", model_teacher, example_sentence, None, None, None, conv_teacher, conv_student, PROMPT_STUDENT_ARGUE_STRAT, 0)
                                    student_u = json.loads(student_utterance.choices[0].message.content)
                                    student_utterance = student_u["res"]
                                    print(student_u["option"])
                                    print(student_utterance)
                                    
                                    conv_student.append(student_utterance)

                                    conversation_teacher.append(ta)
                                    conversation_student.append(student_utterance)
                                    anas.append("")
                                    lm_thought.append("")
                                    sums.append("")
                                    # reles.append("")                                
                                    cp_agr = copy.deepcopy(agr_bank)
                                    cp_disagr = copy.deepcopy(disagr_bank)
                                    coll_bank.append(cp_disagr)
                                    coll_agr.append(cp_agr)
                                    following.append('0')
                                    all_states.append('0')
                                    rs.append('0')
                                    continue

                            #if the student's response is not addressed previously, then we have a new topic. Identify the student's states to be used later
                            if "yes" in relevance["Q1"].lower() and "no" in relevance["Q3"].lower():
                                agreement_bank.append(relevance)
                                # disagr_bank.append(relevance)

                                thought_res = await generate_res("strategy", model_teacher, example_sentence, chat_history, 
                                                                 None, None, None, None, DETECT_FLAW_TEACHER, 0)

                                thought = json.loads(thought_res.choices[0].message.content)["Type"]
                            elif "yes" in relevance["Q3"].lower(): 
                                thought = 7
                            else:
                                thought = 2
                            
                            #add to disagreement bank if new disagreement is proposed
                            cp_bank = copy.deepcopy(disagr_bank)
                            coll_bank.append(cp_bank)
                        
                            print(thought)
                        elif args.use_FSM:
                            thought_res = await generate_res("strategy", model_teacher, example_sentence, chat_history, 
                                                                 None, None, None, None, PROMPT_IDENTIFY_STUDENT_STATE, 0)
                            thought = json.loads(thought_res.choices[0].message.content)["Type"]
                            reles.append("")
                            coll_bank.append([])
                            print(thought)
                        else:
                            reles.append("")
                            coll_bank.append([])
                        
                        
                
                    lm_thought.append('')
                    anas.append(thought)
                    print(disagr_bank)

                    if i == 0 and args.use_toulmin:
                        #teacher's initial analysis and judgement of the sentence
                        teacher_res = await generate_res("tea", model_teacher, example_sentence, toulmin, None, None, conv_teacher, conv_student, PROMPT_TALK_ABOUT_LF, 0)
                        summary = ""
                    elif args.use_FSM and (thought == 7):
                        print("taken")

                        #teacher's response when the student is repeating topics that has been previously discussed
                        teacher_res = await generate_res("teacher_st", model_teacher, example_sentence, summary, relevance["Q3"], None, [], conv_student[-1], PROMPT_REMIND_FOCUSED, 0)
                    elif args.use_FSM:
                        #teacher's response according to detected student behavior
                        # teacher_res = await generate_res("test", model_teacher, example_sentence, BEHAVIORS[str(thought)], option, None, conv_teacher, conv_student, PROCEED_CONV_TEACHER, 1)
                        #transition to next state
                        # transition_res = await generate_res("agent", model_teacher, example_sentence, chat_history, None, None, None, None, TRANSITION_STATES + TRANSITIONS[curr_state], 1)
                        # tr_res = json.loads(transition_res.choices[0].message.content)
                        # next_state = str(tr_res["ans"]) 
                        # if next_state not in STS:
                        #     next_state = STS[3]

                        # print("before random generation: " + next_state)
                        # print(tr_res["rs"])
                        transition = await generate_res("agent", model_teacher, example_sentence, chat_history, None, None, None, None, CHECK_RESPONSE_TEACHER, 1)
                        transition = json.loads(transition.choices[0].message.content)
                        print(transition)
                        #In terms of precedence: request >> assumption (completeness) > examples (evidence) >= logical flaw (attacking point)
                        if "yes" in transition["3"].lower():
                            next_state = "3"
                        elif 'yes' not in cs['2'].lower() and i != 0:
                            next_state = '5'
                        # else: 
                        #     tmp = []
                        #     for k in STS:
                        #         if "yes" in transition[k]:
                        #             tmp.append(k)
                        #     if len(tmp) != 0:
                        #         rds = random.randint(1,len(tmp)) 
                        #         next_state = tmp[rds - 1]
                        #     else:
                        #         next_state = "2"
                        elif "yes" in transition["1"].lower():
                            next_state = "1"
                        elif "yes" in transition["5"].lower():
                            next_state = "2"
                        elif "yes" in transition["4"].lower():
                            next_state = "4"
                        
                        else:
                            next_state = "2"

                        count_states[next_state] += 1
                        tmp_s = next_state
                        print(count_states)
                        print("before random generation: " + next_state)

                        if len(FSM_STATES) >= 3 and FSM_STATES[-2] == FSM_STATES[-1] and FSM_STATES[-1] == next_state and next_state != "3":
                            new_sts = [i for i in STS if(i != next_state or i != "3") ]
                            # print("new states: " + new_sts)
                            rds = random.randint(0,1)   
                            next_state = new_sts[rds]
                            count_states[next_state] += 1
                            count_states[tmp_s] -= 1

                        if "yes" in transition["1"].lower() and count_states["1"] >= count_states["4"] * 2 and count_states["4"] >= 0 and next_state != "3":
                            next_state = "4"
                            count_states[next_state] += 1
                            count_states[tmp_s] -= 1
                            if count_states["1"] >= count_states["2"] * 3 or count_states["4"] >= count_states["2"] * 2:
                                next_state = "2"
                                count_states[next_state] += 1
                                count_states['4'] -= 1
                        
                        if next_state != curr_state:
                            print("-----------------transitioning--------------------" + "from " + curr_state + " to " + next_state)
                        print("next state is: "+ next_state)
                        # if "yes" in transition["5"].lower():
                        #     utterance_teacher = "It seems that you have not responded to my previous request. Would you please answer my question first, before proposing further arguments or requests?"
                        # else:
                        if len(conv_teacher) >= 4:
                            prompt = PROMPT_CTX + summary + STRAT_FOR_STATES[next_state] + TEACHER_ACT_2
                            conv_t = conv_teacher[-3:]
                            print(conv_t)
                            conv_s = conv_student[-3:]
                        else:
                            prompt = TEACHER_ACT_1 + STRAT_FOR_STATES[next_state] + TEACHER_ACT_2
                            conv_t = conv_teacher
                            conv_s = conv_student

                        teacher_res = await generate_res("teacher", model_teacher, example_sentence, None, None, None, conv_t, conv_s, prompt, 1)
                        
                        curr_state = next_state
                        FSM_STATES.append(curr_state)

                        check_following_res = await generate_res("eval_s", model_teacher, example_sentence, teacher_res.choices[0].message.content, STRAT_FOR_STATES[next_state], None, None, None, CHECK_FOLLOW_FSM_AGENT, 0)
                        cs = json.loads(check_following_res.choices[0].message.content)
                        print("is the teacher following the transition? " + cs['1'])
                        print("is the teacher's question relevant? " + cs['2'])
                        following.append(cs['1'])
                        all_states.append(next_state)
                        rs.append(cs['2'])
                    elif args.use_toulmin:
                        print("cont toulmin")
                        teacher_res = await generate_res("tea", model_teacher, example_sentence, toulmin, None, None, conv_teacher, conv_student, PROMPT_TALK_ABOUT_LF_CONV, 0)
                    else:
                        teacher_res = await generate_res("teacher", model_teacher, example_sentence, None, None, None, conv_teacher, conv_student, PROMPT_TEACHER_ARGUE_No_CoT, 0)

                    chat_history = ""

                    utterance_teacher = teacher_res.choices[0].message.content
                    chat_history += "teacher: " + utterance_teacher + "\n"
                    
                    conversation_teacher.append(utterance_teacher)
                    conv_teacher.append(utterance_teacher)
                    
                    #summarizes the teacher's responses


                    
                    print("--------------------utterance--------------------")
                    print(utterance_teacher)
                    utterance_student = await generate_res("stu", model_teacher, example_sentence, start_student_strategy, None, None, conv_teacher, conv_student, PROMPT_STUDENT_ARGUE_STRAT, 0)
                    student_u = json.loads(utterance_student.choices[0].message.content)
                    utterance_student = student_u["res"]
                    print("student strategy:"+student_u["option"])
                    print(utterance_student)
                    start_student_strategy = student_u["option"]

                    # print(utterance_student)
                    conversation_student.append(utterance_student)
                    conv_student.append(utterance_student)
                    
                    print("--------------------------segmentation line------------------------------")
        
                    chat_history += "student: " + utterance_student + "\n"
                    if len(conv_teacher) >= 4:
                        start = 0 if len(conv_teacher) - 7 < 0 else len(conv_teacher) - 7
                        stop = len(conv_teacher) - 3
                        context = construct_context(conv_teacher, conv_student, start, stop)
                        summary = await generate_res("sum", model_teacher, example_sentence, context, None, None, None, None, PROMPT_SUMMARIZE, 0)
                        summary = summary.choices[0].message.content
                        print(summary)
                        if i == 0:
                            agreement_bank.append(summary)
                        sums.append(summary)
                    else:
                        sums.append('')
                    # print(following,all_states)


                    # agree_res = await generate_res("eval_s", model_student, example_sentence, chat_history, None, None, None, None, PROMPT_AGENT_CHECK_AGREEMENT, 0)
                    # agr = json.loads(agree_res.choices[0].message.content)
                    # print(agr)
                    # if "yes" in agr["1"].lower():
                    #     if len(disagr_bank) != 0:
                    #         agr_bank.append(disagr_bank[- 1])
                    #         del disagr_bank[ - 1]
                    #     if "yes" in agr["2"].lower():
                    #         break
                    #check whether the student agrees with the teacher
                    agent_res = await generate_res("eval_s", model_student, example_sentence, chat_history, None, None, None, None, PROMPT_AGENT_CHECK_EVIDENCE, 0)
                    res = json.loads(agent_res.choices[0].message.content)
                    print(res)

                    cp_agr = copy.deepcopy(agr_bank)
                    coll_agr.append(cp_agr)
                    print(cp_agr)
                    full_chat += chat_history
                    if "yes" in res["1"].lower() and "yes" in res["2"].lower():
                        print("student unable to defend their argument")
                        if args.use_banks:
                            if len(disagr_bank) != 0:
                                agr_bank.append(disagr_bank[- 1])
                                del disagr_bank[ - 1]
                        confirm_disagreement = "If you cannot provide any evidence at all, then I would suggest looking for them if you have time later. Do you still have any other concerns regarding the sentence's logical validity?" 
                        print(confirm_disagreement)
                        conv_teacher.append(confirm_disagreement)
                        student_utterance = await generate_res("stu", model_teacher, example_sentence, start_student_strategy, None, None, conv_teacher, conv_student, PROMPT_STUDENT_ARGUE_STRAT, 0)
                        student_u = json.loads(student_utterance.choices[0].message.content)
                        utterance_student = student_u["res"]
                        print("student strategy:"+student_u["option"])
                        print(utterance_student)
                        start_student_strategy = student_u["option"]
                        conv_student.append(utterance_student)
                        appends(confirm_disagreement, utterance_student, "", "", "", "", agr_bank, disagr_bank,'0','0', '0')
                        

        chats.append(full_chat)


    print(len(lm_thought), len(anas), len(conversation_teacher), len(conversation_student), len(sums), len(reles), len(coll_agr), len(coll_bank), len(all_states), len(following), len(rs))
    print(FSM_STATES)
    data_dict = {
                 'teacher_analysis': anas,
                #  'layman_thought': lm_thought, 
                 'teacher_response': conversation_teacher, 
                 'layman_response': conversation_student, 
                #  'tracker': agr,
                 'summary': sums,
                 'student_check_relevance': reles,
                 'disagreement_bank': coll_bank,
                 'agreement_bank': coll_agr,

                }
    if args.use_FSM:
            data_dict['states'] = all_states
            data_dict['following'] = following
            data_dict['relevance_teacher_res'] = rs
    df_result = pd.DataFrame(data_dict)
    df_result.to_excel(args.save_fn + str(args.num_gen) + ".xlsx", index=False)

    df_chats = pd.DataFrame({ "sentences": sentences, "chats": chats})
    df_chats.to_excel("chat_history_" + args.save_fn + ".xlsx", index=False)
    print("done async")


if __name__ == '__main__':
    asyncio.run(main())
