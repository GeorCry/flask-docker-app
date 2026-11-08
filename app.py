from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
import time

app = Flask(__name__)

# Берем адрес базы данных из переменных окружения (которые зададим в Compose)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Описываем модель данных (таблицу в БД)
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

# Ждем пару секунд, пока база данных запустится (частая проблема в Docker)
with app.app_context():
    for _ in range(10):
        try:
            db.create_all()
            break
        except Exception as e:
            print("Ждем базу данных...")
            time.sleep(2)

# Эндпоинт для получения всех записей
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{"id": i.id, "name": i.name} for i in items])

# Эндпоинт для добавления новой записи
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    new_item = Item(name=data.get('name', 'Без имени'))
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"id": new_item.id, "name": new_item.name}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)