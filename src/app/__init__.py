from flask import Flask, request, jsonify
from .service.messageService import MessageService
from kafka import KafkaProducer
import json
import os
import jsonpickle
import logging


app = Flask(__name__)

logger = logging.getLogger(__name__)

messageService = MessageService()

kafka_host = os.getenv('KAFKA_HOST', 'localhost')
kafka_port = os.getenv('KAFKA_PORT', '9092')
kafka_bootstrap_servers = f"{kafka_host}:{kafka_port}"

print("Kafka server is "+kafka_bootstrap_servers)
print("\n")

producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))


@app.route('/v1/ds/message', methods=['POST'])
def handle_message():
    try:

        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return jsonify({'error': 'x-user-id header is required'}), 400

        # Extract the message from the request
        message = request.json.get('message')
        if not message:
            return jsonify({"error": "No message provided"}), 400

        # Process the message using the message service
        result = messageService.process_message(message)

        # Serialize the result (assuming result is a Pydantic model)
        if result is not None:
            serialized_result = result.serialize()
            serialized_result['user_id'] = user_id
            producer.send('expense_service', serialized_result)
            return jsonify(serialized_result)
        else:
            return jsonify({'error': 'Invalid message format'}), 400
        
    except Exception as e:
        # Log the error and return a 500 response
        app.logger.error(f"Error processing message: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def handle_get():
    print("Hello World")
    return "Hello World"

@app.route('/health', methods=['GET'])
def health_check():
    return 'OK'

if __name__ == '__main__':
    app.run(host='localhost', port=8010,debug=True)