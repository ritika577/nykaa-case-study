import pandas as pd



df = pd.read_csv("data/raw/nykaa_popular_brands_products_2022_10_16.csv")
print("shape:", df.shape)
df = df.drop_duplicates(subset="product_id")
print("shape after removing duplicates:", df.shape)
df["in_stock"] = df["in_stock"].fillna(False).astype(bool)
print("in_stock dtype:", df["in_stock"].dtype)