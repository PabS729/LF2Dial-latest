from openai import OpenAI
from prompts_init import *
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

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_to_annotate", type=str, default='edu_train_final.csv')
    parser.add_argument("--components_to_read", type=str, default='decomposed_sentences_toulmin.xlsx')
    parser.add_argument("--definition", type=str, default='proposed')
    parser.add_argument("--use_category", type=bool, default=False)
    parser.add_argument("--use_toulmin", type=bool, default=True)
    parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='results/BASELINE_test_0726_herr_10.xlsx')
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
    
    model_teacher = "gpt-3.5-turbo-0125"
    model_student = 'gpt-3.5-turbo-0125'
    model_agent = model_teacher
    sampled_sentence = []
    sampled_labels = []

    Threshold_res = 2
    # example_sentence = sentences[-2]
    # prompt_find_contradiction = PROMPT_TEACHER_FIND_CONTRADICTION
    prompt_student = SYSTEM_PROMPT_STUDENT_DISCUSS
    prompt_agent = PROMPT_AGENT_CHECK_AGREEMENT
    prompt_basic = SYSTEM_PROMPT_TEACHER_NEW
    # prompt_student_check =PROMPT_STUDENT_CHECK
    conversation_teacher = []
    conversation_student = []
    factdicts = []
    contra_dicts = []

    sc_rele = []
    sc1 = []
    sc2 = []
    sc3 = []



    user_message = """Let's check what we have so far. Do you agree with the following <statement>? Please answer with Yes or No. 
        <statement>: {sentence}
        """

        #TODO: Add agent rating steps and change student behavior steps
    for s in sentences:
        count = 0


        done = False
        chat_history = "\n"
        conv_teacher = []
        conv_student = []
        while not done:

            alternative_appr = False
            #Teacher ask for agreement
            teacher_res = await generate_response("convince", model_teacher, s, None, None, None, conv_teacher, conv_student, prompt_basic, 0)
            teacher_res = teacher_res.choices[0].message.content
            print(teacher_res)
            conversation_teacher.append(teacher_res)
            conv_teacher.append(teacher_res)
            chat_history += "teacher: " + teacher_res + "\n"

            agent_res_RELE = await check_score(model_agent, s, chat_history, SYSTEM_JUDGE, PROMPT_EFFECTIVE_STRAW, 0)
            agent_res_multi = await check_score(model_agent, s, chat_history, SYSTEM_JUDGE, SYSTEM_RATE_RESPONSE_AGENT_MULTI, 0)
            print(agent_res_RELE)
            print(agent_res_multi)
            score_rele = json.loads(agent_res_RELE.content[0].text)["1"]

            ans_dict = json.loads(agent_res_multi.content[0].text)
            score_1, score_2, score_3 = ans_dict["1"], ans_dict["2"], ans_dict["3"]
            sc_rele.append(score_rele)
            sc1.append(score_1)
            sc2.append(score_2)
            sc3.append(score_3)
            # tot_score = int(score_rele) + int(score_1) + int(score_2) + int(score_3)
            tot_score = 0
            print(tot_score)

            if tot_score < Threshold_res:
                #Student responds to teacher with stubborness
                student_res = await generate_response("student", model_student, s, 
                                                        None, None, None, conv_teacher, conv_student, prompt_student, 0)

            else:
                #Force the student to agree with the teacher
                student_res = await generate_response("student_agree", model_student, s, 
                                                        None, None, None, conv_teacher, conv_student, SYSTEM_FORCE_AGREEMENT_BASE, 0)
                    
            conversation_student.append(student_res.choices[0].message.content)
            conv_student.append(student_res.choices[0].message.content)
            chat_history += "student: " + student_res.choices[0].message.content + "\n"
            print(student_res.choices[0].message.content)

                #doublechecking agreement
            sampled_sentence.append(s)
            sampled_labels.append("")
            count += 1
            print(count)

            # user_message_context = user_message.format(sentence=target)
            # print(user_message_context)
            student_res_doublecheck = await generate_response("agent", model_student, s, 
                                                    chat_history, None, None, None, [], PROMPT_AGENT_CHECK_AGREEMENT_BASE, 0)
            rs_doublecheck = student_res_doublecheck.choices[0].message.content
            print(rs_doublecheck)
                # doublecheck_history = "teacher: " + user_message_context + "\n" + "student: " + rs_doublecheck
                
            if ("Yes" in rs_doublecheck) or (tot_score >= Threshold_res):
                done = True
            else:
                if count == length_of_conversation:
                    done = True
                        # alternative_appr = True



    print(len(conversation_teacher), len(conversation_student), len(sampled_sentence), len(sampled_labels))
    data_dict = {
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
