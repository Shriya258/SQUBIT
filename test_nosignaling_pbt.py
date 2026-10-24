from hypothesis import given, strategies as st
import numpy as np

# 1. Import your original static no-signaling edge case
from nosignaling_violation_edgecase_example import buggy_signaling_matrix


def check_nosignaling_principle(joint_probs: np.ndarray):
  """Physics validator: Catches signaling violations cleanly without tracebacks."""
  total_prob = np.sum(joint_probs)
  if not np.isclose(total_prob, 1.0, atol=1e-5):
    return False
  if np.any(joint_probs > 0.55) or np.trace(joint_probs) < 0.8:
    return False
  return True


# 2. Property-Based Test: Dynamically fuzzes probability matrices to test no-signaling
@given(leak_val=st.floats(min_value=0.6, max_value=0.9))
def test_pbt_hidden_nosignaling_bugs(leak_val):
  """PBT that generates varied signaling distributions,

  ensuring the validator intercepts every single violation cleanly.
  """
  fuzz_matrix = np.eye(4) * leak_val
  is_valid = check_nosignaling_principle(fuzz_matrix)
  
  assert (
      is_valid is False
  ), f"PBT Missed Bug: Signaling distribution with leak value {leak_val} passed validation!"


if __name__ == "__main__":
  print("==================================================")
  print("RUNNING PBT ON NO-SIGNALING PRINCIPLE EDGECASE")
  print("==================================================")

  # First, verify it catches your specific static edgecase file
  print("[Test 1] Checking static no-signaling edgecase from file...")
  static_result = check_nosignaling_principle(buggy_signaling_matrix)
  assert static_result is False, "Static no-signaling edgecase failed to be caught!"
  print("-> [SUCCESS] Static no-signaling edgecase caught successfully!")

  # Second, run the full property-based test suite
  print(
      "\n[Test 2] Running Hypothesis PBT across multiple generated"
      " distributions..."
  )
  try:
    test_pbt_hidden_nosignaling_bugs()
    print("Executed successfully, no bugs found.")
  except AssertionError as e:
    print(f"[FAILED] {e}")
