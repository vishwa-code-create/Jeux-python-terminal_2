from rich.align import Align
from rich.panel import Panel

banned_pseudos = ["admin", "root", "superuser"]


def create_panel(title="", text="", color="yellow"):
	text_color = {"red": {"start": "[red]", "end": "[/red]"},
               "green": {"start": "[green]", "end": "[/green]"},
               "blue": {"start": "[blue]", "end": "[/blue]"},
               "yellow": {"start": "[yellow]", "end": "[/yellow]"}
               }

	return Panel(Align.center(text_color[color]["start"] + text + text_color[color]["end"], vertical="middle"), title=title, border_style=color)


def get_username(db):
	while True:
		pseudo = input("Entrez votre pseudo : ").strip()
		if validate_username(pseudo, db):
			return pseudo
		print("Pseudo invalide, veuillez réessayer.")


def validate_username(pseudo, db):
	if len(pseudo) < 3 or len(pseudo) > 20:
		return False
	if pseudo in banned_pseudos:
		return False
	if is_username_in_db(pseudo, db):
		return False
	return True


def is_username_in_db(pseudo, db):
	pseudos_in_db = [user["player_name"] for user in db["scores"].find()]
	if pseudo in pseudos_in_db:
		return True
	return False


def get_user_choice_from_options(options, message):
	while True:
		print(message)
		for i, option in enumerate(options, start=1):
			print(f"{i}. {option}")
		choix = input("Entrez votre choix : ").strip()
		if validate_user_choice(choix, 1, len(options)):
			return int(choix)
		print("Choix invalide, veuillez réessayer.")


def validate_user_choice(choix, minimum, maximum):
	if not choix.isdigit():
		return False
	choix = int(choix)
	if choix < minimum or choix > maximum:
		return False
	return True


def recuperer_choix_utilisateur(options):
	while True:
		afficher_options_numerotees(options)
		choix = input("Entrez votre choix : ")
		if est_choix_valide(choix, 1, len(options)):
			return int(choix)
		print("Choix invalide, veuillez réessayer.")


def afficher_options_numerotees(options):
	for i, option in enumerate(options, start=1):
		print(f"{i}. {option}")


def truc_complexe(choix):
	                       

	return True


def est_choix_valide(choix, minimum, maximum):
	validator = [
            lambda x: x.isdigit(),
            lambda x: minimum <= int(x) <= maximum,
            truc_complexe
        ]
	for v in validator:
		if not v(choix):
			return False
	return True