# Learner Demographics and Course Enrollment Behavior Analysis on EduPro

An advanced data analytics, learner intelligence, and interactive Streamlit web dashboard for the **EduPro** online learning platform.

---

## 🌟 Project Overview

Online learning platforms serve diverse learners with varying age groups, gender distributions, and learning goals. This project focuses on **descriptive learner intelligence**, enabling EduPro to transition from intuition-driven decision-making to data-driven educational planning, targeted marketing, and enhanced inclusivity.

### Key Highlights
* **High-Dimensional Dataset Analysis**: Processes **10,000 transactions** across **3,000 registered learners** and **60 courses** with **100% referential integrity**.
* **Rich Aesthetic UI**: Built with Streamlit and custom CSS glassmorphism, vibrant HSL Plotly visualizations, custom typography (`Outfit` / `Inter`), and responsive KPI metric cards.
* **Demographic & Inclusivity Benchmarking**: Confirms an extraordinary **1:1 gender parity** (50.8% Female vs. 49.2% Male) and identifies young adult professionals (18–35) as the primary growth driver (85.5% of enrollments).
* **Interactive Filtering**: Real-time multi-dimensional filtering across Age Groups, Gender, Course Categories, Course Levels, and Pricing Types.
* **Integrated Executive Deliverables**: Built-in document viewer and one-click downloaders for the full academic **Research Paper** and **Government Policy Brief**.

---

## 📁 Project Architecture & Files

```text
c:\Users\skmah\Code_Playground\Nirjana\
│
├── EduPro Online Platform (1).xlsx    # High-dimensional Excel dataset (Users, Courses, Transactions)
├── app.py                             # Main Streamlit interactive dashboard application
├── data_loader.py                     # Data ingestion, referential integrity joining, and KPI engine
├── requirements.txt                   # Pinned Python package dependencies
├── README.md                          # Project documentation
├── RESEARCH_PAPER.md                  # Complete academic research paper & EDA report
├── EXECUTIVE_SUMMARY.md               # Policy brief & summary for government stakeholders
│
├── utils/
│   └── styling.py                     # Custom CSS, dark-mode glassmorphism, & Plotly chart themes
│
└── .streamlit/
    └── config.toml                    # Streamlit server and dark theme configurations
```

---

## 🚀 Quickstart & Installation

### 1. Set Up Virtual Environment
On Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```
*(Requires `streamlit`, `pandas`, `openpyxl`, `plotly`, and `numpy`)*

### 3. Launch the Streamlit Dashboard
```powershell
streamlit run app.py
```
Open your browser to `http://localhost:8501` to view the live interactive dashboard!

---

## 📑 Core Dashboard Modules (Tabs)

1. **📊 Executive Overview & KPIs**: Displays high-level platform health, engagement scale, demographic reach, and key strategic briefings.
2. **👥 Learner Demographics**: Interactive age-wise distribution charts, gender participation ratios, and granular learner age profiling.
3. **📈 Course Demand & Popularity**: Horizontal bar rankings of the Category Popularity Index, free vs. paid breakdowns, and level distributions.
4. **🔥 Demographics × Preferences**: Multi-dimensional heatmaps mapping Age Bands against Course Categories and gender vs. skill level demand.
5. **🧠 Behavioral & Concentration**: Learner engagement tiers (Casual vs. Active vs. Power learners) and cumulative Pareto enrollment concentration curves.
6. **📑 Reports & Deliverables**: Interactive document reader with one-click download buttons for `RESEARCH_PAPER.md`, `EXECUTIVE_SUMMARY.md`, and filtered CSV analytics datasets.

---

## 🏆 Key Performance Indicators (KPIs) Computed

* **Scale Total Enrollments**: Overall platform engagement and activity scale.
* **Enrollments by Age Group**: Demographic reach and generational participation.
* **Gender Participation Ratio**: Inclusivity metric evaluating gender balance across tech domains.
* **Category Popularity Index**: Relative demand index across 12 high-tech and business disciplines.
* **Level Preference Distribution**: Skill maturity distribution across Beginner, Intermediate, and Advanced tiers.

---
*Developed for EduPro Analytics & Strategic Education Planning.*
