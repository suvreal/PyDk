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

    @classmethod
    def denormalize(cls, data):
        return cls(
            id=UUID(data["id"]),
            name=str(data["name"]),
            description=str(data["description"]),
            offers=List(data["offers"]),
        )
