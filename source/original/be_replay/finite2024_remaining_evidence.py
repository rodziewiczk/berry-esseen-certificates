"""Pure stopped-action readback primitives for the complete58H controller.

These primitives do not establish a complete58H result by themselves. In
particular a source cache, one successful original action or a historical
conditional result cannot acquire a same-law or all-law theorem.
"""
from __future__ import annotations

import math
from pathlib import Path

from . import finite2024_remaining_epoch as epoch
from . import finite2024_remaining_sources as src
from . import finite2024_remaining_native as native
from .finite1039_count_evidence import mapped, same, terminal

MAX_CPU_SECONDS = 82800
MAX_WALL_SECONDS = 82800
MEMORY_BYTES = 2048*src.MIB
DISK_BYTES = 512*src.MIB
LOG_BYTES = 16*src.MIB
FLAGS = ("native_arithmetic_accepted", "actual20_sharp_verified", "full_notebook58H_completed",
         "predecessor_acquisition_verified", "all_index_conclusion_verified")
TIMING_FIELDS = {"seconds", "initial_seconds", "elapsed_seconds", "timings_seconds"}


def finite(value):
    src.need(type(value) in (int, float) and math.isfinite(value) and value >= 0,
             "Typed finite nonnegative resource/time measurement")
    return value


def budget(cpu_seconds, wall_seconds):
    src.need(type(cpu_seconds) is int and 0 < cpu_seconds <= MAX_CPU_SECONDS,
             "Strict positive original-action CPU ceiling up to23hours")
    src.need(type(wall_seconds) in (int, float) and 0 < wall_seconds <= MAX_WALL_SECONDS
             and math.isfinite(wall_seconds), "Strict positive finite external wall ceiling up to23hours")
    return dict(cpu_seconds=cpu_seconds, wall_seconds=float(wall_seconds), memory_bytes=MEMORY_BYTES,
                disk_bytes=DISK_BYTES, log_bytes=LOG_BYTES, heartbeat_seconds=20, sample_seconds=.2)


def guard(policy):
    return dict(kind="UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP", proof_acceptance=False,
        external_wall_seconds=float(policy["wall_seconds"]), per_process_RLIMIT_AS_bytes=MEMORY_BYTES,
        per_process_RLIMIT_CPU_seconds=policy["cpu_seconds"], aggregate_kernel_memory_limit=False,
        aggregate_kernel_cpu_limit=False, sampled_group_RSS_limit_bytes=MEMORY_BYTES,
        sampled_group_CPU_limit_seconds=policy["cpu_seconds"], sampled_file_limit_bytes=DISK_BYTES,
        sampled_log_limit_bytes=LOG_BYTES, descendants_changing_session_are_contained=False,
        equivalent_to_Windows_Job_or_cgroup=False)


def file_map(directory):
    directory = src.ordinary(directory); out = {}
    for p in directory.rglob("*"):
        src.ordinary(p)
        if p.is_file():
            name = p.relative_to(directory).as_posix(); src.parts(name); out[name] = src.digest(p)
    return out


