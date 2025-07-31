# Cell Immune Analysis

This project contains a Python program and interactive dashboard to explore and analyze clinical trial data contained in a CSV file.

The application is designed to:
- Load immune cell count data into a relational database
- Perform summary statistics on immune cell population frequencies
- Compare immune cell frequencies of responders vs. non-responders
- Support querying summaries of specific subgroups of interest
- Display results interactively through a Streamlit dashboard

Has functionality to filter and analyze across any group, but is preconfigured to display melanoma PBMC samples treated with miraclib, as requested.

---

## Instructions

The project uses a `.devcontainer` with Python 3.10 and automatic dependency setup. When opened in GitHub Codespaces, everything should be pre-installed and ready to run.

### Steps

1. Create a codespace with this repository:

https://github.com/codespaces

2. Wait for automatic setup (Python 3.10 and dependencies) or manually install if necessary:

```bash
pip install -r requirements.txt
```

3. Then, launch the dashboard:

```
streamlit run app.py
```

---

## Database Schema
### The data from cell-count.csv is loaded into a SQLite database with the following schema:

#### **`sample_metadata`**

| Column                    | Type     | Description                                           |
|---------------------------|----------|-------------------------------------------------------|
| `sample_id`               | TEXT     | Unique sample identifier (primary key)                |
| `project`                 | TEXT     | Project or study name                                 |
| `subject`                 | TEXT     | Patient/subject identifier                            |
| `condition`               | TEXT     | Disease condition (melanoma, carcinoma, healthy)      |
| `age`                     | INTEGER  | Subject age                                           |
| `sex`                     | TEXT     | Subject sex                                           |
| `treatment`               | TEXT     | Treatment administered (miraclib, phauximab)          |
| `response`                | TEXT     | Treatment response (yes/no)                           |
| `sample_type`             | TEXT     | Sample type (PBMC, WB)                                |
| `time_from_treatment_start` | INTEGER | Time relative to treatment start (in days)           |

#### **`cell_counts`**

| Column      | Type    | Description                                |
|-------------|---------|--------------------------------------------|
| `sample_id` | TEXT    | Foreign key referencing `sample_metadata`  |
| `cell_type` | TEXT    | Immune cell type (e.g. cd8_t_cell)         |
| `count`     | INTEGER | Number of cells of that type               |

### Rationale and Scalability

The database schema and application code logic are designed to be normalized, easily extensible, and scalable for broader clinical and immunological analysis.

The schema separates metadata (`sample_metadata`) from measurements (`cell_counts`), eliminating redundancy and supporting flexible analytics. Foreign key constraints maintain integrity between tables. This design supports efficient operation even with across larger projects with bigger sample size and more cell types, treatments, conditions, and timepoints.

The dashboard and backend logic are built to be dynamic and work for any dataset using the same .csv column structure. Filter options (condition, treatment, sample type, timepoint) are loaded directly from the database at runtime. This enables the dashboard to adapt to any dataset conforming to the schema. No code changes are needed when introducing new disease types, treatments, or sample types.

The analysis module supports:
- Cell frequency computation for each sample and immune cell type
- Statistical comparisons between responder vs. non-responder groups using the Mann-Whitney U test
- Subset summaries of sample distributions across metadata fields

These operations are modular and easily extensible to additional analytics or more complex filtering logic.

---

## Code Structure

cell-immune-analysis/

├── .devcontainer/

│   └── devcontainer.json

├── app.py

├── analysis.py

├── load_data.py

├── cell-count.csv

├── requirements.txt

└── README.md<br><br>

### Descriptions and Contained Functions

`.devcontainer` — Configuration for GitHub Codespaces with prebuilt Python 3.10 environment and automatic dependency installation.<br><br>
  
`app.py` — Streamlit dashboard that displays analyses and summaries. Utilizes functions from `analysis.py` and `load_data.py`.<br><br>
  
`analysis.py` — Functions for summary statistics, statistical testing, and display logic. Contains:

- `get_frequency_summary(db_path="database.db")` — Computes cell-type frequencies for each sample
  
- `display_frequency_summary(filtered_df)` — Displays the filtered summary table in Streamlit

- `compare_response_groups(summary_df, filters, db_path="database.db")` — Compares filtered cell frequencies between responders and non-responders

- `analyze_subset(filters, db_path="database.db")` — Summarizes population distribution of filtered subset<br><br>

`load_data.py` — Database schema creation and CSV loading logic. Contains:

- `create_schema(conn)` — Initializes the database schema with sample_metadata and cell_counts tables

- `load_csv_to_db(csv_path, db_path="database.db")` — Loads data from a CSV into the SQLite database<br><br>

`cell-count.csv` — Raw immune profiling data.<br><br>

`requirements.txt` — Required Python packages.  <br><br>

`README.md` — Project documentation (this file).

### Explanation

The project is structured to separate logic across three key areas: data loading, analysis and display logic, and user interface. This helps with readability, maintainability, and extensibility.

- `load_data.py` handles database schema creation and data loading. It normalized CSV files into relational tables (`sample_metadata` and `cell_counts`), making the data ready for querying and analysis.
- `analysis.py` contains core analytical functions (frequency calculations, statistical comparisons, and subset summaries) and also the code for rendering visual outputs (boxplots, textual summaries) that are displayed within the Streamlit app. This allows new analyses and visualizations to be added directly to this file without requiring changes to `app.py`.
- `app.py` is responsible for the user interface and routing. It provides navigation, leaves computational work to `analysis.py`, and dynamically populates all filter options from the database. This ensures the interface adapts automatically to any valid dataset that conforms to the schema.

By isolating data handling, computation, and interface logic, the project is easy to scale and extend. New views, filters, or statistical tests can be added with minimal impact on the rest of the codebase.

---

## Dashboard Features
- Overview: Relative frequency (%) of each immune cell population across all samples.

- Response Group Comparison: Boxplot comparison and statistical analysis of cell type frequencies between responders and non-responders.

- Subset Summary: Filter samples based on condition, treatment, sample type, and timepoint to view counts by project, response, and gender.

Contains functionality to filter and analyze by any group, but is preconfigured to display the requested melanoma PBMC samples treated with miraclib.

Dashboard URL: https://cell-immune-analysis.streamlit.app/
