import datetime

import edgy
import sqlalchemy as sa
from pydantic import ConfigDict

from .db import get_db_connection
from .fields import VectorFieldFactory

registry = get_db_connection()


def now():
    """Returns the current datetime in UTC."""
    return datetime.datetime.now(tz=datetime.UTC)


class Product(edgy.Model):
    model_config = ConfigDict(from_attributes=True)

    name: str = edgy.CharField(max_length=255)
    description: str = edgy.TextField()
    price: float = edgy.FloatField()
    category: str = edgy.CharField(max_length=100)
    material: str = edgy.CharField(max_length=255)
    color: str = edgy.CharField(max_length=255)
    tags: list[str] = edgy.PGArrayField(sa.String(), default=list)
    sizes: list[int] = edgy.PGArrayField(sa.Integer(), default=list)

    embedding: list[float] | None = VectorFieldFactory(dimensions=1536, null=True)

    created_at: datetime.datetime = edgy.DateTimeField(
        auto_now_add=True, default=now, server_default=sa.func.now()
    )
    updated_at: datetime.datetime = edgy.DateTimeField(
        auto_now=True, default=now, server_default=sa.func.now()
    )

    def __str__(self):
        return "\n".join(
            [
                f"{key.capitalize()}: {value}"
                for key, value in self.dict(
                    exclude={"id", "tags", "embedding", "created_at", "updated_at"}
                ).items()
            ]
        )

    @property
    def metadata(self) -> str:
        return "\n".join(
            [
                f"{key}: {value}"
                for key, value in self.dict(
                    exclude={"id", "embedding", "created_at", "updated_at"}
                ).items()
            ]
        )

    class Meta:
        registry = registry
        tablename = "product"
        unique_together = [("name", "category", "color", "material")]
