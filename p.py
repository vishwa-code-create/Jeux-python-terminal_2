import sys
from pymongo import MongoClient
import random
from typing import List



class Game:
    def __init__(self, mongo_uri: str = "mongodb://localhost:27017/") -> None:
        self.player: Player = Player()
        self.mongoClient: MongoClient = MongoClient(mongo_uri)
        self.db = self.mongoClient["rpg_game"]
        self.vague: Vague = Vague()

    def SaveGame(self) -> None:
        """sauvegarde les données du joueur et la vague actuelle dans MongoDB."""
        save_data = {
            "player_name": self.player.name,
            "score": self.player.score,
            "vague_actuelle": self.vague.vague_actuelle,
            
        }
        self.db["saves"].update_one(
            {"player_name": self.player.name},
            {"$set": save_data},
            upsert=True
        )

    def LoadGame(self) -> None:
        """affiche la vue de chargement et récupère une sauvegarde depuis MongoDB."""
        Affichage.DisplayVue(Vue.VueChargerSauvegarde)
        save_data = self.db["saves"].find_one({"player_name": self.player.name})
        if save_data:
            self.player.score = save_data.get("score", 0)
            self.vague.vague_actuelle = save_data.get("vague_actuelle", 1)
        else:
            Affichage.ShowError("Aucune sauvegarde trouvée.")

    def LaunchGame(self) -> None:
        """gère le démarrage, la création d'équipe et l'enchaînement des vagues."""
        Affichage.DisplayVue(Vue.VueEcranTitre)
        self.player.CreateTeam()

        while self.player.IsTeamAlive():
            self.vague.PickEnemies(self.vague)
            self.vague.PlayVague()

        Affichage.DisplayVue(Vue.VueGameOver)
        self.SaveGame()

    def ShowLeaderboard(self) -> None:
        """récupère les meilleurs scores sur MongoDB et affiche le classement."""
        scores = list(self.db["saves"].find().sort("score", -1).limit(10))
        Affichage.DisplayVue(lambda: Vue.VueLeaderboard(scores))

    def Exit(self) -> None:
        """affiche l'écran de sortie, ferme MongoDB et arrête le programme."""
        Affichage.DisplayVue(Vue.VueQuitter)
        self.mongoClient.close()
        sys.exit(0)



class Vague:
    def __init__(self) -> None:
        self.vague_actuelle: int = 1
        self.monsters: List[Enemy] = []


    def PickEnemies(self, vague: "Vague") -> None:
        """Sélectionne et génère les ennemis en fonction de la difficulté de la vague."""
        difficulte = vague.GetDifficulty()
        self.monsters.clear()
        
        # Génère un nombre d'ennemis proportionnel à la difficulté
        nb_ennemis = random.randint(1, 2 + difficulte)
        for _ in range(nb_ennemis):
            # Crée une instance d'Enemy (à adapter selon le constructeur de votre classe Enemy)
            ennemi = Enemy()
            self.monsters.append(ennemi)


    # methode PlayVague(self) -> None
    # afficher un message de debut de vague avec Affichage
    # boucler tant qu'il reste au moins un monstre vivant dans self.monsters (monster.IsAlive())
        # parcourir les monstres vivants
        # gerer les tours d'attaque entre le joueur et les monstres
    # afficher que la vague est finie
    # ajouter 1 a self.vague_actuelle


    # methode GetDifficulty(self) -> int
    # calculer et renvoyer la difficulte selon vague_actuelle (par ex return self.vague_actuelle)
