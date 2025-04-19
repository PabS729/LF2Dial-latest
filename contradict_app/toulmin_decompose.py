from openai import OpenAI
from contradict_app.def_logical_fallacy import *
from ast import parse
from collections import defaultdict
import json
import os
import asyncio
from prompts_toulmin import * 
import argparse
import pandas as pd
import time


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_to_annotate", type=str, default='edu_train_final.csv')
    parser.add_argument("--components_to_read", type=str, default='decomposed_sentences_toulmin.xlsx')
    parser.add_argument("--definition", type=str, default='proposed')
    parser.add_argument("--use_category", type=bool, default=False)
    parser.add_argument("--use_toulmin", type=bool, default=True)
    parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='results/roleplay_test_1007_4o_adp_toulmin')
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
    sampled_df = df_to_argue.groupby("updated_label").sample(n=1, random_state=10)
    # sampled_df = df_to_argue.sample(n=10, random_state=15)
    # strategy = strategy_dc_commonsense["fallacy of credibility"]
    # strategy = emo_alt
    sentences = sampled_df["source_article"].values.tolist()
    labels = sampled_df["updated_label"].values.tolist()



    tols = []
    model_student = "gpt-4o"
    model_teacher = "gpt-4o"


    # model_teacher = "gpt-4o-mini"
    # model_student = 'gpt-4o-mini'
    model_agent = model_teacher

    for j in range(len(sentences)):
        example_sentence = sentences[j]
        example_label = labels[j]
        agreement_bank = []
        print(example_sentence)


        #Generate social profile
        # profile_res = await generate_res("fact_bank", model_teacher, example_sentence, 
                                                # None, None, None, None, None, PROMPT_GENERATE_PROFILE, 0)
        # profile = json.loads(profile_res.choices[0].message.content)

        toulmin_res = await generate_res("gen_Strategy", model_student, example_sentence, 
                                                None, None, None, None, None, SIMPLIFY_TOULM, 0)
        toulmin = toulmin_res.choices[0].message.content
        tols.append(toulmin)

    data_dict = {
        "sentence": sentences,
        "label": labels,
        "toulmin": tols
    }

    df_n = pd.DataFrame.from_dict(data_dict)
    df_n.to_excel("toulmin_decomp_simplify.xlsx")


if __name__ == '__main__':
    asyncio.run(main())