from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character

DEBUG = True

class Game:

    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    def setup(self):
        # Commands
        help_cmd = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help_cmd
        quit_cmd = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit_cmd
        go_cmd = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O)", Actions.go, 1)
        self.commands["go"] = go_cmd
        back_cmd = Command("back", " :  revenir à la pièce précédente", Actions.back, 0)
        self.commands["back"] = back_cmd
        history_cmd = Command("history", ": afficher l'historique des salles visitées", Actions.history, 0)
        self.commands["history"] = history_cmd
        look_cmd = Command("look"," : observer la pièce et ses items",Actions.look,0)
        self.commands["look"] = look_cmd
        take_cmd = Command("take", " <item> : prendre un item dans la salle", Actions.take, 1)
        self.commands["take"] = take_cmd
        drop_cmd = Command("drop", " <item> : déposer un item dans la salle", Actions.drop, 1)
        self.commands["drop"] = drop_cmd
        check_cmd = Command("check", " : afficher l'inventaire du joueur", Actions.check, 0)
        self.commands["check"] = check_cmd
        
    




        # Rooms (sans "dans")
        entree = Room("Entrée", "L'entrée principale de l'orphelinat.")
        living_room = Room("LivingRoon", "Le hall central de l'orphelinat.")
        dortoir = Room("Dortoir", "Le dortoir des enfants.")

        couloir1 = Room("Couloir1", "Un long couloir usé.")
        bibliotheque = Room("Bibliotheque", "Une bibliothèque ancienne.")
        salle_classe_1 = Room("Salle de classe 1", "Une salle de classe abîmée.")
        salle_classe_2 = Room("Salle de classe 2", "Une autre salle de classe abîmée.")

        couloir2 = Room("Couloir2", "Un couloir menant à plusieurs pièces.")
        cuisine = Room("Cuisine", "La cuisine froide et silencieuse.")
        bathroom = Room("Bathroon", "La salle de bain humide.")

        chambre_mere = Room("ChambreMere", "La chambre de la Mère Supérieure.")
        escalier_cache = Room("Escalier cache", "Un escalier secret caché derrière un meuble.")

        labyrinthe = Room("Labyrinthe", "Une pièce qui mène aux tunnels souterrains.")

        salle_sombre = Room("Salle_sombre", "Une salle plongée dans le noir.")
        couloir_gardien = Room("Couloir_gardien", "Un couloir où rôde un gardien.")
        carrefour = Room("carrefour", "Une intersection dans le labyrinthe.")

        # Exit

        entree.exits = {"N": living_room}
        living_room.exits = { "S": entree,"N": couloir1,"O": dortoir,"E": couloir2}
        dortoir.exits = {"E": living_room}
        couloir1.exits = {"S": living_room,"N": bibliotheque,"O": salle_classe_2,"E": salle_classe_1}
        salle_classe_2.exits = {"E": couloir1}
        salle_classe_1.exits = {"O": couloir1}
        bibliotheque.exits = {"S": couloir1}
        couloir2.exits = {"O": living_room,"E": cuisine,"S": bathroom,"N": chambre_mere}
        cuisine.exits = {"O": couloir2}
        bathroom.exits = {"N": couloir2}
        chambre_mere.exits = {"S": couloir2,"D": escalier_cache}
        escalier_cache.exits = {"D": labyrinthe,"U": chambre_mere}
        labyrinthe.exits = {"E": salle_sombre,"O": couloir_gardien,"S": carrefour,"U": escalier_cache}
        salle_sombre.exits = {"O": labyrinthe,"S": carrefour}
        couloir_gardien.exits = {"E": labyrinthe,"S": carrefour}
        carrefour.exits = {"N": labyrinthe,"O": salle_sombre,"E": couloir_gardien}

        self.rooms = [
        entree, living_room, dortoir, couloir1, bibliotheque, salle_classe_1,
        salle_classe_2, couloir2, cuisine, bathroom, chambre_mere,
        escalier_cache, labyrinthe, salle_sombre, couloir_gardien, carrefour
        ]

       
        # Player
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = entree

        #Création des items
        lampe_de_poche = Item("lampe_de_poche", "une lampe de poche très puissante capable d'éclairer tout une salle", 0.5)
        

        # ajout des items dans les salles

        dortoir.inventory[lampe_de_poche.name] = lampe_de_poche  # correct pour un dict

        # ajout des characters

        perso_sans_nom_1 = Character("Sans_nom","un personnage de test1",living_room,["Je suis un personnage sans nom1","test1"])
        perso_sans_nom_2 = Character("Sans_nom_2","un personnage de test2",living_room,["Je suis un personnage sans nom2","test2"])
        # ajout des characters dans les salles

        living_room.characters[perso_sans_nom_1.name.lower()] = perso_sans_nom_1
        dortoir.characters[perso_sans_nom_2.name.lower()] =  perso_sans_nom_2


        




        

    def play(self):
        self.setup()
        self.print_welcome()
        while not self.finished:
            # Déplacer tous les PNJ avant que le joueur joue
            for room in self.rooms:
                for character in room.characters.values():
                    moved = character.move()
                    if DEBUG and moved:
                        print(f"DEBUG: {character.name} s'est déplacé vers {character.current_room.name}")

            self.process_command(input("> "))
        return None

    def process_command(self, command_string) -> None:
        # Commande vide : ne rien afficher
        if command_string.strip() == "":
            return

        list_of_words = command_string.split(" ")
        command_word = list_of_words[0]

        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        print(self.player.current_room.get_long_description())

def main():
    Game().play()

if __name__ == "__main__":
    main()
