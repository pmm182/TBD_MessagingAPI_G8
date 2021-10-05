from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
from datetime import datetime

from pymongo import MongoClient

from config import local_server


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
    app = Flask(__name__)

    server_config = local_server
    mongo = MongoClient(
        host=server_config.server, port=server_config.port, username=server_config.username,
        password=server_config.password
    )
    app.
    app.run(debug=True)
