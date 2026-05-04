import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

CLEANED_CSV_PATH = "data/cleaned/nykaa_cleaned.csv"
Q1_SUMMARY_CSV = "data/summary/q1_discount_vs_rating.csv"
Q2_SUMMARY_CSV = "data/summary/q2_high_discount_brands_vs_normal_discount_brands.csv"

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
st.info("💡 Most categories show no difference in ratings between heavily discounted and normally priced products. "
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
st.info("💡 High-discount brands have nearly double the bestseller rate (6.2%) compared to normal-discount brands (3.5%). "
  "However, this comes from only 3 high-discount brands (259 products) vs 22 normal-discount brands (3403 products), "
  "so the small sample size means this trend should be interpreted with caution.")
st.divider()