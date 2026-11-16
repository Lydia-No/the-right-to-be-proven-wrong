#!/usr/bin/env python3
"""Reproduce Table 2 for the public eight-probe fixture. Standard library only."""
from itertools import combinations
from fractions import Fraction
import json

Q = frozenset(range(8))
A = (frozenset((0, 1, 2, 3)), frozenset((4, 5, 6, 7)))
B = (frozenset((0, 1, 2, 4)), frozenset((3, 5, 6, 7)))
parts = [(frozenset(s), Q - frozenset(s))
         for s in combinations(sorted(Q), 4) if 0 in s]
assert len(parts) == 35
pairs = list(combinations(sorted(Q), 2))
workloads = {
    "anchored_sensitivity": [(0,1),(0,2),(0,4),(3,7),(5,7),(6,7)],
    "all_cube_edges": [(i,j) for i,j in pairs if (i ^ j).bit_count() == 1],
    "feature_slices": [(i,j) for i,j in pairs if (i >> 2) == (j >> 2)],
    "uniform_pairs": pairs,
}
assert [len(p) for p in workloads.values()] == [6,12,12,28]

def mean_setup(layout, demand):
    return Fraction(sum(1 if any(i in g and j in g for g in layout) else 2
                        for i,j in demand), len(demand))

# Direct projection of the 16 affine truth tables; no rank shortcut.
affine = {sum((((a & x).bit_count() + b) % 2) << x for x in Q)
          for a in Q for b in (0,1)}
assert len(affine) == 16

def fixed_rejection(layout):
    mask = sum(1 << x for x in layout[0])
    allowed = {w & mask for w in affine}
    return sum((w & mask) not in allowed for w in range(256) if w not in affine)

result = {}
for name,demand in workloads.items():
    costs = {p:mean_setup(p,demand) for p in parts}
    best = min(costs.values())
    optimal = [p for p in parts if costs[p] == best]
    # Strict improvement from A: keep A if already optimal. Else select
    # lexicographically first optimum, without using rejection in selection.
    selected = A if A in optimal else min(optimal,key=lambda p:tuple(sorted(p[0])))
    rejected = [fixed_rejection(p) for p in optimal]
    result[name] = {
        "pair_count":len(demand), "optimal_mean_setup":str(best),
        "optimal_layouts":len(optimal),
        "optima_with_positive_reference_rejection":sum(x>0 for x in rejected),
        "reference_rejected_from_A":fixed_rejection(selected),
        "min_reference_rejected_among_optima":min(rejected),
        "max_reference_rejected_among_optima":max(rejected),
    }
assert [(v["optimal_mean_setup"],v["optimal_layouts"],v["reference_rejected_from_A"])
        for v in result.values()] == [("1",1,0),("4/3",3,128),("1",1,128),("11/7",35,128)]
assert result["uniform_pairs"]["optima_with_positive_reference_rejection"] == 7

# At the documented 3/5 mixture, both layouts are equally efficient.
a = Fraction(3,5)
mixed = {p:a*mean_setup(p,workloads["anchored_sensitivity"])
          +(1-a)*mean_setup(p,workloads["feature_slices"]) for p in parts}
assert min(mixed.values()) == Fraction(6,5)
assert {p for p,v in mixed.items() if v == min(mixed.values())} == {A,B}
assert (fixed_rejection(A),fixed_rejection(B)) == (128,0)
print(json.dumps({"status":"PASS","worlds":256,"inadequate_reference_worlds":240,
                  "balanced_partitions":len(parts),"workloads":result,
                  "matched_tie":{"anchored_share":"3/5","mean_setup":"6/5",
                                 "A_rejected":128,"B_rejected":0}},indent=2))
