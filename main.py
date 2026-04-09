import os
import requests
from flask import Flask, request, jsonify

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
    try:
        data = request.get_json()
        
        # Verificar si existe el mensaje y si tiene texto
        if data and "message" in data:
            message = data["message"]
            
            # Verificar si el mensaje tiene texto
            if "text" in message:
                chat_id = message["chat"]["id"]
                texto = message["text"].lower().strip()
                
                if texto in pasillos:
                    respuesta = f"El producto \"{texto}\" está en el PASILLO {pasillos[texto]}"
                else:
                    respuesta = "No entiendo la pregunta. Productos: carne, queso, jamón, leche, yogurth, cereal, bebidas, jugos, pan, pasteles, tortas, detergente, lavaloza"
                
                requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": respuesta})
            else:
                # Mensaje sin texto (foto, sticker, etc.)
                pass
        
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "Bot funcionando", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
