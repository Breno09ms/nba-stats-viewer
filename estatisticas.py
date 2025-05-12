import numpy as np
import pandas as pd
import matplotlib.pyplot as mp
import nba_api as nba
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import playercareerstats


#Função pegar média de pontos contra cada time
def media_pts_por_time(nome_jogador, temporada="2023-24", salvar_csv=False):
    # 1. Buscar jogador pelo nome
    jogador = nba.stats.static.players.find_players_by_full_name(nome_jogador)
    if not jogador:
        print("Jogador não encontrado.")
        return
    player_id = jogador[0]["id"]

    # 2. Obter game logs
    gamelog = nba.stats.endpoints.playergamelog.PlayerGameLog(player_id=player_id, season=temporada, season_type_all_star="Regular Season")
    df = gamelog.get_data_frames()[0]

    # 3. Extrair adversário da coluna MATCHUP
    df["OPPONENT"] = df["MATCHUP"].apply(lambda x: x.split()[-1])

    # 4. Calcular média de pontos por adversário
    media_por_time = df.groupby("OPPONENT")["PTS"].mean().sort_values(ascending=False)

    # 5. Salvar em CSV (opcional)
    if salvar_csv:
        media_por_time.to_csv(f"{nome_jogador.replace(' ', '_')}_media_pts_por_time.csv")

    return media_por_time

#Função grafico média de pontos contra cada time
def grafico_contra_times(nome_atleta):
    media_por_time = media_pts_por_time(nome_atleta)

    if media_por_time is not None:
      dataf = media_por_time.reset_index()
      dataf.sort_values("OPPONENT", inplace=True)
      mp.bar(dataf["OPPONENT"],dataf["PTS"])
      mp.xlabel("teste x")
      mp.ylabel("teste y")
      mp.title("Teste Título")
      mp.tight_layout()
      mp.show()



#Função pegar média de Turnovers contra cada time
def tov_por_time(nome_jogador, temporada="2023-24", salvar_csv=False):
    # 1. Buscar jogador pelo nome
    jogador = nba.stats.static.players.find_players_by_full_name(nome_jogador)
    if not jogador:
        print("Jogador não encontrado.")
        return
    player_id = jogador[0]["id"]

    # 2. Obter game logs
    gamelog = nba.stats.endpoints.playergamelog.PlayerGameLog(player_id=player_id, season=temporada, season_type_all_star="Regular Season")
    df = gamelog.get_data_frames()[0]

    # 3. Extrair adversário da coluna MATCHUP
    df["OPPONENT"] = df["MATCHUP"].apply(lambda x: x.split()[-1])

    # 4. Calcular média de pontos por adversário
    tovmedia_por_time = df.groupby("OPPONENT")["TOV"].mean().sort_values(ascending=False)

    # 5. Salvar em CSV 
    if salvar_csv:
        tovmedia_por_time.to_csv(f"{nome_jogador.replace(' ', '_')}_tov_pts_por_time.csv")

    return tovmedia_por_time
#Função grafico média de Turnovers contra cada time
def tov_grafico_contra_times(nome_atleta):
    tovmedia_por_time = tov_por_time(nome_atleta)

    if tovmedia_por_time is not None:
       dataf = tovmedia_por_time.reset_index()      
       dataf.sort_values("OPPONENT", inplace=True)
       mp.bar(dataf["OPPONENT"],dataf["TOV"])
       mp.xlabel("teste x")
       mp.ylabel("teste y")
       mp.title("Teste Título")
       mp.tight_layout()
       mp.show()


 #Função pegar PPG por temporada
def ppg_per_season(nome_jogador,salvar_csv=True):
    jogador = nba.stats.static.players.find_players_by_full_name(nome_jogador)
    if not jogador:
        print("Jogador não encontrado")
        return
    player_id = jogador[0]["id"]

    carreira = playercareerstats.PlayerCareerStats(player_id=player_id)
    df = carreira.get_data_frames()[0]

    # 3. Filtrar só temporadas da temporada regular
    df_regular = df[df["LEAGUE_ID"] == "00"]  # "00" = NBA
    df_regular = df_regular[df_regular["SEASON_ID"].str.contains("-")]

    # 4. Pegar apenas temporada e PPG (PTS/GP)
    df_regular["PPG"] = df_regular["PTS"] / df_regular["GP"]
    resultado = df_regular[["SEASON_ID", "PPG"]].sort_values("SEASON_ID")

    #Salvar CSV
    if salvar_csv:
        resultado.to_csv(f"{nome_jogador.replace(' ', '_')}_ppg_por_season.csv", index = False)

    return resultado.reset_index(drop=True)

# Função gráfico PPG por temporada
def ppg_grafico_season(nome_atleta, salvar_csv=False):
    nome_atleta_csv = nome_atleta.replace(" ", "_")
    dataf = pd.read_csv(f"{nome_atleta_csv}_ppg_por_season.csv")

    # Ordenar cronologicamente pelas temporadas
    dataf["ANO_INICIAL"] = dataf["SEASON_ID"].apply(lambda x: int(x[:4]))
    dataf = dataf.sort_values("ANO_INICIAL")

    # Plot
    mp.plot(dataf["SEASON_ID"], dataf["PPG"], marker="o", linestyle="-", color="blue")
    mp.xlabel("Temporada")
    mp.ylabel("PPG")
    mp.title(f"PPG por temporada - {nome_atleta}")
    mp.xticks(rotation=45)
    mp.grid(True)
    mp.tight_layout()
    mp.show()

