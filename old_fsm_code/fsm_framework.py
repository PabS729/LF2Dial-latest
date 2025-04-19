from openai import OpenAI
from contradict_app.def_logical_fallacy import *
from ast import parse
from collections import defaultdict
import json
import os
from prompts_toulmin import * 
import argparse
import pandas as pd
import time

from persona_roleplay.respond_role import *
from strategy_handle import * 

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_to_annotate", type=str, default='edu_train_final.csv')
    parser.add_argument("--components_to_read", type=str, default='decomposed_sentences_toulmin.xlsx')
    # parser.add_argument("--definition", type=str, default='proposed')
    # parser.add_argument("--use_category", type=bool, default=False)
    # parser.add_argument("--use_toulmin", type=bool, default=True)
    # parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='results/toul_1120_cau_single_cut_new')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=0)
    
    args = parser.parse_args()

    #reads the dataset
    df_to_argue = pd.read_csv(args.file_to_annotate)
    df_components = pd.read_excel(args.components_to_read)
    # sampled_df = df_to_argue.loc[df_to_argue["updated_label"] == "ad populum"].sample(n=1, random_state=15)
    # strategy = strategy_dc_commonsense["fallacy of credibility"]
    # strategy = emo_alt
    # sentences = sampled_df["source_article"].values.tolist()
    # labels = sampled_df["updated_label"].values.tolist()
    # sentences = ["In fact, it's starting to fall apart not because of lawsuits -- though they are a problem, and John Edwards and I are committed to fixing them -- but because of the larger issue that we don't cover Americans."]
    # labels =["false causality"]
    model_student = "gpt-4o"
    model_teacher = "gpt-4o"

    # sentences = ["Al Gore and I are committed to continuing this acquisition program, transforming the military. There's still fewer people in uniform today, but person - to - person, person - by - person, unit - by - unit, this is the most powerful and effective military, not only in the world today, but in the history of the world. And again, Al Gore and I will do whatever is necessary to keep it that way."]
    # labels = ["Slippery Slope"]

    # sentences = ["You know, nobody likes who shot John, but I think the first negative campaign run in this election was by Governor Clinton, and I'm not going to sit there and be a punching bag; I'm going to stand up and say, hey, listen, here's my side of it."]
    # labels = ["appeal to emotion"]
    sentences = ["After all, the Welfare Reform Act, which Al Gore promised to lead the effort on to get people off of welfare to set time limits, to get people to enjoy the dignity of work. That was a bipartisan act that was adopted. The Anti - Crime Act that has helped to lower crime more than 20% in our country was also bipartisan. The Balanced Budget Act of 1997 which was critical to getting our economy to the point and our government to the point of unprecedented surplus we enjoy today also was bipartisan, and Al Gore was involved."]
    labels = ["false cause"]
    # model_teacher = "gpt-4o-mini"
    # model_student = 'gpt-4o-mini'
    model_agent = model_teacher
    sampled_sentence = []
    sampled_labels = []

    conversation_teacher = []
    conversation_student = []
    sums = []
    anas = []
    pfs = []
    chats = []
    agr = []
    reles = []

    lm_thought = []

    #loops over all sentences, generates one dialogue per sentence
    for j in range(len(sentences)):
        example_sentence = sentences[j]
        example_label = labels[j]
        agreement_bank = []
        print(example_sentence)

        #use toulmin decomposition
        toulmin_res = await generate_res("gen_Strategy", model_student, example_sentence, 
                                                None, None, None, None, None, PROMPT_DECOMPOSE_TOULMIN, 0)
        toulmin = toulmin_res.choices[0].message.content

        #default rounds for debates
        rounds = 10
        conv_teacher = []
        conv_student =[]
        

        chat_history = ""
        full_chat = ""
        summary = ""
    
        for i in range(0, rounds):
            
            #No strategy for first round, since the teacher starts the conversation
            if i == 0:
                sampled_sentence.append(example_sentence)
                sampled_labels.append(example_label)

                thought = "D"
                reles.append("")
            else: 
                
                sampled_sentence.append("")
                sampled_labels.append("")

                #check relevance of the student's response from last round
                relevance_res = await generate_res("eval_s", model_teacher, example_sentence, agreement_bank, utterance_student, None, conv_teacher, conv_student, PROMPT_CHECK_TOPIC_RELEVANCE, 0)
                relevance = relevance_res.choices[0].message.content
                print(relevance)
                reles.append(relevance)

                #if student's response is relevant, teacher responds according to the detected behaviors.
                if relevance[:2].lower() not in "no.":
                    agreement_bank.append(relevance)
                    thought_res = await generate_res("strategy", model_teacher, example_sentence, chat_history, None, None, None, None, PROMPT_IDENTIFY_STUDENT_STATE, 0)

                    thought = json.loads(thought_res.choices[0].message.content)["Type"]
                else: 
                    #otherwise, student is off topic. 
                    thought = 4
                
                print(thought)
                chat_history = ""
            
            # anas.append(thought)

            # print(curr_strat)
                
            anas.append(thought)

            #start the conversation by pointing out the logical flaw
            if i == 0:

                teacher_res = await generate_res("tea", model_teacher, example_sentence, toulmin, None, None, conv_teacher, conv_student, PROMPT_TALK_ABOUT_LF, 0)
            #student is off topic
            elif thought == 4:
                #reminds 
                # print("taken")
                teacher_res = await generate_res("teacher", model_teacher, example_sentence, summary, None, None, [], conv_student[-1], PROMPT_REMIND_FOCUSED, 0)
            
            #teacher chooses strategies and responds to the student
            else:
                teacher_res = await generate_res("teacher_st", model_teacher, example_sentence, indicator[str(thought)], STRATEGY_HANDLE_STUDENT[str(thought)], None, conv_teacher, conv_student, PROMPT_HANDLE_STUDENT_BEHAVIOR, 0)



            utterance_teacher = teacher_res.choices[0].message.content
            chat_history += "teacher: " + utterance_teacher + "\n"
            print(utterance_teacher)
            conversation_teacher.append(utterance_teacher)
            conv_teacher.append(utterance_teacher)

            #summarizes the teacher's reponse, to be used in student's CoT
            summary = await generate_res("sum", model_teacher, example_sentence, conv_teacher, None, None, None, None, PROMPT_SUMMARIZE, 0)
            summary = summary.choices[0].message.content
            if i == 0:
                agreement_bank.append(summary)
            print(summary)
            sums.append(summary)


            #student first analyzes teacher's response, then proposes ways to critically question the teacher
            student_res_thought = await generate_res("", model_teacher, example_sentence, summary, None, None, conv_teacher, conv_student, PROMPT_STUDENT_THINK, 1)
            student_res_thought = json.loads(student_res_thought.choices[0].message.content)["ans"]
            print(student_res_thought)
            lm_thought.append(student_res_thought)

            #student responds to teacher by following the previous CoT
            student_res = await generate_res("student_bio", model_student, example_sentence, student_res_thought, None, None, conv_teacher, conv_student, PROMPT_STUDENT_TALK, 1)
            
            utterance_student = student_res.choices[0].message.content
 
            chat_history += "student: " + utterance_student + "\n"
            full_chat += chat_history
            print(utterance_student)
            conversation_student.append(utterance_student)
            conv_student.append(utterance_student)
            agr.append(agreement_bank)

        chats.append(full_chat)


    print(len(anas), len(conversation_teacher), len(conversation_student), len(sampled_sentence), len(sampled_labels), len(pfs))
    data_dict = {
                 'teacher_analysis': anas,
                 'layman_thought': lm_thought, 
                 'teacher_response': conversation_teacher, 
                 'layman_response': conversation_student, 
                 'tracker': agr,
                 'summary': sums,
                 'student_check_relevance': reles
                }
    df_result = pd.DataFrame(data_dict)
    df_result.to_excel(args.save_fn + str(args.num_gen) + ".xlsx", index=False)

    df_chats = pd.DataFrame({"chats": chats})
    df_chats.to_excel("chat_history_" + args.save_fn + str(args.num_gen) + ".xlsx", index=False)
    print("done async")


if __name__ == '__main__':
    asyncio.run(main())
