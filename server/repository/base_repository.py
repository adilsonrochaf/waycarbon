from collections import OrderedDict

import connexion

from server import db, logger
from server.configurations.logger import get_logger
from server.models.dados import Dados
from server.models.exceptions import ApiBaseException, NotFound
from server.services.utils import serialize_entidade, serialize_pagination


def get_filtros(clazz):
    filtros = {}
    if clazz == Dados:
        filtros["id_empresa"] = lambda id_empresa: (clazz.id_empresa == id_empresa, None)
    return filtros


def fabrica_filtros(filtros_dict, parametros=None):
    """
    Função responsável por selecionar qual método de busca deverá ser realizado
    dependendo do filtro parâmetro passado na URL

    :param parametros: Poderá ser passado como parâmetro caso os filtros precisem ser fabricados manualmente
    :param filtros_dict: terá um dicionário com várias tuplas contendo um objeto
    de filtro e uma lista de objetos de joins, (Entidade.attr == filtro, [Entidade.entidade1, Entidade1.entidade2])

    :return: list: retorna um lista contendo dicts que representam cidades
    """
    logger.info(f"Início criação de filtros")

    # TODO desacoplar o connexion.request.args
    parametros = parametros if parametros is not None else connexion.request.args

    if 'page' in parametros:
        pagina = int(parametros['page'])
        parametros.pop('page', None)
    else:
        pagina = 1

    filtros = []
    # Este set é criado para eliminar joins duplicados
    set_of_joins = OrderedDict()
    for k in parametros:
        # A variável filtro receberá o valor da função que tem o mesmo nome do parâmetro
        # recebido via query string
        filtro = (
            filtros_dict.get(k)(parametros[k])
            if filtros_dict.get(k) is not None
            else None
        )

        if filtro is None:
            # Se o filtro for vazio, significa que um parametro diferente dos registrados no servico
            # foi passado na requisicao
            continue

        if type(filtro) != tuple or len(filtro) < 2:
            raise AttributeError(
                f"O filtro {k} precisa ser uma tupla com dois valores, uma condição/filtro sql e uma lista de joins"
            )
        # Os filtros serão armazenados na lista de [filtros]
        filtros.append(filtro[0])
        if filtro[1] is not None:
            # Como cada filtro pode fazer mais de um join,
            # vamos fazer outro loop para descobrir os joins
            for i in range(len(filtro[1])):
                set_of_joins[filtro[1][i]] = None
    joins = list(set_of_joins)

    return tuple(filtros), tuple(joins), pagina


def get_objeto_por_id(clazz, id_objeto):
    query = db.session.query(clazz).filter(clazz.id == id_objeto)

    return query.first()


def get_por_id_entidade(clazz, entidade, id_objeto):
    query = db.session.query(clazz).filter(entidade == id_objeto)

    return query.first()


def get_all_por_id_entidade(clazz, entidade, id_objeto):
    query = db.session.query(clazz).filter(entidade == id_objeto)

    return query.all()


def get_por_entidade(clazz, entidade, nm_entidade):
    query = db.session.query(clazz).filter(entidade == nm_entidade)

    return query.all()


def gravar_objeto(objeto):
    try:
        db.session.add(objeto)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        if len(error.args) == 1:
            get_logger().error(f'erro ao gravar {objeto.__class__.__name__}: {error.args[0]}')
            raise ApiBaseException(error.args[0])
        else:
            get_logger().error(f'erro ao gravar {objeto.__class__.__name__}: {error}')
            raise ApiBaseException(error.args[0])


def excluir_objeto_por_id(clazz, id_objeto):
    objeto = get_objeto_por_id(clazz, id_objeto)

    if objeto is not None:
        excluir_objeto(objeto)
        return

    raise NotFound()


def excluir_objeto(objeto):
        db.session.delete(objeto)
        db.session.commit()


def listar(clazz, schema):
    query = db.session.query(clazz)
    response = query.all()

    return serialize_entidade(response, schema, apply_jsonify=False)


# def listar_paginado(clazz, schema, paramentros):
#     id_empresa = paramentros.get('token_decode').get('empresa').get('id')
#     query = clazz.query.filter(clazz.id_empresa == id_empresa).paginate(int(paramentros.get('page')), int(paramentros.get('per_page')))
#
#     return serialize_pagination(schema, query)


def listar_paginado(clazz, schema, parametros):
    PER_PAGE = int(parametros.get('per_page'))
    MAX_PER_PAGE = int(parametros.get('per_page'))
    filtros, joins, PAGINA = fabrica_filtros(get_filtros(clazz), parametros)

    pagination = (
        clazz()
            .query.join(*joins)
            .filter(*filtros)
            .paginate(per_page=PER_PAGE, max_per_page=MAX_PER_PAGE, page=PAGINA)
    )

    return serialize_pagination(schema, pagination)


def get_objetos_por_campo_valor(clazz, campo, descricao):
    query = db.session.query(clazz).filter(campo == descricao)
    if hasattr(clazz, 'deleted_at'):
        query = query.filter(clazz.deleted_at == None)
    return query.all()

