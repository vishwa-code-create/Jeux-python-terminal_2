import random
from typing import List
from enemy import Enemy


class Vague:
    def __init__(self) -> None:
        self.vague_actuelle: int = 1
        self.monsters: List[Enemy] = []

    def PickEnemies(self, vague: "Vague") -> None:
        """Génère 3 ennemis adaptés à la difficulté de la vague."""
        difficulte = vague.GetDifficulty()
        self.monsters.clear()
        
        for _ in range(3):
            ennemi = Enemy()
            ennemi.maxHp += difficulte * 10
            ennemi.hp = ennemi.maxHp
            ennemi.attack += difficulte * 2
            self.monsters.append(ennemi)

    def PlayVague(self) -> None:
        """Déroule le combat de la vague tant que des monstres sont en vie."""
        print(f"--- Début de la vague {self.vague_actuelle} ---")
        
        while any(monster.IsAlive() for monster in self.monsters):
            for monster in self.monsters:
                if monster.IsAlive():
                    monster.PlayTurn()
            break  

        print(f"Vague {self.vague_actuelle} terminée !")
        self.vague_actuelle += 1

    def GetDifficulty(self) -> int:
        """Calcule et renvoie le niveau de difficulté selon le numéro de la vague."""
        return self.vague_actuelle
