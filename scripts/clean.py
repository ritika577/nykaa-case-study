import pandas as pd
import os

RAW_DATA_PATH = "data/raw/nykaa_popular_brands_products_2022_10_16.csv"

print("--- EXTRACT: Loading raw data ---")
if not os.path.exists(RAW_DATA_PATH):
    print("File not found:", RAW_DATA_PATH)
    exit()
df = pd.read_csv(RAW_DATA_PATH)
print("shape:", df.shape)
print("data types:\n", df.dtypes)
print("missing values per column:\n", df.isna().sum())
print("--- CLEAN: removing duplicates ---")
df = df.drop_duplicates(subset="product_id")
print("shape after removing duplicates:", df.shape)

print("--- CLEAN: fixing in_stock ---")
df["in_stock"] = df["in_stock"].fillna(False).astype(bool)
print("in_stock dtype:", df["in_stock"].dtype)

print("--- CLEAN: splitting tags ---")
df["is_new"] = df["tags"].str.contains("NEW", na=False)
df["is_bestseller"] = df["tags"].str.contains("BESTSELLER", na=False)
df["is_featured"] = df["tags"].str.contains("FEATURED", na=False)
print("tag counts:\n", df[["is_bestseller", "is_featured", "is_new"]].sum())

print("--- CLEAN: calculating discount ---")
df["discount_pct"] = (df["mrp"] - df["price"]) / df["mrp"] * 100
print("discount stats:\n", df["discount_pct"].describe())

print("--- CLEAN: flagging unrated ---")
df["is_unrated"] = (df["rating"] == 0) & (df["rating_count"] == 0)
print("unrated products:", df["is_unrated"].sum())
  
category_keywords = {
      "Nails": ["nail", "enamel", "polish"],
      "Lips": ["lipstick", "lip", "gloss"],
      "Eyes": ["kajal", "eyeshadow", "mascara", "eye","lash", "brow", "liner"],
      "Hair": ["shampoo", "conditioner", "hair", "hair color", "hair dye"],
      "Face": ["foundation", "compact", "primer", "blush","moisturiser", "foaming face", 
               "powder", "colour corrector", "cleansing wipes","concealer", "highlighter", 
               "illuminator", "facial"],
      "Skin": ["moisturizer", "serum", "sunscreen", "cream", "lotion", "mask", "scrub", 
               "skin","anti aging", "spot", "tonic", "essential oil", "face wash", "cleansing", 
               "whitening", "radiance", "hydration","cleanser", "face pack", "emulsion", "brightening"],
      "Bath & Body": ["body", "shower", "deodorant", "soap", "bath","hand wash","shave"],
      "Accessories": ["brush", "pouch", "sponge", "bag", "blender", "accessory","tweezer","sharpener"],

}

def get_category(title):
    title = title.lower()
    for category, keywords in category_keywords.items():
        if any(word in title for word in keywords):
            return category
    return "Other"

print("--- CLEAN: deriving category ---")
df["category"] = df["product_title"].apply(get_category)
print("category counts:\n", df["category"].value_counts())

print("--- CLEAN: dropping unused columns ---")
df = df.drop(columns=["image_url", "product_url", "listing_url"])
print("columns after drop:", df.columns.tolist())

print("--- SAVE ---")
df.to_csv("data/cleaned/nykaa_cleaned.csv", index=False)
print("final shape:", df.shape)
print("final dtypes:\n", df.dtypes)
