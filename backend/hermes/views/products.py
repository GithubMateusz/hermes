from typing import Annotated

from esmerald import Body, Injects, delete, get, post, status
from esmerald.openapi.datastructures import OpenAPIResponse
from esmerald.routing.apis.views import APIView

from hermes.agent import AsyncAgentClient
from hermes.dependencies import dependencies
from hermes.models import Product
from hermes.schemas import CreateProduct, ResponseProduct


class ProductView(APIView):
    path = "/products"

    @get(
        path="/",
        summary="List all products",
        responses={200: OpenAPIResponse(model=[ResponseProduct])},
    )
    async def list_products(
        self,
    ) -> list[ResponseProduct]:
        """
        List all products in the database.
        """
        return [
            ResponseProduct.model_validate(item) for item in await Product.query.all()
        ]

    @post(
        path="/",
        summary="Create a new product",
        responses={201: OpenAPIResponse(model=ResponseProduct)},
        status_code=status.HTTP_201_CREATED,
    )
    async def create_product(self, data: CreateProduct) -> ResponseProduct:
        """
        Create a new product in the database.
        """
        return ResponseProduct.model_validate(
            await Product.query.create(**data.model_dump())
        )

    @post(
        path="/bulk",
        summary="Bulk create products",
        status_code=status.HTTP_201_CREATED,
    )
    async def bulk_create_products(
        self, data: Annotated[list[CreateProduct], Body(embed=False)]
    ) -> None:
        """
        Bulk create products in the database.
        """
        products = [item.model_dump() for item in data]
        await Product.query.bulk_create(products)

    @delete(
        path="/{product_id}",
        summary="Delete product",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def delete_product(self, product_id: int) -> None:
        """
        Delete a product by its ID.
        """
        await Product.query.filter(id=product_id).delete()

    @delete(
        path="/all",
        summary="Delete all products",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def delete_all_products(self) -> None:
        """
        Delete all products from the database.
        """
        await Product.query.delete()

    @post(
        path="/embedding",
        dependencies=dependencies,
        summary="Generate embeddings for products",
    )
    async def embedding(self, agent: AsyncAgentClient = Injects()) -> None:
        """
        Generate embeddings for products that do not have them yet.
        """
        products: list[Product] = await Product.query.filter(
            Product.columns.embedding.is_(None)
        )
        if products:
            embeddings = await agent.generate_embeddings(
                metadata=[product.metadata for product in products]
            )
            for product, embedding in zip(products, embeddings, strict=False):
                product.embedding = embedding
            await Product.query.bulk_update(products, fields=["embedding"])
