import random
from typing import List, Tuple

# Utiliser un grand nombre premier comme champ fini
PRIME = 2089  # doit être > secret et > n

def generate_polynomial(secret: int, degree: int) -> List[int]:
    """Génère un polynôme aléatoire f(x) = a0 + a1*x + ... + at-1*x^t-1"""
    return [secret] + [random.randint(0, PRIME - 1) for _ in range(degree)]

def evaluate_polynomial(poly: List[int], x: int) -> int:
    """Évalue le polynôme au point x (mod PRIME)"""
    result = 0
    for power, coeff in enumerate(poly):
        result = (result + coeff * pow(x, power, PRIME)) % PRIME
    return result

def generate_shares(secret: int, n: int, t: int) -> List[Tuple[int, int]]:
    """Génère n parts avec un seuil de t"""
    poly = generate_polynomial(secret, t - 1)
    shares = [(i, evaluate_polynomial(poly, i)) for i in range(1, n + 1)]
    return shares

def lagrange_interpolation(x: int, x_s: List[int], y_s: List[int]) -> int:
    """Interpolation de Lagrange pour retrouver le secret f(0)"""
    total = 0
    k = len(x_s)
    for i in range(k):
        xi, yi = x_s[i], y_s[i]
        li = 1
        for j in range(k):
            if i != j:
                xj = x_s[j]
                li *= (x - xj) * pow(xi - xj, -1, PRIME)
                li %= PRIME
        total += yi * li
        total %= PRIME
    return total

def reconstruct_secret(shares: List[Tuple[int, int]]) -> int:
    """Reconstitue le secret à partir d'au moins t parts"""
    x_s, y_s = zip(*shares)
    return lagrange_interpolation(0, list(x_s), list(y_s))

# Exemple d'utilisation
def main():
    secret = random.randint(1, PRIME - 1)
    n = 5    # Nombre total de participants
    t = 3    # Seuil minimal requis pour reconstituer le secret
    
    print(f"🔐 Secret initial à partager : {secret}")
    shares = generate_shares(secret, n, t)
    
    print("\n🧾 Parts générées (à distribuer aux participants) :")
    for i, (x, y) in enumerate(shares, 1):
        print(f"Participant {i} reçoit : (x={x}, y={y})")
    
    # Sélection aléatoire de t parts pour la reconstruction
    selected_shares = random.sample(shares, t)
    print("\n🔄 Reconstruction avec les parts suivantes :")
    for x, y in selected_shares:
        print(f"(x={x}, y={y})")
    
    recovered_secret = reconstruct_secret(selected_shares)
    print(f"\n✅ Secret reconstruit : {recovered_secret}")
    print("✅ Succès" if recovered_secret == secret else "❌ Échec")

if __name__ == "__main__":
    main()
