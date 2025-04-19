


from openai import OpenAI
from contradict_app.def_logical_fallacy import *
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
import anthropic
import dotenv
async def eval_claude(role, model_name, sentence, history, profile, target_statement, 
                            teacher_res, student_res, prompt_gen, temperature=0):
   
    user_prompt = prompt_gen.format(sentence=sentence, history=history, profile=profile)
    dotenv.load_dotenv(".env")
    env_key = os.environ.get("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(
        
        api_key=str(env_key),
    )
    done = False
    while not done:
        try:
            message = client.messages.create(
                model=model_name,
                max_tokens=8192,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            done = True
        except Exception as e:
            print(e)
            time.sleep(5)
    return message

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dialogue1", type=str, default='results/div_fsm_0216_33_s')
    parser.add_argument("--dialogue2", type=str, default='results/div_base_0216_33_s')
    parser.add_argument("--dataset", type=str, default='pos_train_set.csv')
    parser.add_argument("--use_category", type=bool, default=False)
    parser.add_argument("--use_toulmin", type=bool, default=True)
    parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='results/eval_33_diver_rev')
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
    sentences = df_to_argue.groupby('Label').sample(n = 5, random_state=33)
    sentences = sentences["Context"].values.tolist()
    dl1 = dialogues_1["chats"].values.tolist()
    dl2 = dialogues_2["chats"].values.tolist()
    print(len(dl2), len(sentences))
    # print(df_to_argue.loc[0])

    length_of_conversation = 5

    # model_student = "gpt-4o"
    model_agent = "gpt-3.5-turbo"

    cohs = []
    rels = []
    info = []
    arg = []
    help = []
    ded = []

    arr1 = [[],[],[],[],[],[]]
    arr2 = [[],[],[],[],[],[]]
    arr3 = [[],[],[],[],[],[]]
    arr_name_1 = ["coherence", "relevance", "informativeness", "argumentativeness", "activeness", "stance change"]
    arr_name_2 = ["coherence_2", "relevance_2", "informativeness_2", "argumentativeness_2", "activeness_2", "stance change_2"]
    arr_name_3 = ["more coherence", "more relevance", "more informativeness", "more argumentativeness", "more activeness", "more stance change"]
    cohs_2 = []
    rels_2 = []
    info_2 = []
    arg_2 = []
    help_2 = []
    ded_2 = []

    r_cohs = []
    r_rels = []
    r_info = []
    r_arg = []
    r_help = []
    r_ded = []


    eval_prompts = [EVAL_COHERENCE, EVAL_CONSISTENCY, EVAL_TEACHER_HELP, EVAL_VALID_ARGUMENTS, EVAL_TEACHER_ACTIVE, EVAL_STANCE_MAINTENANCE]
    eval_al = [False, True, False, False, False, False]
    # eval_al = [True, True, True, True, True, True]
    for j in range(len(sentences)):
        # print(sentences[j])
        # sentence = sentences[j].split(",")[4]
        sentence = sentences[j]
        dialogue1 = dl2[j]
        dialogue2 = dl1[j]

        print(sentence)
        for k in range(0, len(eval_al)):
            if eval_al[k] == True:
                eval_res_COH = await eval_claude("eval_s", model_agent, sentence, dialogue1, dialogue2, None, None, None, eval_prompts[k], 0)
                eval_coh = load_json(eval_res_COH.content[0].text)
                while eval_coh == False:
                    eval_res_COH = await eval_claude("eval_s", model_agent, sentence, dialogue1, dialogue2, None, None, None, eval_prompts[k], 0)
                    eval_coh = load_json(eval_res_COH.content[0].text)
                arr1[k].append(eval_coh["ans_1"])
                arr2[k].append(eval_coh["ans_2"])
                arr3[k].append(eval_coh["reason"])

        # eval_res_RELE = await generate_res("eval_s", model_agent, sentence, dialogue1, dialogue2, None, None, None, EVAL_CONSISTENCY, 0)
        # eval_rele = json.loads(eval_res_RELE.choices[0].message.content)
        # eval_res_INFO = await generate_res("eval_s", model_agent, sentence, dialogue1, dialogue2, None, None, None, EVAL_INFORMATION_DIV, 0)
        # eval_info = json.loads(eval_res_INFO.choices[0].message.content)
        # eval_res_ARG = await generate_res("eval_s", model_agent, sentence, dialogue1, dialogue2, None, None, None, EVAL_VALID_ARGUMENTS, 0)
        # eval_arg = json.loads(eval_res_ARG.choices[0].message.content)
        # eval_res_HELP = await generate_res("eval_s", model_agent, sentence, dialogue1, dialogue2, None, None, None, EVAL_TEACHER_ACTIVE, 0)
        # eval_help = json.loads(eval_res_HELP.choices[0].message.content)
        # eval_res_DEF = await generate_res("eval_s", model_agent, sentence, dialogue1, dialogue2, None, None, None, EVAL_STANCE_MAINTENANCE, 0)
        # eval_def = json.loads(eval_res_DEF.choices[0].message.content)

        # cohs.append(eval_coh["ans_1"])
        # # rels.append(eval_rele['ans'])
        # info.append(eval_info['ans_1'])
        # arg.append(eval_arg['ans_1'])
        # help.append(eval_help['ans_1'])
        # ded.append(eval_def['ans_1'])
                
                
        # cohs_2.append(eval_coh["ans_2"])
        # # rels.append(eval_rele['ans'])
        # info_2.append(eval_info['ans_2'])
        # arg_2.append(eval_arg['ans_2'])
        # help_2.append(eval_help['ans_2'])
        # ded_2.append(eval_def['ans_2'])

        # r_cohs.append(eval_coh["reason"])
        # # r_rels.append(eval_rele["reason"])
        # r_info.append(eval_info["reason"])
        # r_arg.append(eval_arg["reason"])
        # r_help.append(eval_help["reason"])
        # r_ded.append(eval_def['reason'])

    data_dict = {"sentences": sentences}
    for k in range(0, len(eval_al)):
            if eval_al[k] == True:
                data_dict[arr_name_1[k]] = arr1[k]
                data_dict[arr_name_2[k]] = arr2[k]
                data_dict[arr_name_3[k]] = arr3[k]

    # data_dict = {
    #     "sentences": sentences,
    #     "coherence": cohs,
    #     "coherence_2": cohs_2,
    #     "reason for coherence": r_cohs,
    #     # "relevance": rels,
    #     # "reason for relevance": r_rels,
    #     "informativeness": info,
    #     "informativeness_2": info_2,
    #     "reason for informativeness": r_info,
    #     "argumentativeness": arg,
    #     "argumentativeness_2": arg_2,
    #     "reason for argumentativeness": r_arg,
    #     "helpfulness":help,
    #     "helpfulness_2":help_2,
    #     "reason for helpfulness": r_help,
    #     'stance changes': ded,
    #     'stance changes_2': ded_2,
    #     'reason for stance change': r_ded,



    # }
    df = pandas.DataFrame.from_dict(data_dict)

    df.to_excel("eval_" + args.save_fn + str(args.num_gen) + ".xlsx", index=False)
    print("done eval")

        

if __name__ == '__main__':
    asyncio.run(main())

