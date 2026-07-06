# Online Retail Analytics Platform

Analytics platform for retail sales data — based on the [Online Retail II (UCI)](https://archive.ics.uci.edu/dataset/502/online+retail+ii) dataset.

For the full project plan and task distribution, see the documents in `docs/`.

## Project Structure

```text
online-retail-analytics/
├── data/
│   ├── raw/                      # Original CSV/Excel (gitignored)
│   ├── processed/                # Cleaned datasets directory
│   └── cleaned_retail_data.csv   # Demo dataset for Streamlit
├── notebooks/
│   ├── 01_data_exploration.ipynb    # Initial data exploration
│   ├── 02_eda_analysis.ipynb        # EDA & Insights
│   ├── 03_rfm_recommendations.ipynb # RFM Segmentation & Rules
│   └── 04_visualisations.ipynb      # Charting and plotting examples
├── src/
│   ├── analysis.py               # EDA functions & KPI generation
│   ├── data_cleaning.py          # Data cleaning logic (clean_data)
│   ├── recommendation_engine.py  # RFM and Recommendation rule-engine
│   └── visualisations.py         # Plotly chart generation functions
├── app/
│   └── app.py                    # Streamlit Dashboard Application
├── docs/                         # Project planning documents
├── requirements.txt              # Python dependencies
└── README.md
```

## Setup

```bash
python -m venv venv
# On Mac/Linux: source venv/bin/activate
# On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

**Running Notebooks:**
```bash
jupyter notebook notebooks/
```

**Running the Streamlit App:**
```bash
streamlit run app/app.py
```

## Dataset

The "Online Retail II" dataset from UCI is loaded automatically during the execution of scripts and notebooks, and a cleaned version is provided in `data/cleaned_retail_data.csv`. 
Source: https://archive.ics.uci.edu/dataset/502/online+retail+ii

---

## Current Status (What has been done)

- [x] Basic repository structure setup and dependency management.
- [x] **Phase 1: Data Processing**
  - Completed initial dataset exploration and cleaning.
  - Implemented the reusable `clean_data()` function in `src/`.
- [x] **Phase 2: Analytics & Insights**
  - Developed EDA functions (revenue, products, geography).
  - Built RFM logic and a Business Recommendation Engine.
  - Created interactive Plotly visualisations.
  - Documented everything in Jupyter Notebooks.
- [x] **Phase 3: Streamlit Application**
  - Built a complete, premium Streamlit dashboard with 6 distinct views:
    - **Home & Upload:** Supports raw and pre-cleaned data validation.
    - **Sales Dashboard:** KPIs, revenue trends, product performance.
    - **Customer Analysis:** RFM segments, CLV, churn risk.
    - **Geographic Performance:** Country-based revenue mapping.
    - **Recommendations:** Rule-based insights with profit impact.
    - **What-If Simulator:** Basic structure for revenue projections.
- [x] Cleaned up unused files and updated requirements for production.
- [x] Ready for deployment on Streamlit Cloud.

---

## What's Left (Next Steps)

- [ ] **Phase 4: Database Integration (MongoDB)**
  - Implement a `db_connector.py` for MongoDB.
  - Store uploaded datasets in `raw_uploads`.
  - Log monthly analysis runs to `monthly_analytics`.
  - Log generated recommendations to `recommendations_log`.
  - Track historical KPIs in `kpi_history`.
- [ ] **Phase 5.1: Advanced What-If Simulator**
  - Connect the What-If Simulator in Streamlit directly to the full RFM history and historical KPIs (from MongoDB) for accurate, data-driven projections.
- [ ] **Phase 5.2: Export Features**
  - Add PDF and Excel export functionalities for reports directly from the Streamlit app.
- [ ] **Phase 6: Automated Testing**
  - Add unit tests for the core logic in the `src/` directory (data cleaning, RFM, recommendation engine).