def validate_transport(task, action, observed, context):
    task = Path(task); capsule = task/"capsule"; directory = task/"executions"/action
    recipe = native.recipe(action); original_root = context["original_task_root"]
    policy = budget(context["budget"]["cpu_seconds"], context["budget"]["wall_seconds"])
    src.need(same(context["budget"], policy), "Exact declared action budget, without implicit defaults")
    src.need(same(src.read(directory/"supervisor-result.json"), observed)
             and observed.get("status") == "completed" and type(observed.get("returncode")) is int
             and observed["returncode"] == 0 and observed.get("reason") is None
             and observed.get("mode") == "untrusted_search" and observed.get("proof_accepted") is False
             and type(observed.get("sample_count")) is int and observed["sample_count"] > 0,
             "Actual completed stopped BASIC execution, never rcFalse or an interrupted result")
    for key in ("elapsed_seconds", "maximum_sampled_group_RSS_bytes", "maximum_sampled_group_CPU_seconds"):
        finite(observed[key])
    src.need(same(observed["guard_scope"], guard(policy)), "Exact honest BASIC process-group resource scope")
    launch = src.read(directory/"launch.json")
    expected_fields = {"argv", "cwd", "output_dir", "mode", "checkpoint_paths", *policy}
    src.need(set(launch) == expected_fields and same(launch["argv"], native.command(action, context["python_executable"]))
             and mapped(task, launch["cwd"], original_root) == capsule/recipe["cwd"]
             and mapped(task, launch["output_dir"], original_root) == directory
             and launch["mode"] == "untrusted_search"
             and all(type(launch[k]) is int and launch[k] == policy[k] for k in ("cpu_seconds", "memory_bytes", "disk_bytes", "log_bytes"))
             and type(launch["wall_seconds"]) in (int, float) and launch["wall_seconds"] == policy["wall_seconds"]
             and launch["heartbeat_seconds"] == 20 and launch["sample_seconds"] == .2,
             "Literal original command/cwd and every actual configured limit")
    paths = native.checkpoints(action)
    src.need(type(launch["checkpoint_paths"]) is list
             and [mapped(task, p, original_root) for p in launch["checkpoint_paths"]] == [capsule/p for p in paths],
             "All exact whole output and resource-row stopped-copy requests")
    streams = {}
    for kind in ("stdout", "stderr"):
        p = mapped(task, observed[kind+"_path"], original_root)
        src.ordinary(p)
        src.need(p == directory/(kind+".txt") and p.is_file() and p.stat().st_size <= LOG_BYTES
                 and src.digest(p) == observed[kind+"_sha256"], "Actual bounded whole capture: "+kind)
        streams[kind] = p
    src.need(streams["stderr"].stat().st_size == 0, "Original completed stderr is empty")
    checks = observed["checkpoints"]
    src.need(type(checks) is list and len(checks) == len(paths), "Complete whole stopped output census")
    cwd = capsule/recipe["cwd"]
    for packet, name in zip(checks, paths):
        current = src.ordinary(capsule/name); copied = src.ordinary(directory/"checkpoints"/current.relative_to(cwd))
        src.need(set(packet) == {"source_path", "exists", "trusted_certificate", "path", "bytes", "sha256"}
                 and packet["exists"] is True and packet["trusted_certificate"] is False
                 and mapped(task, packet["source_path"], original_root) == current
                 and mapped(task, packet["path"], original_root) == copied
                 and current.is_file() and copied.is_file() and type(packet["bytes"]) is int
                 and packet["bytes"] == current.stat().st_size == copied.stat().st_size
                 and packet["sha256"] == src.digest(current) == src.digest(copied),
                 "Whole source and actual cwd-relative stopped copy agree")
    before = context["input_files_sha256"]; epoch.hash_map(before)
    after = file_map(capsule); created = set(native.created_outputs(action))
    src.need(not (created & set(before)) and set(after) == set(before)|created
             and all(after[p] == pin for p, pin in before.items()),
             "No original input changed and no hidden code/output appeared during the original action")
    return streams["stdout"].read_text("utf-8")


def _timing_shape(value):
    if type(value) is list:
        return [_timing_shape(x) for x in value]
    finite(value)
    return "<RUNTIME_DURATION>"


def mathematical_view(value, *, references=None, original=False):
    """Retain all numeric/profile/control data; admit only named metadata fields.

    Complete actual source graphs and parent identities are checked separately.
    This normalization alone never validates a mathematical parent or a graph.
    """
    references = references or {}
    if type(value) is dict:
        out = {}
        for key, item in value.items():
            if key == "files_sha256":
                epoch.hash_map(item); out[key] = "<EXPLICIT_REFERENCE_GRAPH>"
            elif key in TIMING_FIELDS:
                out[key] = _timing_shape(item)
            elif key.endswith("sha256") and type(item) is str:
                src.need(epoch.HEX.fullmatch(item), "Exact output reference identity")
                out[key] = references.get(item, item) if original else item
            else:
                out[key] = mathematical_view(item, references=references, original=original)
        return out
    if type(value) is list:
        return [mathematical_view(x, references=references, original=original) for x in value]
    return value


def check_packet(cache, name, current, *, references):
    original = epoch.read(src.original_bytes(cache, name))
    expected = mathematical_view(original, references=references.substitutions(), original=True)
    actual = mathematical_view(current)
    src.need(same(actual, expected), "Every original non-reference mathematical field, row, flag and control remains exact")
    return dict(original_sha256=epoch.digest(src.original_bytes(cache, name)),
                original_mathematical_payload_preserved=True,
                current_metadata_identity_is_separate=True)


