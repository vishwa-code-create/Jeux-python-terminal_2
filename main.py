from pymongo import MongoClient
import os

from game import combat_a_mort, create_team, afficher_game_over
from utils import get_user_choice_from_options, get_username, recuperer_choix_utilisateur

MENU = ["Jouer", "Leaderboard", "Quitter"]


def choix_menu():
	# Recuperer le choix utilisateur valide depuis la liste MENU
	message = "Veuillez choisir une option :"
	return get_user_choice_from_options(MENU, message)


def lancer_processus(choix):
	if choix == 1:
		lancer_jeu()
		pass
	elif choix == 2:
		# Afficher le leaderboard
		pass
	elif choix == 3:
		# Quitter le programme
		pass


def main():
	choix = choix_menu()
	lancer_processus(choix)


def lancer_jeu():
	db = connect_db()
	pseudo = get_username(db)
	heros_disponibles = recuperer_all_heroes(db)
	monstres = recuperer_all_monsters(db)
	equipe = create_team(heros_disponibles)
	score = combat_a_mort(equipe, monstres)
	afficher_game_over(equipe, score)
	enregistrer_resultat_combat(db, pseudo, score)


def enregistrer_resultat_combat(db, pseudo, score):
	db["scores"].insert_one({
		"player_name": pseudo,
		"waves": score
	})


def recuperer_all_heroes(db):
	return list(db["characters"].find())


def recuperer_all_monsters(db):
	return list(db["monsters"].find())


def connect_db():
	client = MongoClient(os.getenv("MONGO_URL"))
	return client["game_db"]


# Lancer le processus choisi

choix = recuperer_choix_utilisateur(["Option 1", "Option 2", "Option 3"])
print(f"Vous avez choisi l'option {choix}")