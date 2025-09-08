import pandas as pd
from estatisticas import ppg_per_season, ppg_grafico_season, win_seasons, grafico_contra_times

nome = "Jaylen Brown"

time="Milwaukee Bucks"

dataframe = ppg_per_season(nome)
dataframet = win_seasons(time)

grafico_contra_times(nome)

