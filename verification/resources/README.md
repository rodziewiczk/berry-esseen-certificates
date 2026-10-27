# Public native resource replay release

This branch runs the **unchanged original numerical programs** in the fixed
source ZIPs. It requires no authority key, signature, historical execution receipt,
cloud service or private campaign token. Python3.12 is the preferred runtime;
the original programs retain their own stricter platform checks where applicable.

From this directory:

```
python -B generic_resource_batch.py list
python -B generic_resource_batch.py verify
python -B generic_resource_batch.py run --task-id indexed40 --output ./runs/indexed40 --seconds 120
python -B generic_resource_batch.py run --task-id initial35_39 --output ./runs/initial3539 --seconds 43200 --jobs 5
```

Each task extracts its complete pinned package to a new output directory and
invokes the original fixed `run --task --deadline [--jobs]` entry. Its original
acceptors, complete controls, numerical reports and stdout/stderr captures are
retained. The adapter additionally checks the complete archive/member pins,
successful process exit, exact complete result status/census, absence of retained
failures, and unchanged source bytes. An incomplete task exits unsuccessfully and
retains an `INCOMPLETE` observation. `verify` checks source bytes only; it runs no
mathematics. The source programs and witnesses are byte-identical; no formula,
gate or hypothesis is rewritten.

The manifest has16 task declarations over15 packages: INITIAL35--39,
resources35--39, positive39, support26--30/31/32--34/35, indexed40,
LOW152, companions9, two HIGH families, and acquisition variants.
The old acquisition archive is explicitly unsupported because it lacks two input
files. `acquisition2_recovery` performs only the two genuine interface calls;
`acquisition10_recovered` invokes the unchanged complete ten-action driver afresh
from the larger recovery source closure. The latter recipe is declared but has
not been replayed in this release. No old8 outputs become new10 outputs.

This is **one numerical branch**, not a completed public13-role proof runner.
G2/G3/ROOT4, actual41, older non-COUNT resource graphs and original finite43/tail
corpora still need their explicit public adapters/data. Unknown task IDs fail.
The separate COUNT worker remains necessary. The observation never issues
`full_proof_pass`, external execution authentication, analytic licenses, or a
global theorem. A publisher must combine genuinely completed numerical slices
with the complete analytic/parent/global DAG.

`build_manifest.py` is a local packaging helper using the existing inventory;
public users need only the two runner files, `TASKS.json` and `packages/`.
