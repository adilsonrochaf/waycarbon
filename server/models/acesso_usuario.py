from datetime import datetime

from marshmallow import fields
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from server import db, ma
from server.models.dominio import DominioSchema


class AcessoUsuario(db.Model):
    __tablename__ = "tb_acesso_usuario"

    id = Column(Integer, primary_key=True)
    id_usuario = Column(ForeignKey("tb_usuario.id"))
    acesso = Column(DateTime, default=datetime.now)


class AcessoUsuarioSchema(ma.ModelSchema):

    class Meta:
        fields = (
            "id",
            "id_usuario",
            "acesso"
        )

