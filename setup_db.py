import pandas as pd
from sqlalchemy import create_engine 

df = pd.read_csv("heart.csv")

#tworzymy tunel
engine = create_engine("postgresql://admin:123@localhost:5432/szpital")

#zrzut do bazy o nazwie pacjenci... przez tunel engine jesli istnieje to usuwa starą i ładuje nową bez indeksowania
df.to_sql('pacjenci_trening', engine, if_exists='replace', index=False)
