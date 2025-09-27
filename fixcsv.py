import pandas as pd
import numpy as np

df = pd.read_csv("C:/Users/flora/Desktop/DiseaseRiskPrediction/diabetic_data.csv")

df.replace('?', pd.NA, inplace=True)
df.replace('', pd.NA, inplace=True)

# Map weight ranges to numeric averages
weight_map = {
    '[0-25)': 12.5,
    '[25-50)': 37.5,
    '[50-75)': 62.5,
    '[75-100)': 87.5,
    '[100-125)': 112.5,
    '[125-150)': 137.5,
    '[150-175)': 162.5,
    '[175-200)': 187.5,
    '[200-225)': 212.5,
    '[225-250)': 237.5,
    '[250-275)': 262.5,
    '[275-300)': 287.5,
    '[300-325)': 312.5,
    '[325-350)': 337.5,
    '[350-375)': 362.5,
    '[375-400)': 387.5,
}

df['weight'] = df['weight'].map(weight_map)

df.to_csv("C:/Users/flora/Desktop/DiseaseRiskPrediction/diabetic_data_clean.csv", index=False, na_rep='\\N')
