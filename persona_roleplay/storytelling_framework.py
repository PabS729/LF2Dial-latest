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
    parser.add_argument("--save_fn", type=str, default='results/storytelling_test_0911_4o_fstraw.txt')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=10)
    
    args = parser.parse_args()

    df_to_argue = pd.read_csv(args.file_to_annotate)
    df_components = pd.read_excel(args.components_to_read)
    # print(df_to_argue.loc[0])

    length_of_conversation = 5
    # st = df_to_annotate["Text"].tolist()
    # sampled_df = df_to_argue.groupby("updated_label").sample(n=1, random_state=10)
    sampled_df = df_to_argue.loc[df_to_argue["updated_label"] == "fallacy of extension"].sample(n=3, random_state=7)
    # strategy = strategy_dc_commonsense["fallacy of credibility"]
    # strategy = emo_alt
    sentences = sampled_df["source_article"].values.tolist()
    labels = sampled_df["updated_label"].values.tolist()


    # model_student = "gpt-4o"
    model_teacher = "gpt-4o"

    # model_teacher = "gpt-4o-mini"
    model_student = 'gpt-4o-mini'
    model_agent = model_teacher
    sampled_sentence = []
    sampled_labels = []

    # example_sentence = sentences[-2]
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
    convs = []
    for j in range(len(sentences)):
        example_sentence = sentences[j]
        example_label = labels[j]
        agreement_bank = []
        print(example_sentence)

        #Generate social profile
        profile_res = await generate_res("fact_bank", model_teacher, example_sentence, 
                                                None, None, None, None, None, PROMPT_GENERATE_PROFILE, 0)
        profile = json.loads(profile_res.choices[0].message.content)
        print(profile)
        conv_res = await generate_res("conv", model_teacher, example_sentence, None, profile, 
                                            None, None, None, PROMPT_GENERATE_CONVERSATION, 0)
        convs.append(conv_res.choices[0].message.content)
        print(conv_res.choices[0].message.content)





    print(len(convs), len(sentences), len(labels))
    f = open(args.save_fn, "w")
    for s in convs:
        f.write(s)
    print("done async")
    f.close()

if __name__ == '__main__':
    asyncio.run(main())
