import pandas as pd
from alert import send_alert

"""
Merge + Cross-Source Alpha Detection

for Home Preview Product
        │
        │
Search 有吗?
        │
        ▼
Merge
        │
        ├── 有, 重复SKU → 检查是否一致/是否有套利空间 by diff price,discount etc
        │        │
        │        ├── 一致 → skip
        │        └── 不一致 → 有Alpha,Alert
        │
        ├── 没有, Home独有 → Append
        │
        │
        ▼
today_skincare.csv

对于home_preview_perfume.csv和clearance_perfume.csv做同样的流程处理
"""

print("=" * 60)
print("Merge Skincare Clearance")
print("=" * 60)

search_skincare = pd.read_csv("clearance_skincare.csv")
home_skincare = pd.read_csv("home_preview_skincare.csv")

alerts_skincare = []

merged = search_skincare.copy()