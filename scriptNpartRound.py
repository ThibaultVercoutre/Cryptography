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


class CircularMultipartyDH:
    """
    Protocole Diffie-Hellman multipartite circulaire (par rounds)
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
        Exécute le protocole circulaire par rounds
        """
        n = len(self.participants)
        print(f"Protocole circulaire - {n} participants")
        print(f"Nombre de rounds nécessaires: {n-1}\n")
        
        # Round 0: Clés publiques initiales
        current_values = []
        print("Round 0 - Clés publiques:")
        for participant in self.participants:
            current_values.append(participant.public_key)
            print(f"  {participant.name}: g^{participant.private_key} = {participant.public_key}")
        print(f"  Valeurs: {current_values}\n")
        
        # Rounds 1 à n-1: Circulation
        for round_num in range(1, n):
            print(f"Round {round_num}:")
            new_values = []
            
            for i, participant in enumerate(self.participants):
                # Prend la valeur du participant précédent (circulation)
                prev_index = (i - 1) % n
                input_value = current_values[prev_index]
                sender = self.participants[prev_index].name
                
                # Applique sa clé privée
                output_value = participant.apply_private_key(input_value)
                new_values.append(output_value)
                
                print(f"  {participant.name} ← {sender}: {input_value}^{participant.private_key} = {output_value}")
            
            current_values = new_values
            print(f"  Valeurs: {current_values}\n")
        
        # Vérification finale
        final_secret = current_values[0]
        all_same = all(value == final_secret for value in current_values)
        
        print("Résultat final:")
        print(f"  Valeurs finales: {current_values}")
        print(f"  Tous identiques: {'Oui' if all_same else 'Non'}")
        print(f"  Secret partagé: {final_secret}")
        
        return final_secret if all_same else None


def circular_example():
    """
    Exemple d'échange Diffie-Hellman multipartite circulaire
    """
    print("=== DIFFIE-HELLMAN CIRCULAIRE ===\n")
    
    # Initialisation
    dh = DiffieHellman()
    multiparty = CircularMultipartyDH(dh)
    
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
    circular_example()