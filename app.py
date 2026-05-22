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
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            current_user_data = data
            return data
    return None

def save_data():
    global current_user_data
    with open(DATA_FILE, 'w') as f:
        json.dump(current_user_data, f, indent=2)

def add_expense(category, item, amount, user_data):
    current_date = datetime.datetime.now()
    expense = {
        "Category": category,
        "Item": item,
        "Amount": amount,
        "Month": current_date.strftime("%B"),
        "Year": current_date.year,
        "Date": current_date.strftime("%Y-%m-%d %H:%M:%S")
    }
    user_data["Expenses"].append(expense)
    return expense

def calculate_total_spending(user_data):
    total = 0
    for expense in user_data["Expenses"]:
        total += expense["Amount"]
    return total

def get_budget_status(user_data):
    total_spent = calculate_total_spending(user_data)
    total_budget = user_data["Total Budget"]
    
    if total_budget == 0:
        return {"status": "No budget set", "percentage": 0, "message": "Please set your budget"}
    
    percentage = (total_spent / total_budget) * 100
    
    if total_spent > total_budget:
        return {"status": "danger", "percentage": percentage, "message": "Danger! Budget exceeded."}
    elif total_spent >= total_budget * 0.8:
        return {"status": "warning", "percentage": percentage, "message": "Warning! Near budget limit."}
    else:
        return {"status": "safe", "percentage": percentage, "message": "Budget is under control!"}

@app.route('/api/profile', methods=['POST'])
def save_profile():
    global current_user_data
    data = request.json
    name = data.get('name')
    age = data.get('age')
    total_budget = data.get('total_budget', 0)
    
    if current_user_data is None:
        current_user_data = {
            "Name": name,
            "Age": age,
            "Total Budget": total_budget,
            "Expenses": []
        }
    else:
        current_user_data["Name"] = name
        current_user_data["Age"] = age
        current_user_data["Total Budget"] = total_budget
    
    save_data()
    return jsonify({"success": True, "user": current_user_data, "budget_status": get_budget_status(current_user_data)})

@app.route('/api/profile', methods=['GET'])
def get_profile():
    global current_user_data
    if current_user_data is None:
        return jsonify({"success": False, "message": "No profile found"})
    return jsonify({"success": True, "user": current_user_data, "budget_status": get_budget_status(current_user_data)})

@app.route('/api/expenses', methods=['POST'])
def add_expense_route():
    global current_user_data
    if current_user_data is None:
        return jsonify({"success": False, "message": "Please create profile first"}), 400
    
    data = request.json
    category = data.get('category')
    item = data.get('item')
    amount = float(data.get('amount', 0))
    
    expense = add_expense(category, item, amount, current_user_data)
    save_data()
    
    return jsonify({
        "success": True,
        "expense": expense,
        "total_spent": calculate_total_spending(current_user_data),
        "budget_status": get_budget_status(current_user_data)
    })

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    global current_user_data
    if current_user_data is None:
        return jsonify({"success": False, "expenses": []})
    return jsonify({
        "success": True,
        "expenses": current_user_data["Expenses"],
        "total_spent": calculate_total_spending(current_user_data),
        "budget_status": get_budget_status(current_user_data)
    })

@app.route('/api/expenses/<int:index>', methods=['DELETE'])
def delete_expense(index):
    global current_user_data
    if current_user_data is None:
        return jsonify({"success": False, "message": "No profile found"}), 400
    
    if 0 <= index < len(current_user_data["Expenses"]):
        deleted = current_user_data["Expenses"].pop(index)
        save_data()
        return jsonify({"success": True, "deleted": deleted, "total_spent": calculate_total_spending(current_user_data)})
    return jsonify({"success": False, "message": "Expense not found"}), 404

@app.route('/api/expenses/clear', methods=['DELETE'])
def clear_all_expenses():
    global current_user_data
    if current_user_data is None:
        return jsonify({"success": False, "message": "No profile found"}), 400
    current_user_data["Expenses"] = []
    save_data()
    return jsonify({"success": True, "total_spent": 0, "budget_status": get_budget_status(current_user_data)})

@app.route('/api/init', methods=['GET'])
def init_data():
    data = load_data()
    if data:
        return jsonify({"success": True, "user": data, "budget_status": get_budget_status(data)})
    return jsonify({"success": True, "user": None})

if __name__ == '__main__':
    load_data()
    app.run(debug=True, port=5000)