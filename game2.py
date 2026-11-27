import sys
from pymongo import MongoClient




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





