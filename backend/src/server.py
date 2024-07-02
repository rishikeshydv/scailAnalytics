from flask import Flask, jsonify, request
from waitress import serve
from flask_cors import CORS
import logging

# Setting up a Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Setting up a GPT model API key (placeholder)
apiKey = "your_api_key"

@app.route('/api/v1/price-trend/individual-property/<property_id>', methods=['GET'])
def individual_property_price_trend(property_id):
    try:
        # Here you would call your GPT model or database to get the price trend
        # For now, we return a placeholder message
        price_trend = f"Single Property Price {property_id}"
        return jsonify(message=price_trend), 200
    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500

if __name__ == '__main__':
    try:
        app.logger.info("Starting the server...")
        serve(app, host="localhost", port=8080)
    except Exception as e:
        app.logger.error(f"Failed to start the server: {e}")
