
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Phil's Health Dashboard", layout="wide")

def load_default_csv():
    try:
        df = pd.read_csv("MegaDataset_v2_Nov2024_onward.csv", parse_dates=["Date"])
        return df
    except Exception as e:
        st.info("Couldn't auto-load MegaDataset_v2_Nov2024_onward.csv. Upload the CSV below.")
        st.caption(f"Loader message: {e}")
        return None

st.title("Phil's Health Dashboard")
st.markdown("Integrated RENPHO • Blood Pressure • Bloods (Nov 2024 → present)")

# Try to load default file, else allow upload
df = load_default_csv()
uploaded = st.file_uploader("Optional: Upload MegaDataset_v2_Nov2024_onward.csv", type=["csv"])
if uploaded is not None:
    try:
        df = pd.read_csv(uploaded, parse_dates=["Date"])
        st.success("CSV loaded from upload.")
    except Exception as e:
        st.error(f"Upload failed: {e}")

if df is None:
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")
min_date, max_date = df["Date"].min(), df["Date"].max()
date_range = st.sidebar.date_input("Date range", [min_date, max_date], min_value=min_date, max_value=max_date)
if len(date_range) == 2:
    start_date, end_date = date_range
    df = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]

# Helper to safely pick only existing columns
def existing(cols):
    return [c for c in cols if c in df.columns]

tabs = st.tabs(["Weight & Body Comp", "Blood Pressure", "Hormones", "FBC", "Lipids", "Vitamins & Others", "Raw Table"])

with tabs[0]:
    st.subheader("Weight & Body Composition")
    if "Weight_kg" in df.columns:
        st.metric("Latest weight (kg)", f"{df['Weight_kg'].dropna().iloc[-1]:.2f}" if df['Weight_kg'].notna().any() else "—")
        fig = px.line(df, x="Date", y="Weight_kg", title="Weight (kg)")
        st.plotly_chart(fig, use_container_width=True)
    cols = existing(["RENPHO_BodyFat_pct", "RENPHO_BodyFat_pct_corrected"])
    if cols:
        fig = px.line(df, x="Date", y=cols, title="Body Fat % (Raw/Corrected)")
        st.plotly_chart(fig, use_container_width=True)
    lean_cols = existing(["RENPHO_LeanMass_st"])
    if lean_cols:
        st.caption("Lean mass shown in stones; convert to kg by × 6.35029.")
        fig = px.line(df, x="Date", y=lean_cols, title="Lean Mass (st)")
        st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    st.subheader("Blood Pressure")
    bp_cols = existing(["BP_Systolic", "BP_Diastolic"])
    if bp_cols:
        fig = px.line(df, x="Date", y=bp_cols, title="Blood Pressure (Sys/Dia)")
        st.plotly_chart(fig, use_container_width=True)
    if "BP_Pulse" in df.columns:
        fig = px.line(df, x="Date", y="BP_Pulse", title="Pulse (bpm)")
        st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.subheader("Hormones")
    h_cols = [c for c in df.columns if c.startswith("Hormone_")]
    if h_cols:
        fig = px.line(df, x="Date", y=h_cols, title="Hormone Trends")
        st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    st.subheader("Full Blood Count")
    f_cols = [c for c in df.columns if c.startswith("FBC_")]
    if f_cols:
        fig = px.line(df, x="Date", y=f_cols, title="FBC Trends")
        st.plotly_chart(fig, use_container_width=True)

with tabs[4]:
    st.subheader("Lipids")
    l_cols = [c for c in df.columns if c.startswith("Lipid_")]
    if l_cols:
        fig = px.line(df, x="Date", y=l_cols, title="Lipid Trends")
        st.plotly_chart(fig, use_container_width=True)

with tabs[5]:
    st.subheader("Vitamins & Others")
    v_cols = existing([c for c in df.columns if c.startswith("Vitamin_")] + ["PSA","TSH"])
    if v_cols:
        fig = px.line(df, x="Date", y=v_cols, title="Vitamins & Other Markers")
        st.plotly_chart(fig, use_container_width=True)

with tabs[6]:
    st.subheader("Raw Data")
    st.dataframe(df.sort_values("Date"))
