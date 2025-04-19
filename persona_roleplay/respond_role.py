from openai import OpenAI
import asyncio
import time
# from mistralai.client import MistralClient
import os
import json
import dotenv
def load_json(json_f):
    success = False
    try:
        ret = json.loads(json_f)
        success = True
    except Exception as e:
        print("load json error, retrying...")
        print(e)
    if success == True:
        return ret
    else:
        return success

async def generate_res(role, model_name, sentence, history, profile, target_statement, 
                            teacher_res, student_res, prompt_gen, temperature=0):
    # if role == "t_edu":
    #     client = MistralClient(api_key=os.environ["MISTRAL_API_KEY"])
    #     # print("c")
    # else:
    #     client = OpenAI()
    dotenv.load_dotenv(".env")
    env_key = os.environ.get("OPENAI_API_KEY")
    ds_key = os.environ.get("QF_API_KEY")
    OF_key = os.environ.get("DS_API_KEY")
    QW_key = os.environ.get("QWEN_API_KEY")
    if model_name in ["deepseek-reasoner", "deepseek-r1"]:
        # client = OpenAI(base_url="https://qianfan.baidubce.com/v2", api_key=ds_key)
        client = OpenAI(base_url="https://api.deepseek.com/v1", api_key=OF_key)
    elif model_name == "qwq-32b":
        client = OpenAI(base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", api_key=QW_key)
    else:
        client = OpenAI(api_key=str(env_key))

    p = prompt_gen
    msgs = []
    if role == "agent" : 
        user_prompt = p.format(sentence=sentence, history=history)
    elif role in ["fact_bank", "gen_strategy", "student", "conv"]:
        user_prompt = p.format(sentence=sentence)
        # user_prompt = p.format(sentence=sentence, NAME = profile["NAME"], AGE = profile["AGE"], BELIEF = profile["BELIEF"], BIAS = profile["BIAS"], PERSONALITY = profile["PERSONALITY"], EDU_LEVEL = profile["EDU_LEVEL"])
    elif role == "teacher" or role == "thought":
        user_prompt = p.format(sentence=sentence, history=history)
    elif role in ["strategy", "teacher_st", "eval_s", "t_edu", "test", "evl"]:
        user_prompt = p.format(sentence=sentence, history=history, profile=profile)
    elif role in ["exp", "check", "tea_strat"]:
        user_prompt = p.format(sentence=sentence, history=history, profile=profile, target_statement=target_statement)
    else:
        user_prompt = p.format(sentence=sentence, history=history)
    

    msgs.append({"role": "system", "content": user_prompt})

    if model_name in ["deepseek-r1","deepseek-reasoner", "qwq-32b"]:
        if role in ["teacher", "agt"]:
            msgs.append({"role": "user", "content": "Talk to the student. Make sure to limit your response in 50 words or less."})
        else:
            msgs.append({"role": "user", "content": "Classify the sentence according to the instruction above. Respond in this form: the answer should be 'yes' / the answer should be 'no'."})

    #teacher and student take turns
    if role in ["teacher_st", "teacher", "t_edu", "exp", "old"]: 
        for (t,s) in zip(teacher_res, student_res):
            msgs.append({"role": "assistant", "content": t})
            msgs.append({"role": "user", "content": s})
    if role in ["student", "student_bio", "stu"]:
        # msgs.append({"role": "system", "content": user_prompt})
        if zip(teacher_res[:-2], student_res) != None: 
            for (t,s) in zip(teacher_res[:-2], student_res):
                msgs.append({"role": "user", "content": t})
                msgs.append({"role": "assistant", "content": s})
        msgs.append({"role": "user", "content": teacher_res[-1]})
    # print(msgs)
    done = False
    while not done:
        try: 
            if model_name in ["o3-mini", "deepseek-r1", "deepseek-reasoner", "qwq-32b"]:
                response = client.chat.completions.create(
                model=model_name,
                stream=True,
            messages=msgs,
            )
            elif role in ["old","check","", "fact_bank", "find_contradiction", "strategy", "thought", "gen_strategy", "agent", "eval_t", "stu", 'eval_s']:
                response = client.chat.completions.create(
                model=model_name,
            messages=msgs,
            temperature=temperature,
            response_format={ "type": "json_object" }
            )
            # elif role == "t_edu":
            #     response = client.chat(
            #     model="mistral-large-latest",
            # messages=msgs,
            # temperature=temperature,
            # )
            else:
                response = client.chat.completions.create(
                model=model_name,
                messages=msgs,
                temperature=temperature,
                )
            # print("done")
            done = True
        except Exception as e:
            print("error caught, waiting...", e)
            time.sleep(10)
    return response
    