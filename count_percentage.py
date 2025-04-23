import pandas as pd
import random
import math
import asyncio
from persona_roleplay.respond_role import generate_res
fi = pd.read_excel("processed_term_base_a.xlsx", index_col=None)
# from sklearn.utils import shuffle


fks = []
kdd = [k for k in fi.keys() if k not in ["sentences", "chats", "Unnamed: 0"]]


fi_1 = fi.drop_duplicates(["sentences"])
print(len(fi_1["sentences"]))
fi2 = pd.read_excel("processed_fsm_eval_div.xlsx")
# comb = pd.concat([fi_1, fi2], axis=0)
comb = fi
# comb.replace(to_replace=r'yes*|Yes*',
#            value="yes")
# comb.replace()
# print(comb)
# comb.to_excel("all_talk_ds.xlsx")
for k in kdd:
    # comb[k] = comb[k].str.replace(r'yes*|Yes*', "yes")
    # comb[k] = comb[k].str.replace(r'no*|No*', "no")
    fks.append(comb[k].values.tolist())
# print(comb)
# ln = [k for k in fi.keys()]
st_note_yes = {}
st_note_no = {}
for k in kdd:
    st_note_yes[k] = []
    st_note_no[k] = []
print(len(comb))

PROMPT_J = """
As an assistant, check if the teacher's <response> expresses whether the teacher's behavior fits <key>. Answer with "yes" or "no" only.

<response>: {sentence}
<key>: {history}

"""
comb_b = comb.copy()
yesss = [0 for j in range(len(kdd))]
nooo = [0 for j in range(len(kdd))]
async def sd():
    cta = 0
    for (ar, k) in zip(fks, kdd):
        if k == "guidance":
            ks = "passive " + k
        elif k == "perspective":
            ks = "balanced " + k 
        elif k == "terms":
            ks = k + " without explanation"
        else:
            ks = k
        print(k)
        yes = 0
        no = 0
        # print(ar)
        ct = 0
        for j,st in zip(ar, comb["sentences"]):
            
            # print(j)
            # print(ct)
            left = str(j).lower().split("the answer should be")
            # print(left)
            if len(left) > 1 and "yes" in left[1]:
                yes+=1
                comb_b.loc[ct, k] = "yes"
                st_note_yes[k].append(st)
            elif "yes" in j.lower():
            # if "yes" in j[:5].lower():
                yes+=1
                comb_b.loc[ct, k] = "yes"
                st_note_yes[k].append(st)
            elif len(left) > 1 and "no" in left[1]:
                no+=1
                comb_b.loc[ct, k] = "no"
                st_note_no[k].append(st)
            else:
                res = str(j).split("\n")[-1]
                re = await generate_res("aft", "gpt-4o-mini", res, ks, None, None, None, None, PROMPT_J, 0)
                
                re = re.choices[0].message.content
                print(res)
                print(re)
                if "yes" in re.lower():
                    yes+=1
                    comb_b.loc[ct, k] = "yes"
                    st_note_yes[k].append(st)
                else:
                    no+=1
                    comb_b.loc[ct, k] = "no"
                    st_note_no[k].append(st)
            ct+=1
        
        print(yes, no)
        yesss[cta] = yes
        nooo[cta] = no
        cta += 1
        print(len(st_note_yes[k]),len(st_note_no[k]))
    return True
d = asyncio.run(sd())
print(yesss)
print(nooo)
comb_b.to_excel("processed_base_eval_term_a.xlsx")
# for k in kdd:
#     random.seed(20)
#     if k in ["divergence", "stance_change", "complex_refutation", "stance_change", "structured"]:
#         continue
#     # rd_yes = random.sample(st_note_yes[k], 15)
#     # rd_no = random.sample(st_note_no[k], 15)
#     # nl_yes = comb.query("sentences == @rd_yes and ")
#     # nl_no = comb.query("sentences == @rd_no"
#     print(k)
#     nl_yes = comb[comb[k] == "yes"].sample(n=7, random_state = 100)
#     nl_no = comb[comb[k] == "no"].sample(n=7, random_state = 100)

#     comab = pd.concat([nl_yes, nl_no], axis=0)
#     # comab.filter(["sentences", "chats", k]).to_excel("resbbb_"+k+".xlsx")
#     shuf = comab.filter(["sentences", "chats"]).sample(frac=1)

    # shuf.to_excel("shuf_gpt_qwq_" + k + ".xlsx")



# print(st_note_yes[k][:30])
    
