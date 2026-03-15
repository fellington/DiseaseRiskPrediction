SHOW VARIABLES LIKE 'pid_file';

SELECT COUNT(*) FROM disease_db.disease_readmis;

SELECT * FROM disease_db.disease_readmis LIMIT 10;

SELECT DISTINCT readmitted FROM disease_db.disease_readmis;

SELECT gender, COUNT(*) AS count
FROM disease_db.disease_readmis
GROUP BY gender;

SELECT readmitted, AVG(time_in_hospital) AS avg_days
FROM disease_db.disease_readmis
GROUP BY readmitted;

SELECT readmitted, COUNT(*)
FROM disease_db.disease_readmis
GROUP BY readmitted;

SELECT patient_nbr,
       AVG(num_lab_procedures) AS avg_lab_tests,
       AVG(num_medications) AS avg_meds,
       MAX(time_in_hospital) AS max_stay,
       SUM(CASE WHEN REPLACE(readmitted, '\r', '') = '<30' THEN 1 ELSE 0 END) AS readmit_within_30,
       SUM(CASE WHEN REPLACE(readmitted, '\r', '') = '>30' THEN 1 ELSE 0 END) AS readmit_after_30,
       SUM(CASE WHEN REPLACE(readmitted, '\r', '') = 'NO' THEN 1 ELSE 0 END) AS never_readmitted
FROM disease_db.disease_readmis
GROUP BY patient_nbr;


SELECT * INTO OUTFILE 'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\diabetes_model_data.csv'
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'
FROM model_data;

