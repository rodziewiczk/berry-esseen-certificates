"""Original-byte admission for the complete grouped58H source assignment.

The source cache holds immutable originals and conditional reference templates.
It is never an accepted mathematical capsule. Runtime epochs and genuinely new
outputs have to be separately derived and validated before an action may run.
"""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import shutil
import time
import urllib.request
import zipfile

from . import finite1039_sources as base
from . import finite2024_remaining_epoch as epoch

ROOT, MIB = base.ROOT, base.MIB
need, ordinary, parts, digest = base.need, base.ordinary, base.parts, base.digest
PLAN = ROOT / "proof/finite2024_remaining_source_plan.json"
PLAN_SHA256 = "bf1550e3cf44c576f35bc869624d425eccc08834500099eda6de4d7759d0331b"
SCHEMA = "SEALED_GROUPED58H_ORIGINAL_REFERENCE_CACHE_V1"


def read(path, *, limit=64*MIB):
    path = ordinary(path)
    need(path.is_file() and path.stat().st_size <= limit, "Bounded ordinary metadata file")
    return epoch.read(path.read_bytes())


def dump(value):
    return epoch.dump(value)


def plan():
    need(digest(PLAN) == PLAN_SHA256, "Exact full grouped58H source specification")
    obj = read(PLAN)
    need(obj["schema"] == "GROUPED58H_CURRENT_SOURCE_PLAN_V1"
         and obj["complete_original_input_source_rows"] == len(obj["original_files"]) == 809
         and obj["original_files_bytes"] == sum(r["bytes"] for r in obj["original_files"].values()) == 46505929
         and len(obj["historical_execution_edges_requiring_genuine_current_replacement"]) == 42
         and [r["id"] for r in obj["components"]] == [
             "actual20.coarse_initial", "actual20.narrow_initial", "actual20.feedback_initial",
             "actual20.resources", "actual20.global_join", "actual21_24.induction_join"]
         and obj["original_math_sources_available"] is True
         and all(obj[k] is False for k in ("original_source_references_conflict", "runtime_ready", "arithmetic_computed",
                 "actual20_sharp_verified", "full_notebook58H_completed", "all_index_conclusion_verified")),
         "Full six-component assignment, with execution/semantic readiness honestly separate")
    for name, row in obj["original_files"].items():
        parts(name); parts(row["member"])
        need(row["archive_key"] in obj["assets"] and type(row["bytes"]) is int and 0 <= row["bytes"] <= 64*MIB,
             "Sealed original source/member identity")
    return obj


def obtain_assets(directory, *, progress=lambda *a, **k: None):
    directory = ordinary(directory); directory.mkdir(parents=True, exist_ok=True)
    out = {}
    for key, row in plan()["assets"].items():
        name = row["name"]; need(parts(name) == (name,), "Original archive basename")
        path = ordinary(directory/name)
        if not path.exists():
            pending = ordinary(path.with_suffix(".zip.pending")); size = 0; last = time.monotonic(); notified = 0
            progress("grouped58H_source_download_started", archive=name, total_bytes=row["bytes"])
            with urllib.request.urlopen(row["url"]) as source, pending.open("wb") as target:
                while block := source.read(MIB):
                    size += len(block); need(size <= row["bytes"], "Exact source archive download ceiling")
                    target.write(block)
                    if size-notified >= 16*MIB or time.monotonic()-last >= 5:
                        progress("grouped58H_source_download", archive=name, bytes=size, total_bytes=row["bytes"])
                        notified=size; last=time.monotonic()
            need(size == row["bytes"] and digest(pending) == row["sha256"], "Whole original source archive bytes")
            pending.replace(path)
        need(path.is_file() and path.stat().st_size == row["bytes"] and digest(path) == row["sha256"],
             "Pinned original archive, never a nearby revision")
        out[key] = path.resolve()
    return out


def _expected_files():
    return {name: row["sha256"] for name, row in plan()["original_files"].items()}


def _inventory(root):
    root = ordinary(root); found = {}
    for path in root.rglob("*"):
        ordinary(path)
        if path.is_file():
            name = path.relative_to(root).as_posix(); parts(name); found[name] = digest(path)
    return found


