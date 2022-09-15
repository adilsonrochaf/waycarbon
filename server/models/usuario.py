from datetime import datetime

from marshmallow import fields
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from server import db, ma
from server.models.dominio import DominioSchema


class Usuario(db.Model):
    __tablename__ = "tb_usuario"

    id = Column(Integer, primary_key=True)
    nome = Column(Text)
    senha = Column(Text)
    email = Column(Text)
    status = Column(Text)
    id_empresa = Column(ForeignKey("tb_dominio.id"))
    empresa = relationship('Dominio', foreign_keys=[id_empresa])

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class UsuarioSchema(ma.ModelSchema):
    empresa = fields.Nested(DominioSchema)

    class Meta:
        fields = (
            "id",
            "nome",
            "senha",
            "status",
            "empresa",
            "email",
            "created_at"
        )

