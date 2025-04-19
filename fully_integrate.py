import pandas as pd


# dffs = []
# for i in range(0, 1000, 100):
#     # fname = "chat_history_results/bsc_0222_base_"+str(i)+"_o.xlsx"
#     fn_2 = "eval_results/classify_gpt_k_rep_"+str(i)+".xlsx"
#     # df = pd.read_excel(fname)
#     df_2 = pd.read_excel(fn_2)
#     # df = pd.concat([df, df_2], axis = 1)
#     dffs.append(df_2)

# new_df = pd.concat(dffs, axis=0)
# new_df.to_excel("okk_all_gpt_k_rep.xlsx")

dffs = []
for i in range(0, 1000, 100):
    # fname = "chat_history_results/bsc_0222_base_"+str(i)+"_o.xlsx"
    fn_2 = "eval_results/fsm_0329_all_"+str(i)+".xlsx"
    # df = pd.read_excel(fname)
    df_2 = pd.read_excel(fn_2)
    # df = pd.concat([df, df_2], axis = 1)
    dffs.append(df_2)

new_df = pd.concat(dffs, axis=0)
new_df.to_excel("processed_all_fsm_a.xlsx")
# dffs = []
# for i in range(50, 250, 50):
#     fname = "eval_results/classify_base_2_"+str(i)+"_new0.xlsx"
#     df = pd.read_excel(fname)
#     dffs.append(df)

# new_df = pd.concat(dffs, axis=0)

# nf = new_df.to_excel("okk_all_new_2.xlsx")

# fd = pd.read_csv("pos_train_set.csv")
# fd = fd.drop_duplicates(["Context"]).to_csv("st_wo_duplicates.csv")

