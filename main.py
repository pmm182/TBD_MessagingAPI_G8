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
    name = request.json['name']
    username = request.json['username']

    duplicate = mongo.db.users.find_one({'username': username}, {})
    if duplicate is not None:
        return user_exists()

    if name and username:
        _id = mongo.db.users.insert(
            {'name': name, 'username': username})
        response = jsonify({
            '_id': str(_id),
            'name': name,
            'username': username
        })
        response.status_code = 200
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
def delete_user(_id):
    mongo.db.users.delete_one({'_id': ObjectId(_id)})
    response = jsonify({'message': 'User' + _id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/rooms', methods=['POST'])
def create_room():
    name = request.json['name']
    members = request.json['members']

    if members:
        _id = mongo.db.rooms.insert(
            {'name': name, 'members': members})
        response = jsonify({
            '_id': str(_id),
        })
        response.status_code = 200
        return response
    else:
        return not_found()


@app.route('/rooms', methods=['GET'])
def get_rooms():
    username = request.json['username']
    rooms = mongo.db.rooms.find({'members': username }, {'_id': False, 'name': True})

    if rooms.count() > 0:
        response = json_util.dumps(rooms)
        return Response(response, mimetype="application/json")
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


@app.errorhandler(409)
def user_exists(error=None):
    message = {
        'message': 'User already exists. ' + request.url,
        'status': 409
    }
    response = jsonify(message)
    response.status_code = 409
    return response


@app.route('/rooms/<id>/messages', methods=['POST'])
def create_message(id):
    # Receiving Data
    room_id = id
    username = request.json['username']
    text = request.json['message']
    now = datetime.now()

    message = {'from': username, 'date': now, 'message': text}

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


@app.route('/rooms/<id>/messages', methods=['GET'])
def get_messages(id):
    # Receiving Data
    room_id = id
    #username = request.json['username']

    messages = mongo.db.messages.find({'room_id': room_id}, {'_id': False})
    response = json_util.dumps(messages)
    return Response(response, mimetype="application/json")


if __name__ == "__main__":
    print("*******************************************************************************************************")
    print('Bem vindo ao servidor de API para mensageria com MongoDB.')
    print('O objetivo desta aplicação é fornecer um caminho para avaliar o comportamento do MongoDB como NoSQL '
          'sob diferentes configurações.')
    print("*******************************************************************************************************")
    app.run(debug=True)