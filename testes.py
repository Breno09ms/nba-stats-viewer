import pandas as pd
from estatisticas import ppg_per_season, ppg_grafico_season

nome = "Jaylen Brown"

dataframe = ppg_per_season(nome)

print(dataframe)

ppg_grafico_season(nome)

