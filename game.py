from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
from quest import Quest, QuestManager
import tkinter as tk
from tkinter import ttk, simpledialog
import sys
from pathlib import Path


DEBUG = True

class Game:

    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.quest_manager = QuestManager()

    
    def setup(self, player_name=None):
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
        talk_cmd = Command("talk", " <personnage> : parler à un personnage non joueur", Actions.talk, 1)
        self.commands["talk"] = talk_cmd
        quests_cmd = Command(   "quests"," : afficher la liste des quêtes disponibles", Actions.quests, 0)
        self.commands["quests"] = quests_cmd
        quest_cmd = Command("quest"," <nom> : afficher le détail d'une quête",Actions.quest,1)
        self.commands["quest"] = quest_cmd
        startquest_cmd = Command("startquest"," <nom> : activer une quête",Actions.startquest,1)
        self.commands["startquest"] = startquest_cmd
        rewards_cmd = Command("rewards"," : afficher les récompenses du joueur",Actions.rewards,0)
        self.commands["rewards"] = rewards_cmd



        
    




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

        # Quêtes
        
        # Quêtes
       
      

        quest1 = Quest("lampe", "Trouve la lampe de poche dans le dortoir.", objectives=["prendre lampe_de_poche dans Dortoir"])
        self.quest_manager.add_quest(quest1)

        quest2 = Quest("Explorer la bibliothèque", "Va jusqu'à la bibliothèque.", objectives=["Explorer Bibliotheque"])
        self.quest_manager.add_quest(quest2)

        quest3 = Quest("Rencontrer un PNJ", "Parle au PNJ dans le living room.", objectives=["parler avec sans_nom"])
        self.quest_manager.add_quest(quest3)

        quest4 = Quest(
        "Découvrir le passage secret",
        "Trouve le passage secret dans la chambre de la mère.",
        objectives=["Explorer ChambreMere"]
        )
        self.quest_manager.add_quest(quest4)

        quest5 = Quest(
        "Descendre au sous-sol",
        "Emprunte l'escalier caché.",
        objectives=["Explorer Escalier cache"]
        )
        self.quest_manager.add_quest(quest5)

        quest6 = Quest(
        "Explorer le labyrinthe",
        "Entre dans le labyrinthe souterrain.",
        objectives=["Explorer Labyrinthe"]
        )
        self.quest_manager.add_quest(quest6)
        quest7 = Quest(
        "Trouver la clé",
        "Récupère la clé dans la bibliothèque.",
        objectives=["prendre cle_bibliotheque dans Bibliotheque"]
        )
        self.quest_manager.add_quest(quest7)

        quest8 = Quest(
        "Carte du labyrinthe",
        "Trouve une carte pour t'orienter.",
        objectives=["prendre carte_labyrinthe dans Salle de classe 1"]
        )
        self.quest_manager.add_quest(quest8)
        quest9 = Quest(
        "Badge du gardien",
        "Récupère le badge du gardien.",
        objectives=["prendre badge_gardien dans Couloir_gardien"]
        )
        self.quest_manager.add_quest(quest9)

        quest10 = Quest(
        "Fuite finale",
        "Prépare ta fuite.",
        objectives=["prendre pied_de_biche dans Cuisine"]
        )
        self.quest_manager.add_quest(quest10)
        quest11 = Quest(
        "Comprendre la vérité",
        "Découvre ce qui se cache derrière l'orphelinat.",
        objectives=["parler avec sans_nom_2"]
        )
        self.quest_manager.add_quest(quest11)

        

       
        # Player

        if player_name is None:
        # Si on est en CLI, on demande le nom dans la console
            player_name = input("\nEntrez votre nom: ")
    
        self.player = Player(player_name)
        self.player.current_room = entree
        

        #Création des items
        lampe_de_poche = Item("lampe_de_poche", "une lampe de poche très puissante capable d'éclairer tout une salle", 0.5)
        cle_bibliotheque = Item("cle_bibliotheque","une vieille clé rouillée",0.2)
        carte_labyrinthe = Item("carte_labyrinthe","un plan partiel du labyrinthe",0.1)
        badge_gardien = Item("badge_gardien","le badge du gardien",0.1)
        pied_de_biche = Item("pied_de_biche","un outil pour forcer des portes",1.0)

        

        # ajout des items dans les salles

        dortoir.inventory[lampe_de_poche.name] = lampe_de_poche  # correct pour un dict
        bibliotheque.inventory[cle_bibliotheque.name] = cle_bibliotheque
        salle_classe_1.inventory[carte_labyrinthe.name] = carte_labyrinthe
        couloir_gardien.inventory[badge_gardien.name] = badge_gardien
        cuisine.inventory[pied_de_biche.name] = pied_de_biche

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

            user_input = input(">")
            self.process_command(user_input)

            command_words = user_input.split()

            if not command_words:
                    continue

       
            self.quest_manager.check_room_objectives(self.player.current_room.name)

            if command_words[0] == "talk" and len(command_words) > 1:
                self.quest_manager.check_action_objectives("parler", command_words[1])
            elif command_words[0] == "take" and len(command_words) > 1:
                self.quest_manager.check_action_objectives("item", command_words[1])

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


