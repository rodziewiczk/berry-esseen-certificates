# actual20 / 41-step source API

This package exposes the original native source API for **n = 20**, comprising
40 original operations and one explicit conditional scalar-parent operation.
The number 41 counts operations; it does not denote n = 41.

It includes a complete executable scalar replay, the fixed 41-step task list,
the original full-protocol entry point, and byte-exact source/input transports.
It is **not yet a complete adapter for the final actual20 continuation epoch**.
The two concrete integration gaps below remain open. Every result is scoped
to numerical replay and keeps `full_pass: false`.

## Quick genuine replay

Use Python 3.11 or later, without optimization, from this directory:

```text
python -I -B replay.py inspect --output NEW_INSPECTION_DIRECTORY
python -I -B replay.py scalar --output NEW_SCALAR_DIRECTORY --timeout 120
```

Each output directory must be new. `inspect` verifies all source/input archive
hashes, materializes the exact original runtime and lists all 41 recipes. It
does not execute numerical programs.

`scalar` really runs the complete original coupled scalar/control program on
the five original contracts B0:37, B0:42, B0:50, BN:37, BN:42. The original
`finite2024_coupled_parent.prepare` constructs its explicit, AST-checked
conditional transport. The original `validate` then checks the whole result,
all five derivations, all source edges and all controls: 144 actual-law cases,
48 rare-distant cases, 52 negative-f cases, one excluded collision domain and
five malformed domains. A zero subprocess exit alone is insufficient.

The mathematical/control source is unchanged. On Windows, `path_abi.py` gives
the standalone program the Linux slash/newline representation required by its
original source graph. This small filesystem representation adapter is explicit;
no historical command capture or environment identity is claimed. The program
has no child processes. The actual interpreter/platform is newly observed in
`RESULT.json`; no historical runtime profile, key or signature is needed.

Development smoke: the complete scalar command exited 0 and the original
whole-result validator accepted all five cases and all 250 controls. This is
one conditional scalar replay, not completion of the 41-step argument.

## Original full-protocol entry point

On Linux, the unchanged original stopped-action API can be invoked explicitly:

```text
python -I -B replay.py original-protocol --inputs INPUTS.json --output NEW_FULL_DIRECTORY
```

`INPUTS.json` has exactly two maps:

```json
{
  "parents": {
    "auxiliary": "/absolute/full-original-auxiliary-stage",
    "universal": "/absolute/full-original-universal-stage",
    "supported": "/absolute/full-original-supported-stage",
    "feedback": "/absolute/full-original-feedback-stage"
  },
  "counts": {
    "LITERAL_ORIGINAL_JOB_ID": "/absolute/full-original-count-stage"
  }
}
```

The COUNT map must contain all 49 exact n=20 job IDs from
`finite1039_count_catalog.json`. No result-only map is admitted. The caller
first invokes `finite2024_actual20_full.prepare`, which calls the four complete
Fourier/feedback validators and every complete COUNT validator. It then invokes
the original `stopped_prefix.advance` in the order fixed by `full.specs()`.
Every native process is followed by the original complete output/control/source
reader. `--stop-after N` permits a bounded prefix; the default is all 41.

These are potentially long computations. The original supervisor gives **each
operation** 82,800 seconds; this is not one total batch allowance. It uses the
original honest Linux process-group resource contract, not a new cgroup claim.
No full 41-step execution was launched while preparing this package.

### Exact remaining integration gaps

1. The fresh public COUNT runner emits its own numerical output format. The
   original full API instead requires each complete stage directory with
   `REQUEST.json`, `SOURCES.json`, `STAGE_OBSERVED.json`, `STAGE_COMPLETED.json`,
   original contract/forest/receipt, real launch/streams/checkpoints and the
   complete inventory. Likewise the four upstream Fourier/feedback parents
   require their complete original stage protocol. A new source-specific bridge
   must bind the real public executions to the original mathematical readers;
   fabricating these files from a PASS boolean is not implemented or allowed.
   The unchanged readers fail closed on incompatible public outputs.

2. The final completed actual20 campaign used explicit later source epochs:
   exact helper-copy corrections, closed metadata contexts and alias splitting,
   a prepared-pin correction and five exact `SOURCE_TRANSFORM.json` closures.
   This runner exposes the **original** `finite2024_actual20_full` API, rather
   than claiming those continuation adapters have been ported to a clean fresh
   run. Their nine exact active source/data files are supplied in
   `sources/current-source-epochs.zip` for the narrow remaining port. They are
   not applied automatically, and no old completed prefix is relabelled fresh.

Thus the original-protocol CLI is a strict real native entry point with a
complete fixed task list, not a claim that the final continuation epoch can
already be reproduced by this package. Source/reference availability, a scalar
success and a full final native reproduction are separate statements.

## Source/input bindings

- `sources/runtime.zip`: 38 unchanged Python files and 14 exact source/reference
  files, including the full mathematical regional reader and original complete
  native/output/control validators.
- `sources/original-source-cache.zip`: original sealed source cache, with 809
  original and 3,134 supplemental paths. Reconstruction verifies each complete
  content object and the original source manifests. Archived numerical objects
  are conditional reference inputs; copying them is not a new acquisition.
- `sources/INITIAL_CAPSULE.zip`: exact original 4,807-file initial capsule,
  SHA256 `eb38f833f8e5fc8db30083f049790507160a1c3570e232368f99ab1f3d1226d3`.
  It is supplied for source/input inspection and the remaining epoch port;
  it is not loaded as an accepted completed transaction.
- `sources/current-source-epochs.zip`: the nine active continuation correction
  source/data files described above, without cloud controllers or authority
  credentials.
- `TASKS.json`: all 41 fixed original recipes, literal cwd/argv, complete created
  outputs and checkpoint paths. The executable obtains the same list from the
  original `full.specs()` rather than trusting a success field in this catalog.

`SOURCE-MANIFEST.json` binds every source transport and runtime file; its whole
hash is pinned in `replay.py`. `PUBLICATION.json` lists the exact files to copy.
No keys, signatures, ROOT grants, historic runtime-profile grants, mathematical
source edits or new all-law theorem licenses are part of this adapter.
