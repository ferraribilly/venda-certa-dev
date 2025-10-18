import requests
import qrcode
import uuid  # Para gerar o X-Idempotency-Key

# Seu Access Token do Mercado Pago
ACCESS_TOKEN = "APP_USR-471764041611765-100917-1c88604eefcc1b34c44c540ab8981cbd-692553977" #Nicolas Ferreira Silva

# Dados do pagamento
payment_data = {
    "transaction_amount": 1.00,
    "description": "Item compra teste producao",
    "payment_method_id": "pix",
    "payer": {
        "email": "Nicolasfreitasferreira5@gmail.com"
    }
}

# Cabeçalhos da requisição, incluindo X-Idempotency-Key
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "X-Idempotency-Key": str(uuid.uuid4())  # gera uma chave única a cada requisição
}

# Endpoint oficial para criar pagamento
url = "https://api.mercadopago.com/v1/payments"

# Fazendo a requisição POST
response = requests.post(url, json=payment_data, headers=headers)

if response.status_code in [200, 201]:
    data = response.json()
    # Pegando o QR Code do Pix
    qr_url = data["point_of_interaction"]["transaction_data"]["qr_code"]

    # Gerando imagem do QR Code
    img = qrcode.make(qr_url)
    img.save("qr_code_pagamento.png")
    print("QR Code gerado com sucesso!")
    print("QR URL:", qr_url)

    # Salvando o Pix Copia e Cola em arquivo
    with open("pix.txt", "w") as f:
        f.write(qr_url)
    print("Pix Copia e Cola salvo em pix.txt ✅")
else:
    print(f"Erro ao criar QR Code: {response.status_code} - {response.text}")

