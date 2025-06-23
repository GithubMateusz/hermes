import edgy
import sqlalchemy
from edgy.core.db.fields.base import BaseField
from edgy.core.db.fields.factories import FieldFactory
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column

from .db import get_db_connection

registry = get_db_connection()


class VectorBaseField(BaseField):
    def __init__(self, **kwargs):
        self.dimensions = kwargs.pop("dimensions")
        self.column_type = Vector(self.dimensions)
        self.inject_default_on_partial_update = False
        super().__init__(**kwargs)

    def get_columns(self, field_name):
        return [Column(field_name, self.column_type)]

    def clean(self, field_name, value, to_query=False):
        if value is None:
            return None
        if not isinstance(value, list | tuple):
            raise ValueError(
                f"Value for {field_name} must be a list or tuple of floats"
            )
        if len(value) != self.dimensions:
            raise ValueError(
                f"Vector length for {field_name} must be {self.dimensions}"
            )
        return value


class VectorFieldFactory(FieldFactory):
    field_bases = (VectorBaseField,)

    @classmethod
    def __new__(cls, *args, **kwargs):
        return VectorBaseField(**kwargs)


class Product(edgy.Model):
    name: str = edgy.CharField(max_length=255)
    description: str = edgy.TextField()
    price: float = edgy.FloatField()
    category: str = edgy.CharField(max_length=100)
    material: str = edgy.CharField(max_length=255)
    color: str = edgy.CharField(max_length=255)
    tags: list[str] = edgy.PGArrayField(sqlalchemy.String(), default=list)
    sizes: list[int] = edgy.PGArrayField(sqlalchemy.Integer(), default=list)

    embedding: list[float] | None = VectorFieldFactory(dimensions=1536, null=True)

    class Meta:
        registry = registry
        tablename = "product"
        unique_together = [("name", "category", "color", "material")]
