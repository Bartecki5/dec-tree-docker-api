import pickle 
import pandas as pd
import numpy as np
import os
from fastapi import FastAPI
from pydantic import BaseModel 
from dec_tree import DecisionTree
from fastapi.middleware.cors import CORSMiddleware


if not os.path.exists("heart_model.pkl"):
    raise FileNotFoundError("BŁĄD: Nie znaleziono pliku 'heart_model.pkl'! Czy na pewno uruchomiłeś najpierw 'python train_model.py'?")

with open("heart_model.pkl", "rb") as file:
    model_package = pickle.load(file)
    model = model_package["model"]
    expected_columns = model_package["columns"]


app = FastAPI(
    title="Kardologiczne API",
    description="Api do przywidywania chorób serca"
)

# --- ODBLOKOWANIE RUCHU Z PRZEGLĄDARKI (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Zezwala na połączenia skądkolwiek
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatientData(BaseModel):
    Age: int
    Sex: str
    ChestPainType: str
    RestingBP: int
    Cholesterol: int
    FastingBS: int
    RestingECG: str
    MaxHR: int
    ExerciseAngina: str
    Oldpeak: float
    ST_Slope: str



@app.post("/predict")
def predict_heart_disease(patient: PatientData):

    df = pd.DataFrame([patient.model_dump()])
    df['Angina_ST'] = ((df['ExerciseAngina'] == "Y") & (df["ST_Slope"] != "Up")).astype(int)
    df["HR_ratio"] = df["MaxHR"] / (220 - df["Age"])
    df["BP_Chol"] = df["RestingBP"] * df["Cholesterol"]
    df["MetabolicRisk"] = df["FastingBS"] * df["Cholesterol"]

    df_encoded = pd.get_dummies(df, dtype=int)
    df_encoded = df_encoded.reindex(columns=expected_columns, fill_value=0)

    X=df_encoded.to_numpy()

    prediction = model.predict(X)
    result = int(prediction[0])

    return {
        "Status" : "Sukces",
        "Diagnoza" : result,
        "Komunikat" : "Wykryto wysokie ryzyko (1)" if result ==1 else "Brak wysokiego ryzyka (0)",
        "Wersja_Modelu" : "v1.0 - DecTree CART"
    }