def check_current_graph(capsule, packet, references):
    """Read actual current bytes for every source edge; never discard a graph.

    Reference registration is a necessary transport condition. It is not an
    acquisition of the mathematical assertion in an archived object.
    """
    capsule = Path(capsule); graph = epoch.hash_map(packet["files_sha256"])
    src.need(set(graph) <= set(references.rows), "Every current graph edge has an explicit original/current role")
    for name, pin in graph.items():
        p = src.ordinary(capsule/name); row = references.rows[name]
        src.need(p.is_file() and src.digest(p) == pin == row["current_sha256"],
                 "Actual current source/parent bytes, not an embedded source graph alone")
        if row["role"] == "validated_fresh_parent":
            src.need(type(row["evidence_sha256"]) is str and epoch.HEX.fullmatch(row["evidence_sha256"]),
                     "Fresh mathematical parent has a distinct full evidence binding")
    return dict(files=len(graph), files_sha256=graph,
                source_graph_validated=True, mathematical_parent_acquired_by_this_helper=False)


def check_native_output(cache, capsule, action, stdout, references):
    """Full original result/terminal/control readback, without a theorem claim."""
    recipe = native.recipe(action); names = recipe["outputs"]
    rows = {}
    for name in names:
        path = src.ordinary(Path(capsule)/name)
        src.need(path.is_file(), "Every original requested output exists")
        if not name.endswith(".json"):
            continue
        packet = src.read(path)
        # Native metadata preparers copy sources and emit deliberately new
        # graph metadata. Their whole static profile still equals the original.
        if name in src.plan()["original_files"]:
            rows[name] = check_packet(cache, name, packet, references=references)
        if type(packet) is dict and "files_sha256" in packet:
            check_current_graph(capsule, packet, references)
    primary = src.read(Path(capsule)/names[0])
    if action in native.REPLAY_CONTROLS:
        field = "malformed_controls" if action.endswith("replay") else "negative_controls"
        controls = primary[field]
        original_controls = epoch.read(src.original_bytes(cache, names[0]))[field]
        if type(original_controls) is int:
            src.need(type(controls) is int and controls == original_controls == native.REPLAY_CONTROLS[action],
                     "Exact original integer replay-control census; bool is not a count")
        else:
            src.need(type(controls) is list and same(controls, original_controls)
                     and len(controls) == native.REPLAY_CONTROLS[action]
                     and len(set(controls)) == len(controls) and all(type(x) is str for x in controls),
                     "Every exact named original replay control")
    if action.endswith("replay"):
        src.need(primary["n"] == 20 and type(primary["n"]) is int and primary["K"] == "0"
                 and primary["full_signed_covers"] == 9 and type(primary["full_signed_covers"]) is int
                 and primary["signed_cells"] == 9*2592 and type(primary["signed_cells"]) is int
                 and primary["probability_panels"] == 100 and type(primary["probability_panels"]) is int
                 and primary["cutoff20_proved"] is False,
                 "Full original signed INITIAL replay census and conditional scope")
        src.need(same(terminal(stdout), {k:v for k,v in primary.items() if k != "files_sha256"}),
                 "Entire original replay terminal binds its actual whole receipt")
    elif action in ("coarse_prepare", "narrow_prepare", "feedback_prepare"):
        src.need(same(terminal(stdout), {k:v for k,v in primary.items() if k != "files_sha256"}),
                 "Whole original source-preparation terminal without an invented SHA marker")
    else:
        lines = [line for line in stdout.splitlines() if line.strip()]
        src.need(lines and src.digest(Path(capsule)/names[0]) in lines[-1],
                 "Original last terminal binds the actual first whole output")
    if action.endswith("resources_accept"):
        check_resource_rows(cache, capsule, recipe["cwd"])
    return dict(action=action, artifacts_sha256={name:src.digest(Path(capsule)/name) for name in native.created_outputs(action)},
                complete_original_output_readback=True, conditional_mathematical_statement_only=True,
                full_notebook58H_completed=False, all_index_conclusion_verified=False)


def check_resource_rows(cache, capsule, family):
    src.need(family in native.RESOURCES, "One selected complete100-row resource family")
    capsule = Path(capsule); candidate = src.read(capsule/family/"CANDIDATE.json")
    src.need(type(candidate["rows"]) is list and len(candidate["rows"]) == 100,
             "All original closed resource probability rows")
    records = []
    for i, row in enumerate(candidate["rows"]):
        name = family+f"/rows/{i:03d}.json"; p = src.ordinary(capsule/name)
        expected = src.plan()["original_files"][name]
        src.need(type(row["index"]) is int and row["index"] == i and row["path"] == f"rows/{i:03d}.json"
                 and p.is_file() and src.digest(p) == row["sha256"] == expected["sha256"],
                 "Whole fresh resource row equals the pinned mathematical reference, without a timing exception")
        records.append(dict(index=i, sha256=row["sha256"], status=row["status"]))
    return records