def verify_cache(cache):
    cache = ordinary(cache); expected = _expected_files(); packet = read(cache/"ORIGINALS.json")
    need(packet == dict(schema=SCHEMA, source_plan_sha256=PLAN_SHA256, files_sha256=expected,
                        original_mathematical_code_executed=False, numerical_acquisition_verified=False,
                        full_notebook58H_completed=False, all_index_conclusion_verified=False),
         "Exact source-only, nonaccepting original reference cache")
    found = _inventory(cache)
    need(set(found) == set(expected)|{"ORIGINALS.json"} and all(found[k] == pin for k, pin in expected.items()),
         "Complete809-file reference seal without extra helpers or outputs")
    allowed_dirs = {str(Path(name).parent).replace("\\", "/") for name in expected}
    allowed_dirs |= {"/".join(parts(name)[:i]) for name in expected for i in range(1, len(parts(name)))}
    allowed_dirs.discard(".")
    actual_dirs = {p.relative_to(cache).as_posix() for p in cache.rglob("*") if p.is_dir()}
    need(actual_dirs == allowed_dirs, "No unbound original-reference directory")
    return packet


def prepare_cache(assets, output, *, progress=lambda *a, **k: None):
    obj = plan(); output = ordinary(output)
    need(not output.exists() or output.is_dir(), "Ordinary source cache directory")
    output.mkdir(parents=True, exist_ok=True)
    opened = {}
    try:
        for key, row in obj["assets"].items():
            path = ordinary(assets[key])
            need(path.is_file() and path.stat().st_size == row["bytes"] and digest(path) == row["sha256"],
                 "Full source archive SHA/length before selected extraction")
            z = zipfile.ZipFile(path); base.zip_index(z); opened[key] = z
        for ordinal, (name, row) in enumerate(obj["original_files"].items()):
            target = ordinary(output.joinpath(*parts(name)))
            if not target.exists():
                z = opened[row["archive_key"]]; info = z.getinfo(row["member"])
                need(info.file_size == row["bytes"], "Selected original member length")
                target.parent.mkdir(parents=True, exist_ok=True)
                with z.open(info) as source, target.open("xb") as stream:
                    shutil.copyfileobj(source, stream, MIB)
            need(target.is_file() and target.stat().st_size == row["bytes"] and digest(target) == row["sha256"],
                 "Exact original source/candidate/provenance bytes")
            if ordinal % 20 == 0:
                progress("grouped58H_original_sources_checked", files=ordinal+1, total_files=809,
                         mathematical_code_executed=False)
        packet = dict(schema=SCHEMA, source_plan_sha256=PLAN_SHA256, files_sha256=_expected_files(),
                      original_mathematical_code_executed=False, numerical_acquisition_verified=False,
                      full_notebook58H_completed=False, all_index_conclusion_verified=False)
        marker = output/"ORIGINALS.json"
        if marker.exists():
            need(marker.read_bytes() == dump(packet), "Existing reference-cache marker unchanged")
        else:
            marker.write_bytes(dump(packet))
        verify_cache(output)
    finally:
        for z in opened.values():
            z.close()
    return output.resolve()


def original_bytes(cache, name):
    parts(name); row = plan()["original_files"].get(name)
    need(row is not None, "Only a declared sealed original source")
    path = ordinary(Path(cache)/name)
    need(path.is_file() and path.stat().st_size == row["bytes"] and digest(path) == row["sha256"],
         "Actual original source still equals its external pin")
    return path.read_bytes()


def clone_originals(cache, destination):
    """Copy references into an isolated provenance directory, never accepted."""
    verify_cache(cache); destination = ordinary(destination)
    need(not destination.exists(), "Exclusive new original-reference directory")
    destination.mkdir(parents=True)
    for name in _expected_files():
        target = destination.joinpath(*parts(name)); target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(original_bytes(cache, name))
    shutil.copyfile(Path(cache)/"ORIGINALS.json", destination/"ORIGINALS.json")
    verify_cache(destination)
    return destination.resolve()
