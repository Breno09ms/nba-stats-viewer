import pandas as pd
from estatisticas import ppg_per_season, ppg_grafico_season, win_seasons

nome = "Jaylen Brown"

time="Milwaukee Bucks"

dataframe = ppg_per_season(nome)
dataframet = win_seasons(time)

print(dataframet)

