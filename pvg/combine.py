import subprocess
import sys
import pandas as pd

"""
combine.py
    ↓
运行
    ├── fragrance.py → fragrance.csv
    ├── shampoo.py   → shampoo.csv
    ├── hair.py      → hair.csv
    ├── serum.py     → serum.csv
    ├── cream.py     → cream.csv
    ├── eye.py       → eye.csv
    ├── bodywash.py  → bodywash.csv
    └── bodylotion.py → bodylotion.csv
                         ↓
                    combined.csv
"""

scripts = [
    "fragrance.py",
    "shampoo.py",
    "hair.py",
    "serum.py",
    "cream.py",
    "eye.py",
    "bodywash.py",
    "bodylotion.py",
]

csv_files = [
    "fragrance.csv",
    "shampoo.csv",
    "hair.csv",
    "serum.csv",
    "cream.csv",
    "eye.csv",
    "bodywash.csv",
    "bodylotion.csv",
]

# run every scraper
for script in scripts:
    print(f"\n===== Running {script} =====")

    result = subprocess.run(
        [sys.executable, script],
        check=True,
    )

# combine csv
dfs = []

for csv_file in csv_files:
    print(f"Reading {csv_file}")
    df = pd.read_csv(csv_file)

    # optional: remember source category
    df["source"] = csv_file.replace(".csv", "")

    dfs.append(df)


combined_df = pd.concat(dfs,ignore_index=True,)
combined_df.to_csv("combined.csv",index=False,encoding="utf-8-sig",)
print(f"\nCombined: {len(combined_df)} products")
print("Saved: combined.csv")

"""
fragrance.py ─┐
shampoo.py    │
hair.py       │
...           ├──> combined.csv ──┐
bodylotion.py ┘                    │
                                   ├──> UNION ──> final combined.csv
pvg.py ───────> pvg.csv ───────────┘
"""

# ============================================================
# Run pvg.py and read pvg.csv
# ============================================================
print("\n===== Running pvg.py =====")
subprocess.run([sys.executable, "pvg.py"],check=True,)
pvg_df = pd.read_csv("pvg.csv")
# pvg.py previously doesn't have source column
pvg_df["source"] = "pvg"
pvg_df.to_csv("pvg.csv",index=False,encoding="utf-8-sig")
print(f"PVG products: {len(pvg_df)}")

# ============================================================
# preprocess before MERGE
# ============================================================
# actualPrice = min(all price columns)
# msrp = max(all price columns)

def clean_csv(file):
    df = pd.read_csv(file)
    price_columns = ["price","originalPrice","costPrice","buyPrice","lowestPrice"]
    df[price_columns] = df[price_columns].apply(pd.to_numeric,errors="coerce")
    df["actualPrice"] = df[price_columns].min(axis=1)
    df["msrp"] = df[price_columns].max(axis=1)
    output = file.replace(".csv", "_clean.csv")
    df.to_csv(output,index=False,encoding="utf-8-sig")
    return df

combined_df_clean = clean_csv("combined.csv")
pvg_df_clean = clean_csv("pvg.csv")
# ============================================================
# UNION combined.csv + pvg.csv
# ============================================================
# combined_df_clean, pvg_df_clean
final_df = pd.concat([combined_df_clean, pvg_df_clean],ignore_index=True)

# 重复的检查是否actualprice和msrp一样，
# 如果不一样print出来 
# 然后keep lowest actualprice->完事了
alpha_found = False
duplicates = final_df[final_df.duplicated("goodsID", keep=False)]
for goods_id, group in duplicates.groupby("goodsID"):
    if group["actualPrice"].nunique() > 1 or group["msrp"].nunique() > 1:
        print("Alpha detected")
        print(f"\nPrice mismatch: goodsID = {goods_id}")
        print(group[["goodsID", "name", "actualPrice", "msrp", "source"]])
if not alpha_found:
    print("No alpha detected")
# keep the one with lowest actualPrice 
# final_df = final_df.drop_duplicates(subset="goodsID",keep="first")  
final_df = (final_df.sort_values("actualPrice").drop_duplicates("goodsID", keep="first"))    

final_df.to_csv("combined_final.csv",index=False,encoding="utf-8-sig")
print("Finished: combined_final.csv")
