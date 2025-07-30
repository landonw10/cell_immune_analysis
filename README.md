# Cell Immune Analysis

This project contains a Python program and interactive dashboard to support exploratory immune profiling from clinical trial data, specifically autoset to and made for evaluating treatment responses to the drug candidate miraclib in melanoma patients with PBMC samples.

The application was developed as a technical assessment and is designed to:
- Load immune cell count data into a relational database
- Perform summary statistics on immune cell population frequencies
- Compare immune cell frequencies of responders vs. non-responders
- Support querying of specific subgroups of interest
- Display results interactively through a Streamlit dashboard

It has functionality to filter and analyze by any group, but it autoset to display melanoma PBMC samples treated with miraclib.

---

## 🚀 Getting Started

### Requirements
This app is designed to run in **GitHub Codespaces** or any Python 3.10 environment (specified in .devcontainer).

1. Create a codespace with this repository:

https://github.com/codespaces

2. Install dependencies:

```bash
pip install -r requirements.txt
```
3. Then, launch the dashboard:

```
streamtlit run app.py
```

---

## 🧱 Database Schema
### The data from cell-count.csv is loaded into a SQLite database with the following schema:

### Rationale and Scaling

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

- **app.py** — Streamlit dashboard with interactive widgets and visualizations  
- **analysis.py** — Functions for summary statistics and statistical testing  
- **load_data.py** — Database schema creation and CSV loading logic  
- **cell-count.csv** — Raw immune profiling data  
- **requirements.txt** — Required Python packages  
- **README.md** — Project documentation (this file)

### Explanation


---

## 📊 Dashboard Features
- Frequency Table: Relative frequency (%) of each immune cell population across all samples.

- Responder Analysis: Boxplot comparison and statistical analysis of cell type frequencies between responders and non-responders.

- Subset Querying: Filter samples based on condition, treatment, sample type, and timepoint to view counts by project, response, and gender.

Contains functionality to filter and analyze by any group, but it autoset to display the requested melanoma PBMC samples treated with miraclib.

## 📎 Submission Details

📁 GitHub Repository: https://github.com/landonw10/cell-immune-analysis

🔗 Dashboard URL: https://cell-immune-analysis.streamlit.app/


