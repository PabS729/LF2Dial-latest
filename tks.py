import pandas as pd

reads = pd.read_excel("okk_all_gpt_k_rep.xlsx")


ks = [k for k in reads.keys() if (k not in ["sentences","chats"]) ]

for j in ks:
    # if j in ["divergence", "stance_change", "complex_refutation"]:
    #     continue
    print(j)
    fn = "classification_results/fd_" + str(j) + ".xlsx"
    print(fn)
    new_r = pd.read_excel(fn)
    # new_r_d = new_r[""]
    sts = new_r["chats"].values.tolist()
    small_k = []
    for s in sts:
        filt_s = reads[reads["chats"] == s]
        small_k.append(filt_s)
    smk = pd.concat(small_k)
    # new_df = pd.concat([fn, smk[j]], axis=1)
    smk.to_excel("res_qwq_k_" + j + ".xlsx")
