from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    description: str
    price: float
    category: str
    material: str
    color: str
    tags: list[str] = []
    sizes: list[int] = []
