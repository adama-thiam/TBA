class Player:
    """
    Représente le joueur dans le jeu.

    Attributes
    ----------
    name : str
        Le nom du joueur.
    current_room : Room
        La salle où se trouve actuellement le joueur.

    Methods
    -------
    move(direction: str) -> bool
        Déplace le joueur dans la direction spécifiée si une sortie existe.
        Retourne True si le déplacement a réussi, False sinon.
    """

    def __init__(self, name):
        """Initialise un joueur avec un nom."""
        self.name = name
        self.current_room = None
        self.history = [] #La liste des salles visitées qu'on va ajouter dans l'histroque

    def move(self, direction):
        """
        Déplace le joueur dans une direction donnée.

        Parameters
        ----------
        direction : str
            La direction dans laquelle le joueur souhaite se déplacer.

        Returns
        -------
        bool
            True si le déplacement est possible, False sinon.
        """
        next_room = self.current_room.exits[direction]  

        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        #Pour mettre la salle dans l'historique
        self.history.append(self.current_room)

        self.current_room = next_room
        print(self.current_room.get_long_description())


        print(self.get_history())
        return True
    
    def go_back(self):
        """
        Permet de revenir à la salle précédente

        """
        if self.history:
            self.current_room = self.history.pop()
            print(f"\nRetour à{self.current_room.name}\n")
            print(self.current_room.get_long_description())
            print(self.get_history())
            return True
        else:
            print("\nImpossible de revenir en arrière.\n")
    
    def get_history(self):
        """
        Retourne une chaîne de caractères listant les pièces visitées.

        """
        if not self.history:
            return "\nVous avez visité aucune autre pièce pour le moment.\n"
        
        
        result = "\nVous avez déjà visité les pièces suivantes:\n"
        for room in self.history:
            result += f"      -{room.description}\n"
        return result 

    