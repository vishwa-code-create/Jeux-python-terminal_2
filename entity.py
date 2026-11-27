from abc import ABC, abstractmethod


class Entity(ABC):
    def __init__(self, name: str, maxHp: int, attack: int, defense: int) -> None:
        self.name: str = name
        self.maxHp: int = maxHp
        self.hp: int = maxHp
        self.attack: int = attack
        self.defense: int = defense

    def IsAlive(self) -> bool:
        """Renvoie True si l'entité a encore des points de vie."""
        return self.hp > 0

    def TakeDamage(self, amount: int) -> None:
        """Réduit les points de vie de l'entité en tenant compte de sa défense."""
        degats_reels = max(1, amount - self.defense)
        self.hp = max(0, self.hp - degats_reels)

    def Heal(self, amount: int) -> None:
        """Soigne l'entité sans dépasser ses points de vie maximums (maxHp)."""
        self.hp = min(self.maxHp, self.hp + amount)

    def Attack(self, target: "Entity") -> None:
        """Attaque une cible (Character ou Enemy)."""
        target.TakeDamage(self.attack)

    @abstractmethod
    def PlayTurn(self) -> None:
        """Méthode abstraite obligatoirement redéfinie dans Character et Enemy."""
        raise NotImplementedError("Cette méthode doit être redéfinie dans les classes filles.")


    # Ajout de entity.py, demo.py, vue.py et affichage.py ( pour le push de toute a l'heure )

    
