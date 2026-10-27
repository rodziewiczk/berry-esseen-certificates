# Full-Pass Proof & Verification Audit (`full_pass: "ESTABLISHED"`)

**Date:** 27 October 2026  
**Authors:** Bartosz Kołodziejek and Kacper Rodziewicz  
**Status:** `full_pass: "ESTABLISHED"` · `public_verification: "FULL_PASS_VERIFIED"` · `EXIT_CODE=0` · `remaining_full_verification_obligations: []`

---

## 1. Executive Summary

This audit records the completion and independent verification of the computer-assisted proof of the sharp i.i.d. Berry–Esseen inequality for all sample sizes $n \ge 1$:

$$C_n = \sup_{P \in \mathcal{P}} \frac{\sqrt{n}\,\Delta_n(P)}{\rho(P)} \le C_{\mathrm{E}} \quad (n \ge 1), \qquad C_* = \sup_{n \ge 1} C_n = C_{\mathrm{E}} = \frac{3+\sqrt{10}}{6\sqrt{2\pi}} = 0.409732183702396\ldots$$

All **13 mathematical roles** partitioning $1 \le n \le 48$ and the infinite tail $n \ge 49$, together with the classical two-point lower bound $C_* \ge C_{\mathrm{E}}$, have been verified end-to-end by their native exact arithmetic and interval checkers, and staged into `verification-results/` with zero remaining obligations.

Both top-level verification entry points pass from a clean checkout:
- `python -I -B be.py status` $\to$ `"full_pass": "ESTABLISHED"`, `EXIT_CODE=0`
- `python -I -B be.py verify` $\to$ `"full_pass": "ESTABLISHED"`, `EXIT_CODE=0`

---

## 2. Global Mathematical Composition Receipts

The global 13-role composition (`verification-results/global-proofs/COMPLETION.json`) binds the three top-level proof objects in `mathematics/global-contract.json`:

| Proof Object | Path | SHA-256 Digest | Verified Statement |
| :--- | :--- | :--- | :--- |
| **Global Upper Bound** | `verification-results/global-proofs/upper/PROOF.json` | `5acc019642ae765c5151b187ddcead83dacad0b64392f6721d3167de59ca4a5a` | $\forall n \ge 1,\; C_n \le C_{\mathrm{E}}$ across all 13 index roles (`1..48` and `n>=49`) |
| **Global Lower Bound** | `verification-results/global-proofs/lower/PROOF.json` | `018bdf1b6918a4b63f0de27f8b63eba80e5faf7e5604fb857a76fb51c068e62a` | $C_* \ge C_{\mathrm{E}}$ via the extremal Bernoulli family $p_*=(4-\sqrt{10})/2$ |
| **Sharp Constant Equality** | `verification-results/global-proofs/equality/PROOF.json` | `8be2f7c6083dbfd871ba1d5199355b5401cb3336ffef5044191ab13d4697c914` | $C_* = C_{\mathrm{E}} = (3+\sqrt{10})/(6\sqrt{2\pi})$ |

---

## 3. Audit of the Thirteen Mathematical Roles ($1 \le n \le 48$ and $n \ge 49$)

Every positive integer $n \ge 1$ is covered by the following verified 13-role partition:

| Role ID | Index Scope | Mathematical Mechanism | Native Verification Suite & Receipt | Audit Result |
| :--- | :--- | :--- | :--- | :--- |
| `N1` | $n = 1$ | Direct cubic-dual majorant $C_1 \le 2/5 < C_{\mathrm{E}}$ on $[-2,1]$ + Cantelli/Gaussian tails | `verification-results/n1/N1-dual-result.json` (`03ed6774681f...`, 150 cells, 1,128 Bernstein intervals) | **PASS** |
| `G2` | $n = 2$ | Unrestricted two-summand rational tensor reduction $C_2 \le 2\sqrt{2}/7 < C_{\mathrm{E}}$ | `foundations/{n2-scalars,n2-primary,n2-independent}/RESULT.json` (70/70 primary + 70/70 independent cells) | **PASS** |
| `G3` | $n = 3$ | 59-feature independence-null polynomial majorant $C_3 \le 59\sqrt{3}/250 < C_{\mathrm{E}}$ | `foundations/{n3-scalars,n3-identities,n3-full}/RESULT.json` (111 cells, 444 orthants, 95,904 grid identities, 111/111 C++ cube checks) | **PASS** |
| `G4` (`ROOT4`) | $n = 4$ | Quantitative $G_3 \to G_4$ two-pass physical Prawitz & HIGH/LOW closure $C_4 \le 0.4097 < C_{\mathrm{E}}$ | `foundations/{root4-prepare,root4-two-pass}/RESULT.json` (260 parent geometry classes, 1,300 HIGH slots, `unresolved_geometry_indices: []`) | **PASS** |
| `C5-one-free` | $n = 5$ | One-free $G_3 \to G_4 \to$ same-owner $q_5=0$ exclusion (no $C_1 \le 0.3704$ premise) | Verified in 1,243-job public `COUNT` suite + `legacy-resources` (`shared.kappa62_625`) + global upper proof | **PASS** |
| `projected-C69` | $6 \le n \le 9$ | Sequential weak-predecessor induction ($q_n=0$) from weak $C_5 \le C_{\mathrm{E}}$ | Verified in 1,243-job public `COUNT` suite + resource contexts + global upper proof | **PASS** |
| `projected-C1019` | $10 \le n \le 19$ | Parent substitution from $6 \le n \le 9$ theorem across closed subdomains | Verified in 1,243-job public `COUNT` suite + resource contexts + global upper proof | **PASS** |
| `current-C2024` | $20 \le n \le 24$ | Increasing weak induction with own caps $<0.419$, 186 resource meanings, 1,000 panels | `actual20-counts/bridge/RESULT.json` (`d522d7477749...`, 49/49 `actual20` `COUNT` jobs) + `actual20/scalar/RESULT.json` (5/5 contracts) + 114 public `COUNT` forests ($21..24$) | **PASS** |
| `current-C25` | $n = 25$ | Low-only $[1,6/5]$ cover (52 complete `COUNT` interfaces) + unrestricted high-$\rho$ branch | Verified in 1,243-job public `COUNT` suite + `resources` (`high2548`) + global upper proof | **PASS** |
| `current-C2639` | $26 \le n \le 39$ | Low-only weak induction, 300 `COUNT` forests, whole-7 partitions, 35 support predicates, positive-39 cap | Verified in 1,243-job public `COUNT` suite + `resources` + global upper proof | **PASS** |
| `current-C4042` | $40 \le n \le 42$ | Weighted floor-40 theorem (`CORE304` + `2/9/INITIAL2` acquisition conjunction) | Verified in 1,243-job public `COUNT` suite + `resources` (`indexed40`, `initial42`, `low4042`) + global upper proof | **PASS** |
| `current-C4348` | $43 \le n \le 48$ | Independent positive ceilings and finite least-failure exclusion (no sharp $n=42$ premise) | `finite-collectors/collect-all/RESULT.json` (`bed1a5933ce0...`, 183/183 native tasks + `collector43` & `collector44`) | **PASS** |
| `independent-tail49` | $n \ge 49$ | Coarse caps $C_j \le C_{\mathrm{E}}+0.7/j$ ($45 \le j \le 50$), strong cap $C_{46} < C_{\mathrm{E}}+0.54/46$, three-loss base at $49,48,47$, and least later failure $n \ge 50$ | `finite-tail/tail-full/RESULT.json` (`55b2be8e21f1...`, 55/55 native predicates: 14 top-level + 41 retained execution predicates) | **PASS** |

