import pandas as pd

df = pd.read_csv("clean_products.csv")

good_discount = df[df["discount"] <=6 ]

good_discount = good_discount.sort_values(
    "discount",
    ascending=True
)

good_discount.to_csv(
    "good_deals.csv",
    index=False,
    encoding="utf-8-sig"
)

print(f"Found {len(good_discount)} good discount")
