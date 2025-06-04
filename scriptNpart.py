import random
import math
from typing import List, Dict, Optional

class DiffieHellman:
    """
    Implémentation du protocole Diffie-Hellman séquentiel optimisé
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


class DHParticipant:
    """
    Participant pour protocole séquentiel multipartite
    """
    
    def __init__(self, name: str, dh_instance: DiffieHellman):
        self.name = name
        self.dh = dh_instance
        self.private_key = self.dh.generate_private_key()
        self.public_key = self.dh.compute_public_key(self.private_key)
        
        print(f"👤 {self.name}")
        print(f"   Clé privée: {self.private_key}")
        print(f"   Clé publique: g^{self.private_key} = {self.public_key}")
    
    def apply_private_key(self, input_value: int) -> int:
        """
        Applique la clé privée à une valeur d'entrée
        """
        result = pow(input_value, self.private_key, self.dh.p)
        return result


class MultipartyDH:
    """
    Gestionnaire pour protocole Diffie-Hellman multipartite séquentiel
    """
    
    def __init__(self, dh_instance: DiffieHellman):
        self.dh = dh_instance
        self.participants = []
        self.final_secret = None
    
    def add_participant(self, name: str) -> DHParticipant:
        """Ajoute un participant"""
        participant = DHParticipant(name, self.dh)
        self.participants.append(participant)
        print(f"✅ Participant {name} ajouté (Total: {len(self.participants)})\n")
        return participant
    
    def add_multiple_participants(self, names: List[str]) -> List[DHParticipant]:
        """Ajoute plusieurs participants d'un coup"""
        print(f"➕ Ajout de {len(names)} participants...\n")
        participants = []
        for name in names:
            participants.append(self.add_participant(name))
        return participants
    
    def list_participants(self):
        """Affiche la liste des participants"""
        print(f"📋 Liste des participants ({len(self.participants)}):")
        for i, p in enumerate(self.participants):
            print(f"   {i+1}. {p.name} - Clé privée: {p.private_key}")
        print()
    
    def run_protocol(self, verbose: bool = True) -> int:
        """
        Exécute le protocole séquentiel multipartite
        Calcule: g^(a1 × a2 × a3 × ... × an) mod p
        """
        n = len(self.participants)
        if n < 2:
            raise ValueError("Il faut au moins 2 participants")
        
        if verbose:
            print(f"🚀 PROTOCOLE DIFFIE-HELLMAN MULTIPARTITE 🚀")
            print(f"Nombre de participants: {n}")
            print(f"Calcul de: g^(clé1 × clé2 × ... × clé{n}) mod p\n")
        
        # Calcul séquentiel
        current_value = self.dh.g
        
        if verbose:
            print(f"Valeur initiale: g = {current_value}")
        
        for i, participant in enumerate(self.participants):
            step_number = i + 1
            new_value = participant.apply_private_key(current_value)
            
            if verbose:
                print(f"Étape {step_number} - {participant.name}: {current_value}^{participant.private_key} = {new_value}")
            
            current_value = new_value
        
        self.final_secret = current_value
        
        if verbose:
            print(f"\n🔐 Secret final partagé: {self.final_secret}")
            print(f"Formule: g^({' × '.join([str(p.private_key) for p in self.participants])}) mod {self.dh.p}")
        
        return self.final_secret
    
    def get_shared_secret(self) -> int:
        """
        Retourne le secret partagé (calcule si nécessaire)
        """
        if self.final_secret is None:
            self.run_protocol(verbose=False)
        return self.final_secret


def demo_2_participants():
    """Démonstration avec 2 participants (classique)"""
    print("=" * 60)
    print("🔹 DÉMONSTRATION 2 PARTICIPANTS (CLASSIQUE) 🔹")
    print("=" * 60)
    
    dh = DiffieHellman()
    multiparty = MultipartyDH(dh)
    
    # Ajout des participants
    multiparty.add_participant("Alice")
    multiparty.add_participant("Bob")
    
    # Exécution du protocole
    secret = multiparty.run_protocol()
    
    return secret


def demo_3_participants():
    """Démonstration avec 3 participants"""
    print("\n" + "=" * 60)
    print("🔹 DÉMONSTRATION 3 PARTICIPANTS 🔹")
    print("=" * 60)
    
    dh = DiffieHellman()
    multiparty = MultipartyDH(dh)
    
    # Ajout des participants
    participants = ["Alice", "Bob", "Charlie"]
    multiparty.add_multiple_participants(participants)
    
    # Exécution du protocole
    secret = multiparty.run_protocol()
    
    return secret


