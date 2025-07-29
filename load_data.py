import sqlite3
import pandas as pd

# Create the database schema for sample_metadata and cell_counts
def create_schema(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sample_metadata (
            sample_id TEXT PRIMARY KEY,
            project TEXT,
            subject TEXT,
            condition TEXT,
            age INTEGER,
            sex TEXT,
            treatment TEXT,
            response TEXT,
            sample_type TEXT,
            time_from_treatment_start INTEGER
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cell_counts (
            sample_id TEXT,
            cell_type TEXT,
            count INTEGER,
            FOREIGN KEY (sample_id) REFERENCES sample_metadata(sample_id)
        );
    """)
    conn.commit()

def load_csv_to_db(csv_path, db_path="database.db"):
    df = pd.read_csv(csv_path)

    # Create DB connection and schema
    conn = sqlite3.connect(db_path)
    create_schema(conn)

    # Insert sample_metadata
    df[
        ["sample", "project", "subject", "condition", "age", "sex",
         "treatment", "response", "sample_type", "time_from_treatment_start"]
    ].rename(columns={"sample": "sample_id"}).to_sql(
        "sample_metadata", conn, if_exists="replace", index=False
    )

    # Insert cell_counts
    df[["sample", "b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]]\
        .melt(id_vars="sample", var_name="cell_type", value_name="count")\
        .rename(columns={"sample": "sample_id"})\
        .to_sql("cell_counts", conn, if_exists="replace", index=False)

    conn.close()
    print("Data loaded successfully.")

if __name__ == "__main__":
    load_csv_to_db("cell-count.csv")