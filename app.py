import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from analysis import get_frequency_summary, compare_response_groups, analyze_baseline_subset
from load_data import create_schema, load_csv_to_db

st.set_page_config(page_title="Immune Cell Dashboard", layout="wide")
st.title("🧬 Immune Cell Frequency Analysis Dashboard")

# Load frequency data
summary = get_frequency_summary()

# Sidebar navigation
view = st.sidebar.selectbox("Select View", [
    "Overview", 
    "Response Group Comparison", 
    "Subset Summary"
])

if view == "Overview":
    st.header("📋 Overview of Cell Frequencies")
    st.write("Interactive view of immune cell frequencies per sample, with filters for sample and cell population.")

    # Filters
    samples = st.multiselect("Select Samples", options=summary["sample"].unique())
    populations = st.multiselect("Select Cell Populations", options=summary["population"].unique())

    filtered = summary.copy()
    if samples:
        filtered = filtered[filtered["sample"].isin(samples)]
    if populations:
        filtered = filtered[filtered["population"].isin(populations)]

    st.dataframe(filtered)

elif view == "Response Group Comparison":
    st.header("📊 Response Group Comparison")
    st.write("Compare responders vs. non-responders based on selected filters.")

    condition = st.selectbox("Condition", options=["melanoma", "carcinoma"])
    treatment = st.selectbox("Treatment", options=["miraclib", "phauximab"])
    sample_type = st.selectbox("Sample Type", options=["PBMC", "WB"])

    filters = {
        "condition": [condition],
        "treatment": [treatment],
        "sample_type": [sample_type]
    }

    compare_response_groups(summary, filters=filters)

elif view == "Subset Summary":
    st.header("🔍 Subset Summary")
    st.write("Explore subject characteristics across different treatment timepoints and sample groups.")

    # Load metadata for filtering
    conn = sqlite3.connect("database.db")
    metadata = pd.read_sql_query("SELECT condition, treatment, sample_type, time_from_treatment_start FROM sample_metadata", conn)
    conn.close()

    # Filters using metadata
    conditions = st.multiselect(
        "Select Condition",
        options=metadata["condition"].unique(),
        default=["melanoma"] if "melanoma" in metadata["condition"].unique() else []
    )

    treatments = st.multiselect(
        "Select Treatment",
        options=metadata["treatment"].unique(),
        default=["miraclib"] if "miraclib" in metadata["treatment"].unique() else []
    )

    sample_types = st.multiselect(
        "Select Sample Type",
        options=metadata["sample_type"].unique(),
        default=["PBMC"] if "PBMC" in metadata["sample_type"].unique() else []
    )

    timepoints = st.multiselect(
        "Select Timepoint (Days from Treatment Start)",
        options=metadata["time_from_treatment_start"].dropna().unique(),
        default=[0] if 0 in metadata["time_from_treatment_start"].dropna().unique() else []
    )
    
    filters = {
        "condition": conditions,
        "treatment": treatments,
        "sample_type": sample_types,
        "timepoint": timepoints
    }

    analyze_baseline_subset(filters)