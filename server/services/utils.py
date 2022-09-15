
from collections import OrderedDict

import connexion
from flask import jsonify
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm.collections import InstrumentedList

from server import logger
from server.models.pagination import PaginationSchema
from server.repository import base_repository


def converte_dto_para_objeto(clazz, dto, objeto=None, recursivo=False):
    """
    Função responsável por converter um dto para a instancia do objeto do tipo "clazz"
    :param clazz: Define a classe do objeto
    :param dto: Contem os dados enviados para conversão
    :param objeto: Caso haja um objeto para atualização
    :param recursivo: Indica se a function está sendo chamada recursivamente, deve ser passado "True" internamente
    :return: objeto: Objeto atualizado de acordo com o dto
    """

    config = configs()

    objeto = clazz() if objeto is None else objeto
    for key in dto:

        if isinstance(getattr(clazz, key).type, JSONB):
            setattr(objeto, key, dto[key])
        elif isinstance(dto[key], dict):
            if key in config:
                setattr(objeto, key, converte_dto_para_objeto(clazz=config[key], dto=dto[key], recursivo=True))
        elif isinstance(dto[key], list):
            val_list = []
            for obj in dto[key]:
                val_list.append(converte_dto_para_objeto(clazz=config[key], dto=obj, recursivo=True))

            setattr(objeto, key, val_list)

        else:
            try:
                setattr(objeto, key, dto[key])
            except:
                logger.error(f'objeto {objeto.__class__.__name__} não possui o atributo {key}')

    if recursivo:
        db_obj = None
        if hasattr(objeto, 'nm_dominio'):
            db_obj = base_repository.get_objetos_por_campo_valor(clazz, clazz.nm_dominio, objeto.nm_dominio)

        if db_obj is not None:
            objeto = db_obj
        else:
            objeto.id = None
            base_repository.gravar_objeto(objeto)

    return objeto


def configs():
    return {}


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

    if 'pagina' in parametros:
        pagina = int(parametros['pagina'])
        parametros.pop('pagina', None)
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

    log_filtros(filtros)

    return tuple(filtros), tuple(joins), pagina


def log_filtros(filtros):
    filtros_rep = []

    for f in filtros:
        try:
            filtros_rep.append(
                (
                    str(f.left.table.name) + "." + str(f.left.name),
                    str(f.right.effective_value),
                )
            )
        except:
            filtros_rep.append(str(f))

    logger.info(f"Busca com os filtros: {filtros_rep}")
    logger.info(f"Fim criação de filtros com {len(filtros)} filtro(s)")


def valida_no_content_ou_no_found(filtros, lista_de_entidades):
    """
    Função responsável por validar se uma query é do tipo 404 ou 204.
    :param filtros: filtros fabricados na função fabrica_filtros
    :param lista_de_entidades: lista de entidades retornadas pela query
    """
    # Se não tem nenhum filtro e também não tem nenhuma entidade, quer dizer que não há registros no
    # banco de dados
    if len(lista_de_entidades) == 0 and len(filtros) == 0:
        logger.info("Sem registros no banco de dados para esta consulta")
        return False
    # Se tem algum filtro e nenhuma entidade, quer dizer que a query não encontrou nenhum registro no
    # banco de dados
    elif len(lista_de_entidades) == 0 and len(filtros) > 0:
        logger.info("Consulta não encontrou nenhum registro no banco de dados")
        return False

    return True


def serialize_entidade(entidade, entidade_schema, apply_jsonify=True):
    """
    Função responsável por serializar uma ou várias entidades
    :param apply_jsonify: Responsável por applicar a função jsonify ao retorno/output
    :param entidade: List ou Entidade - Uma lista ou uma entidade, por exemplo, Cidade
    :param entidade_schema: Schema o esquema da entidade que será serialized
    :return: retorna a entidade serialized
    """
    logger.debug(f"Início serialização de {entidade_schema.__name__}")
    schema = (
        entidade_schema(many=True)
        if type(entidade) == list or type(entidade) == InstrumentedList
        else entidade_schema()
    )
    output = (
        jsonify(schema.dump(entidade).data)
        if apply_jsonify
        else schema.dump(entidade).data
    )
    logger.debug(f"Fim serialização de {entidade_schema.__name__}")
    return output


def serialize_pagination(entidade_schema, pagination):
    entidade = pagination.items
    entidade_serialized = serialize_entidade(
        entidade, entidade_schema, apply_jsonify=False
    )
    pagination_serialized = serialize_entidade(
        pagination, PaginationSchema, apply_jsonify=False
    )
    pagination_serialized["items"] = entidade_serialized

    output = jsonify(pagination_serialized)

    return output

