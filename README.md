# No.72 — A Failed Static-Certificate Route to Capture-Time Bounds on Fibonacci Cubes

**Version:** v1.0 negative research record (18 November 2026)  
**Author:** Ryutaro Yonezu  
**Type:** Negative Research Record / unrefereed preprint  
**License:** All rights reserved  
**Novelty:** INCONCLUSIVE  
**Human peer review:** None  
**Publication URLs and DOI:** Omitted until GitHub release and Zenodo record have been published and independently verified.

## What this record establishes

- Elementary 3-center and 4-center finite-radius coverings of even and odd Fibonacci cubes, respectively.
- The covers use fewer centers than the cop number in specified infinite families. **This does not establish that covering radius is smaller than the minimum-cop capture time in those infinite families.**
- At Gamma_10, static radius 4 with three centers coexists with the independently audited computer-assisted `capt_3(Gamma_10)=5`; the game value relies on the separately supplied finite-game certificate.
- At Gamma_11, the four-center covering and one particular Q6 delayed-retract necessary condition can both hold; **capt(Gamma_11)>=5 is not proved**. The inherited bound remains 4 <= capt(Gamma_11) <= 17.

## Files

- `No72_v10_NEGATIVE_RESEARCH_RECORD.pdf`, `.tex` — paper and source.
- `VERIFY_STATIC_BARRIER.py` — reproduces static geometry checks only (not a full game solver).
- `finite_game/` — minimal Gamma_9/Gamma_10 independent-game evidence code and the 7,148-row Gamma_10 winning policy. See `finite_game/README.md`.
- `NOVELTY_AND_AUDIT_SCOPE.md` — references, limits, reported independent audit status.
- `LICENSE.txt` — All rights reserved.
- `SHA256SUMS.txt` — checksums for all distribution files (excluding this manifest itself).

## Limitations

Neither the infinite-family covering formula nor the failed proof route is claimed as a major independent theorem or established mathematical novelty. No formal proof assistant certificate, complete prior-art review, or human peer review is claimed. No private raw Windows logs or historical failed proof files are distributed.

## Quick verification

From the package root:

```bash
python -B -I VERIFY_STATIC_BARRIER.py
python -B -I finite_game/verify_gamma10_upper.py
python -B -I finite_game/verify_overlap_obstruction.py
```

To independently recompute the finite minimax values use the two C++20 implementations documented in `finite_game/README.md`.