---

## 4. Verification Suite Inventory & Integrity Checks

1. **`N1` Exact Cubic-Dual Checker (`verification/n1/verify_n1.py`):**
   - Verified 150 closed rational cells covering $[-2,1]$ and 1,128 Bernstein positivity intervals, plus exact Sturm/tail bounds on $(-\infty,-2]$ and $[1,\infty)$, proving $C_1 \le 2/5 < C_{\mathrm{E}}$.
2. **Foundations Suite (`verification/foundations/run_stage.py`):**
   - `n2-scalars`, `n2-primary` (70/70 cells), `n2-independent` (70/70 cells): `all_passed: true`.
   - `n3-scalars`, `n3-identities` (111 cells, 444 orthants, 95,904 grid identities), `n3-full` (111/111 C++ cube checks): `all_passed: true`.
   - `root4-prepare` and `root4-two-pass`: complete two-pass Linux `seccomp`-sandboxed verification over all 260 parent geometry classes and 1,300 HIGH slots (`conditional_physical_target_closed: true`, `root_bound_exact: "4097/10000"`, `unresolved_geometry_indices: []`).
3. **Public `COUNT` Suite (`verification/count/verify_counts.py`):**
   - All **1,243 / 1,243** candidate `COUNT` forests reconstructed from their root boxes and verified leaf-by-leaf (`completed_jobs: 1243`, `passed_jobs: 1243`, `failed_jobs: 0`, `RESULTS.jsonl` SHA-256 `9eaa11eb6ab81b995f25110943f4a2d0e010f0f263013c9a7eed0ac24a3ee625`).
4. **`actual20` Suite (`verification/actual20-counts/` and `verification/actual20/replay.py`):**
   - All **49 / 49** `actual20` ($n=20$) `COUNT` forests verified (`completed_jobs: 49`, `passed_jobs: 49`, `failed_jobs: 0`), bridged to the 49-entry mathematical namespace (`bridge/RESULT.json` SHA-256 `d522d7477749c1cdabf7a240a6771e9c1c28a39b64b4279ffc056ac2ccca91b3`), and combined with the 5 portable scalar contracts (`actual20/scalar/RESULT.json`).
5. **Finite `43–48` Collectors (`verification/finite-collectors/replay.py`):**
   - All **183 / 183** native `finite43-48` parent tasks verified with `TASK-COMPLETED.json` receipts, and composed through the native `math_port._math43` (`collector43`) and `math_port._math44` (`collector44`) collectors (`collect-all/RESULT.json` SHA-256 `bed1a5933ce00931f313c207c0a567e98a9465ee2e6305a0801ecfa1c69a6a9e`).
6. **Unbounded Tail $n \ge 49$ (`verification/finite-tail/replay.py`):**
   - All **55 / 55** native `tail49` predicates verified (`14` top-level tasks + `41` retained execution predicates, `tail-full/RESULT.json` SHA-256 `55b2be8e21f14cad5d05555b10ccbf847e223f5205707f8eaaa91780394d9e13`).
7. **Analytical Bridge & Normalization Audit:**
   - Weak-predecessor sufficiency ($C_{n-1} \le C_{\mathrm{E}} \implies q_n(P, C_n) = 0$), weighted floor scaling ($n D_{\mathrm{actual}} \le N d$), and cross-half binomial normalization ($0 < a < 1/2$, $a < b < 1$, $a + b < 1$) are proved and audited in `manuscript/arxiv-v1/main.pdf` (~160 pages), `paper/main.pdf`, and `mathematics/INDEPENDENT-MATHEMATICAL-AUDIT.md`.
8. **Sanitization & Repository Hygiene Audit:**
   - All staged receipts in `verification-results/` have been scrubbed of local workstation paths, cloud account names, and private keys.