class _StdoutRedirector:
    """Redirect sys.stdout writes into a Tkinter Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, msg):
        """Write message to the Text widget."""
        if msg:
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", msg)
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")

    def flush(self):
        """Flush method required by sys.stdout interface (no-op for Text widget)."""

class GameGUI(tk.Tk):
    """Tkinter GUI for the text-based adventure game."""

    IMAGE_WIDTH = 600
    IMAGE_HEIGHT = 400

    def __init__(self):
        super().__init__()
        self.title("TBA")
        self.geometry("900x700")  # Provide enough space
        self.minsize(900, 650)

        # Underlying game logic instance
        self.game = Game()

        # Ask player name via dialog (fallback to 'Joueur')
        name = simpledialog.askstring("Nom", "Entrez votre nom:", parent=self)
        if not name:
            name = "Joueur"
        self.game.setup(player_name=name)  # Pass name to avoid double prompt

        # Build UI layers
        self._build_layout()

        # Redirect stdout so game prints appear in terminal output area
        self.original_stdout = sys.stdout
        sys.stdout = _StdoutRedirector(self.text_output)

        # Print welcome text in GUI
        self.game.print_welcome()

        # Load initial room image
        self._update_room_image()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)


    def _build_layout(self):
        """Organise l'interface en grille (Grid)."""
        # On configure la fenêtre pour que la zone de texte s'étire
        self.grid_rowconfigure(0, weight=0)  # Zone du haut (Image + Boutons)
        self.grid_rowconfigure(1, weight=1)  # Zone du milieu (Texte)
        self.grid_rowconfigure(2, weight=0)  # Zone du bas (Entrée)
        self.grid_columnconfigure(0, weight=1)

        # --- BLOC DU HAUT (Conteneur pour Image + Boutons) ---
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        top_frame.grid_columnconfigure(0, weight=0) # Image
        top_frame.grid_columnconfigure(1, weight=1) # Espace vide / Boutons

        # A. L'image (à gauche)
        self.canvas = tk.Canvas(top_frame, width=self.IMAGE_WIDTH, height=self.IMAGE_HEIGHT, bg="#222")
        self.canvas.grid(row=0, column=0, padx=(0, 10))

        # B. Le panneau de commandes (à droite)
        controls_frame = ttk.Frame(top_frame)
        controls_frame.grid(row=0, column=1, sticky="n")

        # Chargement des images (on suppose qu'elles sont dans /assets)
        assets = Path(__file__).parent / 'assets'
        self._img_up = tk.PhotoImage(file=str(assets / 'up-arrow-50.png'))
        self._img_down = tk.PhotoImage(file=str(assets / 'down-arrow-50.png'))
        self._img_left = tk.PhotoImage(file=str(assets / 'left-arrow-50.png'))
        self._img_right = tk.PhotoImage(file=str(assets / 'right-arrow-50.png'))
        self._img_help = tk.PhotoImage(file=str(assets / 'help-50.png'))
        self._img_quit = tk.PhotoImage(file=str(assets / 'quit-50.png'))

        # Placement des flèches en croix dans un sous-panneau
        arrows_frame = ttk.Frame(controls_frame)
        arrows_frame.pack(pady=10)

        tk.Button(arrows_frame, image=self._img_up, bd=0, command=lambda: self._send_command("go N")).grid(row=0, column=1)
        tk.Button(arrows_frame, image=self._img_left, bd=0, command=lambda: self._send_command("go O")).grid(row=1, column=0)
        tk.Button(arrows_frame, image=self._img_right, bd=0, command=lambda: self._send_command("go E")).grid(row=1, column=2)
        tk.Button(arrows_frame, image=self._img_down, bd=0, command=lambda: self._send_command("go S")).grid(row=2, column=1)

        # Boutons Help et Quit en dessous
        tk.Button(controls_frame, image=self._img_help, bd=0, command=lambda: self._send_command("help")).pack(pady=5)
        tk.Button(controls_frame, image=self._img_quit, bd=0, command=lambda: self._send_command("quit")).pack(pady=5)

        # --- BLOC DU MILIEU (Affichage du texte) ---
        self.text_output = tk.Text(self, state="disabled", wrap="word", bg="#1e1e1e", fg="#00FF00", font=("Consolas", 11))
        self.text_output.grid(row=1, column=0, sticky="nsew", padx=10)

        # --- BLOC DU BAS (Saisie de commande) ---
        self.entry_input = ttk.Entry(self)
        self.entry_input.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        self.entry_input.bind("<Return>", self._on_enter)
        self.entry_input.focus_set()
        

    def _on_enter(self, event):
        """Récupère le texte de l'input et l'envoie au jeu."""
        command = self.entry_input.get()
        if command.strip():
            self._send_command(command)
        self.entry_input.delete(0, tk.END)

    def _send_command(self, command):
        """Traite la commande et met à jour l'interface."""
        if self.game.finished:
            return

        # 1. On affiche la commande dans le terminal (Text widget)
        print(f"\n> {command}") 
        
        # 2. On exécute la commande dans la logique du jeu
        self.game.process_command(command)
        
        # 3. MISE À JOUR VISUELLE (Indispensable pour que le nom de la pièce change)
        self._update_room_image()

        # 4. Vérification des quêtes
        command_words = command.split()
        if command_words:
            self.game.quest_manager.check_room_objectives(self.game.player.current_room.name)
            if command_words[0] == "talk" and len(command_words) > 1:
                self.game.quest_manager.check_action_objectives("parler", command_words[1])
            elif command_words[0] == "take" and len(command_words) > 1:
                self.game.quest_manager.check_action_objectives("item", command_words[1])

        # 5. Gestion de la fin du jeu (Commande 'quit')
        if self.game.finished:
            self.entry_input.configure(state="disabled") # Bloque la saisie
            print("\nFermeture du jeu dans 2 secondes...")
            self.after(2000, self._on_close) # Ferme la fenêtre après 2 secondes

    def _update_room_image(self):
        """Met à jour le Canvas en fonction de la pièce actuelle."""
        if not self.game.player or not self.game.player.current_room:
            return

        room_name = self.game.player.current_room.name
        
        # 1. On nettoie le canvas
        self.canvas.delete("all")

        # 2. Couleurs pour le placeholder
        colors = {
            "Entrée": "#add8e6",
            "LivingRoon": "#90ee90",
            "Dortoir": "#ffffe0",
            "Bibliotheque": "#deb887"
        }
        color = colors.get(room_name, "#333333")

        # 3. Dessin du rectangle et du texte
        self.canvas.create_rectangle(0, 0, self.IMAGE_WIDTH, self.IMAGE_HEIGHT, fill=color, outline="")
        self.canvas.create_text(
            self.IMAGE_WIDTH / 2, 
            self.IMAGE_HEIGHT / 2, 
            text=f"📍 {room_name}", 
            fill="black" if color != "#333333" else "white",
            font=("Arial", 20, "bold")
        )

    def _on_close(self):
        """Ferme proprement l'application."""
        sys.stdout = self.original_stdout 
        self.destroy()
        sys.exit()

# ICI IL NE DOIT PLUS RIEN Y AVOIR AVANT LE MAIN
def main():
    # ... ton code main reste identique

    def _on_close(self):
        """Ferme proprement l'application."""
        sys.stdout = self.original_stdout # Restaurer le stdout original
        self.destroy()
        sys.exit()

   
    # ... (toutes les méthodes _build_layout, _update_room_image, _on_enter, _send_command, _on_close)

def main():
    """Entry point.

    If '--cli' is passed as an argument, start the classic console version.
    Otherwise launch the Tkinter GUI.
    Fallback to CLI if GUI cannot be initialized (e.g., headless environment).
    """
    args = sys.argv[1:]
    if '--cli' in args:
        Game().play()
        return
    try:
        app = GameGUI()
        app.mainloop()
    except tk.TclError as e:
        # Fallback to CLI if GUI fails (e.g., no DISPLAY, Tkinter not available)
        print(f"GUI indisponible ({e}). Passage en mode console.")
        Game().play()

if __name__ == "__main__":
    main()
