# Preserving affordable falsification

**Mathematical supplement added 18 November 2026**  
**Research author — Linda Thorstensen**

This supplement develops the geometry behind the public sprint fixture. It gives a family of workflow arrangements that lose affordable rejection of an explanatory class, followed by a choice of shared records that restores rejection at the same investigation budget. The construction assumes that the affine explanatory class and the probe coordinates are known when the shared records and the read are selected.

The public sprint reconstruction is recorded at commit `3cb1a24906558451d395e34ec5a91631e1f07e51`, dated 16 November 2026. This supplement was added on 18 November. The results here are additional mathematical analysis. The original scripts document their own reconstruction scope and provenance.

## 1. What makes a set of observations capable of rejection

Let $Q$ contain $n$ probes with binary observations. Let $\mathcal M\subseteq\mathbb F_2^Q$ be a linear explanatory class of dimension $r$. A world $w$ can be rejected on an observed set $S$ precisely when no $m\in\mathcal M$ agrees with $w$ on $S$.

Write $\mathcal M|_S$ for the restricted class and define

$$
\nu(S)=|S|-\dim(\mathcal M|_S).
$$

This is the number of independent parity checks supported entirely inside $S$. Under a uniform distribution over all $2^n$ worlds, the probability of evidence-warranted rejection on a fixed set is

$$
P(S)=1-2^{-\nu(S)}.
$$

**Proof.** The observation on $S$ is uniform over $2^{|S|}$ possible strings. Exactly $2^{\dim(\mathcal M|_S)}$ strings belong to the restricted class. Subtract their proportion from one.

For any affordable family $\mathcal F$, the best fixed read therefore has rate

$$
P_{\mathrm{fixed}}=1-2^{-\max_{S\in\mathcal F}\nu(S)}.
$$

For existential coverage, let $\mathcal Z$ be the span of all dual parity checks supported in affordable sets. A world escapes every affordable rejection precisely when it is orthogonal to $\mathcal Z$. Thus

$$
P_{\mathrm{existential}}=1-2^{-\dim\mathcal Z}.
$$

These are different quantities. Existential coverage counts worlds with some affordable witness. The fixed-read rate counts rejection achieved by choosing one set before observing the world. Conditional rates among worlds outside $\mathcal M$ divide either unconditional rate by $1-2^{-(n-r)}$, since every rejected world lies outside $\mathcal M$.

## 2. Two arrangements with the same affordable-set structure

Choose an integer $\ell\ge2$ and put $d=2^\ell-1$, $Q=\mathbb F_2^d$. The explanatory class is

$$
\mathcal M=\{x\mapsto a\cdot x+b\mid a\in\mathbb F_2^d,\ b\in\mathbb F_2\}.
$$

It has dimension $d+1$. For $S\subseteq Q$, form the columns $(1,x)$ for $x\in S$. Their rank equals $\dim(\mathcal M|_S)$. Every set of at most three distinct points has independent columns. Four distinct points with XOR zero form a minimal parity check. Hence the dual girth is four.

Read cost is one per distinct probe, with setup fee $\sigma=d-2$ for each workflow used. Set the budget to

$$
B=2d-1=(d+1)+\sigma.
$$

Compare partitions into blocks of $d+1=2^\ell$ probes.

**Hamming partition.** Label the $d$ coordinates by the nonzero vectors $h_1,\ldots,h_d$ of $\mathbb F_2^\ell$. Use centers

$$
\mathcal H=\left\{c\in\mathbb F_2^d\mid\sum_i c_i h_i=0\right\}
$$

and blocks $H_c=\{c,c+e_1,\ldots,c+e_d\}$. These blocks partition $Q$. To see uniqueness, compute the syndrome of any point $x$. A zero syndrome makes $x$ a center. Otherwise there is a unique coordinate $i$ whose label equals the syndrome, and $x+e_i$ is the unique center at distance one.

Translation by $c$ takes $H_c$ to $\{0,e_1,\ldots,e_d\}$, an affine basis. Consequently every subset inside one Hamming block has zero dual nullity.

**Flat partition.** Fix an $\ell$-dimensional linear subspace $V\subseteq\mathbb F_2^d$ and use its affine cosets as blocks. Each has $2^\ell$ points and affine rank $\ell+1$, giving

$$
k=2^\ell-\ell-1
$$

independent checks per full block.

A read using two or more workflows has at most

$$
B-2\sigma=3
$$

probes and therefore cannot reject the class. Within a single workflow, every subset of its $d+1$ points is affordable. The two partitions consequently have isomorphic affordable simplicial complexes under any bijection matching their blocks. Their fixed-read rejection rates are exactly

$$
P_{\mathrm{Hamming}}=0,\qquad
P_{\mathrm{flat}}=1-2^{-k}.
$$

