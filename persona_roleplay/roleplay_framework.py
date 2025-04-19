from openai import OpenAI
from contradict_app.def_logical_fallacy import *
from ast import parse
from collections import defaultdict
import json
import os
import asyncio
from prompts_roleplay import *
import argparse
import pandas as pd
import time
from check_score import *
from respond_role import *

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_to_annotate", type=str, default='edu_train_final.csv')
    parser.add_argument("--components_to_read", type=str, default='decomposed_sentences_toulmin.xlsx')
    parser.add_argument("--definition", type=str, default='proposed')
    parser.add_argument("--use_category", type=bool, default=False)
    parser.add_argument("--use_toulmin", type=bool, default=True)
    parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='results/roleplay_test_1007_MISTRAL_adp')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=0)
    
    args = parser.parse_args()

    df_to_argue = pd.read_csv(args.file_to_annotate)
    df_components = pd.read_excel(args.components_to_read)
    # sampled_df = df_to_argue
    
    # print(df_to_argue.loc[0])
    # st = df_to_annotate["Text"].tolist()
    # df_to_argue = df_to_argue[df_to_argue.updated_label != "fallacy of logic"]
    # sampled_df = df_to_argue.groupby("updated_label").sample(n=10, random_state=10)
    sampled_df = df_to_argue.loc[df_to_argue["updated_label"] == "ad populum"].sample(n=1, random_state=15)
    # strategy = strategy_dc_commonsense["fallacy of credibility"]
    # strategy = emo_alt
    sentences = sampled_df["source_article"].values.tolist()
    labels = sampled_df["updated_label"].values.tolist()

    # max_len = args.num_gen + 200
    # if  max_len > len(sentences):
    #     max_len = len(sentences)

    # max_len_l = args.num_gen +200
    # if max_len_l > len(labels):
    #     max_len_l = len(labels)

    

    # sentences = sentences[args.num_gen:max_len]
    # labels = labels[args.num_gen:max_len_l]

    # sentences = ["I knew him in high school and he almost flunked out. He can't be a good choice for mayor."]
    # labels = ["ad hominem"]

    

    # sentences = ["Not tipping your waiter is like stealing money right out of someone's wallet."]
    # labels = ["false analogy"]

    # sentences = ["I hold a doctorate in theology, have written 12 books, and personally met the Pope.  Therefore, when I say that Jesusâ€™ favorite snack was raisins dipped in wine, you should believe me."]
    # labels = ["fallacy of credibility"]




    model_student = "gpt-4o"
    model_teacher = "gpt-4o"


    # model_teacher = "gpt-4o-mini"
    # model_student = 'gpt-4o-mini'
    model_agent = model_teacher
    sampled_sentence = []
    sampled_labels = []
    modified_sentence = []
    agent_responses = []

    # example_sentence = sentences[-2]
    # prompt_student_check =PROMPT_STUDENT_CHECK
    conversation_teacher = []
    conversation_student = []
    anas = []
    pfs = []
    n_persuasion = []
    chats = []

    Threshold_counter = 0.5
    Threshold_res = 2
    for j in range(len(sentences)):
        example_sentence = sentences[j]
        example_label = labels[j]
        agreement_bank = []
        print(example_sentence)


        #Generate social profile
        # profile_res = await generate_res("fact_bank", model_teacher, example_sentence, 
                                                # None, None, None, None, None, PROMPT_GENERATE_PROFILE, 0)
        # profile = json.loads(profile_res.choices[0].message.content)

        st_res = await generate_res("gen_Strategy", model_student, example_sentence, 
                                                None, None, None, None, None, PROMPT_AGENT_ADD_OR_SIMPLIFY, 0)
        example_sentence = st_res.choices[0].message.content
        # print(st_res)

        profile_res = await generate_res("gen_Strategy", model_student, example_sentence, 
                                                None, None, None, None, None, PROMPT_GENERATE_BIO_EXP, 0)
        profile = profile_res.choices[0].message.content
        # print(profile)
        
        # strategy_res = await generate_response("gen_strategy", model_teacher, example_sentence, 
                                                # None, None, None, None, None, PROMPT_GENERATE_STRATEGY_TEACHER, 0)
        # strategy = strategy_res.choices[0].message.content
        # print(strategy)



        rounds = 10
        conv_teacher = []
        conv_student =[]
        

        chat_history = ""
        full_chat = ""
        for i in range(0, rounds):
            
            if i == 0:
                sampled_sentence.append(example_sentence)
                modified_sentence.append(st_res)
                sampled_labels.append(example_label)
                pfs.append(profile)
                thought = ""
            else: 
                sampled_sentence.append("")
                modified_sentence.append("")
                sampled_labels.append("")
                pfs.append("")
                # thought_res = await generate_res("agent", model_teacher, example_sentence, chat_history, None, None, None, None, PROMPT_TEACHER_REFUTE, 0)
                # thought = thought_res.choices[0].message.content
                # thought_res = await generate_res("thought", model_teacher, example_sentence, chat_history, None, None, None, None, PROMPT_THINK, 0)

                # thought = json.loads(thought_res.choices[0].message.content)
                # thought = thought["Q1"] +"\n"+ thought["Q2"] + "\n" + thought["Q3"]
                # print(thought)
                chat_history = ""
                thought = ""
            
            anas.append(thought)
            
            # curr_strat = await generate_response("strategy", model_teacher, example_sentence, 
                                                # chat_history, strategy, None, None, None, PROMPT_ANALYZE_STAGE, 0)
            # curr_strat = json.loads(curr_strat.choices[0].message.content)["ans"]
            # print(curr_strat)
            # teacher_res = await generate_response("teacher_st", model_teacher, example_sentence, curr_strat, strategy, None, conv_teacher, conv_student, PROMPT_FOLLOW_STRATEGY, 0)

            teacher_res = await generate_res("t_edu", model_teacher, example_sentence, None, None, None, conv_teacher, conv_student, PROMPT_TEACHER_ARGUE_No_CoT, 0)

            # teacher_res = await generate_res("teacher", model_teacher, example_sentence, thought, None, None, conv_teacher, conv_student, PROMPT_TEACHER_ARGUE, 0)
            utterance_teacher = teacher_res.choices[0].message.content
            chat_history += "teacher: " + utterance_teacher + "\n"
            # print(utterance_teacher)
            conversation_teacher.append(utterance_teacher)
            conv_teacher.append(utterance_teacher)

            # student_res = await generate_res("student", model_teacher, example_sentence, chat_history, profile, None, conv_teacher, conv_student, PROMPT_ARGUE_FOR_LF_PC, 1)
            student_res = await generate_res("student_bio", model_student, example_sentence, profile, None, None, conv_teacher, conv_student, PROMPT_ARGUE_FOR_LF_BIO, 1)

            utterance_student = student_res.choices[0].message.content
            chat_history += "student: " + utterance_student + "\n"
            full_chat += chat_history
            # print(utterance_student)
            conversation_student.append(utterance_student)
            conv_student.append(utterance_student)

            # print("%d\n", i)
            agent_res = await generate_res("agent", model_student, example_sentence, chat_history, None, None, None, None, PROMPT_CHECK_FIN, 0)
            agent_res = json.loads(agent_res.choices[0].message.content)
            # print(agent_res)
            agent_responses.append(agent_res)

            
            if "yes" in agent_res["Q1"].lower():
                n_persuasion.append(i+1)
                break

            else:
                if i == 9 or "yes" in agent_res["Q2"].lower():
                    n_persuasion.append("NO")
                    break
                else: 
                    n_persuasion.append(0)
        chats.append(full_chat)
        #the student is convinced, time to educate the student
        # conv_teacher = []
        # conv_student =[]
        # for i in range(0,3):
        #     n_persuasion.append(0)

        #     sampled_sentence.append("")
        #     sampled_labels.append("")
        #     pfs.append("")
        #     # thought_res = await generate_res("gen_strategy", model_teacher, example_sentence, None, None, None, None, None, PROMPT_TEACHER_THINK, 0)
        #     # thought = json.loads(thought_res.choices[0].message.content)
        #     # thought = thought["Q1"] +"\n"+ thought["Q2"]
        #     # print(thought)
        #     chat_history = ""


        #     thought_res = await generate_res("thought", model_teacher, example_sentence, chat_history, None, None, None, None, PROMPT_TEACHER_EDU_THINK, 0)
        #     thought = json.loads(thought_res.choices[0].message.content)["Q1"]
        #     print(thought)

        #     anas.append(thought)

        #     teacher_res = await generate_res("teacher", model_teacher, example_sentence, thought, None, None,  conv_teacher, conv_student, PROMPT_TEACHER_EDUCATE, 0)
        #     utterance_teacher = teacher_res.choices[0].message.content
        #     chat_history += "teacher: " + utterance_teacher + "\n"
        #     print(utterance_teacher)
        #     conversation_teacher.append(utterance_teacher)
        #     conv_teacher.append(utterance_teacher)

        #     # student_res = await generate_res("student", model_teacher, example_sentence, None, profile, None, conv_teacher, conv_student, PROMPT_STUDENT_INTERACT_NEW, 0)
        #     student_res = await generate_res("student_bio", model_teacher, example_sentence, profile, None, None, conv_teacher, conv_student, PROMPT_STUDENT_INTERACT_BIO, 0)

        #     utterance_student = student_res.choices[0].message.content
        #     chat_history += "student: " + utterance_student + "\n"
        #     print(utterance_student)
        #     conversation_student.append(utterance_student)
        #     conv_student.append(utterance_student)

            






    print(len(anas), len(conversation_teacher), len(conversation_student), len(sampled_sentence), len(sampled_labels), len(pfs))
    data_dict = {
                 'teacher_analysis': anas,
                 'teacher_response': conversation_teacher, 
                 'layman_response': conversation_student, 
                 'sentence_sample': sampled_sentence, 
                 'modified_sample': modified_sentence,
                 'labels': sampled_labels,
                 "profile": pfs,
                 'agent_res': agent_responses,
                 "rounds_persuaded": n_persuasion
                }
    df_result = pd.DataFrame(data_dict)
    df_result.to_excel(args.save_fn + str(args.num_gen) + ".xlsx", index=False)

    df_chats = pd.DataFrame({"chats": chats})
    df_chats.to_excel("chat_history_" + args.save_fn + str(args.num_gen) + ".xlsx", index=False)
    print("done async")


if __name__ == '__main__':
    asyncio.run(main())
