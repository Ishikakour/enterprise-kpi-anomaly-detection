"""
Enterprise KPI Anomaly Detection Dashboard
Author: Ishika Kour
Methodology case study based on Philips procurement analytics experience.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Enterprise KPI Anomaly Detection",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap');

    .stApp {
        background: radial-gradient(1200px 600px at 10% -10%, #1a2744 0%, #0b1020 45%, #080c18 100%);
        color: #d7deee;
        font-family: 'IBM Plex Sans', sans-serif;
    }

    [data-testid="stHeader"], .stDeployButton { display: none; }

    [data-testid="stSidebar"] {
        background: #0a1224;
        border-right: 1px solid rgba(232,184,109,0.18);
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #f3e6c8;
        letter-spacing: 0.04em;
    }

    .hero {
        padding: 0.2rem 0 0.8rem 0;
        border-bottom: 1px solid rgba(232,184,109,0.22);
        margin-bottom: 1.1rem;
    }
    .eyebrow {
        font-size: 0.72rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #e8b86d;
        font-weight: 600;
        margin-bottom: 0.35rem;
    }
    .hero h1 {
        font-size: 2.05rem;
        font-weight: 700;
        color: #f6f3ea;
        margin: 0 0 0.25rem 0;
        line-height: 1.15;
    }
    .hero p { color: #9aa6c2; margin: 0; font-size: 0.95rem; }
    .author {
        margin-top: 0.55rem;
        font-size: 1.05rem;
        font-weight: 600;
        color: #f6f3ea;
    }
    .author strong { color: #e8b86d; font-weight: 700; }

    .kpi-grid, .insight-grid {
        display: grid;
        gap: 12px;
        margin: 0 0 1.4rem;
        width: 100%;
    }
    .kpi-grid { grid-template-columns: repeat(5, minmax(0, 1fr)); }
    .insight-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }

    .kpi {
        background: linear-gradient(180deg, rgba(26,36,62,0.95) 0%, rgba(14,20,38,0.95) 100%);
        border: 1px solid rgba(255,255,255,0.07);
        border-left: 3px solid #e8b86d;
        border-radius: 10px;
        padding: 0.75rem 0.7rem 0.7rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.22);
        min-width: 0;
    }
    .kpi.bad { border-left-color: #ef4444; }
    .kpi.warn { border-left-color: #f59e0b; }
    .kpi.ok { border-left-color: #34d399; }
    .kpi-label { font-size: 0.66rem; letter-spacing: 0.08em; text-transform: uppercase; color: #8b97b3; font-weight: 600; }
    .kpi-value { font-family: 'IBM Plex Mono', monospace; font-size: 1.2rem; color: #f7f4ec; margin: 0.28rem 0 0.1rem; font-weight: 600; }
    .kpi-hint { font-size: 0.74rem; color: #a3adc4; }

    .section-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #eef2fb;
        margin: 0.4rem 0 0.65rem;
        letter-spacing: 0.01em;
    }

    .insight {
        background: #121a30;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 0.95rem 1rem;
        min-height: 118px;
    }
    .insight.crit { border-color: rgba(239,68,68,0.45); }
    .insight.warn { border-color: rgba(245,158,11,0.4); }
    .insight.info { border-color: rgba(96,165,250,0.4); }
    .insight .k { font-size: 0.7rem; letter-spacing: 0.12em; text-transform: uppercase; color: #8b97b3; font-weight: 600; }
    .insight .v { font-size: 1.15rem; color: #f4efe4; font-weight: 600; margin: 0.35rem 0; }
    .insight .d { font-size: 0.86rem; color: #9aa6c2; }

    .stPlotlyChart { border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; background: rgba(10,16,32,0.55); padding: 0.2rem; }

    footer, #MainMenu { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    return pd.read_csv("procurement_data.csv")


def style_fig(fig, height=380):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(family="IBM Plex Sans, sans-serif", color="#c5cde0", size=12),
        margin=dict(t=28, r=18, b=44, l=52),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11), orientation="h", y=1.12),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.14)", linecolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.14)", linecolor="rgba(255,255,255,0.08)"),
        coloraxis_colorbar=dict(outlinewidth=0),
    )
    return fig


def chart(fig, height=380):
    st.plotly_chart(
        style_fig(fig, height),
        use_container_width=True,
        config={"displayModeBar": False},
    )


df = load_data()
color_map = {"Critical": "#EF4444", "High": "#F97316", "Medium": "#E8B86D", "Low": "#34D399"}

st.sidebar.markdown("### Filters")
st.sidebar.caption("Narrow the portfolio. Defaults show everything.")

vendor_filter = st.sidebar.multiselect(
    "Vendor", sorted(df["Vendor"].unique()), default=sorted(df["Vendor"].unique())
)
bu_filter = st.sidebar.multiselect(
    "Business Unit", sorted(df["BusinessUnit"].unique()), default=sorted(df["BusinessUnit"].unique())
)
category_filter = st.sidebar.multiselect(
    "Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique())
)
risk_filter = st.sidebar.multiselect(
    "Risk Tier",
    ["Critical", "High", "Medium", "Low"],
    default=["Critical", "High", "Medium", "Low"],
)

filtered = df[
    df["Vendor"].isin(vendor_filter)
    & df["BusinessUnit"].isin(bu_filter)
    & df["Category"].isin(category_filter)
    & df["RiskTier"].isin(risk_filter)
]

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Procurement risk monitoring · methodology case study</div>
      <h1>Enterprise KPI Anomaly Detection</h1>
      <p>Flag schedule and budget outliers, then trace them to vendor and business-unit drivers.</p>
      <div class="author">By <strong>Ishika Kour</strong></div>
    </div>
    """,
    unsafe_allow_html=True,
)

