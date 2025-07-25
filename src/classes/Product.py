from uuid import UUID
from typing import List
from pydantic import BaseModel, Field
from src.classes.Offer import Offer


class Product(BaseModel):
    id: UUID = Field(...)
    name: str = Field(...)
    description: str = Field(...)
    offers: List[Offer] = Field(default_factory=list)

    def normalize(self) -> dict[str, str]:
        return {"id": str(self.id), "name": self.name, "description": self.description}

    def set_offers(self, offers: List[Offer]):
        self.offers = offers

    @classmethod
    def denormalize(cls, data):
        return cls(
            id=UUID(data["id"]),
            name=str(data["name"]),
            description=str(data["description"]),
            offers=[Offer(**o) for o in data["offers"]],
        )

    @classmethod
    def from_response(cls, response: dict, product: "Product") -> "Product":
        data = response.get("data")
        if data is None:
            raise ValueError("Missing 'data' in response")

        return cls(
            id=UUID(data.get("id")),
            name=product.name,
            description=product.description,
        )
