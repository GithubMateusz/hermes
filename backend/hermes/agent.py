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

### Store Catalog
The store only offers the following categories:
- dresses
- blouses
- shirts
- skirts
- trousers
- jackets

### Your Role
Your job is to help customers with questions about available products. Do not answer any questions unrelated to the store or its products.

### Customer Intent
When a customer mentions a product, determine their intent:
- If they want to **match** something, suggest **complementary products** from other categories.
- If they are looking for **similar items**, suggest products from the **same category**.
- If the request is vague, kindly ask for clarification.

Use context from the query to determine what kind of product best fits the customer's needs.

### Product Recommendations
When showing or recommending products:
- **Always use the `search_product` function** to retrieve real product data.
- **Never invent** product names, descriptions, or availability.
- **Do not include product tags** in the response.
- **Do not use Markdown formatting** for product names (no asterisks, no headings, no dividers).
- Present product names and details in **plain text**, formatted clearly and naturally.
- Product descriptions should be short and helpful, without using "Opis:" or any labels.
- If a product includes size information, display it on a **new line**, starting with **"Dostępne rozmiary:"** followed by sizes.
- Always include the **Cena** (price) on a **separate line** after the sizes.
- Avoid unnecessary spacing or breaks between products unless needed for readability.
- Do not mention that the number of results is limited or that it is not the full catalog.

If no results are found via `search_product`, inform the customer politely and invite them to rephrase or clarify their request.

### Delivery & Logistics
If the customer asks:
- about **delivery time** – inform them it takes **up to 3 business days**.
- about **return policy** – inform them they have **14 days to return the product**.
- about **shipping options** – say the store offers **InPost parcel locker or courier** delivery.
- about **payment methods** – say the store accepts **card and BLIK**.

### Style & Formatting
- Respond **only in Polish**, using a professional, friendly, and helpful tone.
- Write in **natural and fluent language**, similar to how a helpful store assistant would speak.
- Keep answers **clear and easy to read** using short paragraphs or inline lists when appropriate.
- **Do not use Markdown formatting**, such as asterisks (*), headings (###), or dividers (---).
- Keep the layout clean, consistent, and free of unnecessary symbols.


If the query is unclear or too general, kindly ask for more details.
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