The Hamming existential rate is also zero. The flat formula displayed here is the fixed-read rate. As $\ell\to\infty$, $k\to\infty$ and the fixed-read gap tends to one.

## 3. Shared records recover the rate at the same budget

For each Hamming center $c$, choose the flat

$$
F_c=c+\operatorname{span}(e_1,\ldots,e_\ell).
$$

Its intersection with $H_c$ consists exactly of $c,c+e_1,\ldots,c+e_\ell$. Add the remaining points as shared memberships

$$
Y_c=F_c\setminus H_c,\qquad |Y_c|=2^\ell-\ell-1=k,
$$

and let $U_c=H_c\cup Y_c$. A shared membership provides access to the same probe observation from another workflow. Copies represent one coordinate of the world.

**Fixed-budget recovery theorem.** For the cover $\{U_c\}$, where a read costs its number of distinct probes plus $\sigma$ times the number of workflows used, the best fixed-read rejection rate at the original budget $B$ is exactly $1-2^{-k}$.

**Proof.** The read $F_c\subseteq U_c$ has $2^\ell=d+1$ probes and costs $(d+1)+\sigma=B$. Its affine rank is $\ell+1$, so it exposes $k$ independent checks and attains rejection $1-2^{-k}$.

For the upper bound, $U_c$ contains the affine basis $H_c$. Its affine rank is $d+1$ and its dual nullity is $|U_c|-(d+1)=k$. Every subset of $U_c$ supports at most those $k$ independent checks. Reads requiring multiple workflows contain at most three probes and support zero checks. No affordable fixed read can exceed the rate attained by $F_c$.

Arbitrary sets of $k$ distinct external points also give nullity $k$ to the whole expanded block. The flat-completion choice above ensures that all $k$ checks fit inside a read of $d+1$ probes. If a workflow contains only $t$ added memberships, it has total nullity $t$. Therefore at least $k$ additions to some single workflow are required to reach this fixed-read rate under this budget model.

| $\ell$ | $d$ | Probes read | Setup fee | Budget | Added memberships per workflow | Hamming rate | Flat and recovered fixed-read rate |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 3 | 4 | 1 | 5 | 1 | 0 | $1/2$ |
| 3 | 7 | 8 | 5 | 13 | 4 | 0 | $15/16$ |
| 4 | 15 | 16 | 13 | 29 | 11 | 0 | $2047/2048$ |

At $d=7$, the four added points relative to center zero are $e_1+e_2$, $e_1+e_3$, $e_2+e_3$, and $e_1+e_2+e_3$. Together with $0,e_1,e_2,e_3$, they form the eight-point read. Its four checks give a rejection rate of 93.75% over all worlds. The conditional rate among false worlds is $(15/16)/(1-2^{-120})$.

## 4. Connection to the eight-probe sprint fixture

The published Layout B consists of $\{0,1,2,4\}$ and $\{3,5,6,7\}$. Each is a Hamming block and supports no affine check. Adding one membership to each can produce

$$
U_0=\{0,1,2,4,7\},\qquad
U_7=\{0,3,5,6,7\}.
$$

At budget five, each workflow contains an affordable four-point parity check. The two checks are independent, giving fixed-read rejection $128/256$ and existential coverage $192/256$. The corresponding conditional rates are $128/240$ and $192/240$. This recovers Layout A's two reference rates for the known affine class.

The README also describes a distinct guarantee over 30 coordinate-permuted classes. Its single-copy budget-six result chooses five observations without using class identity. The construction in this supplement uses the known affine geometry when choosing the memberships and the read. It establishes the stated guarantee for that class.

Every original center-to-neighbor routine query remains available within its Hamming workflow. For a demand distribution supported on those pairs, mean setup cost stays at its lower bound $\sigma$. The cover adds $k$ memberships per workflow. Storage, synchronization, access-control, replication and maintenance costs are excluded from this setup-cost calculation, as in the public fixture.

## 5. Reproduction and interpretation

Run the supplement from the repository root with Python 3.10 or newer.

```sh
python verify_recovery.py
```

Compare the JSON output with `recovery_results.json`. The checker exhaustively enumerates all 256 worlds and affordable sets for the eight-probe comparisons. For $d=3,7,15$, it constructs both full partitions, checks every Hamming block and every flat block by exact binary rank, and checks every completed workflow and its affordable flat read. The formulas and proof establish the general family and its limit.

The mathematical mechanism is that affordable evidence can expose zero parity checks even when the whole world violates the explanatory class. A geometric choice of shared memberships restores an affordable set of checks. Applying this mechanism to operational records requires a specified explanatory class, identified witnesses and an access-cost model. These results concern the finite synthetic model and its mathematical extension.
