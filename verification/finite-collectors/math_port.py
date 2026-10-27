"""Current-epoch numerical composition using unchanged original math bodies.

Historical capture binding and retained-byte-integrity claims are replaced by
mandatory authenticated31-native/152-producer admission. The mathematical
probability, scalar, phase, dominance and mutation checks are extracted from
their exact pinned source ASTs without rewriting function bodies.

Typed shared12 and analytic licenses are deliberately not inferred from a
CONDITIONAL_RESOURCE_SEALED label. Public output remains pending those licenses.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from types import SimpleNamespace
import ast
import copy
import json
import finite61_batch as native

common = native.common
CAPSULE_PREFIX = "work/toward40_20261007/audit43/capsule/"
WORK_PREFIX = CAPSULE_PREFIX + "work/below49_20261006/"
COLLECT44 = WORK_PREFIX + "entry/cutoff44/check_cutoff44_composition.py"
SCALAR44 = WORK_PREFIX + "entry/cutoff44/check_scalar_probability44.py"
COLLECT43 = "work/toward40_20261007/audit43/accept_cutoff43_join.py"
COMMON43 = "work/toward40_20261007/audit43/fixed_common.py"
DATA = (
    "acquisition/initial42_candidate.json", "package_audit/left42_exact/acquisition42_proof.json",
    "acquisition/central42_acquisition_candidate.json", "acquisition/upper42_candidate.json",
    "package_audit/left42_confinement/pre_sperner42_exact.json", "package_audit/left42_confinement/post_sperner42_exact.json",
    "package_audit/left42_exact/pre_sperner42_exact.json", "package_audit/left42_confinement/confinement42_proof.json",
    "local/left42_final/actual_float_targets.json", "local/left42_final/central42_mid_witnesses.json",
    "local/central42_v2/new_central42_targets.json", "local/central42_v2/central42_mid_witnesses.json",
    "local/left42_tiny_final/targets.json", "package_audit/left42_confinement/profiles42_proof.json",
    "package_audit/left42_confinement/profile_targets.json",
)


def _source(name, cache):
    meta = native.manifest(cache)["files"][name]
    raw = common.regular(Path(cache) / "blobs" / meta["sha256"], native.MAX_INPUT)
    common.need(len(raw) == meta["bytes"] and common.sha(raw) == meta["sha256"], "collector_source_pin", "Exact immutable original source/data")
    return raw


def _compile(nodes, name, namespace):
    module = ast.Module(body=nodes, type_ignores=[])
    exec(compile(ast.fix_missing_locations(module), name, "exec"), namespace)


def _functions(tree, names):
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
    common.need({node.name for node in nodes} == set(names), "source_math_functions", "Only and all named original mathematical functions")
    return nodes


def _assignment(node):
    return [target.id for target in node.targets if isinstance(target, ast.Name)] if isinstance(node, ast.Assign) else []


def _jsonable(value):
    if type(value) is F: return str(value)
    if isinstance(value, (tuple, list)): return [_jsonable(item) for item in value]
    if isinstance(value, dict): return {key: _jsonable(item) for key, item in value.items()}
    return value


def _math44(root, jobs, cache):
    scalar = ast.parse(_source(SCALAR44, cache))
    collector = ast.parse(_source(COLLECT44, cache))
    work = root / "work/below49_20261006"
    ns = dict(F=F, Path=Path, sha256=sha256, copy=copy, json=json, ROOT=root, WORK=work,
              b=SimpleNamespace(digest=common.file_sha), jobs=jobs)
    _compile(_functions(scalar, {"need", "unique", "read", "scalars", "probability_cover", "controls"}), SCALAR44, ns)
    constants = [node for node in scalar.body if "PATHS" in _assignment(node)]
    constants += [node for node in collector.body if set(_assignment(node)) & {"BANDS", "LEFT_REGIONS", "CENTRAL_REGIONS"}]
    _compile(constants + _functions(collector, {"comparison_cover", "left_interfaces"}), COLLECT44, ns)
    main = next(node for node in collector.body if isinstance(node, ast.FunctionDef) and node.name == "main")
    start = next(index for index, node in enumerate(main.body) if "objects" in _assignment(node))
    stop = next(index for index, node in enumerate(main.body[start:], start)
                if "p" in _assignment(node) and isinstance(node.value, ast.BinOp) and ast.unparse(node.value).startswith("RUNS /"))
    # Exact unchanged source statements: probability cover; source joins;
    # both complete phase covers; actual LEFT profile interfaces;11 negative controls.
    _compile(main.body[start:stop], COLLECT44, ns)
    return _jsonable(dict(probability_cover=ns["cover"], comparison_covers=ns["covers"],
                          actual_left_profile_interface=ns["interface"], scalar_composition=ns["scalars"](),
                          mathematical_negative_controls=ns["rejected"]))


def _math43(root, outputs, cache):
    helper = ast.parse(_source(COMMON43, cache)); collector = ast.parse(_source(COLLECT43, cache))
    ns = dict(F=F, Path=Path, copy=copy, json=json, ROOT=root, BASE=root / "work/below49_20261006", outputs=outputs)
    _compile(_functions(helper, {"need", "unique", "load", "same", "rejects", "basic_controls"}), COMMON43, ns)
    _compile(_functions(collector, {"joins"}), COLLECT43, ns)
    ns["joins"](outputs)
    start = next(index for index, node in enumerate(collector.body) if "initial" in _assignment(node))
    stop = next(index for index, node in enumerate(collector.body[start:], start) if "controls" in _assignment(node))
    _compile(collector.body[start:stop], COLLECT43, ns)
    end = next(index for index, node in enumerate(collector.body[stop:], stop)
               if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
               and isinstance(node.value.func, ast.Name) and node.value.func.id == "print")
    _compile(collector.body[stop:end], COLLECT43, ns)
    cells = ns["cells"]
    return _jsonable(dict(probability_cells=len(cells), excluded_probability_cells=sum(row[2] == "excluded" for row in cells),
                          acquired_probability_cells=sum(row[2] == "acquired" for row in cells),
                          inherited_K42=ns["K"], forced_41a41=ns["forced41"], surplus=ns["forced41"] - F(12, 25),
                          mathematical_negative_controls=ns["controls"], cells=cells))


def required_typed_claims(cache):
    data = native.manifest(cache)
    analytic_name = WORK_PREFIX + "entry/cutoff44/ANALYTIC_INPUTS44.json"
    analytic = common.parsed(_source(analytic_name, cache))
    # The retained numerical MANIFEST is NOT an analytic theorem or fresh proof.
    analytic_tex = {name: pin for name, pin in analytic.items() if name.endswith(".tex")}
    common.need(len(analytic_tex) == 13, "analytic_boundary", "Thirteen exact analytic source documents, separate numerical evidence")
    return {
        "shared12.finite_base40_45": dict(kind="strict_scaled_excess_ceiling", actual_indices=list(range(40, 46)),
            bound="3/2", expression="n*(C_n-C_E)", no_tail_input=True,
            source_sha256="54977ac28ce649382ba1854ca230f677bf3157cacfb6bce10561f9f8021f1a2f"),
        "shared12.coarse45_48": dict(kind="strict_scaled_excess_ceiling", actual_indices=list(range(45, 49)),
            bound="7/10", expression="n*(C_n-C_E)", route=["fresh_anchor45", "fresh_propagation46", "corrected_phase_resource_route"]),
        "shared12.uniform_local47": dict(kind="typed_uniform_contact_exclusion", actual_n_min=47,
            interface="BEMap.UniformTail.UniformLocalProvider.reject", assumptions="BEMap.UniformTail.UniformLocalAssumptions",
            positive_noise_and_zero_noise_branches=True),
        "shared12.independent49plus": dict(kind="typed_all_index_tail", actual_n_min=49, actual_n_max=None,
            interface="BEMap.TailAssembly.TailMethodProviders.contracts", finite1_48_is_not_a_dependency=True),
        "accepted_analytic_contracts44": dict(kind="accepted_analytic_contracts", source_document_pins=analytic_tex,
            numerical_manifest_is_not_analytic_truth=True, numerical_manifest_source_pin=analytic["work/below50_push_20260930/release/MANIFEST.json"]),
    }