def demo_5_participants():
    """Démonstration avec 5 participants"""
    print("\n" + "=" * 60)
    print("🔹 DÉMONSTRATION 5 PARTICIPANTS 🔹")
    print("=" * 60)
    
    dh = DiffieHellman()
    multiparty = MultipartyDH(dh)
    
    # Ajout des participants
    team = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
    multiparty.add_multiple_participants(team)
    
    # Exécution du protocole
    secret = multiparty.run_protocol()
    
    return secret


def demo_custom_participants():
    """Démonstration avec nombre personnalisé de participants"""
    print("\n" + "=" * 60)
    print("🔹 DÉMONSTRATION PERSONNALISÉE 🔹")
    print("=" * 60)
    
    dh = DiffieHellman()
    multiparty = MultipartyDH(dh)
    
    # Génération de participants
    n_participants = 7
    participants = [f"Participant_{i+1}" for i in range(n_participants)]
    
    print(f"Création de {n_participants} participants automatiquement...")
    multiparty.add_multiple_participants(participants)
    
    # Liste des participants
    multiparty.list_participants()
    
    # Exécution du protocole
    secret = multiparty.run_protocol()
    
    return secret


def demo_step_by_step():
    """Démonstration pas à pas avec explications"""
    print("\n" + "=" * 60)
    print("🔹 DÉMONSTRATION PAS À PAS DÉTAILLÉE 🔹")
    print("=" * 60)
    
    dh = DiffieHellman()
    multiparty = MultipartyDH(dh)
    
    print("🎯 Objectif: Créer un secret partagé entre 4 participants")
    print("📝 Méthode: Protocole séquentiel g^(a×b×c×d)")
    print()
    
    # Ajout progressif avec explications
    print("--- Étape 1: Création des participants ---")
    alice = multiparty.add_participant("Alice")
    bob = multiparty.add_participant("Bob")
    charlie = multiparty.add_participant("Charlie")
    diana = multiparty.add_participant("Diana")
    
    print("--- Étape 2: Calcul séquentiel du secret ---")
    print("Chaque participant applique sa clé privée au résultat précédent\n")
    
    # Calcul manuel pour illustration
    print("Calcul détaillé:")
    current = dh.g
    print(f"Départ: {current}")
    
    current = alice.apply_private_key(current)
    print(f"Après Alice: g^{alice.private_key} = {current}")
    
    current = bob.apply_private_key(current)
    print(f"Après Bob: (g^{alice.private_key})^{bob.private_key} = {current}")
    
    current = charlie.apply_private_key(current)
    print(f"Après Charlie: (g^{alice.private_key}×{bob.private_key})^{charlie.private_key} = {current}")
    
    current = diana.apply_private_key(current)
    print(f"Après Diana: (g^{alice.private_key}×{bob.private_key}×{charlie.private_key})^{diana.private_key} = {current}")
    
    print(f"\n🔐 Secret final: {current}")
    print(f"Formule: g^({alice.private_key}×{bob.private_key}×{charlie.private_key}×{diana.private_key}) mod {dh.p}")
    
    # Vérification avec la méthode automatique
    multiparty.final_secret = None  # Reset pour recalculer
    auto_secret = multiparty.run_protocol(verbose=False)
    
    print(f"\n✅ Vérification automatique: {auto_secret}")
    print(f"Correspondance: {'✅ OUI' if current == auto_secret else '❌ NON'}")
    
    return current


if __name__ == "__main__":
    print("🌟 DIFFIE-HELLMAN MULTIPARTITE SÉQUENTIEL 🌟\n")
    
    # Démonstrations avec différents nombres de participants
    secret_2 = demo_2_participants()
    secret_3 = demo_3_participants()
    secret_5 = demo_5_participants()
    secret_custom = demo_custom_participants()
    secret_detailed = demo_step_by_step()
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES DÉMONSTRATIONS")
    print("=" * 60)
    print(f"2 participants: Secret = {secret_2}")
    print(f"3 participants: Secret = {secret_3}")
    print(f"5 participants: Secret = {secret_5}")
    print(f"7 participants: Secret = {secret_custom}")
    print(f"4 participants (détaillé): Secret = {secret_detailed}")
    
    print(f"\n🎯 PRINCIPE CLÉS")
    print("✅ Protocole séquentiel: g^(a1×a2×...×an)")
    print("✅ Chaque participant applique sa clé au résultat précédent")
    print("✅ Secret final identique pour tous les participants")
    print("✅ Complexité linéaire O(n)")
    print("✅ Prêt pour intégration avec Shamir!")
    
    print(f"\n📋 Prochaine étape: Jour 3 - Partage de secret avec Shamir")