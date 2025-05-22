import streamlit as st
import pandas as pd
import altair as alt
import os

st.set_page_config(page_title="India ESG Bond Intelligence", layout="wide")

st.title("🇮🇳 India ESG Bond Intelligence Dashboard")
st.markdown("""
This dashboard provides a clean visualization of **Green Bonds**, **Social Bonds**, and **Sustainability-linked Bonds** issued in India, based on SEBI data.
""")

# Debug file existence
st.sidebar.header("🔎 Data File Check")
st.sidebar.write("green_bonds.csv exists? ", os.path.exists("green_bonds.csv"))
st.sidebar.write("social_bonds.csv exists? ", os.path.exists("social_bonds.csv"))
st.sidebar.write("impact_metrics.csv exists? ", os.path.exists("impact_metrics.csv"))

@st.cache_data
def load_data():
    green = pd.read_csv("green_bonds.csv")
    social = pd.read_csv("social_bonds.csv")
    impact = pd.read_csv("impact_metrics.csv")
    return green, social, impact

try:
    green_df, social_df, impact_df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    green_df, social_df, impact_df = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

page = st.sidebar.radio("Navigate", ["📊 Bond Dashboard", "🌍 ESG Ecosystem Overview"])

if green_df.empty or social_df.empty or impact_df.empty:
    st.error("Data not loaded. Please upload CSV files correctly to the repo and check file paths.")
else:
    if page == "📊 Bond Dashboard":
        st.subheader("🟢 Green Bonds Overview")
        year_filter = st.sidebar.multiselect("Select Year(s):", sorted(green_df["Year"].unique()), default=sorted(green_df["Year"].unique()))
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

    elif page == "🌍 ESG Ecosystem Overview":
        st.subheader("🔵 Social & Sustainability-linked Bonds")
        year_filter = st.sidebar.multiselect("Select Year(s):", sorted(social_df["Year"].unique()), default=sorted(social_df["Year"].unique()))
        social_year = social_df[social_df["Year"].isin(year_filter)]

        st.altair_chart(
            alt.Chart(social_year).mark_bar().encode(
                x="Use Case:N", y="Amount (Cr INR):Q", color="Issuer:N"
            ).properties(title="Social Bond Distribution by Use Case", width=700), use_container_width=True
        )

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

        st.dataframe(social_year.sort_values("Year", ascending=False))
        st.dataframe(impact_df)

st.markdown("""
---
📄 Based on data from [SEBI Green Bonds Statistics](https://www.sebi.gov.in/statistics/greenbonds.html) and issuer disclosures.  
📬 Built by Jayakrishnan K.S | [GitHub](https://github.com/frenchman6799)
""")
