import numpy as np

# Hermiticity Violation: Hamiltonians and observables must satisfy H == H.conjugate().T.
# This static edge case defines a non-Hermitian matrix with complex/asymmetric components.
buggy_non_hermitian_matrix = np.array([
    [1.0, 2.0 + 1.0j],
    [2.0 - 0.5j, 3.0]  # Off-diagonal mismatch (2.0 + 1.0j vs 2.0 - 0.5j) breaks Hermiticity
])
