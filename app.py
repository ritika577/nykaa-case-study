import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

CLEANED_CSV_PATH = "data/cleaned/nykaa_cleaned.csv"
Q1_SUMMARY_CSV = "data/summary/q1_discount_vs_rating.csv"
Q2_SUMMARY_CSV = "data/summary/q2_high_discount_brands_vs_normal_discount_brands.csv"
Q3_SUMMARY_CSV = "data/summary/q3_expensive_vs_cheap_bestsellers.csv"
Q4_SUMMARY_CSV = "data/summary/q4_with_or_without_bestseller_discounts.csv"
Q5_SUMMARY_CSV = "data/summary/q5_categories_with_most_discounts_and_bestsellers.csv"

if not os.path.exists(CLEANED_CSV_PATH):
    st.error("File not found!")
    st.stop()
df = pd.read_csv(CLEANED_CSV_PATH)
# ----------------------------------------------------------

st.title("Nykaa Beauty: Behind the Bestsellers 🛍️")
st.caption("What makes a product stand out? Exploring the relationship between discounts, " \
"ratings, and bestseller status across 3600+ Nykaa products")
st.divider()
# -------------------------------------------------------------
# QUESTION 1 VISUALISATION
st.subheader("⭐ Do Bigger Discounts Lead to Better Ratings?")
if not os.path.exists(Q1_SUMMARY_CSV):
    st.error("File not found!")
    st.stop()
q1_summary_csv = pd.read_csv(Q1_SUMMARY_CSV)
fig = go.Figure()

for i, row in q1_summary_csv.iterrows():
      category_name = row["category"]
      heavy_value = row["Heavy Discount (≥30%) - Median Rating"]
      normal_value = row["Normal Discount (<30%) - Median Rating"]
      fig.add_trace(go.Scatter(
            x=[ heavy_value , normal_value ],
            y=[ category_name , category_name ],
            mode="lines",
            hoverinfo="skip",
            showlegend=False  
        ))
fig.add_trace(go.Scatter(
      x=q1_summary_csv["Heavy Discount (≥30%) - Median Rating"],
      y=q1_summary_csv["category"],
      mode="markers",
      marker=dict(size=12, opacity=0.6),
      name="Heavy Discount"
  ))
fig.add_trace(go.Scatter(
      x=q1_summary_csv["Normal Discount (<30%) - Median Rating"],
      y=q1_summary_csv["category"],
      mode="markers",
      marker=dict(size=12, opacity=0.6),
      name="Normal Discount"
  ))
fig.update_layout(
      margin=dict(t=20),
      xaxis=dict(range=[1, 5], title="Median Rating"),
      yaxis=dict(title="Category"),
      hovermode="y unified"
  )
st.plotly_chart(fig)
st.info("💡 Most categories show no difference in ratings between heavily discounted "
"and normally priced products. "
  "Only Accessories shows a notably higher rating for heavy discounts. "
  "Overall, bigger discounts do not lead to better ratings.")
st.divider()
# -------------------------------------------------------------
# QUESTION 2 VISUALISATION
st.subheader("⭐ Do high-discount brands have more bestsellers?")
if not os.path.exists(Q2_SUMMARY_CSV):
    st.error("File not found!")
    st.stop()
q2_summary_csv = pd.read_csv(Q2_SUMMARY_CSV)
fig = go.Figure()

fig.add_trace(go.Bar(
      x=q2_summary_csv["Group"],
      y=q2_summary_csv["Bestseller Rate (%)"],
      customdata=q2_summary_csv[["No: of brands", "Product Count"]],
      hovertemplate="Bestseller Rate: %{y}%<br>Brands: %{customdata[0]}<br>Products: %{customdata[1]}<extra></extra>",
      name="Bestseller Rate"
  ))
fig.update_layout(
      margin=dict(t=20),
      yaxis=dict(title="Bestseller Rate (%)"),
      xaxis=dict(title="Brand Group")
  )
