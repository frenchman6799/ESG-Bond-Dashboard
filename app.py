import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="India ESG Bond Intelligence", layout="wide")

# --- LIVE DATA FETCH FUNCTION ---
@st.cache_data(ttl=12 * 60 * 60)
def fetch_sebi_green_bonds_data():
    url = "https://www.sebi.gov.in/statistics/greenbonds.html"
    try:
        tables = pd.read_html(url)
        green_bonds_table = tables[0]  # adjust index if SEBI changes structure
        green_bonds_table.columns = green_bonds_table.columns.str.strip()
        return green_bonds_table, None
    except Exception as e:
        return None, str(e)

# --- FALLBACK CSV LOADS ---
@st.cache_data
def load_other_data():
    social = pd.read_csv("social_bonds.csv")
    impact = pd.read_csv("impact_metrics.csv")
    return social, impact

# --- LOAD DATA ---
green_df, error = fetch_sebi_green_bonds_data()
if error:
    st.warning(f"Could not fetch SEBI live data. Using fallback CSV. Error: {error}")
    green_df = pd.read_csv("green_bonds.csv")

social_df, impact_df = load_other_data()

# --- HEADER ---
st.title("🇮🇳 India ESG Bond Intelligence Dashboard")
st.markdown("""
This dashboard provides a clean visualization of **Green Bonds**, **Social Bonds**, and **Sustainability-linked Bonds** issued in India, based on SEBI data.
""")

# --- PAGE NAVIGATION ---
page = st.sidebar.radio("Navigate", ["📊 Bond Dashboard", "🌍 ESG Ecosystem Overview"])

# --- BOND DASHBOARD ---
if page == "📊 Bond Dashboard":
    st.subheader("🟢 Green Bonds Overview")

    if "Year" in green_df.columns:
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
    else:
        st.error("SEBI table format may have changed. Check column names.")

# --- ESG ECOSYSTEM OVERVIEW ---
elif page == "🌍 ESG Ecosystem Overview":
    st.subheader("🔵 Social & Sustainability-linked Bonds")
    if "Year" in social_df.columns:
        year_filter = st.sidebar.multiselect("Select Year(s):", sorted(social_df["Year"].unique()), default=sorted(social_df["Year"].unique()))
        social_year = social_df[social_df["Year"].isin(year_filter)]

        st.altair_chart(
            alt.Chart(social_year).mark_bar().encode(
                x="Use Case:N", y="Amount (Cr INR):Q", color="Issuer:N"
            ).properties(title="Social Bond Distribution by Use Case", width=700), use_container_width=True
        )
        st.dataframe(social_year.sort_values("Year", ascending=False))
    else:
        st.error("Check if your social_bonds.csv has a 'Year' column.")

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

# --- FOOTER ---
st.markdown("""
---
📄 Based on data from [SEBI Green Bonds Statistics](https://www.sebi.gov.in/statistics/greenbonds.html) and issuer disclosures.  
📬 Built by Jayakrishnan K.S | [GitHub](https://github.com/frenchman6799)
""")
