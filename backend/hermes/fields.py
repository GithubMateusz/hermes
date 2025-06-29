from typing import Any

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

    def check(self, name: str, value: Any) -> Any:
        if value is None:
            return None
        if not isinstance(value, list | tuple):
            raise ValueError(f"Value for {name} must be a list or tuple of floats")
        if len(value) != self.dimensions:
            raise ValueError(f"Vector length for {name} must be {self.dimensions}")
        return value

    def clean(self, name: str, value: Any, for_query: bool = False) -> dict[str, Any]:
        """
        Converts a field value via check method to a column value.
        """
        return {name: self.check(name, value)}


class VectorFieldFactory(FieldFactory):
    field_bases = (VectorBaseField,)

    @classmethod
    def __new__(cls, *args, **kwargs):
        return VectorBaseField(**kwargs)
