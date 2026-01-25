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
        """Le personnage se déplace aléatoirement, mais uniquement via les sorties cardinales (N, S, E, O)."""
        if not self.current_room.exits:
            return False 
        
        # 50% de chance de bouger à chaque tour
        if random.choice([True, False]):
            # On filtre les sorties pour exclure "U" (Up) et "D" (Down)
            valid_exits = [
                room for direction, room in self.current_room.exits.items() 
                if room is not None and direction not in ["U", "D"]
            ]
            
            if valid_exits:
                self.current_room = random.choice(valid_exits)
                return True
        return False
        
    def get_msg(self):
        """Affiche cycliquement les messages du PNJ"""
        if not self.msgs:
            print(f"{self.name} ne dit rien.")
            return
        msg = self.msgs.pop(0)  
        print(msg)
        self.msgs.append(msg)      