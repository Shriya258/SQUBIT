from qiskit import QuantumCircuit

# Import the static empty qubits edgecase from your file
from empty_qubits_edgecase_example import buggy_empty_circuit


def check_qiskit_empty_qubits(circuit: QuantumCircuit):
  """Uses Qiskit's QuantumCircuit data to check if the register contains qubits."""
  if circuit.num_qubits == 0:
    print(
        "[FLAGGED] Structural Violation: Quantum circuit has 0 qubits"
        " (empty register)!"
    )
    return False

  print("[PASSED] Circuit has a valid qubit count.")
  return True


# ==========================================
# EXECUTE ON THE IMPORTED EDGECASE FILE
# ==========================================
print("Running Qiskit Empty Qubits Check on Edgecase...")
check_qiskit_empty_qubits(buggy_empty_circuit)
