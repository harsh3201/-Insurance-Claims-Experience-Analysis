import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(
    page_title="Insurance Claims Analytics Dashboard",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
    }
    [data-testid="stMetricValue"] {
        color: #1e3a8a !important;
    }
    [data-testid="stMetricLabel"] {
        color: #6b7280 !important;
    }
    h1 {
        color: #1e3a8a;
    }
    .recommendation-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1e3a8a;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .recommendation-card h3 {
        color: #1e3a8a !important;
        margin-top: 0;
    }
    .recommendation-card p {
        color: #1f2937 !important;
        margin-bottom: 0.5rem;
    }
    .summary-box {
        background-color: #e0f2fe;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #0369a1;
        margin-bottom: 20px;
        color: #0c4a6e !important;
    }
    .summary-box b {
        color: #0369a1 !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data():
    df = pd.read_csv("data/claims_data.csv")
    df['submission_date'] = pd.to_datetime(df['submission_date'])
    df['approval_date'] = pd.to_datetime(df['approval_date'])
    df['tat_days'] = (df['approval_date'] - df['submission_date']).dt.days
    df['settlement_ratio'] = df['settlement_amount'] / df['claim_amount']
    df['month_year'] = df['submission_date'].dt.to_period('M').astype(str)
    return df

df_raw = get_data()

st.sidebar.title("🔍 Search & Filters")
channel_filter = st.sidebar.multiselect("Submission Channel", options=df_raw["channel"].unique(), default=df_raw["channel"].unique())
type_filter = st.sidebar.multiselect("Claim Type", options=df_raw["claim_type"].unique(), default=df_raw["claim_type"].unique())
city_filter = st.sidebar.multiselect("User City", options=df_raw["user_city"].unique(), default=df_raw["user_city"].unique())

df = df_raw[
    (df_raw["channel"].isin(channel_filter)) & 
    (df_raw["claim_type"].isin(type_filter)) &
    (df_raw["user_city"].isin(city_filter))
]

st.title("🧩 Insurance Claims Experience Analysis")
st.markdown("Analyzing the lifecycle of claims to improve transparency and turnaround time.")


if not df.empty:
    avg_tat_val = df["tat_days"].mean()
    rej_rate_val = (df["claim_status"] == 'Rejected').mean() * 100
    worst_city = df.groupby('user_city')['tat_days'].mean().idxmax()
    top_reason = df['rejection_reason'].value_counts().idxmax() if not df['rejection_reason'].dropna().empty else "N/A"

    st.markdown(f"""
    <div class="summary-box">
        <b>🚀 Automated Executive Summary:</b><br>
        The current segment shows an average Turnaround Time of <b>{avg_tat_val:.1f} days</b> with a rejection rate of <b>{rej_rate_val:.1f}%</b>. 
        The most frequent bottleneck is <b>'{top_reason}'</b>. Geographically, <b>{worst_city}</b> is experiencing the highest processing delays.
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Performance KPIs", "🌍 Deep Dives", "💡 Product Strategy"])

    with tab1:
        st.subheader("Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Claims", f"{len(df):,}")
        col2.metric("Avg Claim TAT", f"{avg_tat_val:.1f} Days")
        col3.metric("Approval Rate", f"{(df['claim_status'] == 'Approved').mean()*100:.1f}%")
        col4.metric("Avg Settlement Gap", f"{(1 - df['settlement_ratio'].mean())*100:.1f}%")

        st.divider()

        st.subheader("📈 Performance Trends Over Time")
        trend_df = df.groupby('month_year').agg({'tat_days': 'mean', 'claim_status': lambda x: (x == 'Rejected').mean() * 100}).reset_index()
        fig_trend, ax_trend = plt.subplots(figsize=(12, 5))
        sns.lineplot(data=trend_df, x='month_year', y='tat_days', marker='o', label='Avg TAT (Days)', ax=ax_trend, color='#1e3a8a')
        ax_trend_right = ax_trend.twinx()
        sns.lineplot(data=trend_df, x='month_year', y='claim_status', marker='s', label='Rejection Rate (%)', ax=ax_trend_right, color='#ef4444')
        ax_trend.set_ylabel("Days")
        ax_trend_right.set_ylabel("Rejection Rate (%)")
        plt.title("Claims TAT and Rejection Trends (Monthly)")
        st.pyplot(fig_trend)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("⏱️ Avg TAT by Claim Type")
            tat_type = df.groupby("claim_type")["tat_days"].mean().sort_values(ascending=False)
            fig, ax = plt.subplots()
            sns.barplot(x=tat_type.index, y=tat_type.values, palette="Blues_d", ax=ax)
            st.pyplot(fig)
        with c2:
            st.subheader("❌ Rejection Breakdown")
            rej_data = df[df["claim_status"] == "Rejected"]["rejection_reason"].value_counts()
            if not rej_data.empty:
                fig, ax = plt.subplots()
                rej_data.plot(kind='pie', autopct='%1.1f%%', colormap='Reds', ax=ax)
                ax.set_ylabel("")
                st.pyplot(fig)
            else: st.info("No rejections found.")

    with tab2:
        st.subheader("🌍 Geographical Performance Deep-Dive")
        city_perf = df.groupby('user_city').agg({'tat_days': 'mean', 'claim_status': lambda x: (x == 'Rejected').mean() * 100}).reset_index()
        
        col_geo1, col_geo2 = st.columns(2)
        with col_geo1:
            st.markdown("**Avg TAT by City**")
            fig_cat, ax_cat = plt.subplots()
            sns.barplot(data=city_perf.sort_values('tat_days'), y='user_city', x='tat_days', palette='coolwarm', ax=ax_cat)
            st.pyplot(fig_cat)
        with col_geo2:
            st.markdown("**Rejection Rate by City**")
            fig_re, ax_re = plt.subplots()
            sns.barplot(data=city_perf.sort_values('claim_status'), y='user_city', x='claim_status', palette='YlOrRd', ax=ax_re)
            st.pyplot(fig_re)

        st.divider()

        st.subheader("💰 Financial & High-Value Analysis")
        c_fin1, c_fin2 = st.columns(2)
        
        with c_fin1:
            st.markdown("**Settlement Ratio Gap by Type**")
            fig_gap, ax_gap = plt.subplots()
            sns.boxplot(data=df[df['claim_status']=='Approved'], x='claim_type', y='settlement_ratio', palette='Set3', ax=ax_gap)
            plt.title("Settlement vs Claim Amount Ratio")
            st.pyplot(fig_gap)
            st.caption("Lower ratios indicate higher 'Negotiation' or customer dissatisfaction points.")

        with c_fin2:
            st.markdown("**TAT vs Claim Amount**")
            fig_scat, ax_scat = plt.subplots()
            sns.regplot(data=df.sample(min(300, len(df))), x='claim_amount', y='tat_days', scatter_kws={'alpha':0.4}, line_kws={'color':'red'}, ax=ax_scat)
            st.pyplot(fig_scat)
            st.caption("Correlation between claim size and processing speed.")

    with tab3:
        st.subheader("🚀 Data-Backed Product Recommendations")
        recs = [
            {"title": "1. Smart Document Checklist", "problem": "Missing documents drive the high rejection rate shown in Chart 2.", "solution": "Dynamic pre-submission validation.", "impact": "Projected 15% reduction in rejections."},
            {"title": "2. Real-Time Claim Tracker", "problem": f"Life claims take {df_raw[df_raw['claim_type']=='Life']['tat_days'].mean():.1f} days on average.", "solution": "Visual stepper in the app UI.", "impact": "Lower support tickets for 'Status Checks'."},
            {"title": "3. OCR Verification", "problem": "Incomplete data is localized in the verification phase.", "solution": "AI-based blur and document type detection.", "impact": "Faster initial screen TAT."},
            {"title": "4. Regional Service Optimization", "problem": f"{worst_city} is underperforming our national average TAT.", "solution": "Localized TPA (Third Party Administrator) training.", "impact": "Standardized experience across all cities."}
        ]
        for rec in recs:
            st.markdown(f"""<div class="recommendation-card"><h3>{rec['title']}</h3><p><b>⚠️ Problem:</b> {rec['problem']}</p><p><b>✨ Solution:</b> {rec['solution']}</p><p><b>📈 Impact:</b> {rec['impact']}</p></div>""", unsafe_allow_html=True)

    if st.checkbox("Show Raw Data Preview"):
        st.dataframe(df.head(100))
else:
    st.warning("⚠️ No data available for the selected filters. Please adjust your search criteria.")

st.sidebar.markdown("---")
st.sidebar.success("Premium Insights Dashboard Active")
