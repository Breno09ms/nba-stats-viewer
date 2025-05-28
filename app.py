from flask import Flask, request, jsonify
import io
import base64
from flask_cors import CORS
from estatisticas import media_pts_por_time, tov_por_time, ppg_per_season, ppg_grafico_season, win_seasons, grafico_contra_times, tov_grafico_contra_times

app = Flask(__name__)
CORS(app)  # permite requisições do frontend

@app.route("/")
def index():
    return "API da NBA está ativa!"

@app.route("/jogador", methods=["POST"])
def jogador():
    data = request.get_json()
    nome = data.get("nome")
    estatistica = data.get("estatistica")

    if not nome or not estatistica:
        return jsonify({"erro": "Nome ou estatística ausente"}), 400

    if estatistica == "media_ppg_ctime":
        media = media_pts_por_time(nome)
        if media is not None:
            return jsonify(media.to_dict())
        else:
            return jsonify({"erro": "Jogador não encontrado"}), 404

    elif estatistica == "media_tov_ctime":
        media = tov_por_time(nome)
        if media is not None:
            return jsonify(media.to_dict())
        else:
            return jsonify({"erro": "Jogador não encontrado"}), 404
    
    elif estatistica == "ppg_ptemporada":
         ppg_season = ppg_per_season(nome)
         if ppg_season is not None:
          return jsonify(ppg_season.to_dict()) 
         else:
            return jsonify({"erro": "Jogador não encontrado"})

    else:
        return jsonify({"erro": "Estatística não suportada"}), 400
    
@app.route("/grafico", methods=["POST"])
def grafico():
    data = request.get_json()
    nome = data.get("nome")
    tipo = data.get("tipo")
    opt = data.get("opt")

    if not nome or not tipo:
        return jsonify({"erro": "Nome ou opção ausente"}), 400

    try:
       if tipo == "jogador": 
        if opt == "ppg_grafico":
         imagem_base64 = ppg_grafico_season(nome)
         return jsonify({"imagem": imagem_base64})
        elif opt == "media_ppg_ctime":
         imagem_base64 = grafico_contra_times(nome)   
         return jsonify({"imagem": imagem_base64})
        elif opt == "media_tov_ctime":
         imagem_base64 = tov_grafico_contra_times(nome)
         return jsonify({"imagem": imagem_base64})
       elif tipo =="time":
        imagem_base64 = win_seasons(nome)
        return jsonify({"imagem": imagem_base64})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
   



if __name__ == "__main__":
    app.run(debug=True)
