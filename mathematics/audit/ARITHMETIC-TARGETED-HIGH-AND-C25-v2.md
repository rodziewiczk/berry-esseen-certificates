# Targeted follow-up: universal Fourier arithmetic and all four active low-C25 engines

27 October 2026. This follows `ARITHMETIC-CHECKER-AUDIT-v1.md`. It closes that report's specific open review of the four **new low-only C25** COUNT-engine versions, and adds a targeted review of the actual unrestricted high-rho 25--48 Fourier arithmetic. It does not remove the other explicit scope limitations of that report. No source, mathematical certificate, remote output, manuscript, or operational record was changed. There was no cloud use, authority-key read, certificate transfer, heavy COUNT replay, or Fourier-cover integration.

## Result

I found no concrete code-to-proof discrepancy in the Fourier kernels/jet integration reviewed here, or in the active C25 engine deltas and their whole caller/helper graph. The correct conclusion is a source-level soundness finding for these conditional numerical reductions, not a new assertion that a successful execution record proves its analytical hypotheses or that all public replication artifacts are available.

## Unrestricted 25--48 Fourier source scope

I read the actual source bodies under `work/universal2539-v1/source/` and the corresponding 40--48 package, rather than the initial-build-attempt trees. The mathematical arithmetic bodies are the common files under `work/cutoff20_20261016/fourier/`: `kernel.py`, `jet.py`, `integrate.py`, and `batch.py`. I read the complete ordinary proof texts for the real anchor, anchored imaginary bound, sine circle, convex kappa splice, common-H reduction, stable-difference jet, endpoint pieces, and Gaussian tail. The literal sample-size selector is 25--39 in one package and 40--48 in the other; the integral and derivative rules themselves are generic integer rules.

The `universal2539.py`/`universal4048.py` producer calls `cover_v1/protocol.py` and its actual top-level Fourier integrator. An old discovery runner retained under `coupled_v1/` is not the active numerical engine. Its missing former `batch.py` in the selected source tree therefore does not create a missing active import.

### Elementary interval arithmetic and jets

The interval kernel accepts literal `int`/`Fraction` values, rejects floats and booleans, and rounds all endpoints outward on its fixed rational grid. Signed multiplication/division, even powers crossing zero, monotone odd powers, and integer-root upper/lower directions are correct. The midpoint trig evaluation encloses the midpoint before evaluating the degree-64/65 Taylor polynomial, includes the degree-66/67 Lagrange error, and adds the input-radius Lipschitz error. Intersection with `[-1,1]` is justified by the analytic range of sine/cosine.

The exponential construction reduces its nonnegative argument by 16, uses adjacent degree-32/33 alternating bounds on `[0,7/16]`, then raises the nonnegative interval to the 16th power. Endpoint order reverses correctly for `exp(-x)`. The pi constant's fine declared bracket is certified by Machin's identity and rounded outward again when converted into the coarser interval grid.

The value/first/second derivative jet implements the product, reciprocal, positive square-root, integer-power, trig and exponential chain rules. A differentiated reciprocal must exclude zero and a differentiated root requires a strictly positive whole-cell radicand. These checks reject a bad branch; they do not manufacture a derivative bound. The `n=0,1` power cases are explicit.

### A fixed smooth branch is used on every cell

The integrator first forms whole-cell bounds, selects a branch, and passes the same branch specification to both its whole-cell and midpoint evaluations. No derivative of a selected minimum is taken.

For real-coordinate squares, the endpoints are `a` and `b=a+increment`, with `increment>=0`. If the whole-cell sign of `2a+increment` is established, `b^2-a^2=increment*(2a+increment)` selects a valid endpoint square. Otherwise interval separation may select a square. If neither comparison resolves, their whole-cell constant upper bound is used. This constant is a valid smooth majorant. The same construction applies to the low-frequency error disk.

Every candidate modulus branch independently bounds the same `|f|`: one, a positive profile root, a whole-domain-eligible curved root, or the coordinate disk. The curved branch is used only when the entire frequency cell has `4<=D*u<=2*pi`. Selection of the smallest enclosed upper value is safe because the resulting smooth branch is fixed before differentiation. If a derivative-domain condition fails, the code falls back to the complete original upper-Darboux formula with its larger imaginary coefficient. A failure of that original formula still rejects.

