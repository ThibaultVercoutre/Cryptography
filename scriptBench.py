import random
import time
from typing import List, Dict, Tuple

class DiffieHellman:
    """Base Diffie-Hellman pour les deux protocoles"""
    
    def __init__(self, p: int = 2357, g: int = 2):
        self.p = p
        self.g = g
    
    def generate_private_key(self) -> int:
        return random.randint(2, self.p - 2)
    
    def compute_public_key(self, private_key: int) -> int:
        return pow(self.g, private_key, self.p)


class DHParticipant:
    """Participant unifié pour les deux protocoles"""
    
    def __init__(self, name: str, dh_instance: DiffieHellman):
        self.name = name
        self.dh = dh_instance
        self.private_key = self.dh.generate_private_key()
        self.public_key = self.dh.compute_public_key(self.private_key)
        self.operations_count = 0
    
    def apply_key(self, input_value: int) -> int:
        """Applique la clé privée à une valeur"""
        self.operations_count += 1
        return pow(input_value, self.private_key, self.dh.p)
    
    def reset_operations(self):
        """Reset le compteur d'opérations"""
        self.operations_count = 0


class CircularProtocol:
    """Implémentation du protocole circulaire (version Jour 2)"""
    
    def __init__(self, dh_instance: DiffieHellman):
        self.dh = dh_instance
        self.participants = []
        self.total_operations = 0
    
    def add_participants(self, count: int):
        """Ajoute un nombre donné de participants"""
        self.participants = []
        for i in range(count):
            participant = DHParticipant(f"P{i+1}", self.dh)
            participant.reset_operations()
            self.participants.append(participant)
    
    def run_protocol(self) -> Tuple[int, int, float]:
        """
        Exécute le protocole circulaire
        Retourne: (secret, operations_count, execution_time)
        """
        start_time = time.time()
        n = len(self.participants)
        self.total_operations = 0
        
        # Reset des compteurs
        for p in self.participants:
            p.reset_operations()
        
        # Round 0: Clés publiques
        current_values = [p.public_key for p in self.participants]
        
        # Rounds 1 à n-1: Circulation
        for round_num in range(1, n):
            new_values = []
            for i, participant in enumerate(self.participants):
                prev_index = (i - 1) % n
                input_value = current_values[prev_index]
                output_value = participant.apply_key(input_value)
                new_values.append(output_value)
            current_values = new_values
        
        # Calcul du total d'opérations
        self.total_operations = sum(p.operations_count for p in self.participants)
        
        execution_time = time.time() - start_time
        return current_values[0], self.total_operations, execution_time


class SequentialProtocol:
    """Implémentation du protocole séquentiel (version Jour 2.5)"""
    
    def __init__(self, dh_instance: DiffieHellman):
        self.dh = dh_instance
        self.participants = []
        self.total_operations = 0
    
    def add_participants(self, count: int):
        """Ajoute un nombre donné de participants"""
        self.participants = []
        for i in range(count):
            participant = DHParticipant(f"P{i+1}", self.dh)
            participant.reset_operations()
            self.participants.append(participant)
    
    def run_protocol(self) -> Tuple[int, int, float]:
        """
        Exécute le protocole séquentiel
        Retourne: (secret, operations_count, execution_time)
        """
        start_time = time.time()
        self.total_operations = 0
        
        # Reset des compteurs
        for p in self.participants:
            p.reset_operations()
        
        # Calcul séquentiel
        current_value = self.dh.g
        for participant in self.participants:
            current_value = participant.apply_key(current_value)
        
        # Calcul du total d'opérations
        self.total_operations = sum(p.operations_count for p in self.participants)
        
        execution_time = time.time() - start_time
        return current_value, self.total_operations, execution_time


