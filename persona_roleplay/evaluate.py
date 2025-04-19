from openai import OpenAI
from contradict_app.def_logical_fallacy import *
from ast import parse
from collections import defaultdict
import json
import os
import asyncio
from prompts_eval import *
import argparse
import pandas as pd
import time
from check_score import *
from respond_role import *
import pandas

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_to_annotate", type=str, default='results/roleplay_test_1007_MISTRAL_')
    parser.add_argument("--components_to_read", type=str, default='chat_history_results/roleplay_test_1007_MISTRAL_')
    parser.add_argument("--definition", type=str, default='proposed')
    parser.add_argument("--use_category", type=bool, default=False)
    parser.add_argument("--use_toulmin", type=bool, default=True)
    parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='results/storytelling_test_1008_MISTRAL_')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=0)
    
    args = parser.parse_args()

    ann = args.file_to_annotate + str(args.num_gen) + ".xlsx"
    comm = args.components_to_read + str(args.num_gen) + ".xlsx"
    df_to_argue = pd.read_excel(ann)
    df_chat_history = pd.read_excel(comm)
    sentences = df_to_argue["modified_sample"].values.tolist()
    sentences = [j for j in sentences if str(j) != "nan"]
    chat_history = df_chat_history["chats"].values.tolist()
    profiles = df_to_argue["profile"].values.tolist()
    profiles = [j for j in profiles if str(j) != "nan"]
    # print(df_to_argue.loc[0])

    length_of_conversation = 5

    # model_student = "gpt-4o"
    model_agent = "gpt-4o"
    pers = []
    cohs = []
    rels = []
    clas = []
    cres = []
    fids = []
    divs = []
    hums = []

    for j in range(len(sentences)):
        # print(sentences[j])
        # sentence = sentences[j].split(",")[4]
        sentence = sentences[j].split("=")[7][:-5]
        history = chat_history[j]
        profile = profiles[j]

        print(sentence)
        eval_res_TEACHER = await generate_res("eval_t", model_agent, sentence, history, None, None, None, None, PROMPT_EVAL_TEACHER, 0)
        eval_t = json.loads(eval_res_TEACHER.choices[0].message.content)
        per = eval_t["1"]
        coh = eval_t["2"]
        rel = eval_t["3"]
        cla = eval_t["4"]
        cre = eval_t["5"]
        eval_res_STUDENT = await generate_res("eval_s", model_agent, sentence, history, profile, None, None, None, PROMPT_EVAL_STUDENT, 0)
        eval_s = json.loads(eval_res_STUDENT.choices[0].message.content)
        fid = eval_s["1"]
        div = eval_s["2"]
        hum = eval_s["3"]

        pers.append(per)
        cohs.append(coh)
        rels.append(rel)
        clas.append(cla)
        cres.append(cre)
        fids.append(fid)
        divs.append(div)
        hums.append(hum)


    data_dict = {
        "sentences": sentences,
        "persuasiveness": pers,
        "coherence": cohs,
        "relevance": rels,
        "clarity": clas,
        "credibility": cres,
        "fidelity": fids,
        "diversity": divs,
        "human-likeness": hums


    }
    df = pandas.DataFrame.from_dict(data_dict)

    df.to_excel("eval_" + args.save_fn + str(args.num_gen) + ".xlsx", index=False)
    print("done eval")

        

if __name__ == '__main__':
    asyncio.run(main())
