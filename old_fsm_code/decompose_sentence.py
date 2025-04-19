from openai import OpenAI
from contradict_app.def_logical_fallacy import *
from ast import parse
from collections import defaultdict
import json
import os
import asyncio
from prompts_init import *
import argparse
import pandas as pd

async def get_response(model_name, sentence, sys_prompt, user_prompt):
    client = OpenAI()

    await asyncio.sleep(0.1)
    user_prompt = user_prompt.format(sentence=sentence)
    message = []
    message.append({"role": "system", "content": sys_prompt})
    message.append({"role": "user", "content": user_prompt})
    response = client.chat.completions.create(
        model=model_name,
        response_format={ "type": "json_object" },
        messages=message,
        temperature=0
    )
    return response

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_to_annotate", type=str, default='edu_train_cleaned.csv')
    parser.add_argument("--definition", type=str, default='proposed')
    parser.add_argument("--use_category", type=bool, default=True)
    parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='decomposed_sentences_tou_sample2.xlsx')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=10)
    args = parser.parse_args()

    df_to_argue = pd.read_csv(args.file_to_annotate)
    # print(df_to_argue.loc[0])

    length_of_conversation = 5
    # st = df_to_annotate["Text"].tolist()
    sampled_df = df_to_argue.groupby("updated_label").sample(n=1, random_state=2)
    
    sentences = sampled_df["source_article"].values.tolist()
    # sentences = [
    #     "That's what abortion is - killing innocent humans for money. Abortionists are government licensed hit men.""That's what abortion is - killing innocent humans for money. Abortionists are government licensed hit men.",
    #     "Marie notices that many of her friends have started eating a low-carb diet and drinking protein shakes. Marie decides that if this many friends are eating this way that this must be the healthy way to eat so she joins them. This is an example of which logical fallacy?",
    #     "You'll make the right decision because you have something that not many people do: you have heart.",
    #     "Pamela never lies. She told me herself, so it must be true.",
    #     "When the judge asked the defendant why he hadn't paid his parking fines, he said that he shouldn't have to pay them because the sign said 'Fine for parking here' and so he naturally presumed that it would be fine to park there.",
    #     "My brother's girlfriend's Mother's hairdresser said that COVID numbers are going down, so I'm not going to bother with my mask",
    #     "If the argument is supposed to be about whether or not we, as the American public should wear masks, and you argue: 'Asking an infant to wear a mask is ridiculous!'",
    #     "All forest creatures live in the woods.All leprechauns are forest creatures.Therefore, some leprechauns live in the woods.",
    #     "Mother: It’s bedtime Jane Jane: Mom, how do ants feed their babies? Mother: Don’t know dear, close your eyes now. Jane: But mama, do ant babies cry when they’re hungry?",
    #     "every time Joe goes swimming he is wearing his Speedos. Something about wearing that Speedo must make him want to go swimming.",
    #     "If you don’t say the Pledge of Allegiance, then you must be a traitor.",
    #     "If I don't take the right classes in high school, then I won't be able to get into a good college. If I don't get into a good college, then I won't be able to get a job. If I can't get a job, then I am going to end up homeless.",
    #     "Is your stupidity inborn?"
    # ]
    print(len(sentences))
    model = "gpt-4-turbo-2024-04-09"
    sys_prompt = GENERIC_SYSTEM_PROMPT
    user_prompt = USER_PROMPT_TOULMIN
    cl = []
    gr = []
    wa = []
    bk = []
    ql = []
    rb = []
    for j in range(len(sentences)):
        print(sentences[j])
        res = await get_response(model, sentences[j], sys_prompt, user_prompt)
        res_dict = res.choices[0].message.content
        print(res_dict)
        res_dict = json.loads(res_dict)
        cl.append(res_dict["CLAIM"])
        gr.append(res_dict["GROUND"])
        wa.append(res_dict["WARRANT"])
        bk.append(res_dict["BACKING"])
        ql.append(res_dict["QUALIFIER"])
        rb.append(res_dict["REBUTTAL"])


    data_dict = {
        "sentence": sentences,
        "claim": cl,
        "ground": gr,
        "warrant": wa,
        "backing": bk,
        "qualifier": ql, 
        "rebuttal": rb
    }
    df_result = pd.DataFrame(data_dict)
    df_result.to_excel(args.save_fn, index=False)
    print("done async")


if __name__ == '__main__':
    asyncio.run(main())


