from flask_jwt import jwt_required

from server.services import usuario_service


@jwt_required()
def post_usuario(body):
    return usuario_service.post_usuario(body), 201


@jwt_required()
def get_all_usuario():
    return usuario_service.get_all_usuario(), 200


@jwt_required()
def get_usuario_by_id(id):
    return usuario_service.get_usuario_by_id_2(id), 200


@jwt_required()
def put_usuario(id, body):
    return usuario_service.put_usuario(id, body), 201


@jwt_required()
def delete_usuario(id):
    return usuario_service.delete_usuario(id), 200


@jwt_required()
def post_desativar_usuario(id, body=None):
    return usuario_service.desativar_usuario(id, body), 201


@jwt_required()
def post_ativar_usuario(id, body=None):
    return usuario_service.ativar_usuario(id, body), 201
