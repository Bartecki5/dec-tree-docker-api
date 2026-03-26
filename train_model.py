### PAKOWANIE MODELU
import numpy as np
import pickle 
import pandas as pd
from dec_tree import DecisionTree
from sqlalchemy import create_engine

print("1. Rozpoczynam pracę w Laboratorium...")

#wczytanie danych

#df = pd.read_csv("heart.csv")

engine = create_engine('postgresql://admin:123@localhost:5432/szpital')
zapytanie_sql = 'SELECT * FROM pacjenci_trening'
df = pd.read_sql(zapytanie_sql, engine)

#future engineriing
print("2. Inżynieria cech...")
df['Angina_ST'] = ((df['ExerciseAngina'] == "Y") & (df["ST_Slope"] != "Up")).astype(int)
df["HR_ratio"] = df["MaxHR"] / (220 - df["Age"])
df["BP_Chol"] = df["RestingBP"] * df["Cholesterol"]
df["MetabolicRisk"] = df["FastingBS"] * df["Cholesterol"]

#one hot encoding
categorical_cols = ["Sex", "ChestPainType", "RestingECG", "ExerciseAngina", "ST_Slope"]
df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True, dtype=int)

X = df_encoded.drop('HeartDisease', axis=1).to_numpy()
y = df_encoded['HeartDisease'].to_numpy()

expected_columns = df_encoded.drop('HeartDisease', axis=1).columns

print("3. Trenowanie Drzewa Decyzyjnego...")
clf = DecisionTree(max_depth=4)
clf.fit(X, y)

#Pakietowanie (Serializacja)
print("4. Konserwowanie modelu do pliku .pkl...")
model_package  = {
    "model": clf,
    "columns": expected_columns
}

with open("heart_model.pkl", "wb") as file:
    #Funkcja pickle.dump() zrzuciła całą tę strukturę z pamięci RAM prosto do pliku na Twoim dysku.
    pickle.dump(model_package, file)

print("Gotowe! Model został zapakowany i zapisany jako 'heart_model.pkl")