total_projects = len(filtered)
high_risk = filtered[filtered["RiskTier"].isin(["Critical", "High"])].shape[0]
otif_rate = (filtered["OTIF"] == "On-Time").mean() * 100 if total_projects else 0
avg_sched_var = filtered["ScheduleVariancePct"].mean() if total_projects else 0
avg_budget_var = filtered["BudgetVariancePct"].mean() if total_projects else 0
hr_pct = high_risk / total_projects * 100 if total_projects else 0

kpis = [
    ("", "Projects", f"{total_projects:,}", "in current filters"),
    ("bad", "High-risk", f"{high_risk}", f"{hr_pct:.1f}% of portfolio"),
    ("ok" if otif_rate >= 70 else "warn", "OTIF", f"{otif_rate:.1f}%", "on-time in full"),
    ("bad" if avg_sched_var > 0 else "ok", "Schedule var", f"{avg_sched_var:+.1f}%", "vs planned days"),
    ("bad" if avg_budget_var > 0 else "ok", "Budget var", f"{avg_budget_var:+.1f}%", "vs approved budget"),
]
st.markdown(
    '<div class="kpi-grid">'
    + "".join(
        f'<div class="kpi {tone}"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-hint">{hint}</div></div>'
        for tone, label, value, hint in kpis
    )
    + "</div>",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Risk matrix — schedule vs. budget variance</div>', unsafe_allow_html=True)
fig_matrix = px.scatter(
    filtered,
    x="ScheduleVariancePct",
    y="BudgetVariancePct",
    color="RiskTier",
    color_discrete_map=color_map,
    hover_data=["ProjectID", "Vendor", "BusinessUnit"],
    category_orders={"RiskTier": ["Critical", "High", "Medium", "Low"]},
)
fig_matrix.add_hline(y=0, line_dash="dash", line_color="#6b7280", opacity=0.7)
fig_matrix.add_vline(x=0, line_dash="dash", line_color="#6b7280", opacity=0.7)
fig_matrix.update_traces(marker=dict(size=10, opacity=0.82, line=dict(width=0)))
fig_matrix.update_xaxes(title="Schedule variance %")
fig_matrix.update_yaxes(title="Budget variance %")
chart(fig_matrix, 460)

r1a, r1b = st.columns(2)

with r1a:
    st.markdown('<div class="section-title">Root cause: vendor performance</div>', unsafe_allow_html=True)
    vendor_agg = (
        filtered.groupby("Vendor")
        .agg(
            projects=("ProjectID", "count"),
            avg_schedule_var=("ScheduleVariancePct", "mean"),
            avg_budget_var=("BudgetVariancePct", "mean"),
            high_risk=("RiskTier", lambda x: (x.isin(["Critical", "High"])).sum()),
        )
        .reset_index()
    )
    vendor_agg["avg_schedule_var"] = vendor_agg["avg_schedule_var"].round(1)
    vendor_agg["avg_budget_var"] = vendor_agg["avg_budget_var"].round(1)

    fig_v = go.Figure()
    fig_v.add_trace(
        go.Bar(x=vendor_agg["Vendor"], y=vendor_agg["avg_schedule_var"], name="Schedule var %", marker_color="#F87171")
    )
    fig_v.add_trace(
        go.Bar(x=vendor_agg["Vendor"], y=vendor_agg["avg_budget_var"], name="Budget var %", marker_color="#60A5FA")
    )
    fig_v.update_layout(barmode="group", yaxis_title="Variance %", bargap=0.28)
    chart(fig_v)

with r1b:
    st.markdown('<div class="section-title">Root cause: business unit</div>', unsafe_allow_html=True)
    bu_agg = (
        filtered.groupby("BusinessUnit")
        .agg(
            projects=("ProjectID", "count"),
            avg_schedule_var=("ScheduleVariancePct", "mean"),
            avg_budget_var=("BudgetVariancePct", "mean"),
        )
        .reset_index()
    )

    fig_bu = go.Figure(
        data=go.Heatmap(
            z=[bu_agg["avg_schedule_var"].round(1), bu_agg["avg_budget_var"].round(1)],
            x=bu_agg["BusinessUnit"],
            y=["Schedule var %", "Budget var %"],
            colorscale=[[0, "#14532d"], [0.5, "#1f2937"], [1, "#7f1d1d"]],
            text=[
                [f"{v:.1f}%" for v in bu_agg["avg_schedule_var"].round(1)],
                [f"{v:.1f}%" for v in bu_agg["avg_budget_var"].round(1)],
            ],
            texttemplate="%{text}",
            textfont={"size": 13, "color": "#f8fafc"},
            hoverongaps=False,
        )
    )
    chart(fig_bu)

r2a, r2b = st.columns(2)

with r2a:
    st.markdown('<div class="section-title">Risk tier distribution</div>', unsafe_allow_html=True)
    risk_counts = (
        filtered["RiskTier"].value_counts().reindex(["Critical", "High", "Medium", "Low"]).fillna(0).reset_index()
    )
    risk_counts.columns = ["RiskTier", "Count"]
    fig_r = px.pie(
        risk_counts,
        values="Count",
        names="RiskTier",
        hole=0.62,
        color="RiskTier",
        color_discrete_map=color_map,
        category_orders={"RiskTier": ["Critical", "High", "Medium", "Low"]},
    )
    fig_r.update_traces(textinfo="percent", textfont_size=13, marker=dict(line=dict(color="#0b1020", width=2)))
    chart(fig_r, 360)

with r2b:
    st.markdown('<div class="section-title">OTIF delivery rate by vendor</div>', unsafe_allow_html=True)
    otif_data = filtered.groupby(["Vendor", "OTIF"]).size().reset_index(name="Count")
    fig_o = px.bar(
        otif_data,
        x="Vendor",
        y="Count",
        color="OTIF",
        barmode="stack",
        color_discrete_map={"On-Time": "#34D399", "Delayed": "#EF4444"},
    )
    fig_o.update_layout(yaxis_title="Project count", bargap=0.35)
    chart(fig_o, 360)

st.markdown('<div class="section-title">Auto-generated insights</div>', unsafe_allow_html=True)

if total_projects > 0 and len(vendor_agg) and len(bu_agg):
    worst_vendor = vendor_agg.sort_values("avg_schedule_var", ascending=False).iloc[0]
    worst_bu = bu_agg.sort_values("avg_schedule_var", ascending=False).iloc[0]
    critical_pct = (filtered["RiskTier"] == "Critical").mean() * 100
    st.markdown(
        f"""<div class="insight-grid">
        <div class="insight crit"><div class="k">Highest-risk vendor</div><div class="v">{worst_vendor['Vendor']}</div><div class="d">Avg schedule variance {worst_vendor['avg_schedule_var']:.1f}%</div></div>
        <div class="insight warn"><div class="k">Highest-risk business unit</div><div class="v">{worst_bu['BusinessUnit']}</div><div class="d">Avg schedule variance {worst_bu['avg_schedule_var']:.1f}%</div></div>
        <div class="insight info"><div class="k">Critical projects</div><div class="v">{critical_pct:.1f}%</div><div class="d">of the filtered portfolio needs immediate intervention</div></div>
        </div>""",
        unsafe_allow_html=True,
    )
else:
    st.info("No projects match the current filters.")

st.caption("Python · Pandas · SciPy · Plotly · Streamlit")
