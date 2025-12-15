class Room:
    """
    Représente un lieu dans le jeu.

    Attributes
    ----------
    name : str
        Le nom de la salle.
    description : str
        Une phrase décrivant l'endroit où se trouve le joueur.
    exits : dict[str, Room | None]
        Dictionnaire des sorties possibles depuis cette salle.
        Les clés sont des directions ("N", "E", "S", "O") et les valeurs
        sont soit des objets Room, soit None lorsqu'il n'y a pas de sortie.

    Methods
    -------
    get_long_description() -> str
        Retourne une description détaillée de la salle, incluant les sorties.
    """

    def __init__(self, name, description):
        """Initialise une salle avec un nom et une description."""
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {} #dictionnaire

    def get_exit_string(self):
        """Retourne une chaîne contenant la liste des directions disponibles."""
        exit_string = "Sorties: "
        for direction in self.exits:
            if self.exits[direction] is not None:
                exit_string += direction + ", "
        return exit_string[:-2]

    def get_long_description(self):
        """Retourne une description longue affichée au joueur."""
        return f"\nVous êtes dans {self.description}\n\n{self.get_exit_string()}\n"
        def get_inventory(self):
            if not self.inventory:
                return "\nIl n'y a rien ici.\n"

                result = "\nLa pièce contient :\n"
                for item in self.inventory.values():
                    result += f"    - {item}\n"
        return result
