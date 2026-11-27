from typing import List
from character import Character
from item import Item


class Player:
    def __init__(self, name: str = "Joueur") -> None:
        self.name: str = name
        self.score: int = 0
        self.team: List[Character] = []
        self.inventory: List[Item] = []

    def CreateTeam(self) -> None:
        """Permet de constituer l'équipe du joueur (3 personnages)."""
        self.team.clear()

        for i in range(3):
            nom_perso = input(f"Nom du personnage {i + 1} : ")
            perso = Character(name=nom_perso)
            self.team.append(perso)

    def PickCharacter(self) -> Character:
        """Affiche les personnages vivants et renvoie celui choisi par le joueur."""
        persos_vivants = [perso for perso in self.team if perso.IsAlive()]
        
        for index, perso in enumerate(persos_vivants):
            print(f"{index + 1}. {perso}")
            
        choix = int(input("Choisis un personnage (numéro) : ")) - 1
        return persos_vivants[choix]

    def IsTeamAlive(self) -> bool:
        """Renvoie True si au moins un personnage de l'équipe est en vie."""
        return any(perso.IsAlive() for perso in self.team)

    def CheckInventory(self) -> None:
        """Affiche le contenu de l'inventaire du joueur."""
        if not self.inventory:
            print("Ton inventaire est vide.")
            return
            
        print("--- Inventaire ---")
        for index, item in enumerate(self.inventory):
            print(f"{index + 1}. {item}")

    def UseItem(self, item: Item) -> None:
        """Utilise un objet de l'inventaire sur un personnage de l'équipe."""
        if item in self.inventory:
            cible = self.PickCharacter()
            item.Use(cible)
            self.inventory.remove(item)
        else:
            print("Cet objet n'est pas dans ton inventaire.")

    def __str__(self) -> str:
        """Affichage propre du joueur lors d'un print(player)."""
        return f"Joueur : {self.name} | Score : {self.score} | Équipe : {len(self.team)} persos | Inventaire : {len(self.inventory)} objets"
