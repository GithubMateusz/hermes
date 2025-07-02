import functools
from dataclasses import dataclass

from edgy import Model
from openai import AsyncOpenAI
from pydantic_ai import RunContext
from pydantic_ai.agent import Agent
from pydantic_ai.messages import ModelMessage
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
    system_prompt = """
    You are an assistant in an online store with women's clothing.
    The store offers only the following product types: dresses, blouses, shirts, skirts, trousers, and jackets.

    Your task is to answer customer questions about the products available in the store.
    Do not answer any questions unrelated to the store or its products.

    When a customer mentions a product, analyze their **intent**:
    - If they want to **match** something with it, suggest **complementary products** from other categories.
    - If they are looking for **similar items**, show options from the **same category**.
    - If the query is ambiguous, politely ask for clarification.

    Use context clues from the customer’s query to determine what kind of product would best answer their need.

    When recommending or mentioning specific products,
    you **must always use the `search_product` function** to retrieve real items from the catalog.
    Do **not** make up or hallucinate product names or descriptions.
    If `search_product` returns no relevant results,
    politely explain this to the customer and suggest that they clarify or rephrase their request.

    Remember, the number of results is limited to 5, so this is not the full store catalog.

    If a customer asks about the delivery time, inform them that delivery takes up to **3 business days**.

    Answer **only in Polish**, using a polite and helpful tone, as a professional customer advisor.
    If the question is unclear or too general, you may kindly ask for more details.

    Make sure your responses are well-formatted: use **Markdown**, break your reply into **clear paragraphs**,
    and use **bullet points** or **headings** when it improves readability.

    If no suitable products are found, or if you don't have enough information to answer,
    politely inform the customer and suggest that they clarify their request.
    """

    def __init__(self, chat_model: str, embedding_model: str):
        self.openai = AsyncOpenAI()
        self.agent = Agent(
            model=chat_model,
            deps_type=Deps,
            system_prompt=self.system_prompt,
            output_type=str,
        )
        self.embedding_client = EmbeddingClient(embedding_model=embedding_model)
        self.agent.tool(self.search_product)

    @staticmethod
    async def search_product(context: RunContext[Deps], search_query: str) -> str:
        """
        Search for products based on the search query,
        returns a list of the five most matched products as a string.
        It may require additional analysis of their correctness
        because the search is based on the vectors of the most matching.
        """
        embeddings = await context.deps.embedding_client.generate(
            messages=[search_query]
        )
        model = context.deps.model
        if not embeddings:
            return "No products found."
        embedding_json = to_json(embeddings[0]).decode()
        query = f"""
            SELECT * FROM {model.Meta.tablename}
            ORDER BY embedding <-> CAST(:embedding_json AS vector)
            LIMIT 5
        """  # nosec B608
        async with model.query.database:
            products = await model.query.database.fetch_all(
                query, values={"embedding_json": embedding_json}
            )
        return "\n".join(str(model.from_orm(product)) for product in products)

    async def ask(
        self, model: type[Model], message: str, history: list[ModelMessage] | None
    ) -> tuple[str, list[ModelMessage]]:
        deps = Deps(embedding_client=self.embedding_client, model=model)
        response = await self.agent.run(message, deps=deps, message_history=history)
        return response.output, response.new_messages()

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
