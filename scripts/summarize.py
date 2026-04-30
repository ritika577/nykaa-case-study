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
# -----------------------------------------------------------

print("--- Q1: Do heavily discounted products get better ratings? ---")
rated_df = df[df["is_unrated"] == False]
print("Rated products:", rated_df.shape[0])

heavy_discount = rated_df[rated_df["discount_pct"] >= 30]
normal_discount = rated_df[rated_df["discount_pct"] < 30]
print("HEAVY discount — count:", heavy_discount.shape[0], "— median rating:", round(heavy_discount["rating"].median(), 1))
print("NORMAL discount — count:", normal_discount.shape[0], "— median rating:", round(normal_discount["rating"].median(), 1))

heavy_discount_by_cat = heavy_discount.groupby("category")
normal_discount_by_cat = normal_discount.groupby("category")
print("HEAVY discount — median rating by category:\n", heavy_discount_by_cat["rating"].median())
print("NORMAL discount — median rating by category:\n", normal_discount_by_cat["rating"].median())

q1_result = pd.DataFrame({
    "Heavy Discount (≥30%) - Median Rating" : heavy_discount_by_cat["rating"].median(),
    "Normal Discount (<30%) - Median Rating" : normal_discount_by_cat["rating"].median()
})
q1_result.to_csv("data/summary/q1_discount_vs_rating.csv")
# ---------------------------------------------------------------------------

print("--- Q2: Do high-discount brands have more bestsellers? ---")
brand_median_discount = df.groupby("brand_name")["discount_pct"].median()
high_discount_brands = brand_median_discount[brand_median_discount >= 30]
normal_discount_brands = brand_median_discount[brand_median_discount < 30]
print("High-discount brands:", len(high_discount_brands), "—", high_discount_brands.index.tolist())
print("Normal-discount brands:", len(normal_discount_brands), "—", normal_discount_brands.index.tolist())

high_discount_products = df[df["brand_name"].isin(high_discount_brands.index)]
normal_discount_products = df[df["brand_name"].isin(normal_discount_brands.index)]
print("HIGH discount brands — products:", high_discount_products.shape[0], "— bestseller rate:", round(high_discount_products["is_bestseller"].mean() * 100, 1), "%")
print("NORMAL discount brands — products:", normal_discount_products.shape[0], "— bestseller rate:", round(normal_discount_products["is_bestseller"].mean() * 100, 1), "%")

q2_result = pd.DataFrame({
      "Group": ["High Discount Brands", "Normal Discount Brands"],
      "Product Count": [high_discount_products.shape[0], normal_discount_products.shape[0]],
      "Bestseller Rate (%)": [round(high_discount_products["is_bestseller"].mean() * 100, 1), round(normal_discount_products["is_bestseller"].mean() * 100, 1)]
  })
q2_result.to_csv("data/summary/q2_high_discount_brands_vs_normal_discount_brands.csv",index=False)
# ---------------------------------------------------------------------------

print("--- Q3: Are bestsellers the expensive or cheap option within a brand? ---")
brand_median_price = df.groupby("brand_name")["price"].median()
df["brand_median"] = df["brand_name"].map(brand_median_price)
df["is_cheap"] = df["price"] < df["brand_median"]
df["is_expensive"] = df["price"] >= df["brand_median"]
bestsellers = df[df["is_bestseller"] == True]
print("Total bestsellers:", bestsellers.shape[0])
print("CHEAP bestsellers:", round(bestsellers["is_cheap"].mean() * 100, 1), "%")
print("EXPENSIVE bestsellers:", round(bestsellers["is_expensive"].mean() * 100, 1), "%")

q3_result = pd.DataFrame({
    "Group": ["Cheap Bestsellers", "Expensive Bestsellers"],
      "Percentage (%)": [round(bestsellers["is_cheap"].mean() * 100, 1),
                         round(bestsellers["is_expensive"].mean() * 100, 1)]
})
q3_result.to_csv("data/summary/q3_expensive_vs_cheap_bestsellers.csv",index=False)
# ---------------------------------------------------------------------------

print("--- Q4: Do brands with bestsellers give bigger discounts than brands without? ---")
brands_status = df.groupby("brand_name")["is_bestseller"].any()
brands_with_bestsellers = brands_status[brands_status == True]
brands_without_bestsellers = brands_status[brands_status == False]
products_with_bestsellers = df[df["brand_name"].isin(brands_with_bestsellers.index)]
products_without_bestsellers = df[df["brand_name"].isin(brands_without_bestsellers.index)]
print("WITH bestsellers — brands:", len(brands_with_bestsellers), "— products:", products_with_bestsellers.shape[0], "— median discount:", round(products_with_bestsellers["discount_pct"].median(), 2), "%")
print("WITHOUT bestsellers — brands:", len(brands_without_bestsellers), "— products:", products_without_bestsellers.shape[0], "— median discount:", round(products_without_bestsellers["discount_pct"].median(), 2), "%")
# ---------------------------------------------------------------------------

print("--- Q5: Which categories have the biggest discounts and most bestsellers? ---")
category_median_discount = round(df.groupby("category")["discount_pct"].median(), 2)
category_bestseller_rate = round(df.groupby("category")["is_bestseller"].mean() * 100, 2)
print("Median discount by category:\n", category_median_discount)
print("Bestseller rate by category (%):\n", category_bestseller_rate)