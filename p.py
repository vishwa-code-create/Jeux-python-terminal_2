class Entity:
    pass


class Enemy(Entity):
    pass


class Character(Entity):
    def __init__(self) -> None:
        self.equipement: list[Equipable] = []


class Item:
    pass


class Equipable(Item):
    pass


class Consumable(Item):
    pass


class Game:
    def __init__(self) -> None:
        self.player: Player | None = None
        self.vague: Vague | None = None


class Vague:
    def __init__(self) -> None:
        self.monsters: list[Enemy] = []


class Player:
    def __init__(self) -> None:
        self.team: list[Character] = []
        self.inventory: list[Item] = []


class Affichage:
    def utilise(self, game: Game) -> None:
        pass

    def affiche(self, vue: Vue) -> None:
        pass


class Vue:
    pass

 