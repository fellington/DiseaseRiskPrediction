import streamlit as st
from pathlib import Path
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, precision_score, recall_score, accuracy_score, f1_score

st.set_page_config(page_title="Readmission Risk Dashboard", layout="wide", initial_sidebar_state="expanded")

TARGET_COLUMN = "readmit_30d"

TRAINING_FEATURES = [
    "time_in_hospital",
    "num_lab_procedures",
    "num_medications",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "age",
    "gender",
    "A1Cresult",
    "max_glu_serum",
    "insulin",
    "change",
    "diabetesMed"
]

DATA_PATH = Path("data/diabetes_clean.csv")

CATEGORICAL_FIELDS = [
    "age",
    "gender",
    "A1Cresult",
    "max_glu_serum",
    "insulin",
    "change",
    "diabetesMed",
]

CATEGORY_LEVELS = {
    "age": ["[0-10)", "[10-20)", "[20-30)", "[30-40)", "[40-50)",
            "[50-60)", "[60-70)", "[70-80)", "[80-90)", "[90-100)"],
    "gender": ["Female", "Male", "Unknown/Invalid"],
    "A1Cresult": [">7", ">8", "Norm"],
    "max_glu_serum": [">200", ">300", "Norm"],
    "insulin": ["Down", "No", "Steady", "Up"],
    "change": ["Ch", "No"],
    "diabetesMed": ["No", "Yes"],
}

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

def prepare_features(df):
    df = df.copy()

    for field, levels in CATEGORY_LEVELS.items():
        df[field] = pd.Categorical(df[field], categories=levels)

    df = pd.get_dummies(df, columns=CATEGORICAL_FIELDS, drop_first=True)

    df.columns = (
        df.columns
        .str.replace("[", "", regex=False)
        .str.replace("]", "", regex=False)
        .str.replace("<", "lt_", regex=False)
        .str.replace(">", "gt_", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace("-", "_", regex=False)
    )

    return df

def train_model(X, y):
    model = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.1,
        scale_pos_weight=8,
        eval_metric="logloss",
        random_state=42
    )
    model.fit(X, y)
    return model

@st.cache_resource
def build_model():
    X_raw = df[TRAINING_FEATURES]
    y = df[TARGET_COLUMN]

    X = prepare_features(X_raw)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = train_model(X_train, y_train)

    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = model.predict(X_test)

    metrics = {
        "ROC-AUC": roc_auc_score(y_test, y_proba),
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred, zero_division=0),
        "Recall": recall_score(y_test, y_pred, zero_division=0),
        "F1": f1_score(y_test, y_pred, zero_division=0),
    }

    return model, X.columns, y_test, y_proba, metrics

def predict_risk(model, patient_df):
    proba = model.predict_proba(patient_df)[:, 1]
    return proba[0]

df = load_data()
model, model_columns, y_test, y_proba, metrics = build_model()

st.title("Clinical Readmission Risk Dashboard")


page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Model Performance", "Threshold Explorer", 
     "Feature Importance", "Risk Simulator", "Limitations"]
)

st.sidebar.markdown("### About")
st.sidebar.caption(
    "This app rebuilds an XGBoost model, evaluates threshold tradeoffs, "
    "and simulates 30-day readmission risk from patient inputs."
)

