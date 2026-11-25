from time import sleep
import copy
from random import choice
from rich.console import Console
from rich.layout import Layout

from utils import create_panel, get_user_choice_from_options, recuperer_choix_utilisateur

LAYOUT = Layout()
console = Console()

TAILLE_MAX_EQUIPE = 3
LAYOUT.split_row(
    Layout(name="left", ratio=2),
    Layout(name="center", ratio=3),  # Le centre sera 3 fois plus grand
    Layout(name="right", ratio=2)   # La droite sera 2 fois plus grande
)


def afficher_game_over(equipe, score):
	print("Game Over !")
	print(f"Votre équipe a survécu à {score} vagues.")
	print("Statut final de l'équipe :")
	for hero in equipe:
		print(f"{hero['name']} - HP: {hero['hp']}")


def est_entite_en_vie(entite):
	return entite["hp"] > 0


def est_equipe_en_vie(equipe):
	for hero in equipe:
		if est_entite_en_vie(hero):
			return True
	return False


def selectionner_monstre(monstres):
	monstre_choice = choice(monstres)
	return copy.deepcopy(monstre_choice)


def combat_a_mort(equipe, monstres):
	vague = 1
	while est_equipe_en_vie(equipe):
		monstre = selectionner_monstre(monstres)
		victoire = lancer_vague(equipe, monstre)
		if victoire:
			print(f"Victoire pour la vague {vague} !")
			vague += 1
	return vague


def lancer_vague(equipe, monstre):
	while est_entite_en_vie(monstre) and est_equipe_en_vie(equipe):
		evenements = tour_de_vague(equipe, monstre)
		afficher_evenements(evenements, equipe, monstre)
		sleep(1)
	return est_equipe_en_vie(equipe)


def update_layout(equipePanel, monstrePanel, info_panel):
	global LAYOUT
	LAYOUT["left"].update(equipePanel)
	LAYOUT["right"].update(monstrePanel)
	LAYOUT["center"].update(info_panel)


def afficher_evenements(evenements, equipe, monstre):
	console.clear()
	print("\n\n")

	equipePanel = create_panel("Equipe", "\n".join(
		[f"{hero['name']} - HP: {hero['hp']}" for hero in equipe]), "green")
	monstrePanel = create_panel(
		"Monstre", f"{monstre['name']} - HP: {monstre['hp']}", "red")
	info_panel = create_panel("Evenements", "\n".join(evenements), "yellow")

	update_layout(equipePanel, monstrePanel, info_panel)

	console.print(LAYOUT, height=10)


def afficher_stats(equipe, monstre):
	print("-" * 10 + " Stats " + "-" * 10)
	print("Stats de l'equipe :")
	for hero in equipe:
		if not est_entite_en_vie(hero):
			print(f"{hero['name']} est KO")
			continue
		print(f"{hero['name']} - HP: {hero['hp']}")
	print("Stats du monstre :")
	print(f"{monstre['name']} - HP: {monstre['hp']}")
	print("-" * 30)


def tour_de_vague(equipe, monstre):
	evenements = []
	evenements += tour_utilisateur(equipe, monstre)
	if est_entite_en_vie(monstre):
		evenements += tour_monstre(equipe, monstre)
	return evenements


def tour_monstre(equipe, monstre):
	evenements = []
	cible = recuperer_cible(equipe)
	degat = attaquer(monstre, cible)
	evenements.append(
		f"{monstre['name']} inflige {degat} degats a {cible['name']}")
	return evenements


def attaquer(attacker, cible):
	degat = calculer_degats(attacker, cible)
	if degat > cible["hp"]:
		degat = cible["hp"]
	cible["hp"] -= degat
	return degat


def calculer_degats(attacker, cible):
	degat = attacker["attack"] - cible["defense"]
	if degat < 1:
		degat = 1
	return degat


def recuperer_cible(equipe):
	cible_potentielle = recuperer_heros_en_vie(equipe)
	return choice(cible_potentielle)


