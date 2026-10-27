# Key-free native G2 / G3 / ROOT4 execution

This self-contained package runs the unchanged original numerical programs on new output directories. It consumes no private key, legacy HMAC, historical completion marker or old compiler-profile identity. Python 3.10+ is required. G2 and all replay-only Python stages use the standard library; NumPy/SciPy are not needed. G3 full requires `g++` and Boost headers on PATH (on Debian/Ubuntu: `build-essential libboost-dev`).

The source packs contain the entire original G2/G3 189-file source/witness inventory plus its manifest (70+111 rational coefficient witnesses), and the original 99-file ROOT4 source bundle. Every original source/witness byte is checked before execution and afterwards. Source and output validation are separate. The full output validators are copied from the original qualified workers, with only their small standard-library dependency adapter.

## CLI and task API

Use a **new** output directory for each call:

```sh
python -I -B foundations.py n2-scalars     --output RUN/n2-scalars
python -I -B foundations.py n2-primary     --output RUN/n2-primary
python -I -B foundations.py n2-independent --output RUN/n2-independent
python -I -B foundations.py n3-scalars     --output RUN/n3-scalars
python -I -B foundations.py n3-identities  --output RUN/n3-identities
python -I -B foundations.py n3-full        --output RUN/n3-full
```

`n2-primary` runs the original `tensor_certificate.py check` over **all70** cells; `n2-independent` runs the independent whole70 integer checker. `n3-full` runs the original `verify.py`, one new `g++ -O2 -std=c++17` compile and **all111** C++ cube checks plus scalar moment checks. The adapter records actual subprocess arguments, hashes and retains the fresh binary. It rejects incomplete/partial output, missing cells, mismatched dynamic sums, changed witnesses or source drift. These are new executions, not admission of old receipts.

`tasks.json` is the fixed task-entry API. A scheduler invokes the above command with the chosen task's `stage`, fresh `--output`, and optional `--timeout SECONDS` (default54000, maximum86400). Python callers can import `foundations.run(stage, output, timeout=...)`. Results, full native logs, fresh process trace and before/after observed runtime profiles are stored in the task directory. Failure or timeout exits nonzero and does not write a completed `RESULT.json`; the small-stage adapter terminates its task-owned process group on timeout.

For a quick **partial smoke test only**:

```sh
python -I -B foundations.py n2-cell --output RUN/n2-cell --timeout 90
```

This calls the unchanged original `verify_one` on the complete cell000, including tensor and moment positivity. It does not grant the whole70 result.

## ROOT4: actual guarded two-pass implementation

```sh
python -I -B foundations.py root4-prepare  --output RUN/root4-source-check
python -I -B foundations.py root4-two-pass --output RUN/root4 --timeout 54000
```

`root4-prepare` only derives and verifies the already reviewed Linux resource epoch and writes the exact original CLI arguments. It performs no ROOT4 numerical calculation. `root4-two-pass` requires actual Linux and calls the unchanged bundled `be_replay.root4.run`: fresh full `--produce`, then fresh full `--replay-existing`. It uses no archived ROOT4 candidate as an input. This can be expensive; it is run only when explicitly requested.

The Windows vendor source is retained unchanged. Its Windows memory query is unsuitable on Linux. The existing deterministic Linux port changes only that resource monitor and four transitive literal pins, checks all73 mathematical ASTs and125 pin edges, and binds epoch `63f409204df8b1a786ce049dfdd1868f6b7fb736fc4053729b228f7675ce3a90`. No new mathematical kernel is substituted. The bundled Linux native supervisor must establish its guard; unsupported capabilities fail closed. Original CPU43200-second, process256MiB and HIGH64MiB limits remain. Each pass has the explicit external wall limit.

The original whole-result validator reopens the actual captures and candidate, checks both source closures/guards, byte-preserving replay, identical complete summaries, all260 closed parents,1300 HIGH slots, empty unresolved list and exact bound at most4097/10000. **Completed UNKNOWN is rejected.** Successful execution proves the conditional physical-class numerical predicate; the analytical localization and G3 parents are still needed for an all-law C4 theorem.

## What was actually tested here

On Windows, real `n2-scalars` and one complete native n2 cell000 passed (210 tensor nodes,1 moment box). `root4-prepare` derived and verified the sealed73-source Linux epoch successfully. No full70/111/ROOT4 calculation was launched for this adapter development. Smoke records are under `demo-*` and are not publication inputs.

The observed interpreter/compiler profiles are generated locally and compared before/after. They are not legacy profile425 and are not a claim of hermetic toolchain provenance or a cryptographic runtime authority. The compiler and host still form the ordinary execution trust boundary. These packages provide real native execution entrypoints, not an overall theorem validator. Every result retains `all_law_theorem_verified=false` and `full_pass=false`. Public integration must actually run the requested full stages before reporting them complete.

Publish the files listed in `PUBLICATION.json`; omit `demo-*`. `root4-export.zip` is not needed for fresh ROOT4 production/replay, and no historical operational/private logs are copied into this package. Source bundles retain their original license files.
