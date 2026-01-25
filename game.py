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
        bathroom = Room("Bathroom", "La salle de bain humide.")

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

        q1 = Quest("Obscure", "Trouver la lampe", objectives=["prendre lampe_de_poche"])
        q2 = Quest("Le Plan", "Parler à Norman.", objectives=["parler avec norman"])
        q3 = Quest("La Clé", "Récupérer la clé argentée en bibliothèque.", objectives=["prendre clef_mere"])
        q4 = Quest("Partir", "Atteindre le carrefour avec la corde.", objectives=["Explorer carrefour"])

        
        for q in [q1, q2, q3, q4]:
            self.quest_manager.add_quest(q)
            q.is_active = True 
            self.quest_manager.active_quests.append(q)
        
        print(f"\n🗡️  Objectif initial : {q1.description}")
       
      
        
        
       
        # Player

        if player_name is None:
       
            player_name = input("\nEntrez votre nom: ")
    
        self.player = Player(player_name)
        self.player.current_room = entree
        

        #Création des items
        lampe_de_poche = Item("lampe_de_poche", "une lampe de poche très puissante capable d'éclairer tout une salle", 0.3)
        corde = Item("corde", "une corde solide faite de draps tressés", 0.5)
        clef_mere = Item("clef_mere", "une clé argentée cachée dans un vieux livre.", 0.1)
    
        

        # ajout des items dans les salles

        dortoir.inventory[lampe_de_poche.name] = lampe_de_poche  # correct pour un dict         
        bibliotheque.inventory["clef_mere"] = clef_mere
        dortoir.inventory["corde"] = corde


        # ajout des characters

        Emma = Character("Emma","Une fille qui adore jouer",living_room,["Mark ne veut pas jouer avec moi","Il m'a dit qu'il avait quelque chose à faire"])
        Mark = Character("Mark","Un garçon qui adore jouer ",living_room,["Norman m'a demandé de te dire de le rejoindre la dernière fois que je l'ai vu il était à la bibliothèque","Norman avait l'air très inquiet..."])

        isabella = Character("Isabella", "Maman... elle vous fixe avec un sourire glacial.", cuisine, ["Mes chers enfants, l'heure de la livraison approche.", "Où comptez-vous aller comme ça ?"])
        norman = Character("Norman", "Il murmure un secret.", bibliotheque,["Je t'attendais", "Prend cette clef je l'ai dérobé à Mère.",
    "Il faut la clé pour entrer dans sa chambre et atteindre l'escalier !"
        ])
       

        # ajout des characters dans les salles

        living_room.characters[Emma.name.lower()] = Emma
        dortoir.characters[Mark.name.lower()] =  Mark

        cuisine.characters["isabella"] = isabella
        bibliotheque.characters["norman"] = norman


        
       

    def play(self):
        self.setup()
        self.print_welcome()
        while not self.finished:
            self.move_pnjs(is_gui=False) 
            user_input = input(">")
            self.process_command(user_input)


    def move_pnjs(self, is_gui=False):
        """Déplace Isabella à 100% et les autres à 20%. Affiche le debug uniquement en CLI."""
        import random
        moved_characters = set()
        for room in self.rooms:
            for char_id in list(room.characters.keys()):
                character = room.characters[char_id]
                if character not in moved_characters:
                    is_isabella = character.name.lower() == "isabella"
                    
                    # --- RÉGLAGE DES PROBABILITÉS ---
                    # Isabella: 100% (1.0), Autres: 20% (0.2)
                    chance = 1.0 if is_isabella else 0.20
                    
                    if random.random() < chance:
                        old_room = room
                        if character.move(): 
                            new_room = character.current_room
                            del old_room.characters[char_id]
                            new_room.characters[char_id] = character
                            moved_characters.add(character)
                            
                            # --- AFFICHAGE INTELLIGENT ---
                            if is_isabella:
                                # Toujours affiché (GUI et CLI) car c'est du gameplay
                                print(f"\n👣 Des pas lourds résonnent... Maman se déplace vers : {new_room.name}")
                            elif DEBUG and not is_gui:
                                # Affiché UNIQUEMENT dans le terminal (CLI) si DEBUG est True
                                print(f"DEBUG: {character.name} est allé en {new_room.name}")

    
    def process_command(self, command_string) -> None:
        if not command_string.strip():
            return
        
        list_of_words = command_string.split(" ")
        command_word = list_of_words[0].lower()

        #  Vérification de l'existence de la commande
        if command_word not in self.commands:
            print(f"\nCommande '{command_word}' inconnue.")
            return

        #  LOGIQUE DE PROGRESSION 
        if command_word == "go" and len(list_of_words) > 1:
            direction = list_of_words[1][0].upper()
            target = self.player.current_room.exits.get(direction)
            
            if target:
                # Verrou de la Chambre de Maman (nécessite la clé)
                if target.name == "ChambreMere" and "clef_mere" not in self.player.inventory:
                    print("\n🔒 La porte est verrouillée. Norman a dit que la clé est en Bibliothèque !")
                    return
                
                # Verrou du Labyrinthe (nécessite la lampe)
                if target.name == "Labyrinthe" and "lampe_de_poche" not in self.player.inventory:
                    print("\n🌑 Il fait trop noir pour descendre dans les tunnels sans lampe de poche !")
                    return 

        
        command = self.commands[command_word]
        command.action(self, list_of_words, command.number_of_parameters)

        # 4. VALIDATION DES QUÊTES 
        
        self.quest_manager.check_room_objectives(self.player.current_room.name)
        
        # On vérifie les actions spécifiques
        if len(list_of_words) > 1:
            target_obj = list_of_words[1].lower()
            
            if command_word == "take":
                # On traduit "take" en "prendre" pour que Quest.py comprenne
                self.quest_manager.check_action_objectives("prendre", target_obj)
            
            elif command_word == "talk":
              
                self.quest_manager.check_action_objectives("parler", target_obj)

        # 5. CONDITION DE VICTOIRE
        current_room = self.player.current_room
        if current_room.name == "carrefour" and "corde" in self.player.inventory:
            print("\n🏆 LIBERTÉ ! Vous avez utilisé la corde pour franchir le mur ! Vous êtes libre !")
            self.finished = True

    def print_welcome(self):
        """Affiche le message d'introduction et guide le joueur dès le début."""
        print("Entrez 'help' si vous avez besoin d'aide.")
        print(f"\nBienvenue {self.player.name} dans cet orphelinat...")
        print("Maman Isabella rôde dans les couloirs. Trouvez un moyen de vous échapper vite !")
        print("-" * 50)
        print("CONSEIL : Tapez la commande 'quests' pour voir vos objectifs.")
        print("-" * 50)
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
        """Envoie la commande, déplace les PNJ sans debug et vérifie la capture."""
        if self.game.finished: 
            return

        # 1. On affiche la commande dans la zone de texte
        print(f"\n> {command}") 
        
        # 2. On exécute l'action du joueur
        self.game.process_command(command)
        
        # 3. Mouvement des PNJ (uniquement si le joueur n'a pas déjà perdu/gagné)
        if not self.game.finished:
            # On active le mode is_gui=True pour ne voir QUE les pas d'Isabella
            self.game.move_pnjs(is_gui=True) 
            
            # 4. Vérification de capture immédiate après le mouvement des PNJ
            if "isabella" in self.game.player.current_room.characters:
                print("\n😱 Maman entre dans la pièce ! Vous êtes capturé !")
                print("❌ GAME OVER.")
                self.game.finished = True

        # 5. Mise à jour de l'image et du texte
        self._update_room_image()
        self.update_idletasks() # Force l'affichage immédiat du texte

        # 6. Gestion de la fermeture si le jeu est fini
        if self.game.finished:
            self.entry_input.configure(state="disabled")
            print("\nFermeture du jeu dans 5 secondes...")
            self.after(5000, self._on_close)

     
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



def main():
    """Point d'entrée du jeu."""
    args = sys.argv[1:]
    if '--cli' in args:
        # Mode console classique
        game_instance = Game()
        game_instance.play()
    else:
        # Mode Interface Graphique
        try:
            app = GameGUI()
            app.mainloop()
        except tk.TclError as e:
            print(f"GUI indisponible ({e}). Passage en mode console.")
            game_instance = Game()
            game_instance.play()

if __name__ == "__main__":
    main()
