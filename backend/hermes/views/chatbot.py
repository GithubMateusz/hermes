from esmerald import Injects, WebSocket, post, websocket
from esmerald.openapi.datastructures import OpenAPIResponse
from esmerald.routing.apis.views import APIView

from hermes.agent import AsyncAgentClient
from hermes.dependencies import dependencies
from hermes.logger import logger
from hermes.models import Product
from hermes.schemas import ChatResponse, UserMessage


class ChatBotView(APIView):
    path = "/chatbot"

    @post(
        path="/one",
        dependencies=dependencies,
        summary="Chat one message",
        responses={
            200: OpenAPIResponse(
                model=ChatResponse, description="Response from the chatbot"
            )
        },
    )
    async def one(
        self, data: UserMessage, agent: AsyncAgentClient = Injects()
    ) -> ChatResponse:
        """
        Handle a single message from the user and return a response.
        """
        reply, _ = await agent.ask(model=Product, message=data.message, history=None)
        return ChatResponse(response=reply)

    @websocket(path="/socket", dependencies=dependencies)
    async def chatbot(
        self, socket: WebSocket, agent: AsyncAgentClient = Injects()
    ) -> None:
        """
        Handle a websocket connection for the chatbot.
        """
        await socket.accept()
        history: list[str] = []
        while True:
            try:
                logger.info("Waiting for message...")
                message = await socket.receive_text()
                reply, messages = await agent.ask(
                    model=Product, message=message, history=history
                )
                await socket.send_text(reply)
                history.extend(messages)
            except Exception as e:
                logger.exception("Error in chatbot websocket", exc_info=e)
                await socket.close()
                break
