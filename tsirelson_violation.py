import numpy as np

# Import the static tsirelson edgecase from your file
from tsirelson_violation_edgecase_example import buggy_chsh_value


def check_tsirelson_bound(chsh_value: float):
  """Checks if a CHSH correlation parameter respects Tsirelson's bound (S <= 2*sqrt(2))."""
  tsirelson_limit = 2.0 * np.sqrt(2.0)

  # Tsirelson's Bound: Quantum mechanics restricts CHSH values to a maximum of 2*sqrt(2).
  # Anything higher requires hypothetical "super-quantum" correlations (PR boxes).
  if chsh_value > tsirelson_limit:
    print(
        f"[FLAGGED] Tsirelson's Bound Violation: CHSH value {chsh_value} exceeds "
        f"the quantum limit {tsirelson_limit:.4f} (Unphysical / Super-quantum correlation)!"
    )
    return False

  print("[PASSED] CHSH correlation respects Tsirelson's bound.")
  return True


# ==========================================
# EXECUTE ON THE IMPORTED EDGECASE FILE
# ==========================================
print("Running Tsirelson's Bound Check on Edgecase...")
check_tsirelson_bound(buggy_chsh_value)
