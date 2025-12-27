from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Atif", "role": "SDET"},
    {"id": 2, "name": "Ali", "role": "QA"}
]

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    data["id"] = len(users) + 1
    users.append(data)
    return jsonify(data), 201

if __name__ == "__main__":
    app.run(debug=True)
