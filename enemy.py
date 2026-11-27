import random
from typing import List
from entity import Entity
from item import Item


class Enemy(Entity):
    def __init__(self, name: str, maxHp: int, attack: int, defense: int, dropables: List[Item] = None) -> None:
        # Appelle le constructeur de la classe mère Entity
        super().__init__(name, maxHp, attack, defense)
        self.dropables: List[Item] = dropables if dropables is not None else []

    def DropLoot(self) -> List[Item]:
        """Sélectionne et renvoie les objets lâchés par l'ennemi à sa mort."""
        loot: List[Item] = []
        for item in self.dropables:
            
            if random.random() < 0.5:
                loot.append(item)
        return loot

    def PlayTurn(self, target: Entity = None) -> None:
        """Redéfinition (<<override>>) du tour de jeu pour l'ennemi."""
        if target is not None and target.IsAlive():
            self.Attack(target)
