from flask import request
from flask_jwt import jwt_required

from server.services import dados_service


@jwt_required()
def get_all_dados():
    return dados_service.get_all_dados(), 200


@jwt_required()
def post_dados(body):
    return dados_service.post_dados(body), 201


@jwt_required()
def put_dados(id, body):
    return dados_service.put_dados(id, body), 201


@jwt_required()
def delete_dados(id):
    return dados_service.delete_dados(id), 200
