from flask import Flask, request, jsonify
from service.messageService import MessageService
from kafka import KafkaProducer
import json

app = Flask(__name__)

# Initialize the message service
messageService = MessageService()

# Initialize the Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],  # Use a list for bootstrap_servers
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize JSON data
)

@app.route('/v1/ds/message', methods=['POST'])
def handle_message():
    try:
        # Extract the message from the request
        message = request.json.get('message')
        if not message:
            return jsonify({"error": "No message provided"}), 400

        # Process the message using the message service
        result = messageService.process_message(message)

        # Serialize the result (assuming result is a Pydantic model)
        serializer_result = result.model_dump_json()  # Use model_dump_json for Pydantic models

        print("Result: ", result)

        # Send the event to Kafka (deserialize JSON string back to dict)
        producer.send('DataScience_message', value=json.loads(serializer_result))
        producer.flush()  # Ensure the message is sent

        return jsonify(result)
    except Exception as e:
        # Log the error and return a 500 response
        app.logger.error(f"Error processing message: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def handle_get():
    print("Hello World")
    return "Hello World"

if __name__ == '__main__':
    app.run(host='localhost', port=8000)