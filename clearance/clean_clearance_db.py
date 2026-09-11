import sqlite3
from pathlib import Path
from datetime import datetime

"""
Input: clearance.db
Output: clearance_clean.db
删掉没用信息,增加time,source:hk,category:clearance

productId
brandId
productName
price
originalPrice
priceDiscount=price/originalPrice
activityStock
stock
source:hk
category:clearance
time:
"""

SRC = Path("clearance.db")
OUT = Path("clearance_clean.db")
src = sqlite3.connect(SRC)
dst = sqlite3.connect(OUT)

time = datetime.fromtimestamp(SRC.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")

dst.execute(f"ATTACH DATABASE '{SRC}' AS src")
dst.execute("DROP TABLE IF EXISTS clearance_products")

dst.execute("""
CREATE TABLE clearance_products AS
SELECT
    productId,
    brandId,
    productName,
    price,
    originalPrice,
    price * 1.0 / originalPrice AS priceDiscount,
    activityStock,
    stock,
    'hk' AS source,
    'clearance' AS category,
    ? AS time
FROM src.clearance_products
""", (time,))

dst.commit()
src.close()
dst.close()

print(f"Done: {OUT}")