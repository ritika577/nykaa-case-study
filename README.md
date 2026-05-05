# Nykaa Beauty: Behind the Bestsellers

Exploring the relationship between discounts, ratings, and bestseller status across 3600+ Nykaa products.

## Questions Explored

1. Do bigger discounts lead to better ratings?
2. Do high-discount brands have more bestsellers?
3. Are bestsellers the expensive or cheap option within a brand?
4. Do brands with bestsellers give bigger discounts than brands without?
5. Which categories have the biggest discounts and most bestsellers?

## Project Structure

```
nykaa-case-study/
├── app.py                  # Streamlit dashboard
├── scripts/
│   ├── clean.py            # Data cleaning pipeline
│   └── summarize.py        # Business question analysis
├── data/
│   ├── raw/                # Original dataset
│   ├── cleaned/            # Cleaned dataset
│   └── summary/            # Aggregated results per question
└── requirements.txt
```

## Key Findings

- **Discounts don't improve ratings** — most categories show no difference between heavily and normally discounted products.
- **Affordable products become bestsellers** — 67.9% of bestsellers are priced below their brand's median price.
- **Discounts don't define bestseller brands** — brands with and without bestsellers offer nearly identical median discounts (~20%).
- **No clear category pattern** — discount size alone does not determine which categories produce the most bestsellers.

## Tech Stack

- **Python** — pandas for data cleaning and analysis
- **Plotly** — interactive charts (dumbbell, bar, pie, scatter)
- **Streamlit** — web dashboard

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Dataset

[Nykaa Popular Brands Products (Kaggle, Oct 2022)](https://www.kaggle.com/) — 3662 products across 25 brands.
