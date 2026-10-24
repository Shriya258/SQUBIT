from hypothesis import given, strategies as st
import numpy as np

# 1. Import your original static tsirelson edge case
from tsirelson_violation_edgecase_example import buggy_chsh_value


def check_tsirelson_bound(chsh_value: float):
  """Physics validator: Catches CHSH values exceeding Tsirelson's bound cleanly without tracebacks."""
  tsirelson_limit = 2.0 * np.sqrt(2.0)
  if chsh_value > tsirelson_limit:
    return False
  return True


# 2. Property-Based Test: Dynamically fuzzes CHSH parameter values
@given(chsh_val=st.floats(min_value=2.01, max_value=4.0))
def test_pbt_hidden_tsirelson_bugs(chsh_val):
  """PBT that generates varied CHSH values beyond the quantum limit,

  ensuring the validator intercepts every single violation cleanly.
  """
  is_valid = check_tsirelson_bound(chsh_val)
  assert (
      is_valid is False
  ), f"PBT Missed Bug: CHSH value {chsh_val} passed validation!"


if __name__ == "__main__":
  print("==================================================")
  print("RUNNING PBT ON TSIRELSON'S BOUND EDGECASE & FUZZING")
  print("==================================================")

  # First, verify it catches your specific static edgecase file
  print("[Test 1] Checking static tsirelson edgecase from file...")
  static_result = check_tsirelson_bound(buggy_chsh_value)
  assert static_result is False, "Static tsirelson edgecase failed to be caught!"
  print("-> [SUCCESS] Static tsirelson edgecase caught successfully!")

  # Second, run the full property-based test suite
  print(
      "\n[Test 2] Running Hypothesis PBT across multiple generated CHSH"
      " values..."
  )
  try:
    test_pbt_hidden_tsirelson_bugs()
    print("Executed successfully, no bugs found.")
  except AssertionError as e:
    print(f"[FAILED] {e}")
