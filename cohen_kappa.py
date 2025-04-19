from sklearn.metrics import cohen_kappa_score
import pandas as pd

reads_haiku = pd.read_excel("res_new/processed_gpt_new.xlsx")
reads_qwq = pd.read_excel("res_new/processed_gpt.xlsx")
reads_o3 = pd.read_excel("res_new/processed_o3.xlsx")
kdd = [k for k in reads_o3.keys() if k not in ["sentences", "chats", "Unnamed: 0"]]


# for j in kdd:
#     # if j in ["divergence", "stance_change", "complex_refutation", "guidance", "terms"]:
#     #     continue
#     print(j)
#     tor = pd.read_excel("classification_results/fn_" + j + "_final.xlsx")
#     son = j + "_sonnet"
#     o3 = j
#     qwq = j + "_d"
#     haiku = j + "_h"
#     qwq_s = [i for i in tor[qwq]]
    
#     kd = [o3, haiku, son]
#     for k in kd:
#         ks = [i for i in tor[k]]
#         ck = cohen_kappa_score(qwq_s, ks)
#         print(k, ck)

for j in kdd:
    # if j in ["divergence", "stance_change", "complex_refutation", "guidance", "terms"]:
    #     continue
    print(j)
    
    qwq_s = [i for i in reads_qwq[j]]
    o3_s = [i for i in reads_o3[j]]
    haiku_s = [i for i in reads_haiku[j]]
    ck = cohen_kappa_score(qwq_s, o3_s)
    ck_1 = cohen_kappa_score(qwq_s, haiku_s)
    ck_4 = cohen_kappa_score(o3_s, haiku_s)
    print(ck, ck_1, ck_4)



    
    