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


combined_df = pd.concat(
    dfs,
    ignore_index=True,
)


combined_df.to_csv(
    "combined.csv",
    index=False,
    encoding="utf-8-sig",
)


print(
    f"\nCombined: {len(combined_df)} products"
)

print("Saved: combined.csv")