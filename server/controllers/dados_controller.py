from flask import request
from flask_jwt import jwt_required

from server.services import dados_service


@jwt_required()
def get_all_dados():
    return dados_service.get_all_dados(), 200
