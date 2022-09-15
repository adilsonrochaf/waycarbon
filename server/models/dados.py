from datetime import datetime

from marshmallow import fields
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON

from server import db, ma
from server.models.dominio import DominioSchema


class Dados(db.Model):
    __tablename__ = "tb_dados"

    id = Column(Integer, primary_key=True)
    dados = Column(JSON)
    id_empresa = Column(ForeignKey("tb_dominio.id"))

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class DadosSchema(ma.ModelSchema):

    class Meta:
        fields = (
            "id",
            "dados",
            "id_empresa",
            "created_at"
        )

