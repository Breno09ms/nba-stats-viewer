import pandas as pd
from estatisticas import ppg_per_season, ppg_grafico_season

nome = "Jaylen Brown"

ppg_per_season(nome)

df = pd.read_csv("Jaylen_Brown_ppg_por_season.csv")
print(df)


