import pandas as pd
import os

RAW_DATA_PATH = "data/raw/nykaa_popular_brands_products_2022_10_16.csv"

print("--- EXTRACT: Loading raw data ---")
if not os.path.exists(RAW_DATA_PATH):
    print("File not found:", RAW_DATA_PATH)
    exit()
df = pd.read_csv(RAW_DATA_PATH)
print("shape:", df.shape)
print("data type", df.dtypes)
print("missing values each column has" , df.isna().sum())
df = df.drop_duplicates(subset="product_id")
print("shape after removing duplicates:", df.shape)
df["in_stock"] = df["in_stock"].fillna(False).astype(bool)
print("in_stock dtype:", df["in_stock"].dtype)
print(df["tags"].value_counts())

df["is_new"] = df["tags"].str.contains("NEW", na=False)
df["is_bestseller"] = df["tags"].str.contains("BESTSELLER", na=False)
df["is_featured"] = df["tags"].str.contains("FEATURED", na=False)
print(df[["is_bestseller", "is_featured", "is_new"]].sum())

df["discount_pct"] = (df['mrp'] - df['price'])/ df['mrp'] * 100
print(df["discount_pct"].describe())

df["is_unrated"] = (df["rating"] == 0) & (df["rating_count"] == 0)
print(df["is_unrated"].sum())
  
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

df["category"] = df["product_title"].apply(get_category)
print(df["category"].value_counts())

df = df.drop(columns=["image_url", "product_url", "listing_url"])
print("columns after drop:", df.columns.tolist())
df.to_csv("data/cleaned/nykaa_cleaned.csv", index=False)
print("shape:", df.shape)
print(df.dtypes)
