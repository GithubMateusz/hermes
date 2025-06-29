from typing import Annotated

from esmerald import Body, Inject, Injects, WebSocket, get, post, websocket
from esmerald.routing.apis.views import APIView

from .agent import AsyncAgentClient, get_agent_client
from .logger import logger
from .models import Product
from .schemas import ChatResponse, CreateProduct, UserMessage

dependencies = {"agent": Inject(get_agent_client)}


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

    @post(path="/embeddings", dependencies=dependencies)
    async def embeddings(self, agent: AsyncAgentClient = Injects()) -> None:
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


class ChatBotView(APIView):
    path = "/chatbot"

    @post(path="/one", dependencies=dependencies)
    async def one_view(
        self, data: UserMessage, agent: AsyncAgentClient = Injects()
    ) -> ChatResponse:
        reply = await agent.ask(model=Product, message=data.message, history=None)
        return ChatResponse(response=reply)

    @websocket(path="/socket", dependencies=dependencies)
    async def chatbot_view(
        self, socket: WebSocket, agent: AsyncAgentClient = Injects()
    ) -> None:
        await socket.accept()
        logger.info("Waiting for message...")
        history: list[str] = []
        while True:
            try:
                logger.info("Waiting for message...")
                message = await socket.receive_text()
                reply = await agent.ask(model=Product, message=message, history=history)
                await socket.send_text(reply)
                history.append(message)
                history.append(reply)
            except Exception as e:
                logger.exception("Error in chatbot websocket", exc_info=e)
                await socket.close()
                break
