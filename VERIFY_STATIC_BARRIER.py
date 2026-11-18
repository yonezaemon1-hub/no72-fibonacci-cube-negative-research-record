#!/usr/bin/env python3
"""Independent elementary BFS checks for No.72 v0.23 (not a capture-time solver)."""
from collections import deque
from math import ceil
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parent

def vertices(n):
    return [x for x in range(1 << n) if not x & (x >> 1)]

def distances(n, centers, vv):
    allowed = set(vv)
    ds = {}
    for start in centers:
        assert start in allowed
        queue = deque([start]); di = {start: 0}
        while queue:
            v = queue.popleft()
            for b in range(n):
                w = v ^ (1 << b)
                if w in allowed and w not in di:
                    di[w] = di[v] + 1
                    queue.append(w)
        assert len(di) == len(vv), (n, start, len(di))
        for v in vv:
            assert di[v] == (v ^ start).bit_count(), (n, start, v)
        ds[start] = di
    return ds

def cop_number(n):
    return (((n + 1) // 2 + 2) // 2)

def check(n):
    v = vertices(n)
    m = n // 2
    c = (0, 1, 2) if n % 2 == 0 else (0, 1, 2, 20)
    r = m-1
    maps = distances(n, c, v)
    uncovered = [x for x in v if min(maps[y][x] for y in c) > r]
    assert not uncovered, (n, uncovered)
    maximum = max(min(maps[y][x] for y in c) for x in v)
    assert maximum <= r
    return (n,len(v),len(c),r,maximum,cop_number(n))

def main():
    results = []
    for n in range(2,20):
        if n % 2 == 1 and n < 5: continue
        row = check(n)
        results.append(row)
        print('PASS n=%02d |V|=%05d centers=%d radius=%d maxdist=%d c(Gamma_n)=%d' % row)
    assert check(10)[2:4] == (3,4)
    assert check(11)[2:4] == (4,4)
    assert all(cop_number(n)>3 for n in range(12,20,2))
    assert all(cop_number(n)>4 for n in range(15,20,2))
    n=11; v=vertices(n); oddmask=sum(1<<i for i in range(1,n,2))
    H=set(x for x in v if not (x&oddmask))
    assert len(v)==233 and len(H)==64
    C=(0,1,2,20)
    assert [min((c^h).bit_count() for h in H) for c in C] == [0,0,1,0]
    assert all(c in v for c in C)
    assert all(any((x^c).bit_count()<=4 for c in C) for x in v)
    assert all((x&~oddmask) in H for x in v)
    print('PASS Gamma11 combined static radius-4 and Q6 delayed-retract checks')
    print('NOTE: this does not test any 4-turn winning strategy, or prove capt(Gamma11)>=5')
    for name, expect in (
      ('No72_v018_WINDOWS_EVIDENCE_AUDITED_PRIVATE_HOLD_20261118.zip', '7cddb0a34ec12412870b0a8e95739c7314bc0c7c0b11cd732aefeee6ec9db621'),
      ('No72_v022_DELAYED_RETRACT_PRIVATE_HOLD.zip', '6a2373378cdca3b6cabb59aaa785b7f6cc4d5db4516ee1bc4f4df2642428a54f')):
        p=ROOT/name
        if p.exists():
            actual=hashlib.sha256(p.read_bytes()).hexdigest()
            assert actual==expect,(name, actual)
            print('PASS inherited frozen parent SHA256:',name)
    print('FINAL: PASS STATIC_BARRIER_ONLY')

if __name__ == '__main__': main()
