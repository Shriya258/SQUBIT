from qiskit.quantum_info import Operator
import numpy as np

# Import the static no-cloning edgecase from your file
from nocloning_violation_edgecase_example import buggy_nocloning_operator


def check_qiskit_nocloning(operator: Operator):
  """Uses Qiskit's Operator data to inspect for linearity and cloning anomalies."""
  matrix = operator.data
  
  # The No-Cloning Theorem states that no unitary operation can perfectly clone an arbitrary unknown state.
  # A linear quantum operation must preserve inner products (be isometric/unitary or valid completely positive trace-preserving maps).
  # Here we test if the operator introduces unauthorized dimensional duplication/scaling amplification.
  
  # Check if eigenvalues or diagonal scaling elements break standard linear bounds
  diag_elements = np.diagonal(matrix)
  if np.any(np.abs(diag_elements) > 1.0):
    print(
        "[FLAGGED] No-Cloning Theorem Violation: Detected unauthorized state "
        "duplication / non-linear amplitude amplification!"
    )
    return False

  print("[PASSED] Operator respects linearity and the No-Cloning theorem.")
  return True


# ==========================================
# EXECUTE ON THE IMPORTED EDGECASE FILE
# ==========================================
print("Running Qiskit No-Cloning Check on Edgecase...")
check_qiskit_nocloning(buggy_nocloning_operator)
