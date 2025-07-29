import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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
def compare_response_groups(summary_df, db_path="database.db"):
    # Load sample metadata
    conn = sqlite3.connect(db_path)
    metadata = pd.read_sql_query("SELECT sample_id, condition, treatment, sample_type, response FROM sample_metadata", conn)
    conn.close()

    # Merge summary with metadata (summary_df uses sample, metadata uses sample_id)
    merged = summary_df.merge(metadata, left_on="sample", right_on="sample_id")

    # Filter for melanoma + miraclib + PBMC
    filtered = merged[
        (merged["condition"] == "melanoma") &
        (merged["treatment"] == "miraclib") &
        (merged["sample_type"] == "PBMC")
    ]

    # Display data w/ boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(
        data=filtered,
        x="population",
        y="percentage",
        hue="response"
    )
    plt.title("Immune Cell Frequencies by Treatment Response")
    plt.ylabel("Percentage of Total Cells")
    plt.xlabel("Immune Cell Type")
    plt.legend(title="Response")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



    # Statistical analysis using Mann-Whitney U test
    print("Statistical Comparison (Mann-Whitney U Test):")
    populations = filtered["population"].unique()

    significant_pops = []

    for pop in populations:
        group = filtered[filtered["population"] == pop]
        yes = group[group["response"] == "yes"]["percentage"]
        no = group[group["response"] == "no"]["percentage"]

        if len(yes) > 0 and len(no) > 0:
            stat, p = mannwhitneyu(yes, no, alternative="two-sided")
            print(f"{pop}: p = {p:.4f}")
            if p < 0.05:
                significant_pops.append(pop)
        else:
            print(f"{pop}: Not enough data for statistical test")

    # Print summary sentence
    if significant_pops:
        print(
            f"\n{', '.join(significant_pops)} "
            f"{'shows' if len(significant_pops) == 1 else 'show'} a statistically significant "
            "difference in relative frequency between responders and non-responders."
        )
    else:
        print("\nNo cell populations show a statistically significant difference in relative frequency.")



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



if __name__ == "__main__":
    summary = get_frequency_summary()
    compare_response_groups(summary)
    analyze_baseline_subset()