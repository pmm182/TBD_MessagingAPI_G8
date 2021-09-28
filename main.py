from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
from datetime import datetime
import json

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/messaging8'
mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create_user():
    # Receiving Data
    name = request.json['name']
    username = request.json['username']

    if name and username:
        _id = mongo.db.users.insert(
            {'name': name, 'username': username})
        response = jsonify({
            '_id': str(_id),
            'name': name,
            'username': username
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    print(id)
    user = mongo.db.users.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/users/<_id>', methods=['PUT'])
def update_user(_id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    if username and email and password and _id:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set': {'username': username, 'email': email, 'password': hashed_password}})
        response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Not found :( . ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


@app.route('/messages', methods=['POST'])
def create_message():
    # Receiving Data
    room_id = request.json['room_id']
    user = request.json['user']
    text = request.json['message']
    now = datetime.now()

    message = {'from': user, 'date': now, 'message': text}

    partition_date = [datetime(now.year, now.month, now.day, now.hour, 0, 0),
                      datetime(now.year, now.month, now.day, now.hour, 59, 59)]

    if room_id and partition_date and message:
        query = {'partition_date': partition_date, 'room_id': room_id}
        values = {'$push': {'messages': message}}

        _id = mongo.db.messages.update_one(query, values,  upsert=True)
        response = jsonify({
            '_id': str(_id),
            'room_id': room_id,
            'message': message,
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/rooms', methods=['POST'])
def create_room():
    # Receiving Data
    name = request.json['name']
    members = request.json['members']

    if name and members:
        id = mongo.db.users.insert(
            {'name': name, 'members': members})
        response = jsonify({
            '_id': str(id),
            'name': name,
            'members': members,
        })
        response.status_code = 201
        return response
    else:
        return not_found()


if __name__ == "__main__":
    print("*******************************************************************************************************")
    print('Bem vindo ao servidor de API para mensageria com MongoDB.')
    print('O objetivo desta aplicação é fornecer um caminho para avaliar o comportamento do MongoDB como NoSQL '
          'sob diferentes configurações.')
    print("*******************************************************************************************************")
    app.run(debug=True)