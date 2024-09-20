from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
led_status = False


@app.route('/led', methods=['POST'])
def set_led_status():
    global led_status
    data = request.get_json()

    if 'status' in data:
        led_status = data['status']
        return jsonify({"message": "Status do LED alterado", "status": led_status}), 200
    else:
        return jsonify({"error": "Formato inválido. Use {'status': true/false}"}), 400


@app.route('/led', methods=['GET'])
def get_led_status():
    return jsonify({"status": led_status}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
