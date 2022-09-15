import json

from flask import Response


class ApiBaseException(Exception):
    status_code = 500
    message = None
    payload = None
    detail = None

    def __init__(self, message, detail=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload
        self.detail = detail


def generic_render(exception: ApiBaseException):
    return Response(
        response=json.dumps(
            {"message": exception.message, "payload": exception.payload, "detail": exception.detail}
        ),
        status=exception.status_code,
        mimetype="application/json",
    )


class NotFound(ApiBaseException):
    status_code = 404
    message = "Entidade não encontrada"

    def __init__(self, message=None, payload=None):
        self.message = message if message is not None else self.message
        ApiBaseException.__init__(self, self.message, payload)


class NoContent(ApiBaseException):
    status_code = 204
    message = "Sem conteúdo"

    def __init__(self, message=None, payload=None):
        self.message = message if message is not None else self.message
        ApiBaseException.__init__(self, self.message, payload)


class Unauthorized(ApiBaseException):
    status_code = 401
    message = "Não autorizado, token inválido ou inexistente"

    def __init__(self, message=None, payload=None):
        self.message = message if message is not None else self.message
        ApiBaseException.__init__(self, self.message, payload)


class DataFail(ApiBaseException):
    status_code = 400
    message = "Falha na validação de dados do objeto"

    def __init__(self, detail=None, message=None, payload=None):
        self.detail = detail
        self.message = message if message is not None else self.message

        ApiBaseException.__init__(self, self.message, self.detail, payload)


class BusinessFail(ApiBaseException):
    status_code = 422
    message = "Falha na regra de negócio"

    def __init__(self, detail=None, message=None, payload=None):
        self.detail = detail
        self.message = message if message is not None else self.message

        ApiBaseException.__init__(self, self.message, self.detail, payload)


class ConflictFail(ApiBaseException):
    status_code = 409
    message = "Conflito"

    def __init__(self, detail=None, message=None, payload=None):
        self.detail = detail
        self.message = message if message is not None else self.message

        ApiBaseException.__init__(self, self.message, self.detail, payload)
