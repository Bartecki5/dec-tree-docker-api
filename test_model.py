import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from dec_tree import DecisionTree

# --- 1 --- FUNKCJE POMOCNICZE
def run_experiment(X, y, max_depth, experiment_name="Eksperyment"):
    print(f"\n{'='*40}")
    print(f"--- {experiment_name} ---")
    print(f"{'='*40}")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    clf = DecisionTree(max_depth=max_depth)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    
    print(f"Accuracy:  {accuracy_score(y_test, y_pred)*100:.2f}%")
    print(f"Precision: {precision_score(y_test, y_pred)*100:.2f}%")
    print(f"Recall:    {recall_score(y_test, y_pred)*100:.2f}%")
    print(f"F1 Score:  {f1_score(y_test, y_pred)*100:.2f}%")
    return clf

# --- 2 --- WCZYTANIE I PREPROCESSING
data = pd.read_csv("heart.csv")
data_one_hot = pd.get_dummies(data, columns=["Sex","ChestPainType","RestingECG","ExerciseAngina","ST_Slope"], drop_first=True, dtype=int)

X_baseline = data_one_hot.drop('HeartDisease', axis=1).to_numpy()
y_baseline = data_one_hot['HeartDisease'].to_numpy()

# Uruchamiamy pierwszy test!
run_experiment(X_baseline, y_baseline, max_depth=5, experiment_name="Model Bazowy (Bez Feature Eng.)")

# --- 3 --- FEATURE ENGINEERING
data['Angina_ST'] = ((data['ExerciseAngina'] == "Y") & (data["ST_Slope"] != "Up")).astype(int)
data["HR_ratio"] = data["MaxHR"] / (220 - data["Age"])
data["BP_Chol"] = data["RestingBP"] * data["Cholesterol"]
data["MetabolicRisk"] = data["FastingBS"] * data["Cholesterol"]

data_one_hot_fe = pd.get_dummies(data, columns=["Sex","ChestPainType","RestingECG","ExerciseAngina","ST_Slope"], drop_first=True, dtype=int)

X_fe = data_one_hot_fe.drop('HeartDisease', axis=1).to_numpy()
y_fe = data_one_hot_fe['HeartDisease'].to_numpy()

# Uruchamiamy drugi test!
run_experiment(X_fe, y_fe, max_depth=4, experiment_name="Model Ulepszony (Feature Eng.)")