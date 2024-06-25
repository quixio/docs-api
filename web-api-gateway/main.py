from flask import Flask, request, jsonify
from flask_cors import CORS
from quixstreams import Application

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize QuixStreams Application
quix_app = Application(broker_address='localhost:9092')
topic = quix_app.topic(name='user_interactions', value_serializer='json')


@app.route('/', methods=['GET'])
def root():
    return jsonify({"message": "I'm alive"}), 200

@app.route('/publish', methods=['POST'])
def publish_event():
    data = request.json
    if not data or 'sessionId' not in data or 'object' not in data or 'action' not in data:
        return jsonify({"error": "Invalid data provided"}), 400

    with quix_app.get_producer() as producer:
        message = topic.serialize(key=data['sessionId'], value=data)
        producer.produce(topic=topic.name, value=message.value, key=message.key)
    
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=80)