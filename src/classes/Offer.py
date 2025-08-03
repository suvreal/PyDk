from uuid import UUID
from typing import List
from pydantic import BaseModel, Field
from collections.abc import Iterable

from src.client.httpx.http_client_interface import HTTPResponse


class Offer(BaseModel):
    id: UUID = Field(..., description="Unique identifier for the offer")
    price: float = Field(
        ..., description="Price of the offer in the smallest currency unit, e.g., cents"
    )
    items_in_stock: int = Field(..., description="Number of items in stock for this offer")

    def normalize(self) -> dict[str, str | float | int]:
        return {
            "id": str(self.id),
            "price": self.price,
            "items_in_stock": self.items_in_stock,
        }

    @classmethod
    def denormalize(cls, data) -> "Offer":
        return cls(
            id=UUID(data["id"]),
            price=int(data["price"]),
            items_in_stock=int(data["items_in_stock"]),
        )

    @classmethod
    def from_response(cls, response: HTTPResponse) -> List["Offer"]:
        data = response.get("data")
        if not isinstance(data, Iterable):
            raise ValueError("Attribute 'data' is not iterable!")

        offers: List[Offer] = []
        for offer in data:
            offers.append(
                cls(
                    id=UUID(offer.get("id")),
                    price=offer.get("price"),
                    items_in_stock=offer.get("items_in_stock"),
                )
            )

        return offers
