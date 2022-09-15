import connexion

from server import logger, NotFound, db
from server.controllers import util
from server.models.usuario import Usuario, UsuarioSchema
from server.repository import base_repository
from server.services import utils
from server.services.utils import converte_dto_para_objeto


def post_usuario(usuario_dto):
    logger.info(f"Inicio - criar um novo usuário")
    try:
        ja_existe = get_usuario_by_email(usuario_dto['email'])
        if ja_existe:
            return "Usuário já existe!"
        else:
            usuario = utils.converte_dto_para_objeto(Usuario, usuario_dto)
            base_repository.gravar_objeto(usuario)
            return utils.serialize_entidade(usuario, UsuarioSchema)

    except Exception as ex:
        logger.error(f"Erro \n {ex}")
        db.session.rollback()
        raise ex


def get_usuario_by_email(email):
    logger.info(f"Inicio - busca um usuário")
    try:
        return Usuario.query.filter(Usuario.email == email).first()
    except Exception as ex:
        logger.error(f"Erro \n {ex}")
        db.session.rollback()
        raise ex


def get_usuario_by_id(id):
    logger.info(f"Inicio - busca um usuário")
    try:
        return Usuario.query.get(id)
    except Exception as ex:
        logger.error(f"Erro \n {ex}")
        db.session.rollback()
        raise ex


def get_usuario_by_id_2(id):
    logger.info(f"Inicio - busca um usuário")
    try:
        query = Usuario.query.get(id)
        return utils.serialize_entidade(query, UsuarioSchema)
    except Exception as ex:
        logger.error(f"Erro \n {ex}")
        db.session.rollback()
        raise ex


def get_all_usuario():
    logger.info(f"Inicio - busca todos usuários")
    parametros = util.get_parametros(connexion)
    try:
        all_usuarios = base_repository.listar(Usuario, UsuarioSchema)
        return all_usuarios
    except Exception as ex:
        logger.error(f"Erro \n {ex}")
        db.session.rollback()
        raise ex


def put_usuario(id, usuario_dto):
    logger.info(f"Inicio - atualizar usuario por id \n {id}")
    try:
        usuario = base_repository.get_objeto_por_id(Usuario, id)

        if usuario is not None:
            converte_dto_para_objeto(Usuario, usuario_dto, usuario)
            base_repository.gravar_objeto(usuario)

            return utils.serialize_entidade(usuario, UsuarioSchema)

        raise NotFound()

    except Exception as ex:
        logger.error(f"Erro ao atualizar usuario \n {ex}")
        db.session.rollback()
        raise ex


def delete_usuario(id):
    logger.info(f"Inicio - excluir usuario por id \n {id}")
    try:
        base_repository.excluir_objeto_por_id(Usuario, id)
    except Exception as ex:
        logger.error(f"Erro \n {ex}")
        db.session.rollback()
        raise ex


def desativar_usuario(id, body=None):
    logger.info(f"Inicio - Desativar usuario")
    try:
        usuario = base_repository.get_objeto_por_id(Usuario, id)

        if usuario is not None:
            usuario.status = "Desativado"
            base_repository.gravar_objeto(usuario)

            return utils.serialize_entidade(usuario, UsuarioSchema)

        raise NotFound()

    except Exception as ex:
        logger.error(f"Erro ao desativar usuario \n {ex}")
        db.session.rollback()
        raise ex


def ativar_usuario(id, body=None):
    logger.info(f"Inicio - Ativar Usuario")
    try:
        usuario = base_repository.get_objeto_por_id(Usuario, id)

        if usuario is not None:
            usuario.status = "Ativo"
            base_repository.gravar_objeto(usuario)

            return utils.serialize_entidade(usuario, UsuarioSchema)

        raise NotFound()

    except Exception as ex:
        logger.error(f"Erro ao Ativar cliente \n {ex}")
        db.session.rollback()
        raise ex


