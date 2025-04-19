from ast import parse
from collections import defaultdict
import json
import os
import asyncio
import argparse
import pandas as pd
import time
from persona_roleplay.respond_role import *
import pandas
from prompt_eval import *

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dialogue1", type=str, default='results/bsc_0221_fsm_sp10')
    parser.add_argument("--dialogue2", type=str, default='results/bsc_0221_sp10')
    parser.add_argument("--dataset", type=str, default='pos_train_set.csv')
    parser.add_argument("--use_category", type=bool, default=False)
    parser.add_argument("--use_toulmin", type=bool, default=True)
    parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='results/eval_bsc_sp10_r')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=0)
    
    args = parser.parse_args()

    ann = args.dialogue1
    history1 = "chat_history_" + ann + ".xlsx"
    history2 = "chat_history_" + args.dialogue2 + ".xlsx"
    df_to_argue = pd.read_csv(args.dataset)

    dialogues_1 = pd.read_excel(history1)
    dialogues_2 = pd.read_excel(history2)
    sentences = df_to_argue.sample(n = 10, random_state=4)
    sentences = sentences["Context"].values.tolist()
    dl1 = dialogues_1["chats"].values.tolist()
    dl2 = dialogues_2["chats"].values.tolist()
    print(len(dl2), len(sentences))
    model_agent = "gpt-4o"

    goods_1 = []
    goods_2 = []

    for j in range(len(sentences)):
        sentence = sentences[j]
        dialogue1 = dl1[j]
        dialogue2 = dl2[j]

        eval_res = await generate_res("eval_s", model_agent, sentence, dialogue1, dialogue2, None, None, None, COMPARE_DIALOGUES, 0)
        eval_coh = load_json(eval_res.choices[0].message.content)
        goods_1.append(eval_coh["ans_1"])
        goods_2.append(eval_coh["ans_2"])

    data_dict = {"sentences": sentences, "eval_1": goods_1, "eval_2": goods_2}

    df = pandas.DataFrame.from_dict(data_dict)

    df.to_excel("eval_" + args.save_fn + str(args.num_gen) + ".xlsx", index=False)
    print("done eval")

if __name__ == '__main__':
    asyncio.run(main())