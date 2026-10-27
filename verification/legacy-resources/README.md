This package executes the original selected **conditional numerical** resource
checkers. It does not issue an all-law or global theorem.

Publish these four files together: `legacy_resources.py`, `MANIFEST.json`,
`legacy-native-source-data.zip`, and this README. The build helper and smoke
outputs are not required. The archive contains unchanged source/data blobs,
fixed task plans and original reference inputs; no authority keys, database
ledgers or acceptance tokens are included.

```text
python -I -B legacy_resources.py list
python -I -B legacy_resources.py verify
python -I -B legacy_resources.py run --task shared.kappa62_625 --output NEW-SCALAR-RUN
python -I -B legacy_resources.py run --task 65.parent.n7.initial.B0 --output NEW-INITIAL-RUN
```

`verify` checks the complete source/data package, without running mathematics.
`run` and `replay` always create a new task and execute the complete original
native controller. Neither mode reuses a saved PASS. The scalar task is portable
to Windows/Linux; the remaining controllers require Linux and retain their
original process supervision and resource limits.

There are 31 selected C5 actions and 97 runnable C6--9/C10--19 resource tasks.
The manifest also declares one blocked historical C15--19 controls route, which
requires its later current COUNT-fixture port. Other unfinished coverage is
listed in `remaining`; source availability is not a completed numerical replay.

Tasks with `runtime_requires` need `--dependencies dependencies.json`, mapping
each exact dependency name to its original freshly computed `task` directory.
For example, a C15--19 core case requires `57H.high`. The original controllers
validate their concrete dependency inputs where applicable. Same-law analytic
acquisition and the final global join remain separate obligations.

C5 uses the already published original source archive, whose complete size and
SHA256 are declared in `C5_public_archive`. Supply its directory with `--archives`
or explicitly allow the original pinned downloader with `--fetch`:

```text
python -I -B legacy_resources.py run --task C5.initial.B0 --output NEW-C5-RUN --fetch
```

The old C5 full67/graph105/corner branches and final one-free discharge, additional
C10--19 parent/support/high-rho controllers, and the global binder are not
claimed complete by this adapter. Every emitted result keeps
`all_index_full_pass=false` and `global_theorem_accepted=false`.
