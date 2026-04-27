import pandas as pd
import os

CLEANED_CSV_PATH = "data/cleaned/nykaa_cleaned.csv"

print("--- LOAD: clean data ---")
if not os.path.exists(CLEANED_CSV_PATH):
    print("File not found:", CLEANED_CSV_PATH)
    exit()
df = pd.read_csv(CLEANED_CSV_PATH)
print("shape", df.shape)
print("data type", df.dtypes)
print("missing values in each column", df.isna().sum())

print("--- Q1: Do heavily discounted products get better ratings? ---")
filtered_df = df[df["is_unrated"] == False]
print("Rated products:", filtered_df.shape[0])

heavy_discount = filtered_df[filtered_df["discount_pct"] >=30]
print("HEAVY discount — count:", heavy_discount.shape[0])
print("HEAVY discount - median rating:", heavy_discount["rating"].median())
heavy_discount_by_cat = filtered_df[filtered_df["discount_pct"] >=30].groupby("category")
print("HEAVY discount — products per category:", heavy_discount_by_cat.size())
print("HEAVY discount — median rating by category:", heavy_discount_by_cat["rating"].median())

normal_discount = filtered_df[filtered_df["discount_pct"] <30]
print("NORMAL discount — count:", normal_discount.shape[0])
print("NORMAL discount - median rating:", normal_discount["rating"].median())
normal_discount_by_cat = filtered_df[filtered_df["discount_pct"] <30].groupby("category")
print("NORMAL discount — products per category:", normal_discount_by_cat.size())
print("NORMAL discount — median rating by category:", normal_discount_by_cat["rating"].median())


print("--- Q2: Do high-discount brands have more bestsellers? ---")
brand_median_discount = df.groupby("brand_name")["discount_pct"].median()
high_discount_brand = brand_median_discount[brand_median_discount >= 30]
normal_discount_brand = brand_median_discount[brand_median_discount <30]
print("High-discount brands:", high_discount_brand.index.tolist())
print("Normal-discount brands:", normal_discount_brand.index.tolist())

high_discount_products = df[df["brand_name"].isin(high_discount_brand.index)]
print("HIGH discount brands — products:", high_discount_products.shape[0], "— bestseller rate:", high_discount_products["is_bestseller"].mean())

normal_discount_products = df[df["brand_name"].isin(normal_discount_brand.index)]
print("NORMAL discount brands — products:", normal_discount_products.shape[0], "— bestseller rate:", normal_discount_products["is_bestseller"].mean())