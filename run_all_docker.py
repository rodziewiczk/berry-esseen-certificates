#!/usr/bin/env python3
"""Single-command reproducible Docker verification entrypoint.

Automatically uses 100% of available CPU cores (os.cpu_count()).

Modes (controlled by environment variable VERIFY_MODE or --mode):
  - fast (default):
      1. Verifies all source/package SHA-256 manifests (resources, legacy-resources, actual20)
      2. Executes live exact checks in parallel across all CPU cores (N1 150-cell cubic dual,
         actual20 5-contract scalar & 250 controls, legacy-resources shared.kappa62_625,
         G2/G3 scalar & identity checks, plus fast resource packages indexed40, support35,
         acquisition2_recovery)
      3. Verifies all staged 13-role execution receipts via `be.py status` and `be.py verify`
         confirming `full_pass: "ESTABLISHED"` and `EXIT_CODE=0`.
  - resources-all:
      Runs `fast` plus all runnable packages in `verification/resources/TASKS.json` in parallel
      across all CPU cores inside the container.
  - full-recompute:
      Downloads all raw candidate archives (`tools/fetch_certificates.py --all`) and
      re-executes every suite from scratch inside the Linux container (`N1`, `G2`, `G3`,
      `ROOT4` two-pass, 1,243 public `COUNT`s, 49 `actual20` `COUNT`s + namespace bridge +
      5 scalars, 183 `finite43-48` tasks + 2 collectors, 55 `tail49` predicates, and
      `verification/resources` packages), then runs `be.py verify`.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable
CPU_COUNT = max(1, os.cpu_count() or 4)


def run_step(label: str, cmd: list[str], cwd: Path = ROOT) -> dict:
    print(f"\n{'=' * 72}\n[START] {label}\n[CMD]   {' '.join(cmd)}\n{'=' * 72}", flush=True)
    t0 = time.perf_counter()
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, check=False)
    elapsed = round(time.perf_counter() - t0, 3)
    out_tail = (proc.stdout or "").strip()[-800:]
    err_tail = (proc.stderr or "").strip()[-800:]
    print(f"[DONE]  {label} -> exit_code={proc.returncode} ({elapsed}s)", flush=True)
    if out_tail:
        print(out_tail, flush=True)
    if proc.returncode != 0:
        if err_tail:
            print(f"[STDERR]\n{err_tail}", file=sys.stderr, flush=True)
        raise RuntimeError(f"Step failed ({proc.returncode}): {label}")
    return {"label": label, "command": cmd, "exit_code": proc.returncode, "elapsed_seconds": elapsed}


def run_parallel_steps(step_specs: list[tuple[str, list[str]]], max_workers: int) -> list[dict]:
    print(f"\n>>> Launching {len(step_specs)} verification tasks in parallel across {max_workers} CPU workers...", flush=True)
    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        fut_map = {pool.submit(run_step, label, cmd): label for label, cmd in step_specs}
        for fut in as_completed(fut_map):
            results.append(fut.result())
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("fast", "resources-all", "full-recompute"),
        default=os.environ.get("VERIFY_MODE", "fast"),
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=int(os.environ.get("JOBS", str(CPU_COUNT))),
    )
    args = parser.parse_args()
    jobs = max(1, args.jobs)

    print(f"=== Berry-Esseen Reproducible Verifier | mode={args.mode} | cpu_cores={CPU_COUNT} | jobs={jobs} ===", flush=True)
    tmp_root = Path(tempfile.mkdtemp(prefix="be-docker-verify-"))
    steps: list[dict] = []
    t_start = time.perf_counter()

    try:
        # 1. Cryptographic source & package integrity checks + live exact checks in parallel
        parallel_batch: list[tuple[str, list[str]]] = [
            (
                "Verify public resource task archives (16 packages)",
                [PY, "-I", "-B", "verification/resources/generic_resource_batch.py", "verify"],
            ),
            (
                "Verify legacy resource source/data archive (128 tasks)",
                [PY, "-I", "-B", "verification/legacy-resources/legacy_resources.py", "verify"],
            ),
            (
                "Inspect and verify actual20 source/input capsules",
                [
                    PY, "-I", "-B", "verification/actual20/replay.py", "inspect",
                    "--output", str(tmp_root / "actual20-inspect"),
                ],
            ),
            (
                "Live exact verification: N1 (150 cubic-dual cells, 1,128 Bernstein intervals)",
                [
                    PY, "-I", "-B", "verification/n1/verify_n1.py",
                    "--candidate", "verification/count/witnesses/N1-dual.json",
                    "--source", "verification/count/capsules/N1-dual",
                    "--worker", "verification/count/capsule_worker.py",
                    "--output", str(tmp_root / "n1-live"),
                ],
            ),
            (
                "Live exact verification: actual20 5-contract scalar & 250 controls",
                [
                    PY, "-I", "-B", "verification/actual20/replay.py", "scalar",
                    "--output", str(tmp_root / "actual20-scalar"),
                    "--timeout", "180",
                ],
            ),
            (
                "Live exact verification: legacy-resources portable scalar (shared.kappa62_625)",
                [
                    PY, "-I", "-B", "verification/legacy-resources/legacy_resources.py", "run",
                    "--task", "shared.kappa62_625",
                    "--output", str(tmp_root / "legacy-scalar"),
                ],
            ),
            (
                "Live exact verification: foundation stage n2-scalars",
                [
                    PY, "-I", "-B", "verification/foundations/foundations.py",
                    "n2-scalars",
                    "--output", str(tmp_root / "foundation-n2-scalars"),
                    "--timeout", "600",
                ],
            ),
            (
                "Live exact verification: foundation stage n3-scalars",
                [
                    PY, "-I", "-B", "verification/foundations/foundations.py",
                    "n3-scalars",
                    "--output", str(tmp_root / "foundation-n3-scalars"),
                    "--timeout", "600",
                ],
            ),
            (
                "Live exact verification: foundation stage n3-identities (95,904 grid identities)",
                [
                    PY, "-I", "-B", "verification/foundations/foundations.py",
                    "n3-identities",
                    "--output", str(tmp_root / "foundation-n3-identities"),
                    "--timeout", "600",
                ],
            ),
            (
                "Live exact verification: resource package indexed40",
                [
                    PY, "-I", "-B", "verification/resources/generic_resource_batch.py", "run",
                    "--task-id", "indexed40",
                    "--output", str(tmp_root / "res-indexed40"),
                    "--seconds", "300",
                ],
            ),
            (
                "Live exact verification: resource package support35",
                [
                    PY, "-I", "-B", "verification/resources/generic_resource_batch.py", "run",
                    "--task-id", "support35",
                    "--output", str(tmp_root / "res-support35"),
                    "--seconds", "300",
                ],
            ),
            (
                "Live exact verification: resource package acquisition2_recovery",
                [
                    PY, "-I", "-B", "verification/resources/generic_resource_batch.py", "run",
                    "--task-id", "acquisition2_recovery",
                    "--output", str(tmp_root / "res-acquisition2"),
                    "--seconds", "300",
                ],
            ),
        ]

        steps.extend(run_parallel_steps(parallel_batch, max_workers=jobs))

        if args.mode in ("resources-all", "full-recompute"):
            extra_res = [
                "positive39",
                "support16",
                "support32_34",
                "low26_30_support",
                "companions9",
                "low31",
                "initial35_39",
                "resource35_39",
                "shared_high25_39",
                "shared_high40_48",
                "LOW152",
            ]
            res_specs = [
                (
                    f"Resource package {tid}",
                    [
                        PY, "-I", "-B", "verification/resources/generic_resource_batch.py", "run",
                        "--task-id", tid,
                        "--output", str(tmp_root / f"res-{tid}"),
                        "--seconds", "43200",
                        "--jobs", str(max(1, jobs // 2)),
                    ],
                )
                for tid in extra_res
            ]
            steps.extend(run_parallel_steps(res_specs, max_workers=max(1, jobs // 2)))

        if args.mode == "full-recompute":
            steps.append(
                run_step(
                    "Download all public release certificate archives",
                    [PY, "-I", "-B", "tools/fetch_certificates.py", "--all"],
                )
            )
            for stage in ("n2-primary", "n2-independent", "n3-full", "root4-prepare", "root4-two-pass"):
                steps.append(
                    run_step(
                        f"Recompute foundation stage {stage}",
                        [
                            PY, "-I", "-B", "verification/foundations/foundations.py",
                            stage,
                            "--output", str(tmp_root / f"recompute-{stage}"),
                            "--timeout", "43200",
                        ],
                    )
                )
            steps.append(
                run_step(
                    "Recompute all 1,243 public COUNT jobs",
                    [PY, "-I", "-B", "be.py", "verify", "--counts", "--jobs", str(jobs)],
                )
            )
            steps.append(
                run_step(
                    "Recompute all 49 actual20 COUNT jobs + mathematical namespace bridge",
                    [PY, "-I", "-B", "be.py", "verify", "--actual20-counts", "--jobs", str(jobs)],
                )
            )
            steps.append(
                run_step(
                    "Recompute all 183 finite43-48 tasks + collector43 & collector44",
                    [
                        PY, "-I", "-B", "be.py", "verify",
                        "--finite-collectors", "collect-all",
                        "--output", str(tmp_root / "recompute-collect-all"),
                        "--jobs", str(jobs),
                        "--timeout", "64800",
                    ],
                )
            )
            steps.append(
                run_step(
                    "Recompute all 55 tail49 predicates",
                    [
                        PY, "-I", "-B", "be.py", "verify",
                        "--finite-tail", "tail-full",
                        "--output", str(tmp_root / "recompute-tail-full"),
                        "--timeout", "64800",
                    ],
                )
            )

        # Final global status & full_pass verification
        steps.append(
            run_step(
                "Check global repository status (be.py status)",
                [PY, "-I", "-B", "be.py", "status"],
            )
        )
        steps.append(
            run_step(
                "Verify full_pass across all 13 roles (be.py verify)",
                [PY, "-I", "-B", "be.py", "verify"],
            )
        )

        total_elapsed = round(time.perf_counter() - t_start, 3)
        summary = {
            "mode": args.mode,
            "cpu_cores_detected": CPU_COUNT,
            "jobs_configured": jobs,
            "all_steps_passed": True,
            "step_count": len(steps),
            "total_elapsed_seconds": total_elapsed,
            "full_pass": "ESTABLISHED",
            "public_verification": "FULL_PASS_VERIFIED",
            "exit_code": 0,
        }
        print("\n" + "=" * 72)
        print("DOCKER REPRODUCIBLE VERIFICATION SUMMARY:")
        print(json.dumps(summary, indent=2))
        print("=" * 72, flush=True)
        return 0
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
