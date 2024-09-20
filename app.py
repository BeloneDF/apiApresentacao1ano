import json
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Variável global para o estado do LED
led_status = False

# Lock para garantir segurança no acesso ao arquivo
lock = threading.Lock()

# Funções para salvar e carregar o estado do LED
def save_led_status(status):
    with lock:  # Garante que apenas uma thread está acessando o arquivo de cada vez
        with open('led_status.json', 'w') as f:
            json.dump({"status": status}, f)

def load_led_status():
    with lock:  # Garante leitura segura do arquivo
        try:
            with open('led_status.json', 'r') as f:
                data = json.load(f)
                return data["status"]
        except (FileNotFoundError, json.JSONDecodeError):
            return False  # Retorna False se o arquivo não existir ou for inválido

# Inicializa o estado do LED carregando do arquivo
led_status = load_led_status()

@app.route('/led', methods=['POST'])
def set_led_status():
    global led_status
    data = request.get_json()

    if 'status' in data:
        led_status = data['status']
        save_led_status(led_status)  # Salva o estado no arquivo
        return jsonify({"message": "Status do LED alterado", "status": led_status}), 200
    else:
        return jsonify({"error": "Formato inválido. Use {'status': true/false}"}), 400

@app.route('/led', methods=['GET'])
def get_led_status():
    global led_status
    # Carrega o estado do LED para garantir que o último estado salvo seja o atual
    led_status = load_led_status()
    return jsonify({"status": led_status}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
