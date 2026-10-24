from hypothesis import given, strategies as st
from qiskit import QuantumCircuit

# 1. Import your original static empty qubits edge case
from empty_qubits_edgecase_example import buggy_empty_circuit


def check_qiskit_empty_qubits(circuit: QuantumCircuit):
  """Structural validator: Catches 0-qubit registers cleanly without tracebacks."""
  if circuit.num_qubits == 0:
    return False
  return True


# 2. Property-Based Test: Dynamically fuzzes qubit register sizes from 0 to 5
@given(num_qubits=st.integers(min_value=0, max_value=5))
def test_pbt_empty_qubits(num_qubits):
  """PBT that generates circuits with varied qubit counts,

  ensuring 0-qubit registers are caught and valid ones pass.
  """
  qc = QuantumCircuit(num_qubits)

  # Run the validator
  is_valid = check_qiskit_empty_qubits(qc)

  if num_qubits == 0:
    # Invariant: 0-qubit registers must always be caught (return False)
    assert (
        is_valid is False
    ), f"PBT Missed Bug: Circuit with {num_qubits} qubits passed validation!"
  else:
    # Invariant: Valid qubit counts must pass
    assert (
        is_valid is True
    ), f"PBT False Positive: Valid circuit with {num_qubits} qubits was flagged!"


if __name__ == "__main__":
  print("==================================================")
  print("RUNNING PBT ON EMPTY QUBITS EDGECASE & FUZZING")
  print("==================================================")

  # First, verify it catches your specific static edgecase file
  print("[Test 1] Checking static empty qubits edgecase from file...")
  static_result = check_qiskit_empty_qubits(buggy_empty_circuit)
  assert static_result is False, "Static empty qubits edgecase failed to be caught!"
  print("-> [SUCCESS] Static empty qubits edgecase from file caught cleanly!")

  # Second, run the full property-based test suite
  print(
      "\n[Test 2] Running Hypothesis PBT across multiple generated qubit counts..."
  )
  try:
    test_pbt_empty_qubits()
    print(
        "[SUCCESS] PBT execution complete! All empty qubit violations and valid"
        " registers were handled correctly."
    )
  except AssertionError as e:
    print(f"[FAILED] {e}")
