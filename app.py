
import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("MegaDataset_v2_Nov2024_onward.csv", parse_dates=["Date"])
    return df

df = load_data()

st.title("Phil's Health Dashboard")
st.markdown("### Integrated RENPHO, Blood Pressure, and Bloods (Nov 2024 → present)")

# Sidebar filters
st.sidebar.header("Filters")
min_date, max_date = df["Date"].min(), df["Date"].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
if len(date_range) == 2:
    start_date, end_date = date_range
    df = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]

# Tabs for different categories
tabs = st.tabs(["Weight & Body Comp", "Blood Pressure", "Hormones", "FBC", "Lipids", "Vitamins & Others"])

with tabs[0]:
    st.subheader("Weight & Body Composition")
    if "Weight_kg" in df.columns:
        fig = px.line(df, x="Date", y="Weight_kg", title="Weight (kg) over Time")
        st.plotly_chart(fig, use_container_width=True)
    if "RENPHO_BodyFat_pct" in df.columns:
        fig = px.line(df, x="Date", y=["RENPHO_BodyFat_pct", "RENPHO_BodyFat_pct_corrected"],
                      title="Body Fat % (Raw vs Corrected)")
        st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    st.subheader("Blood Pressure")
    if "BP_Systolic" in df.columns:
        fig = px.line(df, x="Date", y=["BP_Systolic", "BP_Diastolic"], title="Blood Pressure (Sys/Dia)")
        st.plotly_chart(fig, use_container_width=True)
    if "BP_Pulse" in df.columns:
        fig = px.line(df, x="Date", y="BP_Pulse", title="Pulse (bpm)")
        st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.subheader("Hormones")
    hormone_cols = [c for c in df.columns if c.startswith("Hormone_")]
    if hormone_cols:
        fig = px.line(df, x="Date", y=hormone_cols, title="Hormone Trends")
        st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    st.subheader("Full Blood Count")
    fbc_cols = [c for c in df.columns if c.startswith("FBC_")]
    if fbc_cols:
        fig = px.line(df, x="Date", y=fbc_cols, title="FBC Trends")
        st.plotly_chart(fig, use_container_width=True)

with tabs[4]:
    st.subheader("Lipids")
    lipid_cols = [c for c in df.columns if c.startswith("Lipid_")]
    if lipid_cols:
        fig = px.line(df, x="Date", y=lipid_cols, title="Lipid Trends")
        st.plotly_chart(fig, use_container_width=True)

with tabs[5]:
    st.subheader("Vitamins & Others")
    vitamin_cols = [c for c in df.columns if c.startswith("Vitamin_")] + ["PSA", "TSH"]
    vitamin_cols = [c for c in vitamin_cols if c in df.columns]
    if vitamin_cols:
        fig = px.line(df, x="Date", y=vitamin_cols, title="Vitamins & Other Markers")
        st.plotly_chart(fig, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.write("Context flags are included in the dataset (see 'Context' column).")
