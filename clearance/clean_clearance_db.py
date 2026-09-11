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

src.backup(dst)

rows = src.execute("""
    SELECT productId, brandId, productName, price, originalPrice,
           activityStock, stock
    FROM clearance_products
""").fetchall()

dst.execute("DROP TABLE IF EXISTS clearance_products")

dst.execute("""
CREATE TABLE clearance_products (
    productId TEXT,
    brandId INTEGER,
    productName TEXT,
    price REAL,
    originalPrice REAL,
    priceDiscount REAL,
    activityStock INTEGER,
    stock INTEGER,
    source TEXT,
    category TEXT,
    time TEXT
)
""")

dst.executemany("""
INSERT INTO clearance_products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    (*r, r[3] / r[4] if r[3] is not None and r[4] else None,
     "hk", "clearance",
     datetime.fromtimestamp(SRC.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"))
    for r in rows
])

dst.commit()
src.close()
dst.close()

print(f"Done: {OUT}")