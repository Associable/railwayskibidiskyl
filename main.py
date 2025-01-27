from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
API_KEY = os.environ.get('API_KEY', 'zyniscool')  # Get from environment variables
DATA_FILE = "data.json"
PORT = int(os.environ.get('PORT', 8080))  # Railway provides PORT

# Create data.json if missing
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

def verify_api_key():
    """Middleware to check API key in headers or query parameters"""
    provided_key = request.headers.get('X-API-KEY') or request.args.get('apikey')
    if provided_key != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401
    return None

@app.route('/status', methods=['GET'])
def status_check():
    """Server health check endpoint"""
    try:
        with open(DATA_FILE, 'r') as f:
            json.load(f)
        return jsonify({
            "status": "OK",
            "environment": os.environ.get('RAILWAY_ENVIRONMENT', 'development'),
            "data_entries": len(json.load(open(DATA_FILE)))
        }), 200
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/store', methods=['POST'])
def store_data():
    """Endpoint to store new data entries"""
    # Authentication check
    auth_check = verify_api_key()
    if auth_check:
        return auth_check
    
    # Data validation
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    required_fields = ['map_name', 'act_name', 'preferred_units']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required fields. Required: {required_fields}"}), 400
    
    try:
        # Read existing data
        with open(DATA_FILE, 'r') as f:
            existing_data = json.load(f)
        
        # Add new entry with timestamp
        entry = {
            **data,
            "timestamp": os.environ.get('RAILWAY_TIMESTAMP', 'no-timestamp')
        }
        existing_data.append(entry)
        
        # Write back to file
        with open(DATA_FILE, 'w') as f:
            json.dump(existing_data, f, indent=2)
            
        return jsonify({"message": "Data stored successfully", "id": len(existing_data)-1}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/retrieve', methods=['GET'])
def retrieve_data():
    """Endpoint to retrieve stored data"""
    # Authentication check
    auth_check = verify_api_key()
    if auth_check:
        return auth_check
    
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        
        # Filtering parameters
        filters = {
            'map_name': request.args.get('map_name'),
            'act_name': request.args.get('act_name'),
            'preferred_units': request.args.get('preferred_units')
        }
        
        # Apply filters
        filtered_data = [
            entry for entry in data
            if all(
                entry.get(key) == value 
                for key, value in filters.items() 
                if value is not None
            )
        ]
        
        return jsonify({
            "count": len(filtered_data),
            "results": filtered_data
        }), 200
    
    except json.JSONDecodeError:
        return jsonify({"error": "Data file corrupted"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