st.plotly_chart(fig)
st.info("💡 High-discount brands have nearly double the bestseller rate (6.2%) compared to " \
"normal-discount brands (3.5%). "
  "However, this comes from only 3 high-discount brands (259 products) vs 22 normal-discount brands "
  "(3403 products), "
  "so the small sample size means this trend should be interpreted with caution.")
st.divider()
# -------------------------------------------------------------
# QUESTION 3 VISUALISATION
st.subheader("⭐ Are bestsellers the expensive or cheap option within a brand?")
if not os.path.exists(Q3_SUMMARY_CSV):
    st.error("File not found!")
    st.stop()
q3_summary_csv = pd.read_csv(Q3_SUMMARY_CSV)
fig = go.Figure()

fig.add_trace(go.Pie(labels = q3_summary_csv["Group"],
                     values = q3_summary_csv["Percentage (%)"],
                     hovertemplate = "Group : %{label}<br>Percentage (%) : %{percent}<extra></extra>"
                     ))
st.plotly_chart(fig)
st.info("💡 67.9(%) of bestsellers are priced below their brand's median price. "
    "This suggests that within a brand, the more affordable products tend to become bestsellers.")
st.divider()
# -------------------------------------------------------------
# QUESTION 4 VISUALISATION
st.subheader("⭐ Do brands with bestsellers give bigger discounts than brands without?")
if not os.path.exists(Q4_SUMMARY_CSV):
    st.error("File not found!")
    st.stop()
q4_summary_csv = pd.read_csv(Q4_SUMMARY_CSV)
st.dataframe(q4_summary_csv)
st.info("💡 Brands with bestsellers (20.04%) and without bestsellers (20.02%) have nearly " \
"identical median discounts. Discounting does not appear to be what separates bestseller brands " \
"from non-bestseller ones. " \
"Note: the 'without bestsellers' group has only 8 brands and 30 products, " \
"so this comparison is limited by sample size.")
st.divider()
# -------------------------------------------------------------
# QUESTION 5 VISUALISATION
st.subheader("⭐ Which categories have the biggest discounts and most bestsellers?")
if not os.path.exists(Q5_SUMMARY_CSV):
    st.error("File not found!")
    st.stop()
q5_summary_csv = pd.read_csv(Q5_SUMMARY_CSV)
fig = go.Figure()
fig.add_trace(go.Scatter(
      x=q5_summary_csv["Median discount by category"],
      y=q5_summary_csv["Bestseller rate by category (%)"],
      text=q5_summary_csv["category"],
      mode="markers",
      marker=dict(size= 15),
      hovertemplate = "Category : %{text}<br>Median discount: "
      "%{x}<br>Bestseller Rate : %{y}<extra></extra>"
      ))
fig.update_layout(
      yaxis=dict(title="Bestseller rate by category (%)"),
      xaxis=dict(title="Median discount by category"),
      margin=dict(t=20)
       )
st.plotly_chart(fig)
st.info("💡 Skin (24%) and Hair (24.95%) have the highest median discounts, " \
"while Lips (4.44%) and Skin (4.57%) lead in bestseller rates. "
"There is no clear pattern — Lips has one of the lowest discounts " \
"yet the second-highest bestseller rate. "
"Discount size alone does not determine which categories produce the most bestsellers.")
st.divider()
# -------------------------------------------------------------
# CONCLUSION
st.subheader("📌 Conclusion")
st.markdown(
    "1. **Discounts ≠ Better Ratings** — Bigger discounts do not lead to better ratings across most categories.\n"
    "2. **High-Discount Brands** — They show a higher bestseller rate (6.2% vs 3.5%), but the small sample size (3 brands) makes this inconclusive.\n"
    "3. **Affordable = Bestseller** — 67.9(%) of bestsellers are priced below their brand's median price.\n"
    "4. **Discounts Don't Define Bestseller Brands** — Brands with and without bestsellers offer nearly identical median discounts (~20%).\n"
    "5. **No Category Pattern** — Discount size alone does not determine which categories produce the most bestsellers."   
)