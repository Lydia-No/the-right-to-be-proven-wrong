#!/usr/bin/env python3
"""Standalone finite reconstruction of selected sprint results. Python 3.10+."""
from itertools import combinations, permutations
from fractions import Fraction
import json
from pathlib import Path

Q = frozenset(range(8))
W = range(256)
A = (frozenset((0, 1, 2, 3)), frozenset((4, 5, 6, 7)))
B = (frozenset((0, 1, 2, 4)), frozenset((3, 5, 6, 7)))

def subsets(k):
    return [frozenset(s) for s in combinations(sorted(Q), k)]

def mask(s):
    return sum(1 << i for i in s)

def affordable(groups, budget):
    return [s for k in range(9) for s in subsets(k)
            if not s or k + (1 if any(s <= g for g in groups) else 2) <= budget]

# Direct enumeration of affine truth tables, not a trained model or judge.
AFFINE = tuple(sorted(sum((((a & x).bit_count() + b) % 2) << x for x in Q)
                      for a in Q for b in (0, 1)))
CONSTANT = (0, 255)
ZERO = (0,)
CLASSES = sorted({tuple(sorted(sum(((w >> i) & 1) << p[i] for i in Q)
                               for w in AFFINE)) for p in permutations(sorted(Q))})
assert len(CLASSES) == 30

def rejection(model, s):
    m = mask(s)
    permitted = {w & m for w in model}
    return frozenset(w for w in W if w & m not in permitted)

def summary(groups):
    sets = affordable(groups, 5)
    fixed = groups[0]
    return {"affordable_counts_1_to_4": [sum(len(s) == k for s in sets) for k in range(1, 5)],
            "fixed_zero_rejected": len(rejection(ZERO, fixed)),
            "fixed_constant_rejected": len(rejection(CONSTANT, fixed)),
            "fixed_affine_rejected": len(rejection(AFFINE, fixed)),
            "affine_existential": len(set().union(*(rejection(AFFINE, s) for s in sets)))}

rows = {"A": summary(A), "B": summary(B)}
assert rows['A'] == dict(affordable_counts_1_to_4=[8,28,56,2],fixed_zero_rejected=240,fixed_constant_rejected=224,fixed_affine_rejected=128,affine_existential=192)
assert rows['B'] == dict(affordable_counts_1_to_4=[8,28,56,2],fixed_zero_rejected=240,fixed_constant_rejected=224,fixed_affine_rejected=0,affine_existential=0)

parts = [(s, Q-s) for s in subsets(4) if 0 in s]
assert len(parts) == 35
assert sum(bool(rejection(AFFINE, p[0])) for p in parts) == 7

# Workload-only selection, with no latent world or explanatory class input.
star = [(0,1),(0,2),(0,4),(7,3),(7,5),(7,6)]
flat = [pair for g in A for pair in combinations(sorted(g),2)]
def within(groups, pairs):
    return Fraction(sum(any(set(pair) <= g for g in groups) for pair in pairs),len(pairs))
def winners(a):
    scores = [a*within(p,star)+(1-a)*within(p,flat) for p in parts]
    return {p for p,v in zip(parts,scores) if v == max(scores)}
assert winners(Fraction(0)) == {A}
assert winners(Fraction(3,5)) == {A,B}
assert winners(Fraction(1)) == {B}
# Each objective is affine in mixture share; endpoint maxima and the tie
# establish the two open intervals by linear interpolation.

# A single copied membership restores a witness for each class.
recovered = []
for j in range(2):
    for x in sorted(B[1-j]):
        g = tuple(b | {x} if i == j else b for i,b in enumerate(B))
        four = [s for s in affordable(g,5) if len(s)==4]
        guaranteed = min(max(len(rejection(c,s)) for s in four) for c in CLASSES)
        existential = min(len(set().union(*(rejection(c,s) for s in four))) for c in CLASSES)
        five = g[j]
        blind = min(len(rejection(c,five)) for c in CLASSES)
        assert (guaranteed, existential, blind) == (128,128,128)
        assert within(g,star) == 1 and five in affordable(g,6)
        recovered.append([j,x])
# With no copy, five reads cost seven; all five-probe subsets work.
assert max(map(len, affordable(B,6))) == 4
assert max(map(len, affordable(B,7))) == 5
assert all(len(rejection(c,s)) == 128 for c in CLASSES for s in subsets(5))
result = {"status":"PASS", "worlds":256, "affine_classes":30,
          "denominators":{"zero_all_worlds":256,"constant_inadequate_worlds":254,"affine_inadequate_worlds":240},
          "layouts":rows,"balanced_partitions":35,"affine_viable_partitions":7,
          "workload_transition":"3/5", "single_copy_options_verified":len(recovered),
          "single_copy_worst_class_aware_at_budget_5":"128/240",
          "single_copy_worst_class_blind_fixed_five_reads_at_budget_6":"128/240",
          "no_copy_worst_class_blind_fixed_five_reads_at_budget_7":"128/240"}
print(json.dumps(result,indent=2))
