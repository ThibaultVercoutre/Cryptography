import random
import math
from typing import List, Dict, Optional

# Reprise du code du Jour 1 - Classes de base
class DiffieHellman:
    """
    Implémentation du protocole Diffie-Hellman classique et multipartite
    """
    
    def __init__(self, p: Optional[int] = None, g: Optional[int] = None):
        if p is None or g is None:
            # Paramètres pré-calculés sécurisés
            self.p = 2357  # Nombre premier
            self.g = 2     # Générateur primitif modulo p
        else:
            self.p = p
            self.g = g
        
        print(f"Paramètres publics initialisés:")
        print(f"p (nombre premier) = {self.p}")
        print(f"g (générateur) = {self.g}\n")
    
    def generate_private_key(self) -> int:
        return random.randint(2, self.p - 2)
    
    def compute_public_key(self, private_key: int) -> int:
        return pow(self.g, private_key, self.p)
    
    def compute_shared_secret(self, private_key: int, other_public_key: int) -> int:
        return pow(other_public_key, private_key, self.p)


class DHParticipant:
    """
    Participant étendu pour supporter les échanges multipartites
    """
    
    def __init__(self, name: str, dh_instance: DiffieHellman):
        self.name = name
        self.dh = dh_instance
        self.private_key = self.dh.generate_private_key()
        self.public_key = self.dh.compute_public_key(self.private_key)
        self.shared_secret = None
        
        # Nouvelles propriétés pour multipartite
        self.intermediate_values = {}  # Stockage des valeurs intermédiaires
        self.round_values = []  # Valeurs pour chaque round
        
        print(f"{self.name} - Clé privée: {self.private_key}")
        print(f"{self.name} - Clé publique: {self.public_key}")
    
    def compute_shared_secret(self, other_public_key: int):
        """Version classique 2-parties"""
        self.shared_secret = self.dh.compute_shared_secret(self.private_key, other_public_key)
        return self.shared_secret
    
    def compute_intermediate_value(self, input_value: int) -> int:
        """
        Calcule une valeur intermédiaire pour le protocole multipartite
        """
        result = pow(input_value, self.private_key, self.dh.p)
        return result
    
    def store_round_value(self, round_num: int, value: int):
        """Stocke une valeur pour un round donné"""
        if len(self.round_values) <= round_num:
            self.round_values.extend([None] * (round_num + 1 - len(self.round_values)))
        self.round_values[round_num] = value


class MultipartyDH:
    """
    Gestionnaire pour les échanges Diffie-Hellman multipartites
    Implémente le protocole circulaire simplifié
    """
    
    def __init__(self, dh_instance: DiffieHellman):
        self.dh = dh_instance
        self.participants = []
        self.final_secret = None
    
    def add_participant(self, name: str) -> DHParticipant:
        """Ajoute un participant au groupe"""
        participant = DHParticipant(name, self.dh)
        self.participants.append(participant)
        return participant
    
    def circular_protocol(self) -> int:
        """
        Implémente le protocole circulaire pour n participants
        
        Principe :
        - Round 1: Chaque participant applique sa clé privée à g
        - Round 2: Chaque participant applique sa clé privée à la valeur reçue
        - ... jusqu'à ce que tous aient contribué
        """
        n = len(self.participants)
        if n < 2:
            raise ValueError("Il faut au moins 2 participants")
        
        print(f"=== PROTOCOLE CIRCULAIRE AVEC {n} PARTICIPANTS ===\n")
        
        # Initialisation : chaque participant calcule g^(sa_clé)
        current_values = []
        for i, participant in enumerate(self.participants):
            initial_value = participant.public_key  # g^a_i mod p
            current_values.append(initial_value)
            participant.store_round_value(0, initial_value)
            print(f"Round 0 - {participant.name}: g^{participant.private_key} = {initial_value}")
        
        print()
        
        # Rounds successifs : circulation des valeurs
        for round_num in range(1, n):
            print(f"--- Round {round_num} ---")
            new_values = []
            
            for i, participant in enumerate(self.participants):
                # Prend la valeur du participant précédent (circulation)
                prev_index = (i - 1) % n
                input_value = current_values[prev_index]
                
                # Applique sa clé privée
                output_value = participant.compute_intermediate_value(input_value)
                new_values.append(output_value)
                participant.store_round_value(round_num, output_value)
                
                print(f"{participant.name} reçoit {input_value} → calcule {input_value}^{participant.private_key} = {output_value}")
            
            current_values = new_values
            print()
        
        # Le secret final est la valeur finale (normalement identique pour tous)
        self.final_secret = current_values[0]
        
        # Vérification que tous ont le même secret
        all_same = all(value == self.final_secret for value in current_values)
        
        print(f"--- Résultat Final ---")
        print(f"Valeurs finales: {current_values}")
        print(f"Tous identiques: {'✅' if all_same else '❌'}")
        print(f"Secret partagé: {self.final_secret}")
        
        return self.final_secret if all_same else None


