import random
from typing import Optional

class DiffieHellman:
    """
    Implémentation du protocole Diffie-Hellman classique pour 2 parties
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
    
    def compute_shared_secret(self, private_key: int, other_public_key: int) -> int:
        return pow(other_public_key, private_key, self.p)


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
    
    def compute_shared_secret(self, other_public_key: int):
        shared_secret = self.dh.compute_shared_secret(self.private_key, other_public_key)
        print(f"  Secret calculé: {shared_secret}")
        return shared_secret


def simple_example():
    """
    Un exemple simple d'échange Diffie-Hellman
    """
    print("=== ÉCHANGE DIFFIE-HELLMAN ===\n")
    
    # Initialisation
    dh = DiffieHellman()
    
    # Participants
    alice = DHParticipant("Alice", dh)
    bob = DHParticipant("Bob", dh)
    print()
    
    # Échange
    print("Échange des clés publiques:")
    print(f"Alice → Bob: {alice.public_key}")
    print(f"Bob → Alice: {bob.public_key}")
    print()
    
    # Calcul des secrets
    print("Calcul des secrets partagés:")
    alice_secret = alice.compute_shared_secret(bob.public_key)
    bob_secret = bob.compute_shared_secret(alice.public_key)
    print()
    
    # Vérification
    if alice_secret == bob_secret:
        print(f"✅ Secret partagé: {alice_secret}")
    else:
        print("❌ Erreur dans le calcul")


if __name__ == "__main__":
    simple_example()