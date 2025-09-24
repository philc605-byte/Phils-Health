
import streamlit as st
import sys, os
import importlib
st.set_page_config(page_title="Diag - Phil's Health Dashboard", layout="wide")

st.title("Diagnostic App")
st.write("If you can see this, Streamlit is running.")

# Show environment info
st.subheader("Environment")
st.write({"python_version": sys.version})
for pkg in ["streamlit", "pandas", "plotly"]:
    try:
        mod = importlib.import_module(pkg)
        st.write(f"{pkg} version:", getattr(mod, "__version__", "unknown"))
    except Exception as e:
        st.write(f"{pkg} import error:", e)

# List files in current repo
st.subheader("Repo Files")
st.write(os.listdir("."))

# Check for dataset
fname = "MegaDataset_v2_Nov2024_onward.csv"
st.subheader("Dataset Check")
if os.path.exists(fname):
    st.success(f"Found {fname}")
    import pandas as pd
    try:
        df = pd.read_csv(fname, parse_dates=["Date"])
        st.write("Head:", df.head())
        st.success("CSV parsed OK")
    except Exception as e:
        st.error(f"Failed to parse CSV: {e}")
else:
    st.warning(f"{fname} not found in repo root. Upload it below or rename in app.")
    uploaded = st.file_uploader("Upload your CSV", type=["csv"])
    if uploaded:
        import pandas as pd
        try:
            df = pd.read_csv(uploaded, parse_dates=["Date"])
            st.write("Head:", df.head())
            st.success("Uploaded CSV parsed OK")
        except Exception as e:
            st.error(f"Upload parse failed: {e}")
