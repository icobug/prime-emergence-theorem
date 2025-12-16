"""
Prime Emergence Theorem - Main Implementation
Author: Hristo Valentinov Nedelchev
Email: Hristo.Valentinov.Nedelchev@gmail.com
Date: January 27, 2025
"""

import mpmath as mp
from sympy import primerange
import numpy as np
from typing import Dict, List, Tuple

class PrimeEmergenceTheorem:
    """Implementation of the Prime Emergence Theorem"""
    
    def __init__(self, precision: int = 100):
        """Initialize with given precision"""
        mp.mp.dps = precision
        self.precision = precision
        
    def get_primes_up_to(self, N: int) -> List[int]:
        """Get all primes up to N"""
        return list(primerange(2, N + 1))
    
    def theorem1_mu_c(self, N: int, D: float = 1.0, alpha: float = 1.0, L: float = 1.0) -> mp.mpf:
        """
        Theorem 1: Pattern formation threshold
        
        μ_c(N) = Dλ₁ - αΣ_{p≤N} cos(2πp/N)/log p
        where λ₁ = (2π/L)²
        """
        primes = self.get_primes_up_to(N)
        
        # Calculate Φ_N(0)
        phi_N = sum(mp.cos(2 * mp.pi * p / N) / mp.log(p) for p in primes)
        
        # Principal eigenvalue λ₁
        lambda1 = (2 * mp.pi / L) ** 2
        
        # Theorem 1 result
        mu_c = D * lambda1 - alpha * phi_N
        
        return mu_c
    
    def theorem2_k_c(self, N: int, mu: float = -0.1, nu: float = -0.2) -> Tuple[mp.mpf, mp.mpf]:
        """
        Theorem 2: Synchronization threshold
        
        k_c(N) = -(μ + ν) / [(π(N) - 1) C(N)]
        where C(N) is prime-phase coherence
        """
        primes = self.get_primes_up_to(N)
        m = len(primes)
        
        # Calculate C(N) - prime-phase coherence
        C = mp.mpf('0')
        for i in range(m):
            for j in range(m):
                if i != j:
                    p, q = primes[i], primes[j]
                    phase = 2 * mp.pi * (p - q) / N
                    C += mp.cos(phase) / (mp.log(p) * mp.log(q))
        C /= (m * (m - 1))
        
        # Theorem 2 result
        k_c = -(mu + nu) / ((m - 1) * C)
        
        return k_c, C
    
    def theorem3_goldbach_relation(self, N: int) -> Tuple[mp.mpf, mp.mpf, mp.mpf]:
        """
        Theorem 3: Goldbach synchronization relation
        
        C(N) = c(N) * G(N) / m²
        where G(N) = Σ_{p+q=N} 1/(log p log q)
        """
        primes = self.get_primes_up_to(N)
        m = len(primes)
        prime_set = set(primes)
        
        # Calculate C(N) - reuse from Theorem 2
        _, C = self.theorem2_k_c(N)
        
        # Calculate G(N) - Goldbach sum
        G = mp.mpf('0')
        goldbach_pairs = []
        
        for p in primes:
            q = N - p
            if q in prime_set and p <= q:
                term = 1 / (mp.log(p) * mp.log(q))
                G += term
                goldbach_pairs.append((p, q, term))
        
        # Calculate c(N)
        c = C * m ** 2 / G if G != 0 else mp.mpf('0')
        
        return G, c, len(goldbach_pairs)
    
    def theorem4_synchronized_solution(self, N: int, k: float) -> Dict:
        """
        Theorem 4: Synchronized solution parameters
        
        Returns amplitude A, frequency ω for given k > k_c(N)
        """
        # Get critical coupling
        k_c, C = self.theorem2_k_c(N)
        
        if k <= float(k_c):
            raise ValueError(f"k must be > k_c = {k_c}. Current k = {k}")
        
        primes = self.get_primes_up_to(N)
        m = len(primes)
        
        # Parameters
        mu, nu = mp.mpf('-0.1'), mp.mpf('-0.2')
        s, r = mp.mpf('0.1'), mp.mpf('0.1')
        alpha = mp.mpf('1.0')
        
        # Frequency ω
        omega = mp.sqrt(s * r * m - mu * nu)
        
        # Amplitude A (near bifurcation approximation)
        delta = k - float(k_c)
        A = mp.sqrt(delta / alpha)
        
        # Amplitude B
        B = (r * m / nu) * A
        
        return {
            'A': A,
            'B': B,
            'omega': omega,
            'k_c': k_c,
            'exceeds_by': delta
        }
    
    def compute_all_constants(self, N: int) -> Dict:
        """Compute all theorem constants for given N"""
        # Theorem 1
        mu_c = self.theorem1_mu_c(N)
        
        # Theorem 2
        k_c, C = self.theorem2_k_c(N)
        
        # Theorem 3
        G, c, num_pairs = self.theorem3_goldbach_relation(N)
        
        # Theorem 4 (example for k = 1.1 * k_c)
        sync_params = self.theorem4_synchronized_solution(N, float(k_c) * 1.1)
        
        primes = self.get_primes_up_to(N)
        m = len(primes)
        
        return {
            'N': N,
            'primes_count': m,
            'primes': primes,
            'theorem1': {'mu_c': mu_c},
            'theorem2': {'k_c': k_c, 'C': C},
            'theorem3': {'G': G, 'c': c, 'goldbach_pairs': num_pairs},
            'theorem4': sync_params,
            'scaling_law': float(k_c) * float(G)  # Should be constant
        }

def example_usage():
    """Example of how to use the PrimeEmergenceTheorem class"""
    print("Prime Emergence Theorem - Example Usage")
    print("=" * 50)
    
    # Initialize theorem
    theorem = PrimeEmergenceTheorem(precision=50)
    
    # Compute for N = 30
    N = 30
    results = theorem.compute_all_constants(N)
    
    print(f"\nResults for N = {N}:")
    print(f"Number of primes ≤ {N}: {results['primes_count']}")
    print(f"Primes: {results['primes']}")
    
    print(f"\nTheorem 1 - Pattern formation threshold:")
    print(f"  μ_c({N}) = {results['theorem1']['mu_c']}")
    
    print(f"\nTheorem 2 - Synchronization threshold:")
    print(f"  k_c({N}) = {results['theorem2']['k_c']}")
    print(f"  C({N}) = {results['theorem2']['C']}")
    
    print(f"\nTheorem 3 - Goldbach relation:")
    print(f"  G({N}) = {results['theorem3']['G']}")
    print(f"  c({N}) = {results['theorem3']['c']}")
    print(f"  Goldbach pairs found: {results['theorem3']['goldbach_pairs']}")
    
    print(f"\nTheorem 4 - Synchronized solution (k = 1.1 × k_c):")
    print(f"  Amplitude A = {results['theorem4']['A']}")
    print(f"  Amplitude B = {results['theorem4']['B']}")
    print(f"  Frequency ω = {results['theorem4']['omega']}")
    
    print(f"\nScaling law verification:")
    print(f"  k_c({N}) × G({N}) = {results['scaling_law']} (should be constant)")

if __name__ == "__main__":
    example_usage()
