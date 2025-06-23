from typing import Annotated

from esmerald import Body, get, post
from esmerald.routing.apis.views import APIView

from .models import Product
from .schemas import CreateProduct


class ProductView(APIView):
    path = "/products"

    @get(path="/")
    async def list_data(
        self,
    ) -> list[Product]:
        return await Product.query.all()

    @post(path="/")
    async def create(self, data: CreateProduct) -> Product:
        return await Product.query.create(**data.model_dump())

    @post(path="/bulk")
    async def bulk_create(
        self, data: Annotated[list[CreateProduct], Body(embed=False)]
    ) -> list[Product]:
        products = [item.model_dump() for item in data]
        return await Product.query.bulk_create(products)
