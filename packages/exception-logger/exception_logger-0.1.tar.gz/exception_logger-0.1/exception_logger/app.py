from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime
import logging
from .config import db_config, API_KEY

def create_app():
    app = Flask(__name__)

    # Logger setup
    logging.basicConfig(level=logging.INFO)

    @app.before_request
    def verify_api_key():
        if request.headers.get("API-Key") != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401

    @app.route('/log_exception', methods=['POST'])
    def log_exception():
        try:
            data = request.get_json()

            if not data or 'message' not in data or 'stack_trace' not in data:
                return jsonify({"error": "Invalid exception data"}), 400

            message = data['message']
            stack_trace = data['stack_trace']
            timestamp = datetime.utcnow()

            # Establish database connection
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Insert the exception log into the database
            query = """
            INSERT INTO ExceptionLog (message, stack_trace, timestamp)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (message, stack_trace, timestamp))

            # Commit the transaction
            conn.commit()

            cursor.close()
            conn.close()

            logging.info("Exception logged successfully")
            return jsonify({"message": "Exception logged successfully"}), 200

        except mysql.connector.Error as err:
            logging.error(f"Database error: {err}")
            return jsonify({"error": f"Database error: {err}"}), 500

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return jsonify({"error": f"Unexpected error: {e}"}), 500

    return app

# Entry point for Flask CLI
if __name__ == '__main__':
    create_app().run(debug=True)
