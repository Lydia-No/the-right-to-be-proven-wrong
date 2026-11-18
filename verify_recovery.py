#!/usr/bin/env python3
"""Exact finite checks for the mathematical supplement. Python 3.10+."""

from fractions import Fraction
from itertools import combinations
import json


def gf2_rank(vectors):
    """Rank of binary vectors represented by integer bit masks."""
    pivots = {}
    for vector in vectors:
        while vector:
            position = vector.bit_length() - 1
            if position in pivots:
                vector ^= pivots[position]
            else:
                pivots[position] = vector
                break
    return len(pivots)


def affine_rank(points, dimension):
    return gf2_rank((1 << dimension) | point for point in points)


def fixed_rate(nullity):
    return 1 - Fraction(1, 1 << nullity)


def verify_eight_probe_worlds():
    """Check projection rejection directly, independently of the rank formula."""
    points = tuple(range(8))
    worlds = range(256)
    model = {
        sum((((a & x).bit_count() + b) % 2) << x for x in points)
        for a in points for b in (0, 1)
    }
    assert len(model) == 16
    layouts = {
        "A": ({0, 1, 2, 3}, {4, 5, 6, 7}),
        "B": ({0, 1, 2, 4}, {3, 5, 6, 7}),
        "two_anchor_cover": ({0, 1, 2, 4, 7}, {0, 3, 5, 6, 7}),
    }
    expected = {"A": (128, 192), "B": (0, 0), "two_anchor_cover": (128, 192)}
    result = {}
    for name, groups in layouts.items():
        rejection_sets = []
        for size in range(9):
            for values in combinations(points, size):
                observed = set(values)
                # Both workflows cover Q. For this two-workflow fixture,
                # a nonempty set uses one setup if contained in either.
                setups = 0 if not observed else 1 if any(observed <= g for g in groups) else 2
                if size + setups > 5:
                    continue
                mask = sum(1 << x for x in observed)
                allowed = {world & mask for world in model}
                rejected = {world for world in worlds if world & mask not in allowed}
                nullity = size - affine_rank(observed, 3)
                assert Fraction(len(rejected), 256) == fixed_rate(nullity)
                assert not rejected.intersection(model)
                rejection_sets.append(rejected)
        fixed = max(map(len, rejection_sets))
        existential = len(set().union(*rejection_sets))
        assert (fixed, existential) == expected[name]
        result[name] = {"fixed_rejected": fixed, "existential_rejected": existential}

    # Every declared routine star query uses one setup before and after recovery.
    star_pairs = ((0, 1), (0, 2), (0, 4), (7, 3), (7, 5), (7, 6))
    for name in ("B", "two_anchor_cover"):
        assert all(any(set(pair) <= g for g in layouts[name]) for pair in star_pairs)
    return {"worlds": 256, "false_worlds": 240, "budget": 5, "layouts": result}


def verify_hamming_family(ell):
    dimension = (1 << ell) - 1
    point_count = 1 << dimension
    block_size = 1 << ell
    setup_fee = dimension - 2
    budget = 2 * dimension - 1
    checks = block_size - ell - 1

    def syndrome(point):
        value = 0
        for coordinate in range(dimension):
            if (point >> coordinate) & 1:
                value ^= coordinate + 1
        return value

    centers = [point for point in range(point_count) if syndrome(point) == 0]
    hamming_blocks = [
        {center} | {center ^ (1 << coordinate) for coordinate in range(dimension)}
        for center in centers
    ]
    flat_blocks = [set(range(start, start + block_size))
                   for start in range(0, point_count, block_size)]
    assert len(centers) == 1 << (dimension - ell)
    assert sorted(point for block in hamming_blocks for point in block) == list(range(point_count))
    assert sorted(point for block in flat_blocks for point in block) == list(range(point_count))
    assert budget - setup_fee == block_size
    assert budget - 2 * setup_fee == 3
    assert all(len(block) == block_size and affine_rank(block, dimension) == block_size
               for block in hamming_blocks)
    assert all(len(block) - affine_rank(block, dimension) == checks for block in flat_blocks)

    added_memberships = 0
    for center, ball in zip(centers, hamming_blocks):
        flat = {center ^ point for point in range(block_size)}
        shared = flat - ball
        expanded = ball | shared
        assert flat.intersection(ball) == {center} | {
            center ^ (1 << coordinate) for coordinate in range(ell)
        }
        assert len(shared) == checks
        assert affine_rank(expanded, dimension) == dimension + 1
        assert len(expanded) - affine_rank(expanded, dimension) == checks
        assert flat <= expanded
        assert len(flat) + setup_fee == budget
        assert len(flat) - affine_rank(flat, dimension) == checks
        assert all({center, center ^ (1 << coordinate)} <= expanded
                   for coordinate in range(dimension))
        added_memberships += len(shared)

    return {
        "ell": ell,
        "d": dimension,
        "probes": point_count,
        "workflows": len(centers),
        "read_size": block_size,
        "setup_fee": setup_fee,
        "budget": budget,
        "checks_per_completed_flat": checks,
        "added_memberships_per_workflow": checks,
        "total_added_memberships": added_memberships,
        "hamming_fixed_rate_all_worlds": "0",
        "flat_fixed_rate_all_worlds": str(fixed_rate(checks)),
        "recovered_fixed_rate_all_worlds": str(fixed_rate(checks)),
    }


def main():
    families = [verify_hamming_family(ell) for ell in (2, 3, 4)]
    assert [row["recovered_fixed_rate_all_worlds"] for row in families] == [
        "1/2", "15/16", "2047/2048"
    ]
    result = {
        "status": "PASS",
        "supplement_date": "2026-11-18",
        "scope": "Exhaustive eight-probe worlds and exact ranks at d=3,7,15",
        "eight_probe_enumeration": verify_eight_probe_worlds(),
        "hamming_flat_and_recovery": families,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
