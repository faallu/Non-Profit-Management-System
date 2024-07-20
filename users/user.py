from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='public', static_url_path='')
            
CORS(app)

users = [{
    "id": 1,
    "username": "janedoe",
    "email": "jdoe@gmail.com", 
    "password": "testPassword",
    "firstName" : "Jane",
    "lastName": "Doe",
    "phone": "7132811234",
    "address" : "1234 Main St.",
    "memberSince" : "2009",
    "location" : "Houston, TX", 
    "skills": ["Cooking", "Teaching"],
    "preferences": {
        "volunteerType": "Community Service",
        "availability": "Weekends"
    }
}]

def user_validation(user):
    valid_conditions = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength" : 2},
            "username": {"type": "string", "minLength" : 2},
            "age": {"type": "integer", "minimum" : 16},
            "email": {"type": "string", "format" : "email"},
            "phone": {"type": "string", "minLength" : 10},
            "password": {"type": "string", "minLength" : 8},
        },
        "required": ["name","username","age","email","phone","password"]
    } 

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User Not found'}), 404

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({'error': 'Not found'}), 404

    data = request.json
    errors = user_validation(data)
    errors = (data)
    if errors:
        return jsonify({'errors': errors}), 400

    user.update(data)
    return jsonify(user)

if __name__ == '__main__':
    app.run(port=3000)
