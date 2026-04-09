import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}"

pasillos = {
    "carne": 1, "queso": 1, "jamon": 1, "jamón": 1,
    "leche": 2, "yogurth": 2, "yogurt": 2, "cereal": 2,
    "bebidas": 3, "bebida": 3, "jugos": 3, "jugo": 3,
    "pan": 4, "pasteles": 4, "pastel": 4, "tortas": 4, "torta": 4,
    "detergente": 5, "lavaloza": 5
}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        texto = data["message"]["text"].lower().strip()
        
        if texto in pasillos:
            respuesta = f"El producto \"{texto}\" está en el PASILLO {pasillos[texto]}"
        else:
            respuesta = "No entiendo la pregunta. Productos: carne, queso, jamón, leche, yogurth, cereal, bebidas, jugos, pan, pasteles, tortas, detergente, lavaloza"
        
        requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": respuesta})
    return "ok"

if __name__ == "__main__":
    app.run(port=5000)