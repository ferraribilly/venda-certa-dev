import os
import uuid
import requests
import qrcode
import io
import base64
from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return send_from_directory("templates", "index.html")

@app.route("/pix", methods=["POST"])
def gerar_pix():
    data_in = request.get_json() or {}
    transaction_amount = float(data_in.get("transaction_amount", 1.00))
    description = data_in.get("description", "Item compra teste")
    payer_email = data_in.get("payer_email", "cliente@exemplo.com")

    payment_data = {
        "transaction_amount": transaction_amount,
        "description": description,
        "payment_method_id": "pix",
        "payer": {"email": payer_email}
    }

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Idempotency-Key": str(uuid.uuid4())
    }

    url = "https://api.mercadopago.com/v1/payments"
    response = requests.post(url, json=payment_data, headers=headers)

    if response.status_code in [200, 201]:
        data = response.json()
        qr_code_str = data["point_of_interaction"]["transaction_data"]["qr_code"]

        # gera imagem em memória (não salva no disco)
        img = qrcode.make(qr_code_str)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # converte pra base64 pra mandar pro navegador
        img_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        img_data_url = f"data:image/png;base64,{img_base64}"

        return jsonify({
            "message": "QR Code gerado com sucesso!",
            "qr_url": img_data_url
        }), 201
    else:
        return jsonify({
            "error": f"Erro ao criar QR Code: {response.status_code} - {response.text}"
        }), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
