# The Right to Be Proven Wrong

**Preserving the Conditions for Challenging an Explanatory Framework**

Research author: **Linda Thorstensen**, independent researcher. AI x Epistemics Research Sprint, Apart Research, November 2026 (Track 4: Open Track).

A resource-bounded system may retain ordinary error detection, individual evidence access and lower-order joint feasibility while losing affordable ways to reject an inadequate explanatory class. This repository accompanies a bounded research application of Future Capability Preservation (FCP), developed by Linda Thorstensen.

## Interactive experiment

[PROVE ME WRONG — guided counterfactual experience](experience.html) (download and open locally). Choose between two equally optimal workflows, spend a real simulated investigation budget, then replay the same hidden world. Blind mode includes adequate-class controls. The operations assistant is scripted; no live model is evaluated. The exact fixture and disclosure scope are unchanged.

[Download the standalone interactive laboratory](index.html) (open the downloaded file in a browser). Optimize an evidence network, investigate one hidden world, then compare alternative arrangements or budgets. The laboratory uses only the public eight-probe fixture, includes an exact mathematical self-test, and needs no external service. The guided world is deliberately constructed, not a sampled empirical result. The demonstration was created on 16 November 2026 during the stated submission interval.

## Reproduce selected results

Requires Python 3.10 or newer; standard library only. No network access, credentials, model weights or external data required.

```sh
python verify.py
```

Compare the output with `expected_results.json`. This standalone reconstruction, prepared on 16 November 2026, checks selected results of the finite structural benchmark; it is not the original adaptive policy implementation or a reproduction of every experiment in the manuscript.

| Budget-five measurement | Layout A | Layout B |
|---|---:|---:|
| Affordable singletons / pairs / triples | 8/28/56 | 8/28/56 |
| Affordable quadruples | 2 | 2 |
| Zero-model refutation, fixed scan | 240/256 | 240/256 |
| Constant-class rejection, fixed scan | 224/254 | 224/254 |
| Affine-class rejection, fixed scan | 128/240 | 0/240 |
| Existential affine rejection | 192/240 | 0/240 |

The checker also enumerates all 35 balanced partitions, verifies the workload mixture threshold of 3/5, and checks the single-membership recovery in all eight possible copy placements across 30 coordinate-permuted affine classes. With one additional membership and budget six, a fixed five-observation set permits rejection of 128/240 inadequate worlds in every class, even without class identity at selection time. Class identity is needed at adjudication.

### Reproduce the workload comparison

```sh
python verify_workloads.py
```

Compare the output with `workload_results.json`. The four declared routine demand families are enumerated across all 35 balanced partitions. The results distinguish retention of the starting layout under strict-improvement scheduling from the range of capabilities across tied optima. This supplemental checker uses the same public eight-probe fixture; no other experimental materials are included.

## Scope and provenance

The fixture is finite, noiseless and synthetic. Individual read and workflow setup costs are stipulated; replication and maintenance costs are excluded. Existential coverage is a reference capability, not achieved investigator performance. The class family is bounded. No empirical AI effect, pretrained-model evaluation, external replication, general scientific priority or intervention superiority is claimed.

FCP predates the sprint. The exact structural benchmark and recovery extensions were developed on 16 November 2026 during the stated submission interval, after the scheduled 13–15 November sprint sessions. Eligibility for this later work has not been independently confirmed. AI assistance supported computational implementation, verification and editing under the research author's direction.

Related prior work by Linda Thorstensen:
- [Future Capability Preservation: A Missing Dimension in System Optimization](https://doi.org/10.2139/ssrn.6892998)
- [Future Capability Preservation: A General Theory for Evaluating Transformation](https://doi.org/10.2139/ssrn.7210078)

## Rights

Copyright © 2026 Linda Thorstensen. All rights reserved. No open-source license or license to unpublished research, architectures, inventions or other intellectual property is granted by this repository. Statutory rights and applicable third-party platform terms remain unaffected.