def recuperer_heros_en_vie(equipe):
	heros_en_vie = []
	for hero in equipe:
		if est_entite_en_vie(hero):
			heros_en_vie.append(hero)
	return heros_en_vie


def tour_utilisateur(equipe, monstre):
	evenements = []
	heros_en_vie = recuperer_heros_en_vie(equipe)
	for hero in heros_en_vie:
		evenements += tour_perso_jouable(hero, monstre)
	return evenements


def tour_perso_jouable(hero, monstre):
	evenements = []
	if est_entite_en_vie(monstre):
		degat = attaquer(hero, monstre)
		evenements.append(
			f"{hero['name']} inflige {degat} degats a {monstre['name']}")
	return evenements


def create_team(heroes):
	equipe = []
	while not equipe_est_complete(equipe):
		afficher_equipe_actuelle(equipe)
		heros_dispo = calculer_heros_disponibles(equipe, heroes)
		options = construire_options(heros_dispo)
		choix = get_user_choice_from_options(options, "Choisissez un héros : ")
		selected_hero = copy.deepcopy(heros_dispo[choix - 1])
		equipe.append(selected_hero)
	return equipe


def equipe_est_complete(equipe):
	if len(equipe) < TAILLE_MAX_EQUIPE:
		return False
	return True


def hero_to_string(hero):
	return f"{hero['name']} - ATK : {hero['attack']} - HP : {hero['hp']} - DEF : {hero['defense']}"


def construire_options(liste_heros_dispo):
	options = []
	for hero in liste_heros_dispo:
		options.append(hero_to_string(hero))
	return options


def calculer_heros_disponibles(equipe, liste_heros):
	heros_disponibles = []
	for hero in liste_heros:
		if hero not in equipe:
			heros_disponibles.append(hero)
	return heros_disponibles


def afficher_personnage(personnage):
	print(hero_to_string(personnage))


def afficher_equipe_actuelle(equipe):
	for i in range(TAILLE_MAX_EQUIPE):
		if i < len(equipe):
			afficher_personnage(equipe[i])
		else:
			print("Vide")


# Besoin la liste des personnages de la DB
def creer_equipe(liste_personnages_db):
	# creer la variable equipe vide
	equipe = []
	# tant que l'equipe n'est pas complete
	while not est_equipe_complete(equipe):
		#     determiner la liste des personnages disponibles
		personnages_disponibles = determiner_personnages_disponibles(
			liste_personnages_db, equipe)
		#     construire la liste des options a afficher disponibles
		options_affichables = construire_options_affichables(personnages_disponibles)
		#     recuperer un choix valide
		choix = recuperer_choix_utilisateur(options_affichables)
		#     ajouter le personnage choisi a l'equipe index = choix - 1
		equipe.append(personnages_disponibles[choix - 1])
	# retourner l'equipe
	return equipe

# construire la liste des options a afficher disponibles


def construire_options_affichables(personnages_disponibles):
	# creer la liste options
	options = []
	# pour chaque personnage dans personnages_disponibles
	for personnage in personnages_disponibles:
		#    ajouter a la liste : f"{personnage["nom"]} - ATK : {personnage["atk"]} - DEF : {personnage["def"]}"
		options.append(
			f"{personnage['nom']} - ATK : {personnage['atk']} - DEF : {personnage['def']}")
	# retourner la liste des options
	return options


def determiner_personnages_disponibles(liste_personnages_db, equipe):
	# creer la liste des personnages disponibles
	personnages_disponibles = []
	# pour chaque personnage dans la liste des personnages de la DB
	for personnage in liste_personnages_db:
		#     si le personnage n'est pas dans l'equipe
		if personnage not in equipe:
			#         l'ajouter a la liste des personnages disponibles
			personnages_disponibles.append(personnage)
	# renvoyer la liste des personnages disponibles
	return personnages_disponibles
