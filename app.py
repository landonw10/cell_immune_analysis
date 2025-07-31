import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os
from analysis import get_frequency_summary, display_frequency_summary, compare_response_groups, analyze_subset
from load_data import create_schema, load_csv_to_db

# Ensure the database and schema exist
if not os.path.exists("database.db"):
    conn = sqlite3.connect("database.db")
    create_schema(conn)
    conn.close()
    load_csv_to_db("cell-count.csv")

st.set_page_config(page_title="Immune Cell Dashboard", layout="wide")
st.title("🧬 Immune Cell Frequency Analysis Dashboard")

# Sidebar navigation
view = st.sidebar.selectbox("Select View", [
    "Overview", 
    "Response Group Comparison", 
    "Subset Summary"
])

if view == "Overview":
    st.header("📋 Overview of Cell Frequencies")
    st.write("Interactive view of immune cell frequencies per sample, with filters for sample and cell population.")

    # Load frequency summary
    summary = get_frequency_summary()

    # Filters
    samples = st.multiselect("Select Samples", options=summary["sample"].unique())
    populations = st.multiselect("Select Cell Populations", options=summary["population"].unique())

    filtered = summary.copy()
    if samples:
        filtered = filtered[filtered["sample"].isin(samples)]
    if populations:
        filtered = filtered[filtered["population"].isin(populations)]

    display_frequency_summary(filtered)

elif view == "Response Group Comparison":
    st.header("📊 Response Group Comparison")
    st.write("Compare responders vs. non-responders based on selected filters.")

    # Load frequency summary
    summary = get_frequency_summary()

    # Load metadata for filtering
    conn = sqlite3.connect("database.db")
    metadata = pd.read_sql_query("SELECT condition, treatment, sample_type, time_from_treatment_start FROM sample_metadata", conn)
    conn.close()

    # Get unique options to index for filters
    condition_options = sorted(metadata["condition"].dropna().unique())
    treatment_options = sorted(metadata["treatment"].dropna().unique())
    sample_type_options = sorted(metadata["sample_type"].dropna().unique())
    timepoint_options = sorted(metadata["time_from_treatment_start"].dropna().unique())

    # Create filters, preset to melanoma, miraclib, and PBMC
    condition = st.selectbox(
        "Condition",
        options=condition_options,
        index=condition_options.index("melanoma") if "melanoma" in condition_options else 0
    )

    treatment = st.selectbox(
        "Treatment",
        options=treatment_options,
        index=treatment_options.index("miraclib") if "miraclib" in treatment_options else 0
    )

    sample_type = st.selectbox(
        "Sample Type",
        options=sample_type_options,
        index=sample_type_options.index("PBMC") if "PBMC" in sample_type_options else 0
    )

    timepoint = st.multiselect(
        "Timepoints to Include (Empty for all)",
        options=timepoint_options,
        default=[]
    )

    filters = {
        "condition": [condition],
        "treatment": [treatment],
        "sample_type": [sample_type],
        "timepoint": timepoint
    }

    compare_response_groups(summary, filters=filters)


elif view == "Subset Summary":
    st.header("🔍 Subset Summary")
    st.write("Explore subject characteristics across different treatment timepoints and sample groups.")

    # Load metadata for filtering
    conn = sqlite3.connect("database.db")
    metadata = pd.read_sql_query("SELECT condition, treatment, sample_type, time_from_treatment_start FROM sample_metadata", conn)
    conn.close()

    # Create filters, preset to melanoma, miraclib, PBMC, and 0 days
    conditions = st.multiselect(
        "Select Condition",
        options=metadata["condition"].dropna().unique(),
        default=["melanoma"] if "melanoma" in metadata["condition"].unique() else []
    )

    treatments = st.multiselect(
        "Select Treatment",
        options=metadata["treatment"].dropna().unique(),
        default=["miraclib"] if "miraclib" in metadata["treatment"].unique() else []
    )

    sample_types = st.multiselect(
        "Select Sample Type",
        options=metadata["sample_type"].dropna().unique(),
        default=["PBMC"] if "PBMC" in metadata["sample_type"].unique() else []
    )

    timepoints = st.multiselect(
        "Select Timepoint (Days from Treatment Start)",
        options=metadata["time_from_treatment_start"].dropna().unique(),
        default=[0] if 0 in metadata["time_from_treatment_start"].unique() else []
    )

    filters = {
        "condition": conditions,
        "treatment": treatments,
        "sample_type": sample_types,
        "timepoint": timepoints
    }

    analyze_subset(filters)