#!/usr/bin/env python3
"""
Simulate the Prime Emergence dynamical system
Author: Hristo Valentinov Nedelchev
"""

import sys
sys.path.append('.')  # Add current directory to path

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

from prime_emergence import PrimeEmergenceTheorem

class PrimeEmergenceSimulator:
    """Simulate the Prime Emergence dynamical system"""
    
    def __init__(self, N: int):
        self.N = N
        self.theorem = PrimeEmergenceTheorem(precision=50)
        self.primes = self.theorem.get_primes_up_to(N)
        self.m = len(self.primes)
        
        # Default parameters
        self.mu = -0.1
        self.nu = -0.2
        self.s = 0.1
        self.r = 0.1
        self.alpha = 1.0
        
    def simulate(self, k: float, T: float = 100.0, dt: float = 0.1):
        """Simulate system with coupling strength k"""
        # Initial conditions
        z0 = []
        for p in self.primes:
            phase = 2 * np.pi * p / self.N
            amplitude = 0.01 / np.log(p)  # Small initial amplitude
            z0.append(amplitude * np.exp(1j * phase))
        
        # Include b(t)
        b0 = 0 + 0j
        
        # Pack initial state (real and imaginary parts separately)
        state0 = np.zeros(2 * self.m + 2)
        for i in range(self.m):
            state0[2*i] = z0[i].real
            state0[2*i + 1] = z0[i].imag
        state0[-2] = b0.real
        state0[-1] = b0.imag
        
        # Define ODE function
        def derivatives(t, state):
            # Unpack state
            z_real = state[0:2*self.m:2]
            z_imag = state[1:2*self.m:2]
            b_real = state[-2]
            b_imag = state[-1]
            
            z = z_real + 1j * z_imag
            b = b_real + 1j * b_imag
            
            # Calculate derivatives
            dzdt = np.zeros(self.m, dtype=complex)
            
            for i in range(self.m):
                # Interaction term
                interaction = 0 + 0j
                for j in range(self.m):
                    if i != j:
                        # Regularized interaction
                        re_part = np.real(z[i] * np.conj(z[j]))
                        norm_sq = np.abs(z[j])**2 + 1e-10
                        interaction += k * (re_part / norm_sq) * z[j]
                
                # Full equation for dz_i/dt
                dzdt[i] = (self.mu * z[i] + interaction + 
                          self.s * b - self.alpha * np.abs(z[i])**2 * z[i])
            
            # Derivative for b
            dbdt = self.r * np.sum(z) + self.nu * b - self.alpha * np.abs(b)**2 * b
            
            # Pack derivatives
            dstate = np.zeros(2*self.m + 2)
            dstate[0:2*self.m:2] = dzdt.real
            dstate[1:2*self.m:2] = dzdt.imag
            dstate[-2] = dbdt.real
            dstate[-1] = dbdt.imag
            
            return dstate
        
        # Solve ODE
        t_eval = np.arange(0, T, dt)
        sol = solve_ivp(derivatives, [0, T], state0,
                       t_eval=t_eval, method='RK45', rtol=1e-8)
        
        return sol
    
    def compute_order_parameter(self, sol, t_index: int = -1):
        """Compute synchronization order parameter R(t)"""
        # Extract state at time t_index
        state = sol.y[:, t_index]
        
        # Unpack z values
        z_values = []
        for i in range(self.m):
            z_values.append(state[2*i] + 1j*state[2*i + 1])
        
        # Compute order parameter R = |Σz_i| / Σ|z_i|
        complex_sum = np.sum(z_values)
        total_magnitude = np.sum([np.abs(z) for z in z_values])
        
        return np.abs(complex_sum) / total_magnitude if total_magnitude > 0 else 0
    
    def analyze_synchronization(self, k_values):
        """Analyze synchronization for different coupling strengths"""
        results = []
        
        for k in k_values:
            print(f"Simulating with k = {k:.6f}")
            
            # Simulate
            sol = self.simulate(k, T=50.0, dt=0.1)
            
            # Compute order parameter at final time
            R = self.compute_order_parameter(sol)
            
            # Get theoretical k_c
            k_c, _ = self.theorem.theorem2_k_c(self.N)
            k_c = float(k_c)
            
            results.append({
                'k': k,
                'k_c': k_c,
                'R': R,
                'k/k_c': k / k_c if k_c > 0 else 0,
                'sync': R > 0.8  # Threshold for synchronization
            })
            
            print(f"  Order parameter R = {R:.6f}")
            print(f"  k/k_c = {k/k_c:.6f}")
            print(f"  Synchronized: {'YES' if R > 0.8 else 'NO'}")
        
        return results

def plot_results(simulation_results, N):
    """Plot synchronization analysis"""
    k_values = [r['k'] for r in simulation_results]
    R_values = [r['R'] for r in simulation_results]
    k_c = simulation_results[0]['k_c']
    
    plt.figure(figsize=(10, 6))
    
    # Plot order parameter vs k
    plt.plot(k_values, R_values, 'bo-', linewidth=2, markersize=6)
    plt.axvline(x=k_c, color='r', linestyle='--', label=f'k_c = {k_c:.6f}')
    plt.xlabel('Coupling strength k')
    plt.ylabel('Order parameter R')
    plt.title(f'Synchronization Order Parameter (N={N})')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    
    # Save and show
    plt.savefig(f'prime_emergence_sync_N{N}.png', dpi=150)
    plt.show()

def main():
    """Main simulation"""
    N = 30  # Example
    
    print("Prime Emergence System Simulation")
    print("=" * 50)
    
    # Initialize
    simulator = PrimeEmergenceSimulator(N)
    
    # Get theoretical k_c
    k_c, C = simulator.theorem.theorem2_k_c(N)
    print(f"\nTheoretical values for N={N}:")
    print(f"  k_c = {k_c:.10f}")
    print(f"  C(N) = {C:.10f}")
    
    # Define k values around k_c
    k_c_float = float(k_c)
    k_values = np.linspace(k_c_float * 0.5, k_c_float * 1.5, 10)
    
    print(f"\nSimulating with k values from {k_values[0]:.6f} to {k_values[-1]:.6f}")
    
    # Run simulations
    results = simulator.analyze_synchronization(k_values)
    
    # Plot results
    plot_results(results, N)
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Synchronization threshold: k_c = {k_c:.10f}")
    print(f"Phase coherence: C(N) = {C:.10f}")
    
    # Find critical k from simulation (where R > 0.5)
    for r in results:
        if r['R'] > 0.5:
            print(f"Simulation shows synchronization for k > {r['k']:.6f}")
            break

if __name__ == "__main__":
    main()
