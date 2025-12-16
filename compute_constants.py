#!/usr/bin/env python3
"""
Compute all theorem constants for various N
Author: Hristo Valentinov Nedelchev
"""

import sys
sys.path.append('.')  # Add current directory to path

from prime_emergence import PrimeEmergenceTheorem

def compute_for_range(N_values):
    """Compute constants for a range of N values"""
    theorem = PrimeEmergenceTheorem(precision=50)
    
    results = []
    for N in N_values:
        print(f"\n{'='*60}")
        print(f"Computing for N = {N}")
        print(f"{'='*60}")
        
        try:
            data = theorem.compute_all_constants(N)
            
            results.append({
                'N': N,
                'm': data['primes_count'],
                'mu_c': float(data['theorem1']['mu_c']),
                'k_c': float(data['theorem2']['k_c']),
                'C': float(data['theorem2']['C']),
                'G': float(data['theorem3']['G']),
                'c': float(data['theorem3']['c']),
                'pairs': data['theorem3']['goldbach_pairs']
            })
            
            # Print summary
            print(f"π({N}) = {data['primes_count']}")
            print(f"μ_c({N}) = {data['theorem1']['mu_c']:.10f}")
            print(f"k_c({N}) = {data['theorem2']['k_c']:.10f}")
            print(f"C({N}) = {data['theorem2']['C']:.10f}")
            print(f"G({N}) = {data['theorem3']['G']:.10f}")
            print(f"c({N}) = {data['theorem3']['c']:.10f}")
            print(f"Goldbach pairs: {data['theorem3']['goldbach_pairs']}")
            
        except Exception as e:
            print(f"Error computing for N={N}: {e}")
            continue
    
    return results

def save_to_csv(results, filename="prime_emergence_results.csv"):
    """Save results to CSV file"""
    import csv
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['N', 'π(N)', 'μ_c(N)', 'k_c(N)', 'C(N)', 'G(N)', 'c(N)', 'Goldbach_Pairs'])
        
        for r in results:
            writer.writerow([
                r['N'], r['m'], r['mu_c'], r['k_c'],
                r['C'], r['G'], r['c'], r['pairs']
            ])
    
    print(f"\nResults saved to {filename}")

def main():
    """Main function"""
    # Define N values to compute
    N_values = [30, 100, 200, 500, 1000]
    
    print("Prime Emergence Theorem - Batch Computation")
    print("=" * 60)
    
    # Compute constants
    results = compute_for_range(N_values)
    
    # Save results
    save_to_csv(results)
    
    # Print summary table
    print(f"\n{'='*80}")
    print("SUMMARY TABLE")
    print(f"{'='*80}")
    print(f"{'N':>6} {'π(N)':>6} {'μ_c(N)':>15} {'k_c(N)':>15} {'C(N)':>15} {'G(N)':>15} {'c(N)':>10}")
    print(f"{'-'*80}")
    
    for r in results:
        print(f"{r['N']:>6} {r['m']:>6} {r['mu_c']:>15.10f} {r['k_c']:>15.10f} "
              f"{r['C']:>15.10f} {r['G']:>15.10f} {r['c']:>10.6f}")

if __name__ == "__main__":
    main()
