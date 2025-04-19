import pandas as pd

reads = pd.read_excel("okk_all_new.xlsx")

kdd = [k for k in reads.keys() if k not in ["sentences", "chats", "Unnamed: 0"]]


for j in kdd:
    # if j in ["divergence", "stance_change", "complex_refutation", "guidance", "terms"]:
    #     continue
    print(j)
    tor = pd.read_excel("classification_results/fn_" + j + "_final.xlsx")
    k = j + "_sonnet"
    sp_pos = tor[tor["label"] == "yes"].sample(n=15)
    sp_neg = tor[tor["label"] == "no"].sample(n=15)

    TP = len(sp_pos[sp_pos[k] == "yes"])
    FN = len(sp_pos[sp_pos[k] == "no"])

    TN = len(sp_neg[sp_neg[k] == "no"])
    FP = len(sp_neg[sp_neg[k] == "yes"])

    F1 = TP * 2 / (TP * 2 + FN + FP)
    print(TP, FP, TN, FN)
    print(k, F1)