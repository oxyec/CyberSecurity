## 2025-07-28 - [Django Migration Conflict]
**Learning:** Conflicting migrations (`0001` and `0002` both creating `Post`) prevented tests from running. Safely resolved by emptying `0002` operations instead of deleting it, preserving history references.
**Action:** When fixing migration history, prefer emptying operations over deleting files to maintain dependency chains.