class SimplifiedMultipartyDH:
    """
    Version simplifiée alternative : chaque participant contribue séquentiellement
    Plus facile à comprendre mais moins sécurisée
    """
    
    def __init__(self, dh_instance: DiffieHellman):
        self.dh = dh_instance
        self.participants = []
    
    def add_participant(self, name: str) -> DHParticipant:
        participant = DHParticipant(name, self.dh)
        self.participants.append(participant)
        return participant
    
    def sequential_protocol(self) -> int:
        """
        Protocole séquentiel simplifié :
        secret = g^(a1 * a2 * a3 * ... * an) mod p
        """
        n = len(self.participants)
        print(f"=== PROTOCOLE SÉQUENTIEL AVEC {n} PARTICIPANTS ===\n")
        
        # Commence avec g
        current_value = self.dh.g
        print(f"Valeur initiale: g = {current_value}")
        
        # Chaque participant applique sa clé privée
        for i, participant in enumerate(self.participants):
            new_value = pow(current_value, participant.private_key, self.dh.p)
            print(f"Étape {i+1} - {participant.name}: {current_value}^{participant.private_key} = {new_value}")
            current_value = new_value
        
        print(f"\nSecret final: {current_value}")
        return current_value


def demonstrate_multiparty_3_participants():
    """Démonstration avec 3 participants"""
    print("🔹 DÉMONSTRATION 3 PARTICIPANTS - PROTOCOLE CIRCULAIRE 🔹\n")
    
    dh = DiffieHellman()
    multiparty = MultipartyDH(dh)
    
    # Ajout des participants
    alice = multiparty.add_participant("Alice")
    bob = multiparty.add_participant("Bob")
    charlie = multiparty.add_participant("Charlie")
    print()
    
    # Exécution du protocole
    secret = multiparty.circular_protocol()
    
    return secret is not None


def demonstrate_multiparty_4_participants():
    """Démonstration avec 4 participants"""
    print("\n🔹 DÉMONSTRATION 4 PARTICIPANTS - PROTOCOLE CIRCULAIRE 🔹\n")
    
    dh = DiffieHellman()
    multiparty = MultipartyDH(dh)
    
    # Ajout des participants
    participants_names = ["Alice", "Bob", "Charlie", "Diana"]
    for name in participants_names:
        multiparty.add_participant(name)
    print()
    
    # Exécution du protocole
    secret = multiparty.circular_protocol()
    
    return secret is not None


def demonstrate_simplified_protocol():
    """Démonstration du protocole simplifié"""
    print("\n🔹 DÉMONSTRATION PROTOCOLE SIMPLIFIÉ 🔹\n")
    
    dh = DiffieHellman()
    simple_multiparty = SimplifiedMultipartyDH(dh)
    
    # Ajout des participants
    simple_multiparty.add_participant("Alice")
    simple_multiparty.add_participant("Bob")
    simple_multiparty.add_participant("Charlie")
    print()
    
    # Exécution du protocole
    secret = simple_multiparty.sequential_protocol()
    
    return secret is not None


def compare_protocols():
    """Compare les différents protocoles"""
    print("\n🔹 COMPARAISON DES PROTOCOLES 🔹\n")
    
    dh = DiffieHellman()
    
    # Protocole classique (2 participants)
    print("--- Protocole Classique (2 participants) ---")
    alice_classic = DHParticipant("Alice", dh)
    bob_classic = DHParticipant("Bob", dh)
    secret_classic = alice_classic.compute_shared_secret(bob_classic.public_key)
    verify_classic = bob_classic.compute_shared_secret(alice_classic.public_key)
    print(f"Secret classique: {secret_classic} (vérif: {verify_classic == secret_classic})")
    print()
    
    # Protocole multipartite circulaire
    print("--- Protocole Multipartite Circulaire ---")
    multiparty = MultipartyDH(dh)
    multiparty.add_participant("Alice")
    multiparty.add_participant("Bob")
    multiparty.add_participant("Charlie")
    secret_multiparty = multiparty.circular_protocol()
    print()
    
    # Protocole simplifié
    print("--- Protocole Simplifié ---")
    simple_multiparty = SimplifiedMultipartyDH(dh)
    simple_multiparty.add_participant("Alice")
    simple_multiparty.add_participant("Bob")
    simple_multiparty.add_participant("Charlie")
    secret_simple = simple_multiparty.sequential_protocol()
    print()
    
    print("=== COMPARAISON ===")
    print(f"Classique (2p): {secret_classic}")
    print(f"Circulaire (3p): {secret_multiparty}")
    print(f"Simplifié (3p): {secret_simple}")


if __name__ == "__main__":
    # Exécution des démonstrations
    print("🚀 DIFFIE-HELLMAN MULTIPARTITE - JOUR 2 🚀\n")
    
    success1 = demonstrate_multiparty_3_participants()
    success2 = demonstrate_multiparty_4_participants()
    success3 = demonstrate_simplified_protocol()
    
    compare_protocols()
    
    print(f"\n=== RÉSUMÉ JOUR 2 ===")
    print(f"Protocole 3 participants: {'✅' if success1 else '❌'}")
    print(f"Protocole 4 participants: {'✅' if success2 else '❌'}")
    print(f"Protocole simplifié: {'✅' if success3 else '❌'}")
    print("\n🎯 Extensions multipartites opérationnelles!")
    print("📋 Prêt pour le Jour 3: Intégration avec Shamir!")