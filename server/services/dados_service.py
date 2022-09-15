import connexion

from server import logger, NotFound, db
from server.controllers import util
from server.models.dados import Dados, DadosSchema
from server.repository import base_repository
from server.services import utils
from server.services.utils import converte_dto_para_objeto


def post_dados(dados_dto):
    logger.info(f"Inicio - criar um novo registro de dados")
    try:
        dados = utils.converte_dto_para_objeto(Dados, dados_dto)
        base_repository.gravar_objeto(dados)
        return utils.serialize_entidade(dados, DadosSchema)

    except Exception as ex:
        logger.error(f"Erro \n {ex}")
        db.session.rollback()
        raise ex


def get_dados_by_id(id):
    logger.info(f"Inicio - busca um registro de dados por id")
    try:
        query = Dados.query.get(id)
        return utils.serialize_entidade(query, DadosSchema)
    except Exception as ex:
        logger.error(f"Erro \n {ex}")
        db.session.rollback()
        raise ex


def get_all_dados():
    logger.info(f"Inicio - busca todos os Dados")
    parametros = util.get_parametros(connexion)
    try:
        all_dados = base_repository.listar_paginado(Dados, DadosSchema, parametros)
        return all_dados
    except Exception as ex:
        logger.error(f"Erro \n {ex}")
        db.session.rollback()
        raise ex


def put_dados(id, dados_dto):
    logger.info(f"Inicio - atualizar dados por id \n {id}")
    try:
        dados = base_repository.get_objeto_por_id(Dados, id)

        if dados is not None:
            converte_dto_para_objeto(Dados, dados_dto, dados)
            base_repository.gravar_objeto(dados)

            return utils.serialize_entidade(dados, DadosSchema)

        raise NotFound()

    except Exception as ex:
        logger.error(f"Erro ao atualizar dados \n {ex}")
        db.session.rollback()
        raise ex


def delete_dados(id):
    logger.info(f"Inicio - excluir dados por id \n {id}")
    try:
        base_repository.excluir_objeto_por_id(Dados, id)
    except Exception as ex:
        logger.error(f"Erro \n {ex}")
        db.session.rollback()
        raise ex
