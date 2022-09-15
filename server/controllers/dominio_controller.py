from flask_jwt import jwt_required

from server.services import dominio_service


@jwt_required()
def post_dominio(body):
    return dominio_service.post_dominio(body), 201


@jwt_required()
def get_dominio_by_id(id):
    return dominio_service.get_dominio_by_id(id), 200


@jwt_required()
def get_dominio_by_tp_dominio(tp_dominio):
    return dominio_service.get_dominio_by_tipo(tp_dominio), 200
