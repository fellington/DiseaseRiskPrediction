-- Core SQL used to validate the dataset and prepare a clean encounter-level view
-- for downstream preprocessing and modeling.

-- Basic validation
SELECT COUNT(*) AS total_rows
FROM disease_db.disease_readmis;

SELECT COUNT(DISTINCT patient_nbr) AS unique_patients
FROM disease_db.disease_readmis;


-- Inspecting readmission labels and remove hidden carriage returns
SELECT DISTINCT REPLACE(readmitted, '\r', '') AS readmitted_clean
FROM disease_db.disease_readmis;


-- Confirming class distribution for the readmission outcome
SELECT
    REPLACE(readmitted, '\r', '') AS readmitted_clean,
    COUNT(*) AS encounter_count
FROM disease_db.disease_readmis
GROUP BY REPLACE(readmitted, '\r', '')
ORDER BY encounter_count DESC;


-- Creating a clean encounter-level view for use in Python
CREATE OR REPLACE VIEW cohort_extraction AS
SELECT
    encounter_id,
    patient_nbr,
    race,
    gender,
    age,
    weight,
    admission_type_id,
    discharge_disposition_id,
    admission_source_id,
    time_in_hospital,
    payer_code,
    medical_specialty,
    num_lab_procedures,
    num_procedures,
    num_medications,
    number_outpatient,
    number_emergency,
    number_inpatient,
    diag_1,
    diag_2,
    diag_3,
    number_diagnoses,
    max_glu_serum,
    A1Cresult,
    metformin,
    repaglinide,
    nateglinide,
    chlorpropamide,
    glimepiride,
    acetohexamide,
    glipizide,
    glyburide,
    tolbutamide,
    pioglitazone,
    rosiglitazone,
    acarbose,
    miglitol,
    troglitazone,
    tolazamide,
    examide,
    citoglipton,
    insulin,
    `glyburide-metformin`,
    `glipizide-metformin`,
    `glimepiride-pioglitazone`,
    `metformin-rosiglitazone`,
    `metformin-pioglitazone`,
    change,
    diabetesMed,
    REPLACE(readmitted, '\r', '') AS readmitted_clean
FROM disease_db.disease_readmis;


-- Previewing the clean view
SELECT *
FROM cohort_extraction
LIMIT 10;