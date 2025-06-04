import random
import math
from typing import Tuple, Optional

class DiffieHellman:
    """
    Implémentation du protocole Diffie-Hellman classique pour 2 parties
    """
    
    def __init__(self, p: Optional[int] = None, g: Optional[int] = None):
        """
        Initialise les paramètres publics p (nombre premier) et g (générateur)
        """
        if p is None or g is None:
            # Utilisation de paramètres pré-calculés sécurisés (pour la démo)
            self.p = 2357  # Nombre premier
            self.g = 2     # Générateur primitif modulo p
        else:
            self.p = p
            self.g = g
        
        print(f"Paramètres publics initialisés:")
        print(f"p (nombre premier) = {self.p}")
        print(f"g (générateur) = {self.g}\n")
    
    def generate_private_key(self) -> int:
        """
        Génère une clé privée aléatoire
        """
        return random.randint(2, self.p - 2)
    
    def compute_public_key(self, private_key: int) -> int:
        """
        Calcule la clé publique à partir de la clé privée
        """
        return pow(self.g, private_key, self.p)
    
    def compute_shared_secret(self, private_key: int, other_public_key: int) -> int:
        """
        Calcule le secret partagé
        """
        return pow(other_public_key, private_key, self.p)


class DHParticipant:
    """
    Représente un participant dans l'échange Diffie-Hellman
    """
    
    def __init__(self, name: str, dh_instance: DiffieHellman):
        self.name = name
        self.dh = dh_instance
        self.private_key = self.dh.generate_private_key()
        self.public_key = self.dh.compute_public_key(self.private_key)
        self.shared_secret = None
        
        print(f"{self.name} - Clé privée générée: {self.private_key}")
        print(f"{self.name} - Clé publique calculée: {self.public_key}")
    
    def compute_shared_secret(self, other_public_key: int):
        """
        Calcule et stocke le secret partagé
        """
        self.shared_secret = self.dh.compute_shared_secret(self.private_key, other_public_key)
        print(f"{self.name} - Secret partagé calculé: {self.shared_secret}")
        return self.shared_secret


def demonstrate_dh_exchange():
    """
    Démonstration complète de l'échange Diffie-Hellman
    """
    print("=== DÉMONSTRATION DIFFIE-HELLMAN CLASSIQUE ===\n")
    
    # 1. Initialisation du protocole
    dh = DiffieHellman()
    
    # 2. Création des participants
    print("--- Création des participants ---")
    alice = DHParticipant("Alice", dh)
    bob = DHParticipant("Bob", dh)
    print()
    
    # 3. Échange des clés publiques (simulation du canal non sécurisé)
    print("--- Échange des clés publiques ---")
    print(f"Alice envoie sa clé publique à Bob: {alice.public_key}")
    print(f"Bob envoie sa clé publique à Alice: {bob.public_key}")
    print()
    
    # 4. Calcul des secrets partagés
    print("--- Calcul des secrets partagés ---")
    alice_secret = alice.compute_shared_secret(bob.public_key)
    bob_secret = bob.compute_shared_secret(alice.public_key)
    print()
    
    # 5. Vérification
    print("--- Vérification ---")
    if alice_secret == bob_secret:
        print("✅ SUCCESS: Les secrets partagés sont identiques!")
        print(f"Secret partagé: {alice_secret}")
    else:
        print("❌ ERROR: Les secrets partagés diffèrent!")
        print(f"Alice: {alice_secret}, Bob: {bob_secret}")
    
    return alice_secret == bob_secret


def demonstrate_security_aspects():
    """
    Démonstration des aspects de sécurité
    """
    print("\n=== ASPECTS DE SÉCURITÉ ===\n")
    
    dh = DiffieHellman()
    
    # Simulation d'un attaquant qui intercepte les communications
    alice_private = dh.generate_private_key()
    bob_private = dh.generate_private_key()
    
    alice_public = dh.compute_public_key(alice_private)
    bob_public = dh.compute_public_key(bob_private)
    
    print(f"Un attaquant intercepte:")
    print(f"- p = {dh.p}")
    print(f"- g = {dh.g}")
    print(f"- Clé publique d'Alice = {alice_public}")
    print(f"- Clé publique de Bob = {bob_public}")
    print()
    
    # L'attaquant ne peut pas calculer le secret sans les clés privées
    real_secret = pow(alice_public, bob_private, dh.p)
    print(f"Secret réel: {real_secret}")
    print("L'attaquant ne peut pas calculer ce secret sans résoudre le problème du logarithme discret!")


def test_different_parameters():
    """
    Test avec différents paramètres
    """
    print("\n=== TESTS AVEC DIFFÉRENTS PARAMÈTRES ===\n")
    
    # Paramètres plus grands pour plus de sécurité
    large_p = 32771  # Plus grand nombre premier
    large_g = 3
    
    print(f"Test avec des paramètres plus grands:")
    dh_large = DiffieHellman(large_p, large_g)
    
    alice = DHParticipant("Alice", dh_large)
    bob = DHParticipant("Bob", dh_large)
    
    alice_secret = alice.compute_shared_secret(bob.public_key)
    bob_secret = bob.compute_shared_secret(alice.public_key)
    
    success = alice_secret == bob_secret
    print(f"Résultat: {'✅ SUCCESS' if success else '❌ FAILURE'}")
    
    return success


if __name__ == "__main__":
    # Exécution des démonstrations
    success1 = demonstrate_dh_exchange()
    demonstrate_security_aspects()
    success2 = test_different_parameters()
    
    print(f"\n=== RÉSUMÉ ===")
    print(f"Test basique: {'✅' if success1 else '❌'}")
    print(f"Test paramètres étendus: {'✅' if success2 else '❌'}")
    print("\nFondations Diffie-Hellman prêtes pour l'extension multi-parties!")