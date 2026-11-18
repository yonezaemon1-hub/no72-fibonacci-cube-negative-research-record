#!/usr/bin/env python3
"""Independent exact check of the Gamma_9->Gamma_10 overlap obstruction.

Validates the endpoint projections as legal stay-allowed retractions and
confirms the exact overlap mismatch for the separately enumerated unique
Gamma9 winning placement. A full game enumeration is required to establish
that the supplied list of Gamma9 winners is COMPLETE.
"""
import csv
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent
n = 9
V9 = [x for x in range(1 << n) if not (x & (x >> 1))]
V10 = [x for x in range(1 << (n + 1)) if not (x & (x >> 1))]
assert (len(V9), len(V10)) == (89, 144)

left = lambda x: x & ((1 << n) - 1)
right = lambda x: x >> 1
# Verify both endpoint deletions on EVERY valid source vertex and edge.
assert all(left(x) in V9 and right(x) in V9 for x in V10)
for x in V10:
    for y in V10:
        if (x ^ y).bit_count() <= 1:
            assert (left(x) ^ left(y)).bit_count() <= 1
            assert (right(x) ^ right(y)).bit_count() <= 1

with (ROOT / 'No72_v018_GAMMA9_ALL_WINNING_STARTS.csv').open(newline='') as f:
    configs = [tuple(int(r[f'c{i}']) for i in range(3)) for r in csv.DictReader(f)]
assert configs == [(0, 1, 256)], configs
assert all(x in V9 for x in configs[0])

def suffix(A):
    return Counter(x >> 1 for x in A)

def prefix(B):
    return Counter(x & ((1 << (n-1)) - 1) for x in B)

assert all(suffix(A) != prefix(B) for A in configs for B in configs)
print('PASS: both endpoint deletions are legal stay-compatible retractions on all 144 vertices/edges')
print('PASS: unique supplied Gamma9 opening {0,1,256}, overlap suffix=(0,0,128), prefix=(0,0,1)')
print('PASS: incompatible overlap => NO Gamma10 three-cop four-turn victory (conditional on Gamma9 full-game enumeration)')
print('STATUS: Gamma10 lower bound uses the proved overlap theorem; novelty pending independent review')
