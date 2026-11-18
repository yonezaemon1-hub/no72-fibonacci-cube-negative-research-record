#!/usr/bin/env python3
"""Independent standard-library checker for No72 Gamma_10 5-round 3-cop policy.

Neither compiles nor executes the program that generated the strategy.
Checks full adversarial branching, police legal moves, and irredundancy.
Does not verify the exhaustive lower bound/uniqueness claims; separate
C++ implementations for complete minimax are included for those claims.
"""
import csv
import itertools
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 10
COP_COUNT = 3
TURN_LIMIT = 5
V = tuple(i for i in range(1 << N) if not (i & (i >> 1)))
assert len(V) == 144
VERTICES = set(V)
NEIGHBORS = {x: tuple(y for y in V if (x ^ y).bit_count() <= 1) for x in V}
INITIAL = (0, 1, 512)
assert INITIAL == tuple(sorted(INITIAL))

policy = {}
with (HERE / 'No72_v017_GAMMA10_STRATEGY.csv').open(encoding='utf-8', newline='') as f:
    for row in csv.DictReader(f):
        t = int(row['t'])
        cops = tuple(int(row[f'c{i}']) for i in range(COP_COUNT))
        robber = int(row['r'])
        dest = tuple(int(row[f'next{i}']) for i in range(COP_COUNT))
        assert 1 <= t <= TURN_LIMIT
        assert cops == tuple(sorted(cops)) and dest == tuple(sorted(dest))
        assert all(x in VERTICES for x in cops + dest)
        assert robber in VERTICES and robber not in cops
        assert any(all(v in NEIGHBORS[u] for u, v in zip(cops, perm))
                   for perm in set(itertools.permutations(dest))), (t, cops, dest)
        key = t, cops, robber
        assert key not in policy, ('duplicate state', key)
        policy[key] = dest

visited = set()
def check(turn, cops, robber):
    if robber in cops:
        return
    assert turn >= 1
    state = turn, cops, robber
    assert state in policy, ('missing strategic action', state)
    if state in visited:
        return
    visited.add(state)
    dest = policy[state]
    if robber in dest:
        return
    assert turn > 1, ('robber escapes the last police move', state)
    for r_next in NEIGHBORS[robber]:
        check(turn - 1, dest, r_next)

for robber in V:
    check(TURN_LIMIT, INITIAL, robber)
assert len(policy) == len(visited), ('unreachable rows', len(policy), len(visited))
assert len(policy) == 7148
print('PASS: 144 legal initial robber placements and every subsequent response')
print('PASS: 7,148 unique, reachable, fully branched noncapture states')
print('PASS: three legal cops starting from (0,1,512) capture within five police moves')
print('STATUS: independent UPPER verification only; lower bound requires full minimax')