class ProtocolBenchmark:
    """Gestionnaire de benchmark pour comparer les deux protocoles"""
    
    def __init__(self):
        self.dh = DiffieHellman()
        self.circular = CircularProtocol(self.dh)
        self.sequential = SequentialProtocol(self.dh)
        self.results = []
    
    def benchmark_single_size(self, n_participants: int, iterations: int = 3) -> Dict:
        """Benchmark pour un nombre donné de participants"""
        print(f"🔄 Benchmark {n_participants} participants ({iterations} itérations)...")
        
        circular_results = []
        sequential_results = []
        
        # Test du protocole circulaire
        for i in range(iterations):
            self.circular.add_participants(n_participants)
            secret, ops, time_taken = self.circular.run_protocol()
            circular_results.append({
                'secret': secret,
                'operations': ops,
                'time': time_taken
            })
        
        # Test du protocole séquentiel
        for i in range(iterations):
            self.sequential.add_participants(n_participants)
            secret, ops, time_taken = self.sequential.run_protocol()
            sequential_results.append({
                'secret': secret,
                'operations': ops,
                'time': time_taken
            })
        
        # Calcul des moyennes
        circular_avg_ops = sum(r['operations'] for r in circular_results) / iterations
        circular_avg_time = sum(r['time'] for r in circular_results) / iterations
        
        sequential_avg_ops = sum(r['operations'] for r in sequential_results) / iterations
        sequential_avg_time = sum(r['time'] for r in sequential_results) / iterations
        
        result = {
            'participants': n_participants,
            'circular': {
                'avg_operations': circular_avg_ops,
                'avg_time': circular_avg_time,
                'theoretical_ops': n_participants * (n_participants - 1),
                'complexity': 'O(n²)'
            },
            'sequential': {
                'avg_operations': sequential_avg_ops,
                'avg_time': sequential_avg_time,
                'theoretical_ops': n_participants,
                'complexity': 'O(n)'
            },
            'speedup': {
                'operations_ratio': circular_avg_ops / sequential_avg_ops if sequential_avg_ops > 0 else 0,
                'time_ratio': circular_avg_time / sequential_avg_time if sequential_avg_time > 0 else 0
            }
        }
        
        self.results.append(result)
        return result
    
    def run_full_benchmark(self, max_participants: int = 10, iterations: int = 3):
        """Exécute un benchmark complet"""
        print("🏁 BENCHMARK COMPLET: CIRCULAIRE vs SÉQUENTIEL")
        print("=" * 60)
        
        self.results = []
        
        # Tests de 2 à max_participants
        for n in range(2, max_participants + 1):
            result = self.benchmark_single_size(n, iterations)
            
            # Affichage immédiat des résultats
            print(f"\n📊 Résultats pour {n} participants:")
            print(f"   Circulaire  : {result['circular']['avg_operations']:.1f} ops, {result['circular']['avg_time']:.4f}s")
            print(f"   Séquentiel  : {result['sequential']['avg_operations']:.1f} ops, {result['sequential']['avg_time']:.4f}s")
            print(f"   Gain opérations: {result['speedup']['operations_ratio']:.1f}x")
            print(f"   Gain temps     : {result['speedup']['time_ratio']:.1f}x")
    
    def print_summary_table(self):
        """Affiche un tableau récapitulatif"""
        print("\n" + "=" * 80)
        print("📋 TABLEAU RÉCAPITULATIF")
        print("=" * 80)
        print(f"{'N':>3} | {'Circulaire':>15} | {'Séquentiel':>15} | {'Gain Ops':>10} | {'Gain Temps':>10}")
        print("-" * 80)
        
        for result in self.results:
            n = result['participants']
            circ_ops = result['circular']['avg_operations']
            seq_ops = result['sequential']['avg_operations']
            ops_ratio = result['speedup']['operations_ratio']
            time_ratio = result['speedup']['time_ratio']
            
            print(f"{n:>3} | {circ_ops:>12.1f} ops | {seq_ops:>12.1f} ops | {ops_ratio:>8.1f}x | {time_ratio:>8.1f}x")
    
    def print_complexity_analysis(self):
        """Analyse de la complexité théorique vs réelle"""
        print("\n" + "=" * 60)
        print("🔬 ANALYSE DE COMPLEXITÉ")
        print("=" * 60)
        
        print("\nComplexité théorique:")
        print("   Circulaire  : O(n²) = n × (n-1) opérations")
        print("   Séquentiel  : O(n)  = n opérations")
        
        print("\nVérification avec les résultats:")
        print(f"{'N':>3} | {'Théorique Circ':>15} | {'Réel Circ':>12} | {'Théorique Seq':>15} | {'Réel Seq':>12}")
        print("-" * 70)
        
        for result in self.results:
            n = result['participants']
            theo_circ = result['circular']['theoretical_ops']
            real_circ = result['circular']['avg_operations']
            theo_seq = result['sequential']['theoretical_ops']
            real_seq = result['sequential']['avg_operations']
            
            print(f"{n:>3} | {theo_circ:>15} | {real_circ:>10.1f} | {theo_seq:>15} | {real_seq:>10.1f}")
    
    def print_performance_insights(self):
        """Insights sur les performances"""
        print("\n" + "=" * 60)
        print("💡 INSIGHTS PERFORMANCE")
        print("=" * 60)
        
        if len(self.results) >= 3:
            # Analyse de la croissance
            small_n = self.results[0]  # 2 participants
            large_n = self.results[-1]  # max participants
            
            circ_growth = large_n['circular']['avg_operations'] / small_n['circular']['avg_operations']
            seq_growth = large_n['sequential']['avg_operations'] / small_n['sequential']['avg_operations']
            
            print(f"📈 Croissance des opérations (2 → {large_n['participants']} participants):")
            print(f"   Circulaire  : ×{circ_growth:.1f}")
            print(f"   Séquentiel  : ×{seq_growth:.1f}")
            
            # Point de rupture
            print(f"\n⚡ Gain du séquentiel:")
            max_gain = max(r['speedup']['operations_ratio'] for r in self.results)
            max_gain_n = next(r['participants'] for r in self.results if r['speedup']['operations_ratio'] == max_gain)
            print(f"   Gain maximum: {max_gain:.1f}x avec {max_gain_n} participants")
            
            # Recommandation
            print(f"\n🎯 RECOMMANDATION:")
            print(f"   Pour votre projet (contrainte de temps): SÉQUENTIEL")
            print(f"   - Plus simple à implémenter et déboguer")
            print(f"   - {max_gain:.1f}x moins d'opérations")
            print(f"   - Parfait pour intégration avec Shamir")


