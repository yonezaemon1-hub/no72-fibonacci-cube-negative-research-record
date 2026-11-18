# Frozen finite-game supporting code (Gamma_9 and Gamma_10)

All code here is supplied as reproducibility material for the **separately audited** finite-game claim `capt_3(Gamma_10)=5`. It is not a formal machine-checked mathematical proof. The static-cover paper itself does not recompute Gamma_10 capture time.

## Quick check (Python >=3.10)

From this directory:

```bash
python -B -I verify_gamma10_upper.py
python -B -I verify_overlap_obstruction.py
```

## Complete minimax recomputation (C++20)

```bash
g++ -O3 -std=c++20 no72_v017_generic_minimax.cpp -o no72_dp
./no72_dp 9 4
./no72_dp 10 5

g++ -O3 -std=c++20 no72_v017_csr_crosscheck.cpp -o no72_csr
./no72_csr 9 4 /tmp/no72_gamma9_winners.csv
./no72_csr 10 5 /tmp/no72_gamma10_winners.csv
```

Expected: Gamma_9 unique four-move winning opening `(0,1,256)`; Gamma_10 no four-move winning opening and 61 five-move winning openings. Program output and CSV ordering should be inspected; do not treat timeout as game loss or game win.

The CSV with 7,148 states certifies a five-move strategy from `(0,1,512)` when independently checked by Python. The Gamma_10 lower bound is independently supported by 9-dimensional uniqueness and the overlapping-retract obstruction, and by the complete minimax calculations.
