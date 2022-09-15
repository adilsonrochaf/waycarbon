from server import logger, db
from server.models.dominio import Dominio, DominioSchema
from server.repository import base_repository
from server.services import utils


def post_dominio(dominio_dto):
    logger.info(f"Inicio - criar um novo dominio")
    try:
        dominio = utils.converte_dto_para_objeto(Dominio, dominio_dto)
        base_repository.gravar_objeto(dominio)
        return utils.serialize_entidade(dominio, DominioSchema)

    except Exception as ex:
        logger.error(f"Erro \n {ex}")
        db.session.rollback()
        raise ex


def get_dominio_by_id(id):
    logger.info(f"Inicio - busca um dominio")
    try:
        query = Dominio.query.get(id)
        return utils.serialize_entidade(query, DominioSchema)
    except Exception as ex:
        logger.error(f"Erro \n {ex}")
        db.session.rollback()
        raise ex


def get_dominio_by_tipo(tp_dominio):
    logger.info(f"Inicio - busca um dominio")
    try:
        query = base_repository.get_por_entidade(Dominio, Dominio.tp_dominio, tp_dominio)
        return utils.serialize_entidade(query, DominioSchema)
    except Exception as ex:
        logger.error(f"Erro \n {ex}")
        db.session.rollback()
        raise ex
