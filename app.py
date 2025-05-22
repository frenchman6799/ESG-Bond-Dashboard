
# ESG Bond Intelligence Dashboard – Streamlit App with Ecosystem Overview & Scraping

import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="India ESG Bond Intelligence", layout="wide")

st.title("🇮🇳 India ESG Bond Intelligence Dashboard")
st.markdown("This dashboard provides a clean visualization of **Green Bonds**, **Social Bonds**, and **Sustainability-linked Bonds** issued in India, based on SEBI data.")

# ---- Data Fetch Function (SEBI) ----
def fetch_sebi_green_bonds():
    try:
        url = "https://www.sebi.gov.in/statistics/greenbonds.html"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table")
        df = pd.read_html(str(table))[0]
        df.to_csv("green_bonds.csv", index=False)
        return df
    except Exception as e:
        st.error(f"Failed to fetch live data: {e}")
        return pd.DataFrame()

# ---- Data Load ----
@st.cache_data
def load_data():
    try:
        green = pd.read_csv("green_bonds.csv")
        social = pd.read_csv("social_bonds.csv")
        impact = pd.read_csv("impact_metrics.csv")
        return green, social, impact
    except:
        return fetch_sebi_green_bonds(), pd.DataFrame(), pd.DataFrame()

green_df, social_df, impact_df = load_data()

tab1, tab2 = st.tabs(["📊 Bond Dashboard", "🌍 ESG Ecosystem Overview"])

with tab1:
    if not green_df.empty:
        st.sidebar.header("🔍 Filters")
        year_filter = st.sidebar.multiselect("Select Year(s):", sorted(green_df["Year"].unique()), default=sorted(green_df["Year"].unique()))
        type_filter = st.sidebar.selectbox("Select Bond Type:", ["Green Bonds", "Social Bonds", "Impact Metrics"])

        if type_filter == "Green Bonds":
            st.subheader("🟢 Green Bonds Overview")
            green_year = green_df[green_df["Year"].isin(year_filter)]

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Green Bonds Issued", f"₹{green_year['Amount (Cr INR)'].sum():,.0f}")
            with col2:
                st.metric("Unique Issuers", green_year["Issuer"].nunique())

            st.altair_chart(
                alt.Chart(green_year).mark_bar().encode(
                    x="Year:O", y="Amount (Cr INR):Q", color="Use of Proceeds:N"
                ).properties(title="Green Bond Issuances by Year and Sector", width=700), use_container_width=True
            )
            st.dataframe(green_year.sort_values("Year", ascending=False))

        elif type_filter == "Social Bonds":
            st.subheader("🔵 Social & Sustainability-linked Bonds")
            social_year = social_df[social_df["Year"].isin(year_filter)]
            st.altair_chart(
                alt.Chart(social_year).mark_bar().encode(
                    x="Use Case:N", y="Amount (Cr INR):Q", color="Issuer:N"
                ).properties(title="Social Bond Distribution by Use Case", width=700), use_container_width=True
            )
            st.dataframe(social_year.sort_values("Year", ascending=False))

        elif type_filter == "Impact Metrics":
            st.subheader("🌱 Environmental Impact Dashboard")
            st.altair_chart(
                alt.Chart(impact_df).mark_line(point=True).encode(
                    x="Year:O", y="CO2 Saved (tons):Q", color="Metric:N"
                ).properties(title="CO₂ Emissions Avoided Over Time"), use_container_width=True
            )
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Cumulative CO₂ Saved", f"{impact_df['CO2 Saved (tons)'].sum():,.0f} tons")
            with col2:
                st.metric("Renewable Energy Added", f"{impact_df['Renewable Capacity (MW)'].sum():,.0f} MW")
            st.dataframe(impact_df)
    else:
        st.warning("Data not loaded. Please make sure CSV files are available.")

with tab2:
    st.subheader("🌍 India ESG Bond Ecosystem Overview")
    if not green_df.empty:
        top_issuers = green_df.groupby("Issuer")["Amount (Cr INR)"].sum().nlargest(10).reset_index()
        st.altair_chart(
            alt.Chart(top_issuers).mark_bar().encode(
                x="Amount (Cr INR):Q",
                y=alt.Y("Issuer:N", sort="-x"),
                color="Issuer:N"
            ).properties(title="Top ESG Bond Issuers", height=400),
            use_container_width=True
        )
        sector_dist = green_df.groupby("Use of Proceeds")["Amount (Cr INR)"].sum().reset_index()
        st.altair_chart(
            alt.Chart(sector_dist).mark_arc().encode(
                theta="Amount (Cr INR):Q",
                color="Use of Proceeds:N",
                tooltip=["Use of Proceeds", "Amount (Cr INR)"]
            ).properties(title="Sector-wise ESG Proceeds Distribution"),
            use_container_width=True
        )
    else:
        st.info("Ecosystem visuals will appear when Green Bond data is available.")

st.markdown("---")
st.markdown("📄 Based on data from [SEBI Green Bonds Statistics](https://www.sebi.gov.in/statistics/greenbonds.html) and issuer disclosures. Built by Jayakrishnan K.S")
