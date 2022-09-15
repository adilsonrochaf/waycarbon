from pprint import pformat

import connexion

from server.configurations.logger import get_logger


def before_request():
    logger = get_logger()

    try:
        logger.info(f"request url: {pformat(connexion.request.base_url)} - {connexion.request.method}")
        logger.info(f"request headers: {pformat(connexion.request.headers)}")
        logger.info(f"request params: {pformat(connexion.request.args)}")
        logger.info(f"request body: {pformat(connexion.request.data)}")
    except Exception as ex:
        logger.warning(f"Erro ao logar request. Continuando fluxo da aplicação. Erro: [{ex}].")

