"""Native-stage recipes and explicit reference epochs for grouped58H.

Only the Colab controller may execute these original programs. All functions
here prepare/check bytes and metadata; they never import a numerical module.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import shutil

from . import finite2024_remaining_sources as src
from . import finite2024_remaining_epoch as epoch

B = "work/cutoff20_20261016/"
COARSE = B+"finite/sharp20_banded_initial_v1"
COARSE_AUDIT = B+"analytic/sharp20_initial_replay_v1"
NARROW = B+"root/narrow_initial_v1"
NARROW_AUDIT = B+"analytic/narrow_initial_replay_v1"
FEEDBACK = B+"finite/feedback20_initial_v1"
FEEDBACK_AUDIT = B+"analytic/feedback20_initial_replay_v1"
LEGACY = B+"finite/sharp20_resources_v1"
RESOURCES = (B+"finite/sharp20_b0_resources_all_v1", B+"finite/feedback20_b0_resources_v1",
             B+"fourier/feedback_bn_resources_v1")

# Each recipe is a complete original call, with all output paths declared before
# launch. The legacy five-row pair precedes feedback source preparation because
# the original source-gate graph consumes that explicit ancestor.
RECIPES = (
    ("coarse_b0_construct", COARSE, ("pilot.py", "B0"), ("B0_RESULT.json",)),
    ("coarse_b1_construct", COARSE, ("pilot.py", "B1"), ("B1_RESULT.json",)),
    ("coarse_prepare", COARSE_AUDIT, ("prepare.py",), ("PREPARED.json",)),
    ("coarse_b0_replay", COARSE_AUDIT, ("replay.py", "B0"), ("B0_REPLAY_CHECKED.json",)),
    ("coarse_b1_replay", COARSE_AUDIT, ("replay.py", "B1"), ("B1_REPLAY_CHECKED.json",)),
    ("legacy_construct", LEGACY, ("pilot.py", "construct"), ("CANDIDATE.json",)),
    ("legacy_accept", LEGACY, ("pilot.py", "accept"), ("ACCEPTED.json",)),
    ("narrow_native_prepare", NARROW, ("prepare.py",), ("PREPARED.json", "pilot.py", "COPIED_SOURCES.json", "SOURCE_PORT.diff")),
    ("narrow_construct", NARROW, ("pilot.py", "BN"), ("BN_RESULT.json",)),
    ("narrow_prepare", NARROW_AUDIT, ("prepare.py",), ("PREPARED.json",)),
    ("narrow_replay", NARROW_AUDIT, ("replay.py", "BN"), ("BN_REPLAY_CHECKED.json",)),
    ("feedback_native_prepare", FEEDBACK, ("prepare.py",), ("PREPARED.json", "pilot.py", "COPIED_SOURCES.json", "SOURCE_PORT.diff")),
    ("feedback_source_audit", FEEDBACK, ("audit_sources.py",), ("SOURCE_CHECKED.json",)),
    ("feedback_source_audit_v2", FEEDBACK, ("audit_sources_v2.py",), ("SOURCE_CHECKED_V2.json",)),
    ("feedback_b0_construct", FEEDBACK, ("pilot.py", "B0"), ("B0_RESULT.json",)),
    ("feedback_bn_construct", FEEDBACK, ("pilot.py", "BN"), ("BN_RESULT.json",)),
    ("feedback_prepare", FEEDBACK_AUDIT, ("prepare.py",), ("PREPARED.json",)),
    ("feedback_b0_replay", FEEDBACK_AUDIT, ("replay.py", "B0"), ("B0_REPLAY_CHECKED.json",)),
    ("feedback_bn_replay", FEEDBACK_AUDIT, ("replay.py", "BN"), ("BN_REPLAY_CHECKED.json",)),
    ("coarse_resources_construct", RESOURCES[0], ("batch.py", "construct"), ("CANDIDATE.json",)),
    ("coarse_resources_accept", RESOURCES[0], ("batch.py", "accept"), ("ACCEPTED.json",)),
    ("feedback_b0_resources_construct", RESOURCES[1], ("batch.py", "construct"), ("CANDIDATE.json",)),
    ("feedback_b0_resources_accept", RESOURCES[1], ("batch.py", "accept"), ("ACCEPTED.json",)),
    ("feedback_bn_resources_construct", RESOURCES[2], ("batch.py", "construct"), ("CANDIDATE.json",)),
    ("feedback_bn_resources_accept", RESOURCES[2], ("batch.py", "accept"), ("ACCEPTED.json",)),
)

CAPTURES = {
    "coarse_b0_construct": "runs/cutoff20_20261016/finite/sharp20_b0_initial01",
    "coarse_b1_construct": "runs/cutoff20_20261016/finite/sharp20_b1_initial01",
    "coarse_b0_replay": "runs/cutoff20_20261016/analytic/sharp20_initial_b0_replay01",
    "coarse_b1_replay": "runs/cutoff20_20261016/analytic/sharp20_initial_b1_replay01",
    "narrow_construct": "runs/cutoff20_20261016/root/narrow_initial_construct01",
    "narrow_replay": "runs/cutoff20_20261016/analytic/narrow_initial_replay01",
    "feedback_native_prepare": "runs/cutoff20_20261016/finite/feedback20_initial_prepare01",
    "feedback_source_audit_v2": "runs/cutoff20_20261016/finite/feedback20_source_audit02",
    "feedback_b0_construct": "runs/cutoff20_20261016/finite/feedback20_b0_initial01",
    "feedback_bn_construct": "runs/cutoff20_20261016/finite/feedback20_bn_initial01",
}

COPIED_MODULES = ("cantelli_high.py", "direct_gaussian_support.py", "finite_binomial_core.py",
                  "heat_support50.py", "high_grid.py", "high_window_common.py", "high_window_core.py",
                  "initial34_indexed.py", "integer_exphi.py", "kernel.py", "small_index_support.py")
REPLAY_CONTROLS = {"coarse_b0_replay": 14, "coarse_b1_replay": 14, "narrow_replay": 14,
                   "feedback_b0_replay": 18, "feedback_bn_replay": 18,
                   "legacy_accept": 10, "coarse_resources_accept": 16,
                   "feedback_b0_resources_accept": 16, "feedback_bn_resources_accept": 20}


def recipe(action):
    rows = [r for r in RECIPES if r[0] == action]
    src.need(len(rows) == 1, "One complete selected original action")
    action, cwd, arguments, outputs = rows[0]
    return dict(action=action, cwd=cwd, arguments=list(arguments),
                outputs=[cwd+"/"+name for name in outputs])


def command(action, python):
    r = recipe(action)
    src.need(type(python) is str and python, "Actual current interpreter")
    # Several original consumers require the exact plain-B tail. Do not add-S
    # to those original commands and subsequently claim a different invocation.
    return [python, "-B", *r["arguments"]]


def created_outputs(action):
    r = recipe(action); outputs = list(r["outputs"])
    if action in ("coarse_prepare", "narrow_prepare", "feedback_prepare"):
        outputs += [r["cwd"]+"/engine/"+name for name in COPIED_MODULES]
    if action in ("narrow_native_prepare", "feedback_native_prepare"):
        outputs += [r["cwd"]+"/"+name for name in COPIED_MODULES]
    if action in ("coarse_resources_construct", "feedback_b0_resources_construct", "feedback_bn_resources_construct"):
        outputs += [r["cwd"]+"/CONSTRUCT_TIMINGS.json"]
        outputs += [r["cwd"]+f"/rows/{i:03d}.json" for i in range(100)]
    return outputs


def checkpoints(action):
    r = recipe(action); outputs = created_outputs(action)
    if action in ("legacy_accept", "coarse_resources_accept", "feedback_b0_resources_accept", "feedback_bn_resources_accept"):
        outputs += [r["cwd"]+"/CANDIDATE.json"]
        if action != "legacy_accept":
            outputs += [r["cwd"]+f"/rows/{i:03d}.json" for i in range(100)]
    return outputs


def original_registry(cache, capsule, *, evidence_bindings=None, derived_metadata=()):
    """Account for every present original-name input using its actual bytes.

    Numerical parents can enter the registry only with an explicit checked
    evidence SHA supplied by the controller. Other changed bytes must be one
    of the explicitly declared metadata/source epochs.
    """
    capsule = Path(capsule); evidence_bindings = evidence_bindings or {}
    permitted = set(derived_metadata); refs = epoch.References()
    for name, row in src.plan()["original_files"].items():
        p = src.ordinary(capsule/name)
        if not p.is_file():
            continue
        actual = p.read_bytes()
        if epoch.digest(actual) == row["sha256"]:
            role = "unchanged_source" if name.endswith((".py", ".txt", ".md", ".diff")) else "conditional_archived_input"
            refs.add(name, row["sha256"], actual, role=role)
        elif name in evidence_bindings:
            refs.add(name, row["sha256"], actual, role="validated_fresh_parent", evidence_sha256=evidence_bindings[name])
        else:
            src.need(name in permitted, "Changed input requires its exact source/metadata epoch or fresh mathematical evidence: "+name)
            refs.add(name, row["sha256"], actual, role="derived_metadata")
    for name, row in src.plan()["historical_execution_edges_requiring_genuine_current_replacement"].items():
        p = src.ordinary(capsule/name)
        if p.is_file():
            src.need(name in evidence_bindings, "A missing historical execution edge needs genuine stopped current evidence")
            refs.add(name, row["pin"], p.read_bytes(), role="validated_fresh_parent", evidence_sha256=evidence_bindings[name])
    return refs


def write_program_epoch(cache, capsule, name, references):
    original = src.original_bytes(cache, name)
    current, report = epoch.rewrite_reference_literals(original, references.substitutions())
    target = src.ordinary(Path(capsule)/name)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        src.need(target.read_bytes() in (original, current), "Do not overwrite an unrelated or stale source epoch")
    target.write_bytes(current)
    return report


def write_graph_epoch(cache, capsule, name, references, *, scalar_reference_fields=()):
    original = src.original_bytes(cache, name)
    current, report = epoch.derive_graph_packet(original, references, scalar_reference_fields=scalar_reference_fields)
    target = src.ordinary(Path(capsule)/name)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        src.need(target.read_bytes() in (original, current), "Do not rewrite an unrelated prepared/source graph")
    target.write_bytes(current)
    return report


def capture_input_map(capsule, action):
    """Original-consumed flat input names plus a separately sealed full graph.

    This is only the flat compatibility field; the controller's capture bridge
    must bind the complete source/input inventory and actual outer launch.
    """
    r = recipe(action); directory = Path(capsule)/r["cwd"]
    if action == "feedback_native_prepare":
        return {"prepare.py": src.digest(directory/"prepare.py")}
    outputs = {Path(p).name for p in r["outputs"]}
    result = {p.name: src.digest(p) for p in sorted(directory.iterdir())
              if p.is_file() and p.name not in outputs and p.suffix in (".py", ".json", ".txt", ".diff", ".md")}
    src.need(r["arguments"][0] in result, "Actual original entry source in captured input graph")
    return result


def generated_code_identity(cache, capsule, name):
    """A native metadata preparer may copy original math code, never new code."""
    actual = src.ordinary(Path(capsule)/name)
    src.need(actual.is_file() and actual.read_bytes() == src.original_bytes(cache, name),
             "Original preparer generated the exact originally selected numerical source")
    return src.digest(actual)


def graft_capsule(parent_capsule, capsule, names):
    """Copy bound parent bytes unchanged; do not rewrite their capture paths."""
    parent_capsule, capsule = Path(parent_capsule), Path(capsule)
    mapping = {}
    for name in names:
        src.parts(name); parent = src.ordinary(parent_capsule/name)
        src.need(parent.is_file(), "Actual validated parent artifact exists")
        target = src.ordinary(capsule/name); target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            src.need(target.read_bytes() == parent.read_bytes(), "Consistent shared canonical parent bytes")
        else:
            shutil.copyfile(parent, target)
        mapping[name] = src.digest(target)
    return mapping
