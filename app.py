from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "budget_data.json"
current_user_data = None

def load_data():
    global current_user_data
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                current_user_data = json.load(f)
        except:
            current_user_data = None
    return current_user_data

def save_data():
    global current_user_data
    with open(DATA_FILE, 'w') as f:
        json.dump(current_user_data, f, indent=2)

@app.route('/api/init', methods=['GET'])
def init():
    return jsonify({"success": True, "user": current_user_data})

@app.route('/api/profile', methods=['GET'])
def get_profile():
    if current_user_data is None:
        return jsonify({"success": False, "message": "No profile found"})
    return jsonify({"success": True, "user": current_user_data})

@app.route('/api/profile', methods=['POST'])
def save_profile():
    global current_user_data
    data = request.json
    
    if current_user_data is None:
        current_user_data = {
            "Name": data.get('name'),
            "Age": data.get('age'),
            "Total Budget": data.get('total_budget'),
            "Expenses": []
        }
    else:
        current_user_data["Name"] = data.get('name')
        current_user_data["Age"] = data.get('age')
        current_user_data["Total Budget"] = data.get('total_budget')
    
    save_data()
    return jsonify({"success": True, "user": current_user_data})

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    if current_user_data is None:
        return jsonify({"success": True, "expenses": []})
    return jsonify({"success": True, "expenses": current_user_data.get("Expenses", [])})

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    global current_user_data
    if current_user_data is None:
        return jsonify({"success": False, "message": "Create profile first"}), 400
    
    data = request.json
    now = datetime.datetime.now()
    
    expense = {
        "Category": data.get('category'),
        "Item": data.get('item'),
        "Amount": data.get('amount'),
        "Month": now.strftime("%B"),
        "Year": now.year
    }
    
    if "Expenses" not in current_user_data:
        current_user_data["Expenses"] = []
    current_user_data["Expenses"].append(expense)
    save_data()
    
    return jsonify({"success": True, "expense": expense})

@app.route('/api/expenses/<int:index>', methods=['DELETE'])
def delete_expense(index):
    global current_user_data
    if current_user_data is None:
        return jsonify({"success": False, "message": "No profile"}), 400
    
    expenses = current_user_data.get("Expenses", [])
    if 0 <= index < len(expenses):
        expenses.pop(index)
        current_user_data["Expenses"] = expenses
        save_data()
        return jsonify({"success": True})
    
    return jsonify({"success": False, "message": "Expense not found"}), 404

@app.route('/api/expenses/clear', methods=['DELETE'])
def clear_expenses():
    global current_user_data
    if current_user_data:
        current_user_data["Expenses"] = []
        save_data()
    return jsonify({"success": True})

# ========== IMPORTANT: This is what Render needs ==========
if __name__ == '__main__':
    load_data()
    # Get the port from environment variable (Render sets this)
    port = int(os.environ.get('PORT', 5000))
    # Bind to 0.0.0.0 to accept all connections
    app.run(host='0.0.0.0', port=port)
