import random

class Character:
    """
    Représente un personnage non joueur (PNJ).
    """

    def __init__(self, name, description, current_room, msgs):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs

    def __str__(self):
        return f"{self.name} : {self.description}"

    def move(self):
        """Le personnage peut se déplacer aléatoirement dans une salle adjacente."""
        if not self.current_room.exits:
            return False  # pas de sorties, reste sur place
        
        # 50% de chance de bouger
        if random.choice([True, False]):
            valid_exits = [room for room in self.current_room.exits.values() if room is not None]
            if valid_exits:
                self.current_room = random.choice(valid_exits)
                return True
        return False
    