For the stable difference, the actual function is

`cos(u)-exp(-u^2/2) = u^4 P(u^2) + remainder`.

The retained coefficients have the correct signs. For derivatives of order `j=0,1,2`, the omitted absolute series is bounded by `2*(22)_j*u_upper^(22-j)/(2^11*11!)`; the ratio bound by one half holds from the first omitted term on `u<=1`. Multiplication by `c^j` converts to derivatives with respect to the integration variable. The code adds separate value/derivative error intervals; it never differentiates the artificial error endpoints. The square-selection sign uses the equivalent normalized expression `2u P(u^2)+(rho_upper-1)/6` with its separately bounded remainder. The low-piece gate `c*tau<pi*.3<1` supplies the series domain.

For each smooth majorant, the upper integral is the smaller of its full upper Darboux bound and its midpoint bound with `width^2*max(0,sup F'')/24`. The second-derivative term has the correct coefficient and includes the whole closed cell.

### The iid integer powers and all four smoothing terms

The Gaussian base is `g=exp(-u^2/2)` and the common marginal modulus is `M`. The recurrence `S_(n+1)=M*S_n+g^n`, starting at `S_1=1`, is exactly the finite geometric sum in `f^n-g^n`. It includes equal bases and zero bases without division. The code retains the smaller of the completed `error*S_n` and triangle `M^n+g^n` integral upper bounds. Every literal exponent is computed; there is no monotonicity-in-n substitution.

With the doubled Prawitz kernel, the code includes the low error integral, high modulus integral, low Gaussian correction, and infinite Gaussian tail. I independently checked the endpoint formulas:

* Near zero, `|K(t)|<=1+1/(pi*t)` and the ordinary cubic characteristic-function error plus the fourth-order Gaussian error give exactly the stated `lowhead` polynomial.
* The normal correction is `(1-t)*sqrt(1+d(pi*t)^2)` where `d(x)=1/x-cot(x)` is bounded by `x/[3(1-x^2/6)]`. Its omitted head is at most `epsilon+pi*epsilon^2/2`.
* Near one the doubled norm is at most `(1-t)*sqrt(1+d(pi*(1-t))^2)`, yielding `epsilon^2/2+pi*epsilon^3/3`.
* `E1(a)/(2*pi)<=exp(-a)/(2*pi*a)` with `a=n*c^2*tau^2/2`; the implemented expression `exp(-c^2*tau^2/2)^n/(pi*n*c^2*tau^2)` has exactly this normalization.

The final outward factor is `sqrt(n)/rho_lower`. The lower endpoint, not the upper endpoint, belongs in the denominator. Both probability-discrepancy signs are covered by the Prawitz inequality; support, contact, predecessors and constrained optimizers are not added as hidden hypotheses. Shevtsova (2012), Lemma 4.1, printed page 263 / PDF page 23, states `n>=1`, as checked directly by the parent auditor. Every active literal index 25--48 satisfies this condition. The earlier audit wording `n>1` was unnecessarily restrictive; it was not a defect in these applications.

### Common-H and kappa

For the same law, `h=E|X|`, `eta=E|X-X'|^3/2-rho`, and `zeta=2AB/r` have different meanings. The ordinary proofs give `eta<=h<=1`, `zeta>=h`, `rho+zeta>=2/h`, and `zeta>=beta(rho)`. Therefore `H=max(h,beta(rho))` satisfies `eta<=H<=1` and `zeta>=H`; it does not assert `h>=H`. In a closed H-cell `[hl,hu]` and rho-strip `[lo,hi]`, all three lower bounds in `max(hl,2/hu-hi,beta_lower(hi))` are valid for the same zeta. The fallback uses only `eta<=hu` and remains valid when it discards the stronger zeta bound.

The real anchor's domain is retained: `u<=pi` on the entire frequency interval. I checked its elementary proof by the weighted cubic remainder and the global minimum of `cos(v)+sin(u)*v^2/(2u)`. The anchored imaginary proof uses a valid Cauchy factorization with the same weight. The sine-circle mixture proof preserves zero atoms and finite integrability under the third absolute moment. None of these identities depends on a bounded support assumption.

