import pandas as pd

doc = pd.read_excel("results/fsm_EXP_0318_150.xlsx")

# doc = doc[doc["following"] != '0']
T = doc['teacher_response'].values.tolist()
S = doc['layman_response'].values.tolist()
id = doc['teacher_analysis'].values.tolist()

all_his = []
chat_his = ""
i = 0
while i < len(T):
    next_id = "0"
    if id[i] == "A":
        next_id = "A"
        chat_his += "Teacher: " + T[i] + "\n" + "Student: " + S[i] + '\n'
        i+=1
        # print(i)
        while i < len(T) and id[i] != next_id :
            if "It seems that we have different opinions on this:" in T[i]:
                i+=1
                continue
            chat_his += "Teacher: " + T[i] + "\n" + "Student: " + S[i] + '\n'
            i+=1
            # print(i)
        all_his.append(chat_his)
    chat_his = ''
data_dic = {"chats": all_his} 
df = pd.DataFrame(data_dic)

df.to_excel("chat_history_results/fsm_EXP_0318_150.xlsx")

