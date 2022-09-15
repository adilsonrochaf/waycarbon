import datetime

import connexion
from flask_cors import CORS
from flask_jwt import JWT
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from server.configurations import environments_variables
from server.configurations.logger import factory_logger
from server.filters.filters import before_request
from server.models.exceptions import DataFail, generic_render, NotFound, NoContent, Unauthorized, BusinessFail, \
    ConflictFail

db = SQLAlchemy()
ma = Marshmallow()
logger = factory_logger()


def inicia_autenticacao():
    from server.services.authentication import authenticate, identity
    return authenticate, identity


def init_api():
    app = connexion.App(__name__, specification_dir="./swagger/")
    app.add_api("swagger.yaml",
                arguments={"host_with_port": f"{environments_variables.HOST}:{environments_variables.PORT}"})
    app.add_error_handler(DataFail, generic_render)
    app.add_error_handler(NotFound, generic_render)
    app.add_error_handler(NoContent, generic_render)
    app.add_error_handler(Unauthorized, generic_render)
    app.add_error_handler(BusinessFail, generic_render)
    app.add_error_handler(ConflictFail, generic_render)
    app.app.config["SQLALCHEMY_DATABASE_URI"] = environments_variables.DBCONN
    app.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.app.config['SECRET_KEY'] = '%C*F-JaNdRgUkXp2s5v8y/B?E(G+KbPee'
    app.app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(minutes=100)
    db.init_app(app.app)
    CORS(app.app)
    ma.init_app(app.app)
    authenticate, identity = inicia_autenticacao()
    jwt = JWT(app.app, authenticate, identity)

    @jwt.jwt_payload_handler
    def make_payload(usuario):
        iat = datetime.datetime.utcnow()
        exp = iat + app.app.config.get('JWT_EXPIRATION_DELTA')
        nbf = iat + app.app.config.get('JWT_NOT_BEFORE_DELTA')
        return {'exp': exp,
                'iat': iat,
                'nbf': nbf,
                'identity': usuario.json['id'],
                'empresa': usuario.json['empresa'],
                'nome': usuario.json['nome']}
    return app
