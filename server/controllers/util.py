from flask import request
import jwt


def get_parametros(connexion):
    token = request.headers.environ.get('HTTP_AUTHORIZATION').replace('JWT ', '')
    token_decode = jwt.decode(token, options={"verify_signature": False})
    parametros = {'token_decode': token_decode, 'id_empresa': token_decode.get('empresa').get('id')}

    for key in connexion.request.args:
        arr_keys = []
        valor = connexion.request.args[key]
        if key in arr_keys:
            if isinstance(valor, str):
                valor = valor.replace(' ', '').split(',')
        else:
            if valor == "true":
                valor = True
            elif valor == "false":
                valor = False

        parametros[key] = valor

    return parametros
