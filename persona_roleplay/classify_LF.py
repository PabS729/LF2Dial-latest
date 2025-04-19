
from openai import OpenAI
from contradict_app.def_logical_fallacy import *
from ast import parse
from collections import defaultdict
import json
import os
import asyncio
from contradict_app.prompt_bank import *
from respond_role import * 
from contradict_app.def_logical_fallacy import *
import argparse
import pandas as pd
import time
from tqdm import tqdm


async def generate_response(model_name, sentence, prompt_gen, temperature=0):
    client = OpenAI()
    # llm = OpenAIChat(temperature=temperature, openai_api_key=API_KEY)
    
    await asyncio.sleep(0.01)

        
    p = prompt_gen
    user_prompt = p.format(sentence=sentence)
    msgs = []
    msgs.append({"role": "system", "content": user_prompt})

    #teacher and student take turns
    done = False
    while not done:
        try: 
            response = client.chat.completions.create(
            model=model_name,
        messages=msgs,
        temperature=temperature,
        response_format={ "type": "json_object" }
        )
            # print("done")
            done = True
        except:
            print("error caught, waiting...")
            time.sleep(60)
    return response


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_to_annotate", type=str, default='edu_train_final copy.xlsx')
    parser.add_argument("--components_to_read", type=str, default='decomposed_sentences_toulmin.xlsx')
    parser.add_argument("--definition", type=str, default='proposed')
    parser.add_argument("--use_category", type=bool, default=False)
    parser.add_argument("--use_toulmin", type=bool, default=True)
    parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='results/classification_full_cht_0808.xlsx')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=10)
    
    args = parser.parse_args()

    df_to_argue = pd.read_excel(args.file_to_annotate)
    df_components = pd.read_excel(args.components_to_read)
    
    # print(df_to_argue.loc[0])

    length_of_conversation = 5
    # st = df_to_annotate["Text"].tolist()
    # sampled_df = df_to_argue.groupby("updated_label").sample(n=1, random_state=1)
    
    sentences = df_to_argue["source_article"].values.tolist()
    gt_labels = df_to_argue["updated_label"].values.tolist()

    # model_teacher = model_student
    model_teacher = "gpt-3.5-turbo"
    sampled_sentence = []
    sampled_labels = []
    full = []
    for k in range(12):
        full.append([])
    for j in tqdm(range(len(sentences))):
        example_argument = sentences[j]
        # ct = 0
        # for k in fallacy_dc.keys():
        #     results_conversation_teacher = await generate_response(model_teacher, example_argument, k, fallacy_dc[k], SYSTEM_CHECK, 0)
        #     cat = results_conversation_teacher.choices[0].message.content
        #     cat = json.loads(cat)["1"]
        #     full[ct].append(cat)
        #     ct+=1
        results_conversation_teacher = await generate_response(model_teacher, example_argument, SYSTEM_CLASSIFY_FALLACY, 0)
        cat = results_conversation_teacher.choices[0].message.content
        cat = json.loads(cat)["1"]
        sampled_labels.append(cat)

    data_dict = {'sentence_sample': sentences, 'labels': sampled_labels, 'gt_labels': gt_labels}
    # data_dict = {"sentence": sentences, "gt_labels": gt_labels}
    # print(len(full[0]))
    # ct = 0
    # for k in fallacy_dc.keys():
    #     data_dict[k] = full[ct]
    #     ct+=1
    df_result = pd.DataFrame(data_dict)
    df_result.to_excel(args.save_fn, index=False)
    print("done async")


if __name__ == '__main__':
    asyncio.run(main())
