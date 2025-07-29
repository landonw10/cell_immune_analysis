import sqlite3
import pandas as pd

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