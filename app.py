import streamlit as st
import pandas as pd

# Basic Dashboard Setup
st.title("🇮🇳 Indian Green Bonds Dashboard")
st.caption("Simple no-code solution - Just update the Excel file monthly")

# Load Data
try:
    df = pd.read_excel("data/green_bonds.xlsx")
    st.success("Data loaded successfully!")
except:
    st.error("""
    Error: File not found. Please:
    1. Create a 'data' folder
    2. Save your Excel file as 'green_bonds.xlsx' inside it
    """)
    st.stop()

# Show Data
st.dataframe(df)

# Key Metrics
st.subheader("Summary Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Bonds", len(df))
col2.metric("Total Value (₹ Cr)", df["Amount Raised (In Rs. Crs)"].sum())
col3.metric("Avg. Coupon Rate", f"{df['Coupon (%)'].mean():.2f}%")

# Update Instructions
st.info("""
**How to update:**
1. Get new data from SEBI/RBI
2. Replace the table in 'data/green_bonds.xlsx'
3. Re-run the app (no coding needed)
""")
