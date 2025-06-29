import functools
from dataclasses import dataclass

from edgy import Model
from openai import AsyncOpenAI
from pydantic_ai import RunContext
from pydantic_ai.agent import Agent
from pydantic_core import to_json

from .settings import settings


class EmbeddingClient:
    def __init__(self, embedding_model: str):
        self.openai = AsyncOpenAI()
        self.embedding_model = embedding_model

    async def generate(self, messages: list[str]) -> list[list[float]]:
        response = await self.openai.embeddings.create(
            input=messages,
            model=self.embedding_model,
        )
        return [row.embedding for row in response.data]


@dataclass
class Deps:
    embedding_client: EmbeddingClient
    model: type[Model]


class AsyncAgentClient:
    system_prompt_template = """
        You are an assistant to an online store.
        Your job is to answer customer questions about the products available in the store. You can search the list of the most suitable products using search_product.
        Answer as a store assistant, only in Polish.
        Take care of a nice format of your answer, using markdown and blank lines.
    """

    def __init__(self, chat_model: str, embedding_model: str):
        agent = Agent(
            model=chat_model,
            deps_type=Deps,
            system_prompt=self.system_prompt_template,
            output_type=str,
        )
        self.openai = AsyncOpenAI()
        self.chat = agent
        self.embedding_client = EmbeddingClient(embedding_model=embedding_model)
        agent.tool(self.search_product)

    @staticmethod
    async def search_product(context: RunContext[Deps], search_query: str) -> str:
        """
        Search for products based on the search query.
        This method should be implemented to return a formatted string of product lines.
        """
        embeddings = await context.deps.embedding_client.generate(
            messages=[search_query]
        )
        if not embeddings:
            return "No products found."
        embedding_json = to_json(embeddings[0]).decode()
        query = f""" #
            SELECT * FROM {context.deps.model.Meta.tablename}
            ORDER BY embedding <-> CAST(:embedding_json AS vector)
            LIMIT 5
        """  # nosec B608
        products = await context.deps.model.query.database.fetch_all(
            query, values={"embedding_json": embedding_json}
        )
        products = [context.deps.model.from_orm(product) for product in products]
        return "\n".join(product.metadata for product in products)

    async def ask(
        self, model: type[Model], message: str, history: list[str] | None
    ) -> str:
        deps = Deps(embedding_client=self.embedding_client, model=model)
        response = await self.chat.run(message, deps=deps, message_history=history)
        return response.output

    async def generate_embeddings(self, metadata: list[str]) -> list[list[float]]:
        return await self.embedding_client.generate(messages=metadata)


@functools.cache
def get_agent_client() -> AsyncAgentClient:
    """
    Initialize and return an instance of AgentClient with the configured OpenAI client.
    """
    return AsyncAgentClient(
        chat_model=settings.chat_model, embedding_model=settings.embedding_model
    )
