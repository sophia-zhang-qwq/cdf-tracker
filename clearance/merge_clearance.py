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

# A Rule Engine
CHECK_RULES = [
    ("price", "Price", 0.01),
    ("originalPrice", "Original Price", 0.01),
    ("priceDiscount", "Price Discount", 0.1),
    ("activityDiscount", "Activity Discount", 0.1),
    ("activityStock", "Activity Stock", 0),
    ("stock", "Stock", 0),
]

search_skincare = pd.read_csv("clearance_skincare.csv")
home_skincare = pd.read_csv("home_preview_skincare.csv")

import pandas as pd

from alert import send_alert


def merge_clearance(search_csv, home_csv, output_csv, category):
    print("=" * 60)
    print(f"Merge {category}")
    print("=" * 60)
    search = pd.read_csv(search_csv)
    home = pd.read_csv(home_csv)
    merged = search.copy()
    alerts = []
    # --------------------------------------------------
    # Home Preview Products
    # --------------------------------------------------
    for _, home_row in home.iterrows():
        product_id = home_row["productId"]
        match = search[search["productId"] == product_id]
        # --------------------------------------------------
        # In Search? No, Home ONLY, Append to Search
        # --------------------------------------------------
        if match.empty:
            merged = pd.concat([merged,pd.DataFrame([home_row])],ignore_index=True)
            continue
        # --------------------------------------------------
        # In Search? Yes, Same Product,Check for Alpha
        # --------------------------------------------------
        search_row = match.iloc[0]
        alpha_rules = []
        # Cross Source Alpha
        # Rule 1
        for col, title, tol in CHECK_RULES:
            search_value = search_row[col]
            home_value = home_row[col]
            # both NaN
            if pd.isna(search_value) and pd.isna(home_value):
                continue
            # one side NaN
            if pd.isna(search_value) != pd.isna(home_value):
                alpha_rules.append(
                    f"{title}\n"
                    f"Search : {search_value}\n"
                    f"Home   : {home_value}"
                )
                continue
            # both numeric values
            if (pd.api.types.is_number(search_value) and pd.api.types.is_number(home_value)):
                if abs(search_value - home_value) > tol:
                    alpha_rules.append(
                        f"{title}\n"
                        f"Search : {search_value}\n"
                        f"Home   : {home_value}")
        # --------------------------------------------------
        # Alert: Find Alpha
        # --------------------------------------------------
        if alpha_rules:
            alerts.append(
                "=== CROSS SOURCE ALPHA ===\n"
                f"{home_row['productName']}\n\n"
                + "\n".join(alpha_rules)
                + "\n")

    # --------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------
    merged = merged.drop_duplicates(
        subset="productId",
        keep="first")

    merged.to_csv(
        output_csv,
        index=False,
        encoding="utf-8-sig")
    # --------------------------------------------------
    # Summary
    # --------------------------------------------------
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)

    print(f"Search Pool : {len(search)}")
    print(f"Home Preview: {len(home)}")
    print(f"Merged Pool : {len(merged)}")

    print()
    print(f"Saved: {output_csv}")

    return alerts

# ==================================================
# Run Merge
# ==================================================

alerts = []

# def merge_clearance(search_csv, home_csv, output_csv, category):
# Skincare
alerts_skincare = merge_clearance("clearance_skincare.csv","home_preview_skincare.csv","today_skincare.csv","Skincare")
alerts.extend(alerts_skincare)

# Perfume
alerts_perfume = merge_clearance("clearance_perfume.csv","home_preview_perfume.csv","today_perfume.csv","Perfume")  
alerts.extend(alerts_perfume)

# ==================================================
# Summary
# ==================================================

print()
print("=" * 60)
print("Merge Finished")
print("=" * 60)

print("Generated Files")
print("  today_skincare.csv")
print("  today_perfume.csv")

# ==================================================
# Alert
# ==================================================
alert_text = "\n".join(alerts)
print()
if alert_text:
    print(alert_text)
    send_alert(alert_text)
else:
    print("No Cross Source Alpha")


