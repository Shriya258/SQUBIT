from qiskit.quantum_info import DensityMatrix

# Positivity Violation concept: A density matrix with negative eigenvalues (unphysical state).
# Here we define a matrix where diagonal elements or eigenvalues dip below zero.
buggy_density_matrix = DensityMatrix([[1.5, 0.0], [0.0, -0.5]])
