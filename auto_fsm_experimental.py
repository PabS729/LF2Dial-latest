from openai import OpenAI
from contradict_app.def_logical_fallacy import *
import json
import copy
from prompts_toulmin import * 
import argparse
import pandas as pd
from persona_roleplay.prompts_roleplay import *
from persona_roleplay.respond_role import *
from Intent_prompts import *
from prompt_fsm_experimental import *
import random


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_to_annotate", type=str, default='st_wo_duplicates.csv')
    parser.add_argument("--components_to_read", type=str, default='decomposed_sentences_toulmin.xlsx')
    parser.add_argument("--use_diverge", type=bool, default=False)
    parser.add_argument("--use_edu", type=bool, default=False)
    parser.add_argument("--use_nm_debate", type=bool, default=False)
    parser.add_argument("--use_banks", type=bool, default=False)
    parser.add_argument("--use_adv", type=bool, default=True)
    parser.add_argument("--use_toulmin", type=bool, default=False)
    parser.add_argument("--use_FSM", type=bool, default=True)
    parser.add_argument("--save_fn", type=str, default='results/0424_gui_fsm_1025')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=0)
    
    args = parser.parse_args()

    df_to_argue = pd.read_csv(args.file_to_annotate)
    sampled_df = df_to_argue.sample(n=1, random_state=25)
    # sampled_df = df_to_argue
    # sampled_df = df_to_argue["Context"].values.tolist()
    # labels = df_to_argue["Label"].values.tolist()
    # df_lf = pd.read_csv
    # df_components = pd.read_excel(args.components_to_read)
    # sampled_df = df_to_argue.loc[df_to_argue["updated_label"] == "ad populum"].sample(n=1, random_state=15)
    # strategy = strategy_dc_commonsense["fallacy of credibility"]
    # strategy = emo_alt
    sentences = sampled_df["Context"].values.tolist()
    # labels = sampled_df["Label"].values.tolist()
    # sentences = sampled_df[args.num_gen:args.num_gen+100]
    # sentences = set(sentences)
    # sentences = list(sentences)[150:172]
    # labels = labels[1000:1300]
    
    model_student = "gpt-4o"
    model_teacher = "gpt-4o"
    # model_teacher = "deepseek-reasoner"
    # model_teacher = "deepseek-r1"
    model_agent = "gpt-4o-mini"
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

    ADV_PROMPT = [PROMPT_STUDENT_ADV_DIVERT, PROMPT_STUDENT_ADV_PERSUASION, PROMPT_STUDENT_ADV_REPETITION, PROMPT_STUDENT_ADV_CONTEXT, PROMPT_STUDENT_ADV_TERMS, PROMPT_STUDENT_ADV_GUIDANCE]
    
    adv_p = ADV_PROMPT[-1]
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

    for j in range(len(sentences)):
        example_sentence = sentences[j]
        # example_label = labels[j]
        agreement_bank = []
        disagr_bank = []
        print(example_sentence)

        # Generates toulmin Decomposition of sentence.
        # toulmin_res = await generate_res("gen_strategy", model_teacher, example_sentence, 
        #                                             None, None, None, None, None, PROMPT_DECOMPOSE_TOULMIN, 0)
        # toulmin = json.loads(toulmin_res.choices[0].message.content)
        # print(toulmin)
        # for k in toulmin.keys():
        #     disagr_bank.append(toulmin[k])
        if args.use_toulmin:
            toulmin_res = await generate_res("gen_strategy", model_teacher, example_sentence, 
                                                    None, None, None, None, None, PROMPT_DECOMPOSE_TOULMIN, 0)
            toulmin = load_json(toulmin_res.choices[0].message.content)
            while toulmin == False:
                toulmin_res = await generate_res("gen_strategy", model_teacher, example_sentence, 
                                                    None, None, None, None, None, PROMPT_DECOMPOSE_TOULMIN, 0)
                toulmin = load_json(toulmin_res.choices[0].message.content)
            print(toulmin)
            # for k in toulmin.keys():
            #     disagr_bank.append(toulmin[k])

            # opening_res = await generate_res("conv", model_student, example_sentence, 
            #                                         None, None, None, None, None, PROMPT_OPENING, 0)
            # appends(opening_res.choices[0].message.content, STUDENT_RESPONDS, "", "", "", "", [], [], '0', '0', '0')

        rounds = 10
        chat_history = ""
        full_chat = ""
        summary = ""
        agr_bank = []
        conv_teacher = []
        conv_student = []
        count_states = {"1":0,"2":0,"3":0,"4":0,"5":0}
        #Check if student agrees with the components. Ideally, the student should agree with all of them.
        
        # for k in toulmin.keys():
        if True:
            if args.use_FSM:
                teacher_res = await generate_res("teacher", model_teacher, example_sentence, None, None, None, conv_teacher, conv_student, OPENING_PROMPT, 0)
            else:
                teacher_res = await generate_res("teacher", model_teacher, example_sentence, None, None, None, conv_teacher, conv_student, PROMPT_TEACHER_ARGUE_DS, 0)
            # teacher_res = await generate_res("teacher", model_teacher, example_sentence, None, None, None, conv_teacher, conv_student, PROMPT_TEACHER_ARGUE_BASELINE, 0)
            teacher_res = teacher_res.choices[0].message.content
            conv_teacher.append(teacher_res)
            utterance_teacher = teacher_res
            print(utterance_teacher)

            
            # student_res = await generate_res("student_bio", model_teacher, example_sentence, "["+ k + ": " + decomp + "]", None, None, conv_teacher, conv_student, PROMPT_STUDENT_RESPOND, 0)
            
            #student responds. 
            if args.use_toulmin:
                student_res = await generate_res("student_bio", model_student, example_sentence, toulmin, None, None, conv_teacher, conv_student, PROMPT_STUDENT_RESPOND, 0)
            elif args.use_adv:
                student_res = await generate_res("stu", model_student, example_sentence, "", None, None, conv_teacher, conv_student, adv_p, 0)
                student_u = load_json(student_res.choices[0].message.content)
                while student_u == False:
                    utterance_student = await generate_res("stu", model_student, example_sentence, start_student_strategy, None, None, conv_teacher, conv_student, adv_p, 0)
                    student_u = load_json(utterance_student.choices[0].message.content)
            else:
                student_res = await generate_res("stu", model_student, example_sentence, "request the teacher to provide examples that support their claim", None, None, conv_teacher, conv_student, PROMPT_STUDENT_ARGUE_NORMAL + PT_2, 0)
                student_u = load_json(student_res.choices[0].message.content)
                while student_u == False:
                    utterance_student = await generate_res("stu", model_student, example_sentence, start_student_strategy, None, None, conv_teacher, conv_student, PROMPT_STUDENT_ARGUE_NORMAL + PT_2, 0)
                    student_u = load_json(utterance_student.choices[0].message.content)
            
            utterance_student = student_u["res"]
            chat_history = "teacher: " + utterance_teacher + "\n" + "student: " + utterance_student  
            conv_student.append(utterance_student)
            full_chat += "teacher: " + utterance_teacher + "\n"
            full_chat += "student: " + utterance_student + "\n"
            
            print(utterance_student)
            anas.append("")
            lm_thought.append("")
            sums.append("")
            reles.append("")
            coll_bank.append([])
            conversation_teacher.append(utterance_teacher)
            conversation_student.append(utterance_student)
            cp_agr = copy.deepcopy(agr_bank)
            coll_agr.append(cp_agr)
            following.append('0')
            all_states.append('0')
            rs.append('0')
            # agr_bank.append()

            #If yes, end conversation
            if "yes" in student_res.choices[0].message.content.lower():
                print("initial agreement")
                if args.use_banks:
                    agr_bank.append(conv_teacher[-1])

            # if no, enter debate
            else: 
                tmp = conv_teacher[-1]
                
                #if the student disagrees, enter discussion
                #starts at state 3 since it is a neutral state
                curr_state = "3"
                FSM_STATES = [curr_state]
                start_student_strategy = "None"
                cs = {"1": "no", "2": "no"}
                for i in range(0, rounds):
                    # print(i)
                    
                    if i == 0:
                        sampled_sentence.append(example_sentence)
                        # sampled_labels.append(example_label)

                        thought = "D"
                        reles.append("")
                        coll_bank.append([])
                        # coll_agr.append([])
                    else: 
                        
                        sampled_sentence.append("")
                        # sampled_labels.append("")

                        #checks the relevance and potential repetition of the student's response
                        thought = 0
                        if args.use_banks:
                            relevance_res = await generate_res("check", model_agent, example_sentence, disagr_bank, 
                                                               chat_history, agr_bank, None, None, PROMPT_CHECK_RELEVANCE_AGENT, 0)
                            relevance = load_json(relevance_res.choices[0].message.content)
                            while relevance == False:
                                relevance_res = await generate_res("check", model_agent, example_sentence, disagr_bank, 
                                                               chat_history, agr_bank, None, None, PROMPT_CHECK_RELEVANCE_AGENT, 0)
                                relevance = load_json(relevance_res.choices[0].message.content)

                            print("relevance check: ", relevance)
                            reles.append(relevance)

                            if "yes" not in relevance["Q1"].lower():
                                thought = 6
                            elif "yes" in relevance["Q4"]:
                                thought = 7
                            elif "yes" not in relevance["Q2"].lower(): 
                                disagr_bank.append(relevance["Q1"])

                                #Maybe instead of asking for agreement, the teacher should dictate the contents of the conversation by stating the specific parts of the toulmin's model that they are discussing. 

                                confirm_disagreement = "It seems that we have different opinions on this: " + relevance["Q1"][4:].lower()+ ", do you agree? If yes, then we can focus our discussion on this part." 
                                # print(confirm_disagreement)
                                # student_res = await generate_res("ag", model_student, relevance["Q1"][4:].lower(), chat_history, None, None, conv_teacher, conv_student, PROMPT_STUDENT_CONFIRM_TOUL, 0)
                                # student_res = student_res.choices[0].message.content
                                # print(student_res)
                                student_res = "yes"
                                # conv_teacher.append(confirm_disagreement)
                                # conv_student.append(student_res)
                                # conversation_teacher.append(confirm_disagreement)
                                # conversation_student.append(student_res)
                                appends(confirm_disagreement, student_res, "", "", "", "", agr_bank, disagr_bank, '0', '0', '0')
                                if "yes" in student_res.lower():
                                    a = 0
                                else:
                                    print("Can you tell me which point you don't agree with?")
                                    student_utterance = await generate_res("stu", model_student, example_sentence, None, None, None, conv_teacher, conv_student, PROMPT_STUDENT_ARGUE_STRAT + PT_2, 0)
                                    student_u = load_json(student_utterance.choices[0].message.content)
                                    while student_u == False:
                                        student_utterance = await generate_res("stu", model_student, example_sentence, None, None, None, conv_teacher, conv_student, PROMPT_STUDENT_ARGUE_STRAT + PT_2, 0)
                                        student_u = load_json(student_utterance.choices[0].message.content)

                                    student_utterance = student_u["res"]
                                    print(student_u["option"])
                                    print(student_utterance)
                                    conv_teacher.append("Can you tell me which point you don't agree with?")
                                    conv_student.append(student_utterance)
                                    conversation_teacher.append("Can you tell me which point you don't agree with?")
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
                            # elif "yes" in relevance["Q1"].lower() and "yes" not in relevance["Q2"].lower():
                            #     # agreement_bank.append(relevance)
                            #     disagr_bank.append(relevance["Q1"])
                            #     a = ""
                            #     thought = 5

                            elif "yes" not in relevance["Q4"] and "yes" in relevance["Q5"]:
                                disagr_bank.append(relevance["Q5"])
                                # thought = 7
                            
                            elif "yes" in relevance["Q3"].lower(): 
                                thought = 7
                            else:
                                thought = 2
                            
                            #add to disagreement bank if new disagreement is proposed
                            cp_bank = copy.deepcopy(disagr_bank)
                            coll_bank.append(cp_bank)
                        
                            print(thought)
                        elif args.use_FSM:
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
                    elif i != 0 and args.use_banks and (thought == 7):
                        print("student response is already discussed ------------ ")

                        #teacher's response when the student is repeating topics that has been previously discussed
                        if args.use_FSM and next_state in ["1", "4"]:
                            teacher_res = await generate_res("test", model_teacher, example_sentence, relevance["Q5"], conv_teacher[-1], None, [], None, PROMPT_RESTATE, 0)
                        else:
                            teacher_res = await generate_res("cov", model_teacher, example_sentence, relevance["Q5"], None, None, [], None, PROMPT_REMIND_FOCUSED, 0)
                        
                        if args.use_FSM:
                            following.append('0')
                            all_states.append('0')
                            rs.append('0')
                    elif i != 0 and thought == 6 and args.use_banks:
                        print("student response is irrelevant ------------ ")
                        teacher_res = await generate_res("cov", model_teacher, example_sentence, relevance["Q1"], None, None, [], None, PROMPT_REMIND_RELEVANCE, 0)
                        if args.use_FSM:
                            following.append('0')
                            all_states.append('0')
                            rs.append('0')
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
                        transition = load_json(transition.choices[0].message.content)
                        while transition == False:
                            transition = await generate_res("agent", model_teacher, example_sentence, chat_history, None, None, None, None, CHECK_RESPONSE_TEACHER, 1)
                            transition = load_json(transition.choices[0].message.content)
                        
                        print("transition: ", transition)
                        #In terms of precedence: request >> assumption (completeness) > examples (evidence) >= logical flaw (attacking point)
                        if "yes" in transition["3"].lower():
                            next_state = "3"
                        elif 'yes' not in cs['2'].lower() and i != 0:
                            next_state = '2'
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

                        elif "yes" in transition["4"].lower():
                            next_state = "4"

                        else:
                            next_state = "2"

                        count_states[next_state] += 1
                        tmp_s = next_state
                        print(count_states)
                        print("before random generation: " + next_state)

                        if count_states["3"] > 2 or FSM_STATES[-1] == "3":
                            count_states["3"] -= 1
                            next_state = "2"
                            count_states[next_state] += 1

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

                        # if next_state in ["1", "4"]:
                        #     res_T = await generate_res("sf", model_teacher, example_sentence, conv_student[-1], None, None, None, None, PRECONDITION, 1)
                        #     RES_T = res_T.choices[0].message.content
                        #     print("thought:", RES_T)
                        # if "no" in following[-1].lower() and "no" in following[-2].lower():
                        #     next_state = "2"
                        #     count_states[next_state] += 1
                        #     count_states[tmp_s] -= 1
                        
                        if next_state != curr_state:
                            print("-----------------transitioning--------------------" + "from " + curr_state + " to " + next_state)
                        print("next state is: "+ next_state)
                        # if "yes" in transition["5"].lower():
                        #     utterance_teacher = "It seems that you have not responded to my previous request. Would you please answer my question first, before proposing further arguments or requests?"
                        # else:
                        teacher_res = await generate_res("teacher", model_teacher, example_sentence, None, None, None, conv_teacher, conv_student, TEACHER_ACT_1 + STRAT_FOR_STATES_R[next_state] + TEACHER_ACT_2, 1)
                        
                        curr_state = next_state
                        FSM_STATES.append(curr_state)

                        check_following_res = await generate_res("eval_s", model_student, example_sentence, teacher_res.choices[0].message.content, STRAT_FOR_STATES_R[next_state], None, None, None, CHECK_FOLLOW_FSM_AGENT, 0)
                        cs = load_json(check_following_res.choices[0].message.content)
                        while cs == False:
                            check_following_res = await generate_res("eval_s", model_student, example_sentence, teacher_res.choices[0].message.content, STRAT_FOR_STATES_R[next_state], None, None, None, CHECK_FOLLOW_FSM_AGENT, 0)
                            cs = load_json(check_following_res.choices[0].message.content)
                        print("is the teacher following the transition? " + cs['1'])
                        print("is the teacher's question relevant? " + cs['2'])
                        
                        #rephrase the teacher's response, if we found that it is not following the expected state.
                        
                        if ("no" in cs['1'].lower() or "no" in cs['2'].lower()):
                            if next_state in ['1', '4']:
                                pt = TEACHER_ACT_EX_AS
                            elif next_state == "2":
                                pt = TEACHER_ACT_REFUTE
                            else:
                                pt = TEACHER_ACT_ANS
                            teacher_res = await generate_res("agents", model_teacher, example_sentence, teacher_res.choices[0].message.content, None, None, None, None, TEACHER_ACT_1 + STRAT_FOR_STATES_R[next_state] + pt, 1)
                            check_following_res = await generate_res("eval_s", model_student, example_sentence, teacher_res.choices[0].message.content, STRAT_FOR_STATES_R[next_state], None, None, None, CHECK_FOLLOW_FSM_AGENT, 0)
                            cs = load_json(check_following_res.choices[0].message.content)
                            while cs == False:
                                check_following_res = await generate_res("eval_s", model_student, example_sentence, teacher_res.choices[0].message.content, STRAT_FOR_STATES_R[next_state], None, None, None, CHECK_FOLLOW_FSM_AGENT, 0)
                                cs = load_json(check_following_res.choices[0].message.content)
                            print("is the teacher following the transition after rephrasing? " + cs['1'])
                            print("is the teacher's question relevant after rephrasing? " + cs['2'])
                        
                        following.append(cs['1'])
                        all_states.append(next_state)
                        rs.append(cs['2'])
                    elif args.use_toulmin:
                        print("cont toulmin")
                        teacher_res = await generate_res("tea", model_teacher, example_sentence, toulmin, None, None, conv_teacher, conv_student, PROMPT_TALK_ABOUT_LF_CONV, 0)
                    else:
                        teacher_res = await generate_res("teacher", model_teacher, example_sentence, None, None, None, conv_teacher, conv_student, PROMPT_TEACHER_ARGUE_DS, 1)

                    chat_history = ""

                    utterance_teacher = teacher_res.choices[0].message.content
                    chat_history += "teacher: " + utterance_teacher + "\n"
                    
                    conversation_teacher.append(utterance_teacher)
                    conv_teacher.append(utterance_teacher)
                    
                    #summarizes the teacher's responses

                    # if i == 0:
                    #     agreement_bank.append(summary)
                    summary = ""
                    # print(summary)
                    sums.append(summary)

                    # if i != 0 and args.use_FSM and next_state in ["1", "4"]:
                    #     STU_PROMPT = PROMPT_STUDENT_ARGUE_STRAT + PT_2
                    # else:
                    #     STU_PROMPT = PROMPT_STUDENT_ARGUE_STRAT + PT_S + PT_2

                    STU_PROMPT = PROMPT_STUDENT_ADV_REFUTATION + PT_2_ADV
                    
                    print("--------------------utterance--------------------")
                    print(utterance_teacher)
                    if args.use_adv:
                        student_res = await generate_res("stu", model_student, example_sentence, start_student_strategy, None, None, conv_teacher, conv_student, adv_p, 0)
                        student_u = load_json(student_res.choices[0].message.content)
                        while student_u == False:
                            utterance_student = await generate_res("stu", model_student, example_sentence, start_student_strategy, None, None, conv_teacher, conv_student, adv_p, 0)
                            student_u = load_json(utterance_student.choices[0].message.content)
                        utterance_student = student_u["res"]
                        print("student strategy:"+student_u["option"])
                        print(utterance_student)
                        start_student_strategy = student_u["option"]
                    elif args.use_nm_debate:
                        utterance_student = await generate_res("stu", model_student, example_sentence, start_student_strategy, None, None, conv_teacher, conv_student, PROMPT_STUDENT_ARGUE_NORMAL + PT_2, 0)
                        student_u = load_json(utterance_student.choices[0].message.content)
                        while student_u == False:
                            utterance_student = await generate_res("stu", model_student, example_sentence, start_student_strategy, None, None, conv_teacher, conv_student, PROMPT_STUDENT_ARGUE_NORMAL + PT_2, 0)
                            student_u = load_json(utterance_student.choices[0].message.content)                           
                        utterance_student = student_u["res"]
                        print("student strategy:"+student_u["option"])
                        print(utterance_student)
                        start_student_strategy = student_u["option"]
                    # elif args.use_edu:
                    #     utterance_student = await generate_res("student", model_student, example_sentence, start_student_strategy, None, None, conv_teacher, conv_student, PROMPT_STUDENT_LACK_UNDERSTAND, 1)
                    #     utterance_student = utterance_student.choices[0].message.content
                    #     print(utterance_student)
                    else:
                        utterance_student = await generate_res("stu", model_student, example_sentence, start_student_strategy, None, None, conv_teacher, conv_student, STU_PROMPT, 0)
                        student_u = load_json(utterance_student.choices[0].message.content)
                        while student_u == False:
                            utterance_student = await generate_res("stu", model_student, example_sentence, start_student_strategy, None, None, conv_teacher, conv_student, STU_PROMPT, 0)
                            student_u = load_json(utterance_student.choices[0].message.content)                           
                        utterance_student = student_u["res"]
                        print("student strategy:"+student_u["option"])
                        print(utterance_student)
                        start_student_strategy = student_u["option"]

                    # print(utterance_student)
                    conversation_student.append(utterance_student)
                    conv_student.append(utterance_student)
                    
                    print("--------------------------segmentation line------------------------------")
        
                    chat_history += "student: " + utterance_student + "\n"
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
                    agent_res = await generate_res("eval_s", model_agent, example_sentence, chat_history, None, None, None, None, PROMPT_AGENT_CHECK_EVIDENCE, 0)
                    res = load_json(agent_res.choices[0].message.content)
                    while res == False:
                        agent_res = await generate_res("eval_s", model_agent, example_sentence, chat_history, None, None, None, None, PROMPT_AGENT_CHECK_EVIDENCE, 0)
                        res = load_json(agent_res.choices[0].message.content) 

                    print("agreement check: ", res)

                    his_chat = chat_history
                    if "?" in utterance_teacher and "?" in utterance_student:
                        utter = "You have not answered the question I asked. Please answer it before making any requests. " + utterance_teacher
                        conv_teacher.append(utter)
                        utterance_student = await generate_res("stu", model_student, example_sentence, start_student_strategy, None, None, conv_teacher, conv_student, adv_p, 0)
                        student_u = load_json(utterance_student.choices[0].message.content)
                        while student_u == False:
                            utterance_student = await generate_res("stu", model_student, example_sentence, start_student_strategy, None, None, conv_teacher, conv_student, adv_p, 0)
                            student_u = load_json(utterance_student.choices[0].message.content)                           
                        utterance_student = student_u["res"]
                        print("student strategy:"+student_u["option"])
                        print(utterance_student)
                        
                        conv_student.append(utterance_student)
                        appends(utter, utterance_student, "", "", "", "", agr_bank, disagr_bank,'0','0', '0')
                        full_chat += his_chat
                        chat_history = "teacher: " + utter + "\n" + "student: " + utterance_student + "\n"
                        # relevance_res = await generate_res("check", model_agent, example_sentence, disagr_bank, 
                        #                                        chat_history, agr_bank, None, None, PROMPT_CHECK_RELEVANCE_AGENT, 0)
                        # relevance = load_json(relevance_res.choices[0].message.content)
                        # while relevance == False:
                        #     relevance_res = await generate_res("check", model_agent, example_sentence, disagr_bank, 
                        #                                        chat_history, agr_bank, None, None, PROMPT_CHECK_RELEVANCE_AGENT, 0)
                        #     relevance = load_json(relevance_res.choices[0].message.content)
                        # if "yes" not in relevance["Q2"].lower(): 
                        #     disagr_bank.append(relevance["Q2"])
                        




                    cp_agr = copy.deepcopy(agr_bank)
                    coll_agr.append(cp_agr)
                    print(cp_agr)
                    full_chat += chat_history                    
                    if args.use_banks and "yes" in res["3"] and "no" in res["4"] and len(disagr_bank) > 0:
                        agr_bank.append(disagr_bank[-1])
                        del disagr_bank[-1]
                        continue
                    if "yes" in res["1"].lower() and "yes" in res["2"].lower():
                        print("student unable to defend their argument")
                        if args.use_banks and len(disagr_bank) > 0:
                            if len(disagr_bank) != 0:
                                agr_bank.append(disagr_bank[-1])
                                del disagr_bank[-1]
                        confirm_disagreement = "If you cannot provide any evidence at all, then I would suggest looking for them if you have time later. Do you still have any other concerns regarding the sentence's logical validity?" 
                        print(confirm_disagreement)
                        conv_teacher.append(confirm_disagreement)
                        student_utterance = await generate_res("stu", model_student, example_sentence, start_student_strategy, None, None, conv_teacher, conv_student, adv_p, 0)
                        student_u = load_json(student_utterance.choices[0].message.content)
                        while student_u == False:
                            student_utterance = await generate_res("stu", model_student, example_sentence, start_student_strategy, None, None, conv_teacher, conv_student, adv_p, 0)
                            student_u = load_json(student_utterance.choices[0].message.content)
                        utterance_student = student_u["res"]
                        print("student strategy:"+student_u["option"])
                        print(utterance_student)
                        start_student_strategy = student_u["option"]
                        conv_student.append(utterance_student)
                        appends(confirm_disagreement, utterance_student, "", "", "", "", agr_bank, disagr_bank,'0','0', '0')

        #summary of conversation and ending
        summary = await generate_res("sum", model_student, example_sentence, full_chat, None, None, None, None, PROMPT_SUMMARIZE, 0)
        summary = summary.choices[0].message.content
        t_res = await generate_res("agt", model_teacher, example_sentence, summary, None, None, [], [], ENDING_PROMPT, 1)
        t_res = t_res.choices[0].message.content
        s_res = await generate_res("student", model_student, example_sentence, None, None, None, [t_res], [], ENDING_STUDENT, 1)
        s_res = s_res.choices[0].message.content
        full_chat += "teacher: " + t_res + "\n"
        full_chat += "student: " + s_res + "\n"
            
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

    print(len(sentences), len(full_chat))
    df_chats = pd.DataFrame({ "sentences": sentences, "chats": chats})
    df_chats.to_excel("chat_history_" + args.save_fn + str(args.num_gen) + ".xlsx", index=False)
    print("done async")


if __name__ == '__main__':
    asyncio.run(main())
