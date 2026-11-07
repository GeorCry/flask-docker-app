from flask import Flask, jsonify

app = Flask(__name__)

# Наш эндпоинт, который мы будем дергать
@app.route('/items', methods=['GET'])
def get_items():
    items = [
        {"id": 1, "name": "test"},
        {"id": 2, "name": "docker is working"}
    ]
    return jsonify(items)

if __name__ == '__main__':
    # Обязательно host='0.0.0.0', чтобы Docker мог достучаться до приложения
    app.run(host='0.0.0.0', port=5000, debug=True)