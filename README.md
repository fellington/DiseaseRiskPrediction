# Predicting 30-day Hospital Readmissions

## TL;DR (Quick Summary)

Developed an end-to-end machine learning pipeline to predict 30-day hospital readmissions using structured EHR data.  
Using a gradient boosting model (XGBoost) improved detection of high-risk patients (recall ~0.54, AUC ~0.64) compared to a logistic regression baseline.  
Results highlight the importance of prior healthcare utilization and disease severity in predicting readmission risk.

## Overview

In this project, I developed an end-to-end machine learning pipeline to predict 30-day hospital readmissions using structured electronic health record (EHR) data. Since hospital readmissions are costly and often preventable, identifying high-risk patients can support targeted interventions and improve patient outcomes.

## Objectives

- Predict 30-day readmission risk
- Handle class imbalance in clinical data
- Evaluate model performance using appropriate metrics (ROC-AUC, precision, recall)
- Interpret key drivers of readmission risk

## Quick Project Links

- [EDA & Preprocessing Notebook](notebooks/01_eda_and_preprocessing.ipynb)
- [Modeling Notebook](notebooks/02_modeling.ipynb)
- [SQL Script](sql/cohort_extraction.sql)

## Dataset

- Source: [UCI Diabetes 130-US hospitals dataset](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)
- About 100,000 patient encounters included
- Features include:
  - Demographics (e.g. age, gender, race)
  - Clinical variables (e.g. A1C, glucose levels)
  - Medications (e.g. insulin, diabetes medications)
  - Healthcare utilization (e.g. inpatient, outpatient, emergency visits)

## Workflow

### 1. Data Processing

- Cleaned the raw dataset (i.e. handled hidden formatting issues like \r)
- Created binary target:
  - 1 = readmitted within 30 days
  - 0 = readmitted over 30 days or never readmitted
- Addressed missing values and encoded categorical variables

### 2. Modeling

- **Baseline model: Logistic Regression**  
  - Reason: Provides a simple, interpretable baseline for binary classification and is commonly used in clinical settings. However, its performance is limited when relationships between variables are nonlinear, like in this dataset.
- **Improved model: XGBoost**  
  - Reason: Selected for its strong performance on tabular data, capturing nonlinear relationships and feature interactions. It improves predictive performance over the baseline, particularly in identifying high-risk patients.
- Addressed the class imbalance using:
  - Class weighting
  - scale_pos_weight

### 3. Evaluation

- Metrics used:
  - ROC-AUC
  - Precision/Recall
- Threshold tuning to balance sensitivity vs specificity

## Results

The XGBoost model achieved modest improvements over the baseline, particularly in recall, indicating better detection of high-risk patients.

| Model | ROC-AUC | Recall (30-day readmission) | Precision |
| ----- | ------- | --------------------------- | --------- |
| Logistic Regression | ~0.63 | ~0.45 | ~0.17 |
| XGBoost | ~0.64 | ~0.54 | ~0.17 |

### Threshold Tuning

| Threshold | Recall | Precision |
| --------- | ------ | --------- |
| 0.5 | 0.54 | 0.17 |
| 0.4 | 0.85 | 0.13 |

Conclusion: Lower thresholds improve recall but increase false positives, highlighting the tradeoff in clinical applications.

### ROC Curve

![ROC Curve](images/roc_curve.png)

*Figure 1: ROC curve showing model discrimination performance.*

### Feature Importance

![Feature Importance](images/feature_importance.png)

*Figure 2: Top 10 features influencing readmission risk.*

## Key Insights

- Prior inpatient visits are the strongest predictor of readmission risk
- Emergency visits and length of stay indicate patient instability and higher healthcare utilization
- A1C levels and diabetes medications reflect the disease severity
- Age shows a nonlinear effect on risk

Overall, the readmission risk is driven by a combination of:

- Healthcare utilization
- Disease severity
- Patient characteristics

## Clinical Relevance

This model could be used to:

- Identify high-risk patients at discharge
- Trigger follow-up interventions
- Support hospital resource allocation

In practice, threshold selection can be adjusted depending on whether the priority is **maximizing detection (recall)** or **minimizing false positives (precision)**.

## Limitations

- Moderate predictive performance (AUC ~0.64)
- Only structured data used (no clinical notes included)
- No temporal modeling of patient history

## Future Work

- Incorporate time-series/longitudinal modeling
- Use unstructured clinical text (NLP)
- Deploy as an interactive dashboard (e.g. Streamlit)

## Tech Stack

- Python (Pandas, NumPy)
- Scikit-learn
- XGBoost
- SQL (MySQL)
- Matplotlib/Seaborn

## Project Structure

```
project/
├── data/
│   └── diabetes_clean.csv
├── notebooks/
│   ├── 01_eda_and_preprocessing.ipynb
│   └── 02_modeling.ipynb
├── sql/
│   └── cohort_extraction.sql
├── images/
│   ├── roc_curve.png
│   └── feature_importance.png
├── README.md
```

## About Me

PhD-trained computer engineer with experience in healthcare systems and applied data science. This project reflects my transition into industry-focused machine learning, with a focus on healthcare applications.

I am currently seeking data science roles at the intersection of healthcare and machine learning. Feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/floranne-ellington/).
