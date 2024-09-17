from flask import Flask, jsonify, request

app = Flask(__name__)

# Root route
@app.route('/')
def home():
    return "Todo Api - Yout Task List Manager"

if __name__ == "_main_":
    app.run(debug=True)
