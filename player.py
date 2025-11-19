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

        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True
