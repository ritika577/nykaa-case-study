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

filtered_df = df[df["is_unrated"] == False]
print("filtered df on rating basis:",filtered_df)
heavily_dct = filtered_df[filtered_df["discount_pct"] >=30]
print("discount percentage filtered worked on heavily_dct:", heavily_dct)
median_h_rating = heavily_dct["rating"].median()
print("median rating of heavily discounted products:", median_h_rating)
normal_dct = filtered_df[filtered_df["discount_pct"] <30]
print("discount percentage filtered worked on normal_dct:", normal_dct)
median_n_rating = normal_dct["rating"].median()
print("median rating of Normal discounted products:", median_n_rating)
