import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import mannwhitneyu



# Create a summary of immune cell frequencies across samples
def get_frequency_summary(db_path="database.db"):
    # Connect to database
    conn = sqlite3.connect(db_path)

    # Load cell counts
    df = pd.read_sql_query("SELECT * FROM cell_counts", conn)
    conn.close()

    # Calculate total cell count per sample
    total_counts = df.groupby("sample_id")["count"].sum().reset_index()
    total_counts = total_counts.rename(columns={"count": "total_count"})

    # Merge total counts back into main table
    merged = df.merge(total_counts, on="sample_id")

    # Calculate relative percentage
    merged["percentage"] = (merged["count"] / merged["total_count"]) * 100

    # Rename columns (keep count, percentage, and total_count)
    summary = merged.rename(columns={
        "sample_id": "sample",
        "cell_type": "population",
    })

    return summary[["sample", "total_count", "population", "count", "percentage"]]



# Compare immune cell frequencies between treatment response groups
def compare_response_groups(summary_df, filters=None, db_path="database.db"):
    # Load sample metadata
    conn = sqlite3.connect(db_path)
    metadata = pd.read_sql_query(
        "SELECT sample_id, condition, treatment, sample_type, response FROM sample_metadata", conn
    )
    conn.close()

    # Merge summary with metadata
    merged = summary_df.merge(metadata, left_on="sample", right_on="sample_id")

    # Apply data filters
    if filters:
        if filters.get("condition"):
            merged = merged[merged["condition"].isin(filters["condition"])]
        if filters.get("treatment"):
            merged = merged[merged["treatment"].isin(filters["treatment"])]
        if filters.get("sample_type"):
            merged = merged[merged["sample_type"].isin(filters["sample_type"])]

    if merged.empty:
        st.warning("No data available for the selected filters.")

    # Display data w/ boxplot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        data=merged,
        x="population",
        y="percentage",
        hue="response",
        ax=ax
    )
    ax.set_title("Immune Cell Frequencies by Treatment Response")
    ax.set_ylabel("Percentage of Total Cells")
    ax.set_xlabel("Immune Cell Type")
    ax.legend(title="Response")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    col1, col2 = st.columns([1, 1])
    with col1:
        st.pyplot(fig)

    # Statistical analysis using Mann-Whitney U test
    print("Statistical Comparison (Mann-Whitney U Test):")
    st.subheader("Mann-Whitney U Test Results between Responders and Non-Responders")
    populations = merged["population"].unique()
    significant_pops = []

    for pop in populations:
        group = merged[merged["population"] == pop]
        yes = group[group["response"] == "yes"]["percentage"]
        no = group[group["response"] == "no"]["percentage"]

        if len(yes) > 0 and len(no) > 0:
            stat, p = mannwhitneyu(yes, no, alternative="two-sided")
            print(f"{pop}: p = {p:.4f}")
            st.write(f"**{pop}**: p = {p:.4f}")
            if p < 0.05:
                significant_pops.append(pop)
        else:
            print(f"{pop}: Not enough data for statistical test")
            st.write(f"{pop}: Not enough data")

    # Print summary sentence
    st.subheader("Summary")
    if significant_pops:
        print(
            f"\n{', '.join(significant_pops)} "
            f"{'shows' if len(significant_pops) == 1 else 'show'} a statistically significant "
            "difference in relative frequency between responders and non-responders for the selected filters."
        )
        st.markdown(
            f"**{', '.join(significant_pops)}** "
            f"{'shows' if len(significant_pops) == 1 else 'show'} a statistically significant "
            "difference in relative frequency between responders and non-responders for the selected filters."
        )
    else:
        print("\nNo cell populations show a statistically significant difference in relative frequency for the selected filters.")
        st.write("No significant differences found.")



# Melanoma baseline subset analysis
def analyze_baseline_subset(db_path="database.db"):
    conn = sqlite3.connect(db_path)
    
    # Load sample metadata
    df = pd.read_sql_query("SELECT * FROM sample_metadata", conn)
    conn.close()

    # Filter for baseline melanoma PBMC samples treated with miraclib
    subset = df[
        (df["condition"] == "melanoma") &
        (df["sample_type"] == "PBMC") &
        (df["time_from_treatment_start"] == 0) &
        (df["treatment"] == "miraclib")
    ]

    print("\nFiltered subset shape:", subset.shape)
    
    # Samples per project
    samples_per_project = subset["project"].value_counts()
    print("Number of samples per project:")
    print(samples_per_project.to_string(index=True))

    # Subjects by response
    subjects_by_response = subset.groupby("response")["subject"].nunique()
    print("\nNumber of unique subjects by response:")
    print(subjects_by_response.to_string(index=True))

    # Subjects by sex
    subjects_by_sex = subset.groupby("sex")["subject"].nunique()
    print("\nNumber of unique subjects by sex:")
    print(subjects_by_sex.to_string(index=True))

    # Display in Streamlit
    st.subheader("Samples per Project")
    samples_per_project = subset["project"].value_counts()
    st.text(samples_per_project.to_string())

    st.subheader("Subjects by Response")
    subjects_by_response = subset.groupby("response")["subject"].nunique()
    st.text(subjects_by_response.to_string())

    st.subheader("Subjects by Sex")
    subjects_by_sex = subset.groupby("sex")["subject"].nunique()
    st.text(subjects_by_sex.to_string())



if __name__ == "__main__":
    summary = get_frequency_summary()
    compare_response_groups(summary)
    analyze_baseline_subset()