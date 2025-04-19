from openai import OpenAI
from contradict_app.def_logical_fallacy import *
from ast import parse
from collections import defaultdict
import json
import os
import asyncio
from prompt_bank import *
import argparse
import pandas as pd
import time
from check_score import *
from generate_response import *
from prompts_roleplay import *
from respond_role import generate_res

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_to_annotate", type=str, default='edu_train_final.csv')
    parser.add_argument("--components_to_read", type=str, default='decomposed_sentences_toulmin.xlsx')
    parser.add_argument("--definition", type=str, default='proposed')
    parser.add_argument("--use_category", type=bool, default=False)
    parser.add_argument("--use_toulmin", type=bool, default=True)
    parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='results/agreement_test_0906_rele_chat_l_10.xlsx')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=10)
    
    args = parser.parse_args()

    df_to_argue = pd.read_csv(args.file_to_annotate)
    df_components = pd.read_excel(args.components_to_read)
    # print(df_to_argue.loc[0])

    length_of_conversation = 5
    # st = df_to_annotate["Text"].tolist()
    # sampled_df = df_to_argue.groupby("updated_label").sample(n=1, random_state=2)
    sampled_df = df_to_argue.loc[df_to_argue["updated_label"] == "fallacy of relevance"].sample(n=3, random_state=10)
    # strategy = strategy_dc_commonsense["fallacy of credibility"]
    # strategy = emo_alt
    sentences = sampled_df["source_article"].values.tolist()
    labels = sampled_df["updated_label"].values.tolist()


    # model_student = "gpt-4o"
    # model_teacher = "gpt-4o"

    model_teacher = "gpt-3.5-turbo"
    model_student = 'gpt-3.5-turbo'
    model_agent = model_teacher
    sampled_sentence = []
    sampled_labels = []

    # example_sentence = sentences[-2]
    done = False
    prompt_fact_bank = PROMPT_FACT_BANK
    # prompt_find_contradiction = PROMPT_TEACHER_FIND_CONTRADICTION
    prompt_teacher_agreement = PROMPT_TEACHER_PERSUASION
    prompt_teacher_alt = SYSTEM_PROMPT_ALT_STRATEGY
    prompt_student = SYSTEM_PROMPT_STUDENT_DISCUSS
    prompt_agent = PROMPT_AGENT_CHECK_AGREEMENT
    prompt_counter = PROMPT_COUNTEREXAMPLE
    prompt_circ = PROMPT_CIRCULAR_REASONING
    prompt_break = PROMPT_BREAKDOWN
    # prompt_student_check =PROMPT_STUDENT_CHECK
    conversation_teacher = []
    conversation_student = []
    factdicts = []
    contra_dicts = []

    sc_rele = []
    sc1 = []
    sc2 = []
    sc3 = []
    sc4 = []

    Threshold_counter = 0.5
    Threshold_res = 2
    for j in range(len(sentences)):
        example_sentence = sentences[j]
        example_label = labels[j]
        agreement_bank = []
        print(example_sentence)

        #First identify the category of fallacy
        type_of_fallacy = await generate_response("fact_bank", model_teacher, example_sentence, 
                                                  None, None, None, None, None, PROMPT_IDENTIFY_CATEGORY, 0)
        fallacy = json.loads(type_of_fallacy.choices[0].message.content)["1"]
        print(fallacy)
        if fallacy.lower == "tu quoque":
            fallacy = "ad hominem"
        if fallacy.lower() in ["appeal to authority", "appeal to tradition", "appreal to nature"]:
            fallacy = "fallacy of credibility"
        if fallacy == "straw man fallacy": 
            fallacy = "fallacy of extension"
        if fallacy == "red herring":
            fallacy = "fallacy of relevance"
        strategy = strategy_dc_commonsense[fallacy.lower()]


        profile_res = await generate_res("fact_bank", model_teacher, example_sentence, 
                                                None, None, None, None, None, PROMPT_GENERATE_PROFILE, 0)
        profile = json.loads(profile_res.choices[0].message.content)
        print(profile)



        #At the same time, the teacher finds all facts and put them into the fact bank
        fact_bank_res = await generate_response("fact_bank", model_teacher, example_sentence, 
                                                None, None, None, None, None, PROMPT_BREAKDOWN, 0)
        fact_dict = json.loads(fact_bank_res.choices[0].message.content)
        print(fact_dict)

        if fallacy == "circular reasoning": 
            ct_break = await generate_response("counter_ex", model_teacher, example_sentence, None, 
                                                              None, None, None, None, prompt_circ, 0)
            ct_dict = json.loads(ct_break.choices[0].message.content)
            contradiction_dict = list(ct_dict.values())

        else:
            #find a counterexample using the given strategy, then decompose the counterexample into premise and conclusion
            #TODO: add code for changing counterexamples, should the threshold check fail
            done = False
            first = True
            while not done: 
                if first:
                    counterexample_res = await generate_response("counter_ex", model_teacher, example_sentence, strategy, 
                                                            None, None, None, None, prompt_counter, 0)
                    counter_ex = json.loads(counterexample_res.choices[0].message.content)["1"]
                    counter_break = await generate_response("fact_bank", model_teacher, counter_ex, 
                                                            None, None, None, None, None, PROMPT_BREAKDOWN, 0)
                    ct_dict = json.loads(counter_break.choices[0].message.content)
                    print(ct_dict)
                    contradiction_dict = list(fact_dict.values()) + list(ct_dict.values())

                    #check the counterexample with Claude/mistralai
                    results_rational_agent = await check_score(model_agent, example_sentence, counter_ex, None, AGENT_CHECK_COUNTEREXAMPLE, 0)
                    # score = results_conversation_teacher.content[0].text
                    score = results_rational_agent.content[0].text
                    print(score)

                
                if "Yes" in score:
                    done = True
                    first = False
                #If the counterexample does not meet threshold, come up with a new counterexample and recompute score
                else:
                    counterexample_res = await generate_response("counter", model_teacher, example_sentence, None, strategy, 
                                                        counter_ex, None, None, PROMPT_ALT_COUNTEREXAMPLE, 0)
                    print(counterexample_res.choices[0].message.content)
                    counter_ex = json.loads(counterexample_res.choices[0].message.content)["1"]
                    results_rational_agent = await check_score(model_agent, example_sentence, counter_ex, None, AGENT_CHECK_COUNTEREXAMPLE, 0)
                    # score = results_conversation_teacher.content[0].text
                    score = results_rational_agent.content[0].text
                    first = False
        
        agreement_bank = []
        user_message = """Let's check what we have so far. Do you agree with the following <statement>? Please answer with Yes or No. 
        <statement>: {sentence}
        """

        #TODO: Add agent rating steps and change student behavior steps
        for target in contradiction_dict:
            print(target)
            count = 0
            done = False
            chat_history = "\n"
            conv_teacher = []
            conv_student = []
            alternative_appr = False
            while not done: 
                if count == 0:
                    factdicts.append(fact_dict)
                    contra_dicts.append(contradiction_dict)
                else:
                    factdicts.append("")
                    contra_dicts.append("")

                #Teacher ask for agreement
                teacher_res = await generate_response("get_agreement", model_teacher, example_sentence, 
                                                    None, agreement_bank, target, conv_teacher, conv_student, prompt_teacher_agreement, 0)
                teacher_res = teacher_res.choices[0].message.content
                print(teacher_res)
                conversation_teacher.append(teacher_res)
                conv_teacher.append(teacher_res)
                chat_history += "teacher: " + teacher_res + "\n"

                agent_res_RELE = await check_score(model_agent, target, conversation_teacher[count], SYSTEM_JUDGE, PROMPT_EFFECTIVE_STRAW, 0)
                agent_res_multi = await check_score(model_agent, example_sentence, conversation_teacher[count], SYSTEM_JUDGE, SYSTEM_RATE_RESPONSE_AGENT_MULTI, 0)
                print(agent_res_RELE)
                print(agent_res_multi)
                score_rele = json.loads(agent_res_RELE.content[0].text)["1"]

                ans_dict = json.loads(agent_res_multi.content[0].text)
                # score_1, score_2, score_3 = ans_dict["1"], ans_dict["2"], ans_dict["3"]
                # sc_rele.append(score_rele)
                # sc1.append(score_1)
                # sc2.append(score_2)
                # sc3.append(score_3)
                # tot_score = int(score_rele) + int(score_1) + int(score_2) + int(score_3)
                # print(tot_score)

                # if tot_score < Threshold_res:
                #Student responds to teacher with stubborness
                    # student_res = await generate_response("student", model_student, example_sentence, 
                                                        # None, agreement_bank, None, conv_teacher, conv_student, prompt_student, 0)

                # else:
                #Force the student to agree with the teacher
                # student_res = await generate_res("student_agree", model_student, example_sentence, 
                                                        # None, agreement_bank, target, conv_teacher, conv_student, PROMPT_ARGUE_FOR_LF, 0)

                student_res = await generate_res("student", model_teacher, example_sentence, None, profile, None, conv_teacher, conv_student, PROMPT_ARGUE_FOR_LF, 0)

                    
                conversation_student.append(student_res.choices[0].message.content)
                conv_student.append(student_res.choices[0].message.content)
                chat_history += "student: " + student_res.choices[0].message.content + "\n"
                print(student_res.choices[0].message.content)

                #doublechecking agreement
                agent_res = await generate_response("agent", model_agent, target, 
                                                    chat_history, None, None, None, None, prompt_agent, 0)

                agreed = agent_res.choices[0].message.content
                print(agreed)
                sampled_sentence.append(example_sentence)
                sampled_labels.append(example_label)
                count += 1
                print(count)

                tot_score = 0
                user_message_context = user_message.format(sentence=target)
                print(user_message_context)
                #double checks whether student agrees with target, using hardcoded question
                student_res_doublecheck = await generate_response("student", model_student, example_sentence, 
                                                    None, agreement_bank, None, [user_message_context], [], prompt_student, 0)
                rs_doublecheck = student_res_doublecheck.choices[0].message.content
                print(rs_doublecheck)
                # doublecheck_history = "teacher: " + user_message_context + "\n" + "student: " + rs_doublecheck
                
                if (agreed == "True" and "Yes" in rs_doublecheck) or (tot_score >= Threshold_res):
                    done = True
                    agreement_bank.append(target)
                else:
                    if count == length_of_conversation:
                        done = True
                        # alternative_appr = True




        print(agreement_bank)
        #Teacher points out the contradiction
        point_out_res = await generate_response("point_out", model_teacher, example_sentence, 
                                                None, contradiction_dict, None, conv_teacher, conv_student, PROMPT_TEACHER_POINT_OUT, 0)
        conversation_teacher.append(point_out_res.choices[0].message.content)
        conv_teacher.append(point_out_res.choices[0].message.content)
        print(point_out_res.choices[0].message.content)
        
        student_res = await generate_response("student", model_student, example_sentence, 
                                                    None, agreement_bank, None, conv_teacher, conv_student, prompt_student, 0)
        conversation_student.append(student_res.choices[0].message.content)

        sc_rele.append("0")
        sc1.append("0")
        sc2.append("0")
        sc3.append("0")
        print(student_res.choices[0].message.content)
        # print(conv_teacher, conv_student)
        sampled_sentence.append(example_sentence)
        sampled_labels.append(example_label)
        factdicts.append("")
        contra_dicts.append("")


    print(len(conversation_teacher), len(conversation_student), len(sampled_sentence), len(sampled_labels))
    data_dict = {"fact_dict": factdicts,
                 "contradiction_dicts": contra_dicts,
                 'score_relevance': sc_rele,
                 'score_cogency': sc1,
                 'score_effective': sc2,
                 'score_sufficient': sc3,
                 'teacher_response': conversation_teacher, 
                 'layman_response': conversation_student, 
                 'sentence_sample': sampled_sentence, 
                 'labels': sampled_labels}
    df_result = pd.DataFrame(data_dict)
    df_result.to_excel(args.save_fn, index=False)
    print("done async")


if __name__ == '__main__':
    asyncio.run(main())
