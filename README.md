# Cell Immune Analysis

This project contains a Python program and interactive dashboard to support exploratory immune profiling from clinical trial data, specifically made for and auto-set to evaluating treatment responses to the drug candidate miraclib in melanoma PBMC samples.

The application was developed as a technical assessment and is designed to:
- Load immune cell count data into a relational database
- Perform summary statistics on immune cell population frequencies
- Compare immune cell frequencies of responders vs. non-responders
- Support querying of specific subgroups of interest
- Display results interactively through a Streamlit dashboard

Has functionality to filter and analyze across any group, but is preconfigured to display melanoma PBMC samples treated with miraclib, as requested.

---

## 🚀 Getting Started

✅ This project uses a `.devcontainer` with Python 3.10 and automatic dependency setup. When opened in GitHub Codespaces, everything should be pre-installed and ready to run.

### Requirements
This app is designed to run in **GitHub Codespaces** or any Python 3.10 environment (specified in .devcontainer).

1. Create a codespace with this repository:

https://github.com/codespaces

2. Install dependencies (if not done automatically):

```bash
pip install -r requirements.txt
```

3. Then, launch the dashboard:

```
streamlit run app.py
```

---

## 🧱 Database Schema
### The data from cell-count.csv is loaded into a SQLite database with the following schema:

This project uses a normalized SQLite database with the following schema:

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

The database schema and application architecture are designed to be normalized, extensible, and scalable for broader clinical and immunological analysis.

The schema separates metadata (`sample_metadata`) from measurements (`cell_counts`), eliminating redundancy and supporting flexible analytics. Foreign key constraints maintain integrity between tables. This design supports efficient operation even with:

- Hundreds of projects
- Thousands of samples
- Dozens of immune cell types
- Multiple treatment timepoints and conditions

The dashboard and backend logic are built to be dynamic and work for any dataset using the same .csv column structure. Filter options (condition, treatment, sample type, timepoint) are loaded directly from the database at runtime. This enables the dashboard to adapt seamlessly to any dataset conforming to the schema. No code changes are needed when introducing new disease types, treatments, or sample types.

The analysis module supports:
- Cell frequency computation for each sample and immune cell type
- Statistical comparisons between responder vs. non-responder groups using the Mann-Whitney U test
- Subset summaries of sample distributions across metadata fields

These operations are modular and easily extensible to additional analytics or more complex filtering logic.

The architecture is also designed for performance at scale:
- Indexing on frequently queried fields (`sample_id`, `cell_type`) would support fast filtering and aggregation
- Additional tables can be added to support longitudinal data or multi-modal inputs such as protein markers or imaging features

---

## 🧠 Code Structure

cell-immune-analysis/

├── .devcontainer/

│   └── devcontainer.json

├── app.py

├── analysis.py

├── load_data.py

├── cell-count.csv

├── requirements.txt

└── README.md

### Descriptions

- `.devcontainer` — Configuration for GitHub Codespaces with prebuilt Python 3.10 environment and automatic dependency installation
- `app.py` — Streamlit dashboard with interactive widgets and visualizations  
- `analysis.py` — Functions for summary statistics and statistical testing  
- `load_data.py` — Database schema creation and CSV loading logic  
- `cell-count.csv` — Raw immune profiling data  
- `requirements.txt` — Required Python packages  
- `README.md` — Project documentation (this file)

### Explanation

The project is structured to separate concerns across three key areas: data loading, analysis logic, and user interface. This modular architecture enhances readability, maintainability, and extensibility.

- **`load_data.py`** handles database schema creation and data loading. It ensures that the raw CSV file is consistently normalized into relational tables (`sample_metadata` and `cell_counts`), making the data ready for querying and analysis.
- **`analysis.py`** contains not only the core analytical functions (frequency calculations, statistical comparisons, and subset summaries) but also the code for rendering visual outputs (boxplots, textual summaries) that are displayed within the Streamlit app. This design allows new analyses and visualizations to be added directly to `analysis.py` without requiring changes to the main application file.
- **`app.py`** is responsible for the user interface and routing. It provides a clean navigation structure, leaves computational work to `analysis.py`, and dynamically populates all filter options from the database. This ensures the interface adapts automatically to any valid dataset that conforms to the schema.

By isolating data handling, computation, and interface logic, the project is easy to scale and extend. Analysts can introduce new views, filters, or statistical tests with minimal impact on the rest of the codebase.

---

## 📊 Dashboard Features
- Overview: Relative frequency (%) of each immune cell population across all samples.

- Response Group Comparison: Boxplot comparison and statistical analysis of cell type frequencies between responders and non-responders.

- Subset Summary: Filter samples based on condition, treatment, sample type, and timepoint to view counts by project, response, and gender.

Contains functionality to filter and analyze by any group, but it autoset to display the requested melanoma PBMC samples treated with miraclib.

## 📎 Submission Details

📁 GitHub Repository: https://github.com/landonw10/cell-immune-analysis

🔗 Dashboard URL: https://cell-immune-analysis.streamlit.app/
