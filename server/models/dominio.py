from datetime import datetime

from sqlalchemy import Column, Integer, Text, DateTime

from server import db, ma


class Dominio(db.Model):
    __tablename__ = "tb_dominio"

    id = Column(Integer, primary_key=True)
    nm_dominio = Column(Text)
    tp_dominio = Column(Text)
    origem_dominio = Column(Text)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class DominioSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "id",
            "nm_dominio",
            "tp_dominio",
            "origem_dominio"
        )

