from flask import Flask, request, jsonify
from flask_cors import CORS
from estatisticas import media_pts_por_time, tov_por_time, ppg_per_season, ppg_grafico_season

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

if __name__ == "__main__":
    app.run(debug=True)
