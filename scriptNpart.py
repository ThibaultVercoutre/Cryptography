import random
from typing import List, Optional

class DiffieHellman:
    """
    Implémentation du protocole Diffie-Hellman
    """
    
    def __init__(self, p: Optional[int] = None, g: Optional[int] = None):
        if p is None or g is None:
            self.p = 2357  # Nombre premier
            self.g = 2     # Générateur primitif modulo p
        else:
            self.p = p
            self.g = g
        
        print(f"Paramètres publics:")
        print(f"p = {self.p}, g = {self.g}\n")
    
    def generate_private_key(self) -> int:
        return random.randint(2, self.p - 2)
    
    def compute_public_key(self, private_key: int) -> int:
        return pow(self.g, private_key, self.p)


class DHParticipant:
    """
    Participant dans l'échange Diffie-Hellman
    """
    
    def __init__(self, name: str, dh_instance: DiffieHellman):
        self.name = name
        self.dh = dh_instance
        self.private_key = self.dh.generate_private_key()
        self.public_key = self.dh.compute_public_key(self.private_key)
        
        print(f"{self.name}:")
        print(f"  Clé privée: {self.private_key}")
        print(f"  Clé publique: {self.public_key}")
    
    def apply_private_key(self, input_value: int) -> int:
        """Applique la clé privée à une valeur"""
        return pow(input_value, self.private_key, self.dh.p)


class MultipartyDH:
    """
    Protocole Diffie-Hellman multipartite séquentiel
    """
    
    def __init__(self, dh_instance: DiffieHellman):
        self.dh = dh_instance
        self.participants = []
    
    def add_participant(self, name: str) -> DHParticipant:
        participant = DHParticipant(name, self.dh)
        self.participants.append(participant)
        return participant
    
    def run_protocol(self) -> int:
        """
        Exécute le protocole séquentiel
        Calcule: g^(a1 × a2 × a3 × ... × an) mod p
        """
        n = len(self.participants)
        print(f"Protocole multipartite - {n} participants")
        print(f"Calcul: g^(a1 × a2 × ... × a{n}) mod p\n")
        
        current_value = self.dh.g
        print(f"Valeur initiale: g = {current_value}")
        
        for i, participant in enumerate(self.participants):
            new_value = participant.apply_private_key(current_value)
            print(f"Étape {i+1} - {participant.name}: {current_value}^{participant.private_key} = {new_value}")
            current_value = new_value
        
        print(f"\nSecret partagé: {current_value}")
        return current_value


def multiparty_example():
    """
    Exemple d'échange Diffie-Hellman multipartite avec 3 participants
    """
    print("=== DIFFIE-HELLMAN MULTIPARTITE ===\n")
    
    # Initialisation
    dh = DiffieHellman()
    multiparty = MultipartyDH(dh)
    
    # Ajout des participants
    multiparty.add_participant("Alice")
    multiparty.add_participant("Bob")
    multiparty.add_participant("Charlie")
    multiparty.add_participant("David")
    multiparty.add_participant("Eve")
    multiparty.add_participant("Mallory")
    multiparty.add_participant("Trent")
    multiparty.add_participant("Wendy")
    multiparty.add_participant("Xavier")
    multiparty.add_participant("Yves")
    print()
    
    # Exécution du protocole
    secret = multiparty.run_protocol()
    
    return secret


if __name__ == "__main__":
    multiparty_example()