I also independently checked the kappa ordinary proof: the degree-16 Taylor polynomial is a global cosine upper bound on the nonnegative half-line by sixteen integrations of `cos(x)-1<=0`. Its degree-13 quotient polynomial is positive on the complete 81-cell closed cover; the outer ray is immediate from `x>=625/124`. The convex-splice derivative jump is the **new** `258*sin(4)+119*(1-cos(4))>=0` comparison, not the former one-tenth comparison. The curved second derivative and its stated sign domains are correct. Jensen is applied to a nonnegative size-biased argument; convexity on the full even real-line extension is not asserted.

### New pure checks actually executed

I ran `kernel.validate` on the actual current kappa certificate SHA-256 `02dc46c334ec9c9cbf0e7bb4c982869c6e3e0649a915169d3542b8820b51aac7`, using source SHA-256 `16170505dece7571725e4e601f1546989d546ed64685616f9d13283c59702b0a`. It checked all 81 cells and 1134 positive Bernstein coefficients, with minimum `2479189/65585520000`, including the inverse Bernstein identities and splice arithmetic. I separately executed the unchanged exact Machin pi certification. These are small pure checks, not Fourier-cover executions or reinterpretations of an old `CHECKED.json`.

## All four active new low-only C25 engines

The exact whole source list is `work/CURRENT25-LOW52-COUNT-SOURCE-BINDINGS-v1.json`. All four engine bodies are local ordinary files in `work/qualified-replay-source/count25-source-cache/blobs/<SHA-256>`:

| Engine SHA-256 | Active jobs | Function differences from the current20--24 `512c...` body |
| --- | ---: | --- |
| `512c70ead43294a7f1d4e14922c9c3a55d3928c9555f4af1415cacf5ad6657bb` | 28 | baseline |
| `660a83656239d197346392a053f021a07a8b121453e34c4771a56c893a2b903d` | 16 | `incoming_per_count` lines 147--197 and `cell35` lines 230--369; the other 13 functions agree exactly by AST |
| `67cb474849d0a2e68f5e00f04212ff1356ecb592312a64a04fb9386b0ac9bd57` | 2 | `incoming_per_count` lines 141--179 only; the other 14 functions agree exactly by AST |
| `908c406f64298f5e8f111016a5cadac8c1597dd67b5c45e4cbf87f0be61d410b` | 6 | `incoming_per_count` lines 143--181 and `cell35` lines 214--345; the other 13 functions agree exactly by AST |

No functions are added or deleted in these deltas. I read the complete differences, not merely the AST function-name counts. A new static comparison of all 52 actual protocols found exactly one AST body each for `same`, `unique`, `rootbox`, `children`, `evaluate`, and `replay`. Thus all 52 have the same complete n25 topology induction, with 26 roots and the previously reviewed strict leaf target.

### Reachable helper graph and inert included files

The added active mathematical modules, each with one whole body across all selected C25 capsules using it, are:

| Module | SHA-256 |
| --- | --- |
| `sharp_mgf.py` | `c2491627a57bbb7fbee3be27138a7accb8ad4c30f9e3a299372eddf428dc5cb2` |
| `tangent_mgf.py` | `74caaf13691b59b12a9492d3cdcc32209bb74c76b41504f95f0851b02a94838b` |
| `cubic_mgf.py` | `d360be74b191529b2a7e76d03feb3db7c9e303fc5b05be4fb403eb342aa5168e` |
| `cubic_mgf_mixed.py` | `dc8f4d30e9f3473f65bec8f21ad86245ff9c8e5025f847f5ca0e62f6819e2595` |
| `common_cubic_bound.py` | `f62a02b6e081b377b584a100cf704ed0966589e1de80177b4a33002af665af1c` |
| `centered_tail.py` | `40eb7500f391bd1b04cbb8e84e1aed5317f88a4cf1f48f1bd2e9fd1b524d1d1e` |
| `shifted_centered_tail.py` | `771540cd476f79007b9ee0466f7ae030360efa84874e126082731e5932bc0e43` |
| `common_shifted.py` | `947ef9b4b43e265fc3250d2c43b69976f11ed7229387d9e0ab51673e683e35b6` |
| `general_quartic_sos.py` | `e8159858cafb60c2f469479367a73946688757ebb097be213fcf1ddb8a00ebec` |
| `general_quartic_sos_bounds.py` | `716eda950209111c78960e819e20d0e86b83cb51868a9eaa583b839dbe32c4b5` |

