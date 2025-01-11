from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import json

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Test URL to check if the server is running
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Server is up and running!"}), 200

# Analyze Stocks Route
@app.route("/analyze-stocks", methods=["GET"])
def analyze_stocks():
    tickers = request.args.get("tickers")
    if not tickers:
        return jsonify({"error": "Tickers query parameter is required"}), 400

    # Sanitize the tickers input to prevent command injection
    sanitized_tickers = "".join(c for c in tickers if c.isalnum() or c == ",")
    tickers_list = sanitized_tickers.split(",")  # Convert to list for better handling

    # Path to the Python script
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "analyze_stock.py"))

    # Execute the Python script
    try:
        # Pass arguments as a list of strings instead of a single string
        result = subprocess.run(
            ["python3", script_path, "--tickers", sanitized_tickers],
            capture_output=True,
            text=True,
            check=True
        )
        stdout = result.stdout  # Capture the standard output of the script
        return jsonify(json.loads(stdout))  # Convert the output to JSON and return it
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Error executing Python script: {e.stderr}"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "Error parsing Python script output. Output is not valid JSON."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start the server
if __name__ == "__main__":
    port = int(os.getenv("PORT", 3001))
    app.run(host="0.0.0.0", port=port)
