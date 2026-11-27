from equipable import Equipable
from entity import Entity
from typing import List, Optional



class Character(Entity):
    def __init__(self, name: str, maxHp: int = 100, attack: int = 10, defense: int = 5) -> None:

        self._base_attack: int = attack
        self._base_defense: int = defense
        self.equipement: List[Equipable] = []
        super().__init__(name, maxHp, attack, defense)

  
    @property
    def attack(self) -> int:
        """Calcule l'attaque totale (attaque de base + bonus des équipements)."""
        bonus_atk = sum(getattr(item, "attack_bonus", 0) for item in self.equipement)
        return self._base_attack + bonus_atk

    @attack.setter
    def attack(self, value: int) -> None:
        self._base_attack = value

    @property
    def defense(self) -> int:
        """Calcule la défense totale (défense de base + bonus des équipements)."""
        bonus_def = sum(getattr(item, "defense_bonus", 0) for item in self.equipement)
        return self._base_defense + bonus_def

    @defense.setter
    def defense(self, value: int) -> None:
        self._base_defense = value


    def EquipItem(self, item: Equipable) -> None:
        """Équipe un objet si l'emplacement (slot) est libre."""
        if self.IsSlotAvailable(item.slot):
            self.equipement.append(item)
        else:
            print(f"L'emplacement {item.slot} est déjà occupé.")

    def UnequipItem(self, item: Equipable) -> None:
        """Retire un objet équipé."""
        if item in self.equipement:
            self.equipement.remove(item)

    def IsSlotAvailable(self, slot_name: str) -> bool:
        """Renvoie True si aucun équipement n'occupe déjà ce slot."""
        return self.GetEquipment(slot_name) is None

    def GetEquipment(self, slot_name: str) -> Optional[Equipable]:
        """Renvoie l'objet équipé sur ce slot, ou None s'il est vide."""
        for item in self.equipement:
            if item.slot == slot_name:
                return item
        return None


    def ProjectDamage(self, target: Entity) -> int:
        """Calcule et renvoie les dégâts estimés contre une cible sans l'attaquer."""
        return max(1, self.attack - target.defense)

    def PlayTurn(self, target: Entity = None) -> None:
        """Redéfinition (<<override>>) du tour de jeu du personnage."""
        if target is not None and target.IsAlive():
            self.Attack(target)
