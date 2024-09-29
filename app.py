from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

button_status = False  


def getButtonStatus():
    return button_status


def setButtonState(button):
    global button_status  
    button_status = button


@app.route('/button', methods=['GET', 'POST'])  
def led_control():  
    if request.method == "GET":
        try:
            return jsonify({"button_status": button_status})
        except Exception as error:  
            return jsonify({"error": str(error)})
    elif request.method == "POST":
        try:
            data = request.get_json()
            button = data['button_state']
            setButtonState(button)
            print(button_status)
            return jsonify({"message": "Estado do botão alterado com sucesso"})
        except Exception as error:
            return jsonify({"error": str(error)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
