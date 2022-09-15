from server import logger, db
from server.models.usuario import UsuarioSchema
from server.services import usuario_service, utils, acesso_usuario_service


def authenticate(username, password):
    try:
        usuario = usuario_service.get_usuario_by_email(username)
        if usuario and usuario.senha == password and usuario.status == 'Ativo':
            body_acesso = {
                'id_usuario': usuario.id
            }
            retorno = acesso_usuario_service.post_acesso(body_acesso)
            if retorno:
                return utils.serialize_entidade(usuario, UsuarioSchema)
    except Exception as ex:
        logger.error(f"Erro \n {ex}")
        db.session.rollback()
        raise ex


def identity(payload):
    try:
        user_id = payload['identity']
        return usuario_service.get_usuario_by_id(user_id)
    except Exception as ex:
        logger.error(f"Erro \n {ex}")
        db.session.rollback()
        raise ex
