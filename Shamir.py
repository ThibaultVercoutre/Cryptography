import random
from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np

# Utiliser un grand nombre premier comme champ fini
PRIME = 2089  # doit être > secret et > n

def isprime(n: int) -> bool:  # Renvoie True si n est un nombre premier, False sinon.    
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_polynomial(secret: int, degree: int) -> List[int]:            # Génère un polynôme aléatoire f(x) = a0 + a1*x + ... + at-1*x^t-1
    return [secret] + [random.randint(0, PRIME - 1) for _ in range(degree)]

def print_polynomial(poly: List[int]):        # Affiche le polynôme sous forme mathématique : f(x) = a0 + a1·x + a2·x² + ...
    terms = []
    for power, coeff in enumerate(poly):
        if coeff == 0:
            continue
        if power == 0:
            terms.append(f"{coeff}")
        elif power == 1:
            terms.append(f"{coeff}x")
        else:
            terms.append(f"{coeff}x^{power}")
    polynomial_str = " + ".join(terms)
    print(f"f(x) = {polynomial_str}\n")


def evaluate_polynomial(poly: List[int], x: int, prime: int = PRIME) -> int:    # Évalue le polynôme en un point x modulo prime.
    return sum(coef * pow(x, i, prime) for i, coef in enumerate(poly)) % prime

def plot_polynomial(poly: List[int], prime: int = PRIME, x_range: Tuple[int, int] = (-50, 50)) -> None:         # Trace la courbe du polynôme sur une plage de valeurs de x.
    x_vals = list(range(*x_range))
    y_vals = [evaluate_polynomial(poly, x, prime) for x in x_vals]

    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_vals, marker='o')
    plt.title("Courbe du polynôme (modulo {})".format(prime))
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.show()

def evaluate_polynomial_real(poly: List[int], x: float) -> float:  # Évalue le polynôme en un point x sans modulo (dans ℝ).
    return sum(coef * (x ** i) for i, coef in enumerate(poly))

def plot_polynomial_real(poly: List[int], x_range: Tuple[float, float] = (-50, 50), num_points: int = 200) -> None:   # Trace la courbe du polynôme sur une plage de valeurs de x sans modulo (dans ℝ).
    x_vals = np.linspace(*x_range, num_points)
    y_vals = [evaluate_polynomial_real(poly, x) for x in x_vals]

    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_vals)
    plt.title("Courbe réelle du polynôme")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.show()


def generate_shares(secret: int, n: int, t: int) -> Tuple[List[Tuple[int, int]], List[int]]:    # Génère n parts avec un seuil de t, retourne aussi le polynôme
    poly = generate_polynomial(secret, t - 1)
    shares = [(i, evaluate_polynomial(poly, i)) for i in range(1, n + 1)]
    return shares, poly


def lagrange_interpolation(x: int, x_s: List[int], y_s: List[int]) -> int:     # Interpolation de Lagrange pour retrouver le secret f(0)
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

def reconstruct_secret(shares: List[Tuple[int, int]]) -> int:   # Reconstitue le secret à partir d'au moins t parts
    x_s, y_s = zip(*shares)
    return lagrange_interpolation(0, list(x_s), list(y_s))

# Exemple d'utilisation
def main():
    if not isprime(PRIME):
        print(f"Le nombre {PRIME} n'est pas premier. Veuillez choisir un nombre premier.")
        return 0
    
    secret = random.randint(1, PRIME - 1)
    n = 4    # Nombre total de participants
    t = 3    # Seuil de reconstruction (nombre minimum de parts nécessaires)
    if t > n:
        print("Le seuil t doit être inférieur ou égal au nombre de participants n.")
        return 0
    
    print(f"Secret initial à partager : {secret}")
    shares, poly = generate_shares(secret, n, t)
    

    print("\nPolynôme généré :")
    print_polynomial(poly)
    
    print("\nParts générées (à distribuer aux participants) :")
    for i, (x, y) in enumerate(shares, 1):
        print(f"Participant {i} reçoit : (x={x}, y={y})")
    
    # Affichage de la courbe
    plot_polynomial(poly)  

    plot_polynomial_real(poly) 
    
    selected_shares = random.sample(shares, t)
    print("\nReconstruction avec les parts suivantes :")
    for x, y in selected_shares:
        print(f"(x={x}, y={y})")
    
    recovered_secret = reconstruct_secret(selected_shares)
    print(f"\nSecret reconstruit : {recovered_secret}")
    print("✅ Succès" if recovered_secret == secret else "❌ Échec")

if __name__ == "__main__":
    main()