def quick_demo():
    """Démonstration rapide des deux protocoles"""
    print("🚀 DÉMONSTRATION RAPIDE - 4 PARTICIPANTS\n")
    
    dh = DiffieHellman()
    
    # Test circulaire
    print("🔄 Protocole Circulaire:")
    circular = CircularProtocol(dh)
    circular.add_participants(4)
    secret_c, ops_c, time_c = circular.run_protocol()
    print(f"   Secret: {secret_c}, Opérations: {ops_c}, Temps: {time_c:.4f}s")
    
    # Test séquentiel
    print("\n⚡ Protocole Séquentiel:")
    sequential = SequentialProtocol(dh)
    sequential.add_participants(4)
    secret_s, ops_s, time_s = sequential.run_protocol()
    print(f"   Secret: {secret_s}, Opérations: {ops_s}, Temps: {time_s:.4f}s")
    
    # Comparaison avec vérification pour éviter division par zéro
    print(f"\n📊 Comparaison:")
    
    if ops_s > 0:
        ops_ratio = ops_c / ops_s
        print(f"   Gain opérations: {ops_ratio:.1f}x")
    else:
        print(f"   Gain opérations: N/A (ops_s = 0)")
    
    if time_s > 0:
        time_ratio = time_c / time_s
        print(f"   Gain temps: {time_ratio:.1f}x")
        print(f"   Séquentiel est {ops_c/ops_s if ops_s > 0 else 'N/A'}x plus efficace!")
    else:
        print(f"   Gain temps: N/A (temps séquentiel trop rapide: {time_s:.6f}s)")
        print(f"   Le protocole séquentiel s'exécute instantanément!")


if __name__ == "__main__":
    print("⚔️  BENCHMARK: CIRCULAIRE vs SÉQUENTIEL ⚔️\n")
    
    # Démonstration rapide
    quick_demo()
    
    print("\n" + "="*60)
    
    # Benchmark complet
    benchmark = ProtocolBenchmark()
    benchmark.run_full_benchmark(max_participants=8, iterations=3)
    
    # Affichage des résultats
    benchmark.print_summary_table()
    benchmark.print_complexity_analysis()
    benchmark.print_performance_insights()
    
    print(f"\n🏆 VERDICT: Le protocole SÉQUENTIEL est clairement supérieur")
    print(f"   pour votre projet avec contrainte de temps!")
    print(f"   → Utilisez le séquentiel pour l'intégration Shamir 🎯")