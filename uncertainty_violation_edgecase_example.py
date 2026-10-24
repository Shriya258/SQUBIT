import numpy as np

# Heisenberg Uncertainty Principle Violation: The product of standard deviations 
# for non-commuting observables (e.g., Pauli X and Pauli Z) must satisfy Delta A * Delta B >= 0.5.
# This static edge case defines an unphysical state where standard deviations violate the bound.
buggy_uncertainty_state = {
    "delta_x": 0.2,  # Too sharp
    "delta_z": 0.2,  # Too sharp -> Product is 0.04 (violates the 0.5 quantum limit!)
    "commutator_expectation": 1.0
}
