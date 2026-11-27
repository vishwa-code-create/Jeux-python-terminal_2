from abc import ABC
from typing import Dict


class Item(ABC):
    def __init__(
        self,
        name: str,
        description: str,
        dropRate: int,
        rarity: str,
        item_type: str,
        stats: Dict[str, int] = None,
    ) -> None:
        self.name: str = name
        self.description: str = description
        self.dropRate: int = dropRate
        self.rarity: str = rarity
        self.item_type: str = item_type
        self.stats: Dict[str, int] = stats if stats is not None else {}

    def __str__(self) -> str:
        """Affichage propre de l'objet dans l'inventaire ou les loots."""
        return f"{self.name} ({self.rarity}) - {self.description}"