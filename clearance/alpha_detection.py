import sqlite3
import pandas as pd
import os

from alert import send_alert


# Update perfume_clearance.csv and skincare_clearance.csv to latest version
print("Updating perfume...")
os.system("python3 perfume_clearance.py")

print("Updating skincare...")
os.system("python3 skincare_clearance.py")

print("Running alpha detection...")


conn = sqlite3.connect("clearance.db")

first_run = False

try:
    # read old database
    old_df = pd.read_sql(
        "SELECT * FROM clearance_products",
        conn
    )
except Exception:
    print("First run")
    first_run = True
    old_df = pd.DataFrame()

# read new csv files
new_perfume = pd.read_csv("clearance_perfume.csv")
new_skincare = pd.read_csv("clearance_skincare.csv")

new_df = pd.concat(
    [new_perfume, new_skincare],
    ignore_index=True
)

if first_run:
    new_df.to_sql(
        "clearance_products",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("Database initialized with", len(new_df), "products.")
    exit()
    
# merge new data, find potential alpha
compare = old_df.merge(
    new_df,
    on="productId",
    how="outer",
    suffixes=("_old", "_new")
)
# old database
# productId     price       stock 
# p1            290         2
# p2            189         1

# new database
# productId     price       stock 
# p1            99          1
# p2            189         1
# p3            299         3

# merge database 
# productId     price_old   price_new
# p1            290         99
# p2            189         189
# p3            NaN         299

#['productId', 'brandId', 'productName', 'price', 'originalPrice', 'discount', 
# 'activityStock', 'stock', 'sellNum', 'timeLabel', 
# 'activityId', 'activityProductId', 'categoryId', 'thirdCategoryId', 'category']


# create alerts
alerts = []

# alpha 1: price drop alert
# only show price change if before and after are both valid
drops = compare[
    compare["price_old"].notna()
    &
    compare["price_new"].notna()
    &
    (compare["price_old"] != compare["price_new"])
]
if len(drops) > 0:
    alerts.append("=== PRICE DROPS ===")

    for _, row in drops.iterrows():
        alerts.append(
            f"{row['productName_old']}\n"
            f"Price: HK${row['price_old']} -> HK${row['price_new']}\n"
            f"Stock: {row['stock_old']} -> {row['stock_new']}\n"
            f"Discount: {row['discount_old']} -> {row['discount_new']}\n"
            f"Original Price: HK$ {row['originalPrice_new']}\n"
)

# alpha 2: new product alert
# productID not in old_df but in new_df
new_products = new_df[~new_df["productId"].isin(old_df["productId"])]
if len(new_products) > 0:
    alerts.append("=== NEW PRODUCTS ===")

    for _, row in new_products.iterrows():
        alerts.append(
            f"{row['productName']}\n"
            f"Price: HK${row['price']}\n"
            f"Stock: {row['stock']}\n"
            f"Discount: {row['discount']}\n"
            f"Original Price: HK$ {row['originalPrice']}\n"
)

# alpha 3： product sold out
# productID in old_df but not in new_df
removed_products = old_df[~old_df["productId"].isin(new_df["productId"])]
if len(removed_products) > 0:
    alerts.append("=== REMOVED PRODUCTS ===")

    for _, row in removed_products.iterrows():
        alerts.append(
            f"{row['productName']}\n "
            f"HK${row['price']} \n"
            f"(Removed, Last Stock: {row['stock']})\n"
            f"Original Price: HK$ {row['originalPrice']}\n"
    )

# alpha 4: restock alert
# TO-DO

mismatch_alert = []

# alpha 5: price mismatch detection
for _, row in new_df.iterrows():

    alpha_rules = []

    # Rule 1: discount != price
    if (abs(row["discount"] - row["price"]) > 0.01):
        alpha_rules.append(
            f"Rule 1: Discount Price != Price "
            f"({row['discount']} != {row['price']})")

    # Rule 2:
    if (pd.notna(row["priceDiscount"]) and pd.notna(row["originalPrice"])):
        actual_discount = (row["price"]/row["originalPrice"] * 10)

        if abs(actual_discount - row["priceDiscount"]) > 0.1:
            alpha_rules.append(
                f"Rule 2: Actual Discount "
                f"({actual_discount:.1f}折)"
                f" != Displayed Discount "
                f"({row['priceDiscount']}折)")

    # Rule 3: priceDiscount != activityDiscount(3.5折!=3.5折)
    if (pd.notna(row["priceDiscount"]) and pd.notna(row["activityDiscount"])
        and abs(row["priceDiscount"]-row["activityDiscount"])> 0.1):

        alpha_rules.append(
            f"Rule 3: Price Discount "
            f"({row['priceDiscount']}折)"
            f" != Activity Discount "
            f"({row['activityDiscount']}折)")

    # No Alpha
    if len(alpha_rules) == 0:
        continue

    mismatch_alert.append(
        f"{row['productName']}\n"
        f"Price: HK${row['price']}\n"
        f"Discount Price: HK${row['discount']}\n"
        f"Original Price: HK${row['originalPrice']}\n"
        f"\n"
        + "\n".join(alpha_rules)
        + "\n"
    )

# only print once
if len(mismatch_alert) > 0:
    alerts.append("=== POSSIBLE PRICE MISMATCH ARBITRAGE ===")
    alerts.extend(mismatch_alert)

# update database
new_df.to_sql(
    "clearance_products",
    conn,
    if_exists="replace",
    index=False
)

print(
    "\nDatabase updated:",
    len(new_df),
    "products"
)
# ,
conn.close()

# send email alerts
alert_text = "\n".join(alerts)
print(alert_text)

"""
=== PRICE DROPS ===
LANCOME奇迹香氛:
HK$290 -> HK$99

=== NEW PRODUCTS ===
La Mer精华:
HK$299
"""

if len(alert_text) > 0:
    send_alert(alert_text)
else:
    print("No Alpha")


"""
clearance.db
      ↓
    old_df

today csv
      ↓
    new_df

old_df + new_df
      ↓
    compare
      ↓
 Alpha Detection

      ↓
(检测完就扔掉)

new_df
      ↓
to_sql()
      ↓
new clearance.db
"""
