from uuid import UUID
from pydantic import BaseModel, Field


class Offer(BaseModel):
    id: UUID = Field(..., description="Unique identifier for the offer")
    price: float = Field(
        ..., description="Price of the offer in the smallest currency unit, e.g., cents"
    )
    items_in_stock: int = Field(..., description="Number of items in stock for this offer")

    def normalize(self):
        return {
            "id": str(self.id),
            "price": self.price,
            "items_in_stock": self.items_in_stock,
        }

    @classmethod
    def denormalize(cls, data):
        return cls(
            id=UUID(data["id"]),
            price=int(data["price"]),
            items_in_stock=int(data["items_in_stock"]),
        )
