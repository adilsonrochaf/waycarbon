from server import logger, db
from server.models.acesso_usuario import AcessoUsuario, AcessoUsuarioSchema
from server.repository import base_repository
from server.services import utils


def post_acesso(acesso_dto):
    logger.info(f"Inicio - criar um novo dominio")
    try:
        acesso = utils.converte_dto_para_objeto(AcessoUsuario, acesso_dto)
        base_repository.gravar_objeto(acesso)
        return True

    except Exception as ex:
        logger.error(f"Erro \n {ex}")
        db.session.rollback()
        raise ex
