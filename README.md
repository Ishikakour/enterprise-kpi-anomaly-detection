# Enterprise KPI Anomaly Detection — Procurement Risk Case Study

**Live Dashboard:** [YOUR-STREAMLIT-URL] ← *update after deployment*

> **Methodology Note:** This project is a methodology case study based on my experience building KRI tracking dashboards at Philips. No proprietary data is used. The synthetic dataset mirrors real enterprise procurement structures — project timelines, vendor performance, and budget variance across business units.

---

## Business Problem

An enterprise procurement organization manages 500+ concurrent projects across 4 vendors and 4 business units. Project managers manually review timelines in Excel, discovering schedule and budget overruns only after they occur. Leadership needs an automated way to:

1. **Flag high-risk projects** before they breach schedule or budget thresholds
2. **Identify root causes** — which vendors and business units are driving most risk
3. **Prioritize intervention** using a risk matrix (schedule variance × budget variance)

## Methodology

1. **Data Generation** — Synthetic procurement dataset modeling real distributions (500 projects, 4 vendors, 4 BUs)
2. **Anomaly Detection** — Z-score and IQR-based outlier detection on schedule and budget variance
3. **Root Cause Analysis** — Group by vendor and BU to surface systemic issues
4. **Risk Matrix** — 2D classification into Low / Medium / High / Critical quadrants
5. **Interactive Dashboard** — Streamlit app with real-time filtering by vendor, BU, and risk tier

## Data Architecture
generate_data.py → procurement_data.csv → app.py (Streamlit)
      ↓
analysis.sql (KRI queries)


## Key Metrics Tracked

| Metric | Definition | Business Use |
|---|---|---|
| Schedule Variance % | (Actual Days - Planned Days) / Planned Days | On-time delivery monitoring |
| Budget Variance % | (Actual Spend - Budget) / Budget | Cost overrun detection |
| Z-Score (Schedule) | Standard deviations from mean | Outlier flagging |
| Z-Score (Budget) | Standard deviations from mean | Outlier flagging |
| Risk Tier | Composite of both Z-scores | Prioritization |

## Risk Tier Logic

- **Critical:** Both Z-scores > 2 (schedule AND budget are outliers)
- **High:** Either Z-score > 2 (one dimension is severely off)
- **Medium:** Either Z-score between 1 and 2
- **Low:** Both Z-scores < 1

## Key Findings (from synthetic run)

- Vendor C consistently shows the highest schedule variance across all business units
- BU-2 has the highest concentration of critical-risk projects
- 12% of the portfolio is at risk, representing a disproportionate share of total spend
- On-Time-In-Full (OTIF) delivery rate is lowest when actual days exceed 1.4× planned days

## Tech Stack

- **Python:** Pandas, NumPy, SciPy (Z-score, IQR)
- **Streamlit:** Interactive dashboard with risk matrix
- **Plotly:** Scatter plots, heatmaps, bar charts
- **SQL:** KRI aggregation, vendor ranking, risk tier classification

## Repository Contents

| File | Purpose |
|---|---|
| `generate_data.py` | Generates synthetic procurement dataset (500 projects) |
| `procurement_data.csv` | Generated dataset |
| `app.py` | Streamlit dashboard |
| `analysis.sql` | KRI queries with window functions |
| `requirements.txt` | Dependencies |
| `dashboard.png` | Screenshot |

## How to Run

```bash
pip install -r requirements.txt
python generate_data.py
streamlit run app.py

Author
Ishika Kour — M.Tech Data Analytics, NIT Jalandhar | Ex-Philips Analytics | GATE CSE/DA Qualified