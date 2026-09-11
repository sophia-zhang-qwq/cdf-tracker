import sqlite3
import pandas as pd
import os
import sys
from pathlib import Path

# put file root directory into the Python search path,
# so that we can import modules from the root directory
sys.path.append(str(Path(__file__).resolve().parent.parent))
from clearance.alert import send_alert

# Update favor.csv to latest version
print("Updating favor...")
os.system("python3 favor.py")

print("Running alpha detection...")

conn = sqlite3.connect("favor.db")

first_run = False

try:
    # read old database
    old_df = pd.read_sql(
        "SELECT * FROM favor_products",
        conn)
except Exception:
    print("First run")
    first_run = True
    old_df = pd.DataFrame()

# read new csv files
new_df = pd.read_csv("favor.csv")

if first_run:
    new_df.to_sql("favor_products",conn,if_exists="replace",index=False)
    conn.close()

    print("Database initialized with", len(new_df), "products.")
    exit()
    
# merge new data, find potential alpha
compare = old_df.merge(new_df,on="productId",how="outer",suffixes=("_old", "_new"))
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
drops = compare[compare["price_old"].notna() & compare["price_new"].notna() & (compare["price_old"] != compare["price_new"])]
if len(drops) > 0:
    alerts.append("=== PRICE DROPS ===")
    for _, row in drops.iterrows():
        alerts.append(
            f"{row['productName_old']}\n"
            f"Price: HK${row['price_old']} -> HK${row['price_new']}\n"
            # activityStock is actual stock for clearance price, stock is normal price stock
            f"Stock: {row['activityStock_old']} -> {row['activityStock_new']}\n"
            f"Discount: {row['priceDiscount_old']} -> {row['priceDiscount_new']}\n"
            f"Original Price: HK$ {row['originalPrice_new']}\n")

# alpha 2: new product alert
# productID not in old_df but in new_df
new_products = new_df[~new_df["productId"].isin(old_df["productId"])]
if len(new_products) > 0:
    alerts.append("=== NEW PRODUCTS ===")

    for _, row in new_products.iterrows():
        alerts.append(
            f"{row['productName']}\n"
            f"Price: HK${row['price']}\n"
            f"Stock: {row['activityStock']}\n"
            f"Discount: {row['priceDiscount']}\n"
            f"Original Price: HK$ {row['originalPrice']}\n")

# alpha 3-1: Product Sold Out
# productID in old_df but not in new_df
# 真正的Removed(保留了)是指在新数据中没有这个productId了,说明这个产品已经下架了
removed_products = old_df[~old_df["productId"].isin(new_df["productId"])]
if len(removed_products) > 0:
    alerts.append("=== PRODUCT REMOVED FROM API ===")
    for _, row in removed_products.iterrows():
        alerts.append(
            f"{row['name']}\n "
            f"HK${row['price']} \n"
            f"(Removed, Last Stock: {row['activityStock']})\n"
            f"Original Price: HK$ {row['originalPrice']}\n")
# alpha 3-2: Clearance Sold Out 
# Clearance Sold Out: activityStock > 0 -> 0, but stoc>0 and regular price
activity_sold_out = compare[(compare["activityStock_old"] > 0) & (compare["activityStock_new"] == 0)]
if len(activity_sold_out) > 0:
    alerts.append("=== CLEARANCE SOLD OUT ===")
    for _, row in activity_sold_out.iterrows():
        alerts.append(
            f"{row['productName_new']}\n"
            f"Clearance Stock: {row['activityStock_old']} → {row['activityStock_new']}\n"
            f"Regular Stock: {row['activityStock_old']} → {row['activityStock_new']}\n"
            f"Price: HK${row['price_new']}\n"
            f"Discount: {row['priceDiscount_new']}\n"
            f"Original Price: HK${row['originalPrice_new']}\n")

# alpha 5: restock alert
# activityStock 0 -> 5 补货啦
restock = compare[(compare["activityStock_old"] == 0) & (compare["activityStock_new"] > 0)]
if len(restock) > 0:
    alerts.append("=== RESTOCK ALERT ===")
    for _, row in restock.iterrows():
        name = row.get("productName_new")
        alerts.append(
            f"{name}\n"
            f"Clearance Stock: {row['activityStock_old']} → {row['activityStock_new']}\n"
            f"Price: HK${row['price_new']}\n"
            f"Discount: {row['discount_new']}\n"
            f"Original Price: HK${row['originalPrice_new']}\n")

# alpha 6: price mismatch detection
# alph 6 removed

# update database
new_df.to_sql("favor_products",conn,if_exists="replace",index=False)

print("\nDatabase updated:",len(new_df),"products")
conn.close()

# send email alerts
alert_text = "\n".join(alerts)
print(alert_text)

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
