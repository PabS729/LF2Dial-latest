
from openai import OpenAI
from contradict_app.def_logical_fallacy import *
from ast import parse
from collections import defaultdict
import json
import os
import asyncio
from contradict_app.prompt_bank import *
from contradict_app.def_logical_fallacy import *
import argparse
import pandas as pd
import time
from tqdm import tqdm
from dotenv import load_dotenv
import anthropic
from mistralai.client import MistralClient
from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage


load_dotenv()
key = os.getenv("ANTHROPIC_API_KEY")
# key = os.environ["ANTHROPIC_API_KEY"]
# print(key)
client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=key,
)
# key = os.environ["MISTRAL_API_KEY"]


async def check_score(model_name, sentence, example, system, prompt_gen, temperature=0):
    
    # llm = OpenAIChat(temperature=temperature, openai_api_key=API_KEY)
    
    await asyncio.sleep(0.01)

    # cl = MistralClient(api_key=key)
    p = prompt_gen
    user_prompt = p.format(sentence=sentence, example=example)
    msgs = []
    msgs.append(ChatMessage(role="user", content=user_prompt))

    #teacher and student take turns
    done = False
    while not done:
        try: 
            message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            temperature=temperature,
            messages=msgs,
            # tool_choice={ "type": "json_object" }
        )
            # message = msgs
            # response = client.chat_stream(model=model_name, messages=msgs)
            
            # print(next(response))
            print("done")
            done = True
        except Exception as e:
            print("error caught, waiting...")
            print(e)
            time.sleep(60)
    return message


#For testing Mistralai/Claude 3.5 API only
async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_to_annotate", type=str, default='edu_train_final.csv')
    parser.add_argument("--components_to_read", type=str, default='decomposed_sentences_toulmin.xlsx')
    parser.add_argument("--definition", type=str, default='proposed')
    parser.add_argument("--use_category", type=bool, default=False)
    parser.add_argument("--use_toulmin", type=bool, default=True)
    parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='results/m_claude.xlsx')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=10)
    
    args = parser.parse_args()

    df_to_argue = pd.read_csv(args.file_to_annotate)
    df_components = pd.read_excel(args.components_to_read)
    
    # print(df_to_argue.loc[0])

    length_of_conversation = 5
    # st = df_to_annotate["Text"].tolist()
    # sampled_df = df_to_argue.groupby("updated_label").sample(n=1, random_state=1)
    
    sentences = df_to_argue["source_article"].values.tolist()
    gt_labels = df_to_argue["updated_label"].values.tolist()

    # model_teacher = model_student
    model_agent = "mistral-large-latest"
    sampled_sentence = []
    sampled_labels = []
    full = []
    for k in range(12):
        full.append([])
    for j in tqdm(range(5)):
        
        example_argument = sentences[j]
        print(example_argument)

        results_rational_agent = check_score(model_agent, example_argument, SYSTEM_CLASSIFY_FALLACY, 0)
        # score = results_conversation_teacher.content[0].text
        # print(results_rational_agent)
        score = results_rational_agent.content[0].text
        print(score)

    data_dict = {'sentence_sample': sentences, 'labels': sampled_labels, 'gt_labels': gt_labels}

    df_result = pd.DataFrame(data_dict)
    df_result.to_excel(args.save_fn, index=False)
    print("done async")


if __name__ == '__main__':
    asyncio.run(main())
