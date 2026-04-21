# Predicting 30-day Hospital Readmissions

## Overview

In this project, I built an end-to-end machine learning pipeline to predict whether a patient will be readmitted within 30-days using structured electronic health record (EHR) data. Since hospital readmissions are costly and often preventable, identifying high-risk patients can support targeted interventions and improve patient outcomes.

## Objectives

- Predict the 30-day readmission risk
- Handling class imbalance in clinical data
- Evaluate the models performances using appropriate metrics (e.g. ROC-AUC, precision, recall)
- Interpret the key drivers of readmission risk

## Dataset

- Source: [UCI Diabetes 130-US hospitals dataset](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)
- About 100,000 patient encounters included
- Features include:
  - Demographics (e.g. age, gender, race)
  - Clinical variables (e.g. A1C, glucose levels)
  - Medications (e.g. insulin, diabetes medications)
  - Healthcare utilization (e.g. inpatient, outpatient, emergency visits)

## Workflow

1) Data Processing
   - Cleaned the raw dataset (i.e. handled hidden formatting issues like \r)
   - Created binary target:
     - 1 = readmitted within 30 days
     - 0 = readmitted over 30 days or never readmitted
   - Addressed missing values and encoded categorical variables
2) Modeling
   - Baseline model: Logistic Regression
     - Reason:
   - Improved model: XGBoost
     - Reason:
   - Addressed the class imbalance using:
     - Class weighting
     - scale_pos_weight
3) Evaluation
   - Metrics used:
     - ROC-AUC
     - Precision/Recall
   - Threshold tuning to balance sensitivity vs specificity

## Results

| Model | ROC-AUC | Recall (30-day readmission) | Precision |
| ----- | ------- | --------------------------- | --------- |
| Logistic Regression | ~0.63 | ~0.45 | ~0.17 |
| XGBoost | ~0.64 | ~0.54 | ~0.17 |

### Threshold Tuning

| Threshold | Recall | Precision |
|----------|--------|----------|
| 0.5 | 0.54 | 0.17 |
| 0.4 | 0.85 | 0.13 |

Conclusion: The lower thresholds led to improved recall, but it also increased false positives, which highlights the tradeoff of using this approach in clinical applications.

### 📈 ROC Curve

![ROC Curve](images/roc_curve.png)

### 🔍 Feature Importance

![Feature Importance](images/feature_importance.png)

## Key Insights

- Prior inpatient visits are the strongest predictor of readmission risk
- Emergency visits and length of stay indicate the patient's instability
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

In practice, threshold selection can be adjusted depending on whether the priority is maximizing detection (recall) or minimizing false positives (precision).

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

Hi, I'm a PhD-trained computer engineer with experience in performing end-to-end data science projects for remote healthcare systems, and I am transitioning into applied data science. I'm interested in roles at the intersection of healthcare and machine learning. Please feel free to connect with me on LinkedIn for questions or to just network. :D
