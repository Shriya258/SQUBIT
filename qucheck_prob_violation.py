from hypothesis import given, strategies as st
from qiskit.quantum_info import Statevector
import numpy as np


# Import your validation function or logic
def check_qiskit_probability(state_vector: Statevector):
  amplitudes = state_vector.data
  total_prob = np.sum(np.abs(amplitudes) ** 2)

  if not np.isclose(total_prob, 1.0, atol=1e-7):
    # Successfully flags the violation instead of crashing with a traceback
    return False
  return True


# Strategy to generate random complex amplitude pairs that DO NOT sum to 1.0 (Flawed Physics)
@given(
    real_part=st.floats(min_value=1.5, max_value=5.0),
    imag_part=st.floats(min_value=0.0, max_value=2.0),
)
def test_pbt_probability_violation(real_part, imag_part):
  # Construct a deliberately unnormalized quantum state vector
  flawed_state = Statevector([real_part + 1j * imag_part, 0.0])

  # Property: The validator MUST return False (caught violation) and NOT raise an error
  result = check_qiskit_probability(flawed_state)

  assert (
      result is False
  ), "PBT Failed: Unnormalized state was incorrectly approved!"


if __name__ == "__main__":
  # Run the property-based test manually or via pytest
  print("Running Property-Based Testing (PBT) for Probability Violation...")
  try:
    test_pbt_probability_violation()
    print(
        "[PASSED] PBT successfully verified that all generated flawed states"
        " were caught!"
    )
  except AssertionError as e:
    print(f"[FAILED] {e}")
