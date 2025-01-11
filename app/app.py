from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pika
import redis
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de RabbitMQ
rabbitmq_host = 'rabbitmq'
rabbitmq_queue = 'test_queue'

# Configuración de PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@postgres:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Configuración de Redis
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

# Modelo de la base de datos
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

# Esperar a que los servicios estén listos
time.sleep(10)

# Conectar a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()
channel.queue_declare(queue=rabbitmq_queue)

@app.route('/send', methods=['POST'])
def send_message():
    message = request.json.get('message')
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=message)
    
    # Guardar en PostgreSQL
    new_message = Message(content=message)
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify({"status": "Message sent"}), 200

@app.route('/receive', methods=['GET'])
def receive_message():
    method_frame, header_frame, body = channel.basic_get(queue=rabbitmq_queue, auto_ack=True)
    if method_frame:
        message = body.decode()
        redis_client.set('last_message', message)
        return jsonify({"message": message}), 200
    return jsonify({"message": "No messages"}), 200

@app.route('/last', methods=['GET'])
def get_last_message():
    last_message = redis_client.get('last_message')
    if last_message:
        return jsonify({"message": last_message.decode()}), 200
    return jsonify({"message": "No cached messages"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