I read every body above and its callers. The two active rho wrappers are `1fe8fefd...` and `f1650ff9...`; both were read. The latter adds the already reviewed theta/mean/allocation/corner contractions and keeps the original joint-plane intercept. The scalar and Bernstein optimizations, probability-extrema primitive, generalized scope, rho/beta floors and common-cubic polytope bodies were already covered by the first audit and were matched to their active pins.

`general_quartic_v2.py` and `general_quartic_bounds_v2.py` are included in sixteen capsules but are not imported in the reachable active source graph. The installed late route calls the fixed SOS version. Similarly, old signed-moment wrapper variants may be retained as files without being imported. There is no active V14 local-contact preprocessing, fixed-peak or stop-loss engine in this **new low-only 52-job** route. Their presence in broader legacy inventories must not broaden this route's audit obligations or claim.

### Caller/eligibility checks

The `67cb...` change takes the minimum of three complete positive-MGF upper bounds: the original common-allocation envelope, the independent sharp marginal product, and the coupled tangent product. The sharp bound handles zero variance and a zero support ceiling before division; its positive exponential range is explicitly checked. The tangent has nonnegative slope, so the actual allocation-derived variance upper bounds can be inserted. Its entire allocation product is maximized, rather than independently choosing unrelated marginal allocations.

The `908c...` and `660a...` callers acquire the common cubic polygon **before** passing cubic lower bounds to the improved incoming evaluator. They keep the same physical rho range, supports, D cap, and moments. For incoming `-W_j`, the two cubic upper bounds are `-mu0_lower` and `-mu1_lower`; the source signs are correct. The independent mixed product is a minimum of valid marginal MGF bounds before multiplying their positive integer powers.

The common cubic and shifted routes keep a single common pair `(mu0,mu1)`. The affine MGF coefficient midpoint plus coefficient-error allowance is outward for either cubic sign. The `max(1,affine_upper)` clamp is convex and remains an upper bound because a centered MGF is at least one. Weighted AM--GM gives a convex polynomial numerator, with a fixed positive pivot. The denominator is a positive affine rho floor on each of the two closed polygon pieces, so the convex-numerator/affine-denominator vertex argument is valid. The outgoing quartic has affine cubic coefficients; taking its complete Bernstein-control maximum preserves convexity. A rate, shift or Cantelli alternative is fixed for each count before computing all vertices and phase controls.

The old incoming line is removed algebraically before adding the new one. The caller verifies the entire same-cell phase/variance/context and its frozen Gaussian slope. In particular, `base_intercept=intercept-left+lip*ul` and `base_drift=-gaussian` retain the original Gaussian lower envelope without double charging the old incoming bound.

The exponential-excess upper bounds have positive distance `j-k-u`, since `j>k` and `u<=1/2`. Their numerator is nonnegative. The affine phase slopes are valid upper bounds over the entire phase interval; the code compares complete line endpoints when retaining a proposed improved line. The reciprocal-excess factor has a complete upper chord, using positive endpoint denominator lower bounds. A rounded denominator lower bound is not differentiated. The general SOS calls retain the same entire context and the fixed `gamma=3/2`, with exact global normalizer 2.

All domain/denominator/rate violations raise a rejection. No helper failure is caught and recast as a favorable leaf. No new caller uses an optional gate failure as an emptiness proof. Moving the same necessary rho/polytope exclusions before the incoming evaluation does not strengthen their statements or assume that a relaxed vertex is a realizable law.

Accordingly, the first report's limitation concerning the four selected C25 engine variants is superseded by this targeted whole-delta/helper review. The numerical certificates were not replayed again here, and the separate analytical proof that the selected same owner satisfies each entire physical contract remains the parent auditor's obligation.

## Remaining boundary

These findings concern the precise source reductions described above. They do not extend automatically to every distinct COUNT engine at the other finite-index roles, every Fourier/Sperner/resource implementation elsewhere, or a full local read of certificates held only on the VMs. The complete public replication obligation remains open. A comprehensive final verdict must combine these bounded findings with the separately reviewed analytical hypotheses, actual qualified numerical completions and complete global dependency/coverage checks.
