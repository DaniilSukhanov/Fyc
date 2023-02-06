import datetime
import sqlalchemy as sa
from sqlalchemy.orm import InstrumentedAttribute
from .database import SqlAlchemyBase


class Cars(SqlAlchemyBase):
    __tablename__ = "cars"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    fuel_tank_volume = sa.Column(sa.Integer)
    consumption_petrol = sa.Column(sa.Float)
    power = sa.Column(sa.Integer)
    max_speed = sa.Column(sa.Integer)
    assembly_country = sa.Column(sa.String)
    images = sa.Column(sa.String)
    name_car = sa.Column(sa.String)

    def get_all_parameters(self):
        cls = self.__class__
        result = dict()
        for attr in self.__dict__:
            if type(getattr(cls, attr, None)) is InstrumentedAttribute:
                result[attr] = getattr(self, attr)
        return result
