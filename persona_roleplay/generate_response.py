from openai import OpenAI
import asyncio
import time

role_bank = ["agent", "fact_bank", "find_contradiction", "point_out", "student", "get_agreement", "check_agreement"]

async def generate_response(role, model_name, sentence, history, bank, target_statement, 
                            teacher_res, student_res, prompt_gen, temperature=0):
    client = OpenAI()

    p = prompt_gen
    msgs = []
    if role == "agent" : 
        user_prompt = p.format(sentence=sentence, chat_history=history)
    elif role in ["fact_bank", "convince"]:
        user_prompt = p.format(sentence=sentence)
    elif role in ["find_contradiction", "point_out"]: 
        user_prompt = p.format(sentence=sentence, fact_bank=bank)
    elif role == "counter_ex":
        user_prompt = p.format(sentence=sentence, counter=history)
    elif role == "student":
        user_prompt = p.format(sentence=sentence, agreement_bank=bank)
    else:
        user_prompt = p.format(sentence=sentence, agreement_bank=bank, target_statement=target_statement)
    

    msgs.append({"role": "system", "content": user_prompt})

    #teacher and student take turns
    if role in ["get_agreement", "convince"]: 
        for (t,s) in zip(teacher_res, student_res):
            msgs.append({"role": "assistant", "content": t})
            msgs.append({"role": "user", "content": s})
    if role == "student":
        if zip(teacher_res[:-2], student_res) != None: 
            for (t,s) in zip(teacher_res[:-2], student_res):
                msgs.append({"role": "user", "content": t})
                msgs.append({"role": "assistant", "content": s})
        msgs.append({"role": "user", "content": teacher_res[-1]})
    done = False
    while not done:
        try: 
            if role in ["fact_bank", "find_contradiction", "counter_ex"]:
                response = client.chat.completions.create(
                model=model_name,
            messages=msgs,
            temperature=temperature,
            response_format={ "type": "json_object" }
            )
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
            time.sleep(60)
    return response