if page == "Overview":
    st.markdown("## Overview")
    st.markdown("### This dashboard explores a machine learning model for predicting "
                "30-day hospital readmission risk using structured EHR data.")

    readmission_rate = df["readmit_30d"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", f"{len(df):,}")
    col2.metric("Readmission Rate", f"{readmission_rate:.1%}")
    col3.metric("ROC-AUC", f"{metrics['ROC-AUC']:.2f}")
    col4.metric("Recall", f"{metrics['Recall']:.1%}")

elif page == "Model Performance":
    st.markdown("## Model Performance")
    st.markdown("### The ROC curve shows how well the model distinguishes between patients "
                "who were readmitted within 30 days and those who were not.")

    roc_path = Path("images/roc_curve.png")

    if roc_path.exists():
        col1, col2 = st.columns([2, 1])

        with col1:
            st.image(str(roc_path), caption="ROC Curve", use_container_width=True)

        st.info("An AUC around 0.64 suggests moderate predictive performance. "
                "For this project, recall is especially important because the "
                "goal is to identify more high-risk patients.")
    else:
        st.warning("ROC curve image not found. Expected: images/roc_curve.png")

elif page == "Threshold Explorer":
    st.markdown("## Threshold Tradeoff")
    st.markdown("### The decision threshold controls how many patients are flagged "
                "as high risk. Lower thresholds identify more high-risk patients, "
                "but also increase false positives.")

    threshold_rows = []

    for t in [0.5, 0.4, 0.3]:
        y_pred_t = (y_proba > t).astype(int)

        threshold_rows.append({
            "Threshold": t,
            "Precision": precision_score(y_test, y_pred_t, zero_division=0),
            "Recall": recall_score(y_test, y_pred_t, zero_division=0),
            "F1": f1_score(y_test, y_pred_t, zero_division=0),
            "Alert Rate": y_pred_t.mean()
        })

    threshold_data = pd.DataFrame(threshold_rows)
    threshold_data = threshold_data.sort_values("Threshold", ascending=False)

    for col in ["Precision", "Recall", "F1", "Alert Rate"]:
        threshold_data[col] = threshold_data[col].map(lambda x: f"{x:.1%}")

    st.markdown("#### Model Performance at Different Thresholds")

    st.dataframe(threshold_data.style.set_properties(**{'font-size': '15px'}), use_container_width=True)

    st.info("Lower thresholds improve recall, meaning the model catches more " 
            "patients who may be readmitted. The tradeoff is that more patients "
            "may also be flagged incorrectly. In practice, the best threshold "
            "depends on whether missing high-risk patients or over-alerting is "
            "more costly.")

elif page == "Feature Importance":
    st.markdown("## Feature Importance")
    st.markdown("### Feature importance shows which variables contributed most to the model. "
                "Prior inpatient utilization and overall care intensity were the strongest signals.")

    fi_path = Path("images/feature_importance.png")

    if fi_path.exists():
        feature_importance = pd.DataFrame({
            "Feature": model_columns,
            "Importance": model.feature_importances_
        }).sort_values("Importance", ascending=False).head(10)

        feature_importance["Feature"] = feature_importance["Feature"].str.replace("_", " ").str.title()
        feature_importance["Importance"] = feature_importance["Importance"].map(lambda x: f"{x:.3f}")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.image(str(fi_path), caption="Top Feature Importances", use_container_width=True)

        with col2:
            st.markdown("#### Top Features")
            st.dataframe(feature_importance, use_container_width=True)

        st.info("Patients with more prior inpatient visits and higher clinical utilization tend "
                "to have higher predicted readmission risk. This lines up with expected clinical "
                "patterns around readmission.")

    else:
        st.warning("Feature importance image not found. Expected: images/feature_importance.png")

elif page == "Risk Simulator":
    st.markdown("## Patient Risk Simulator")
    st.markdown("### Adjust the patient profile below to see how the predicted readmission risk "
                "changes.")

    col1, col2 = st.columns(2)

    with col1:
        time_in_hospital = st.number_input("Time in hospital", 1, 14, 4)
        num_lab_procedures = st.number_input("Number of lab procedures", 1, 132, 44)
        num_medications = st.number_input("Number of medications", 1, 81, 15)
        number_outpatient = st.number_input("Outpatient visits", 0, 42, 0)
        number_emergency = st.number_input("Emergency visits", 0, 76, 0)
        number_inpatient = st.number_input("Inpatient visits", 0, 21, 1)

    with col2:
        age = st.selectbox("Age group", df["age"].dropna().unique())
        gender = st.selectbox("Gender", df["gender"].dropna().unique())
        a1c = st.selectbox("A1C result", df["A1Cresult"].dropna().unique())
        glucose = st.selectbox("Max glucose serum", df["max_glu_serum"].dropna().unique())
        insulin = st.selectbox("Insulin", df["insulin"].dropna().unique())
        change = st.selectbox("Medication change", df["change"].dropna().unique())
        diabetes_med = st.selectbox("Diabetes medication", df["diabetesMed"].dropna().unique())

    patient_df = pd.DataFrame([{
        "time_in_hospital": time_in_hospital,
        "num_lab_procedures": num_lab_procedures,
        "num_medications": num_medications,
        "number_outpatient": number_outpatient,
        "number_emergency": number_emergency,
        "number_inpatient": number_inpatient,
        "age": age,
        "gender": gender,
        "A1Cresult": a1c,
        "max_glu_serum": glucose,
        "insulin": insulin,
        "change": change,
        "diabetesMed": diabetes_med
    }])

    patient_encoded = prepare_features(patient_df)
    patient_encoded = patient_encoded.reindex(columns=model_columns, fill_value=0)

    risk = predict_risk(model, patient_encoded)

    st.markdown("---")

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        st.metric("Predicted 30-Day Readmission Risk", f"{risk:.1%}")

    if risk >= 0.5:
        category = "Very High"
        message = "This profile would be flagged using the default model threshold."
    elif risk >= 0.4:
        category = "High"
        message = "This profile would be flagged at a lower threshold that prioritizes identifying more high-risk patients."
    elif risk >= 0.3:
        category = "Moderate"
        message = "This profile is near the lower-threshold range explored in this project."
    else:
        category = "Low"
        message = "This profile is below the alert thresholds tested in this project."

    with result_col2:
        st.markdown(f"### Risk category: **{category}**")
        st.info(message)

    st.caption("This dashboard is for portfolio demonstration only and is not intended for clinical use.")

elif page == "Limitations":
    st.markdown("## Limitations")

    st.markdown(""" 
        - Moderate predictive performance
        - Uses structured data only
        - No temporal modeling of patient history
        - Not clinically validated
        - May reflect bias present in historical healthcare data
    """)

    st.info("A stronger version of this project would incorporate longitudinal patient history, "
            "additional clinical variables, and external validation on a separate dataset.")