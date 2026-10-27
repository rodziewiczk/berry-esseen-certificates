"""Resource-only source epoch for the eleven ordinary B5 jobs inside66.

This module performs only source/JSON/AST/closed-tree metadata operations.
It never imports an original numerical module or accepts a mathematical leaf.
The two mixed-parent capsules are deliberately outside this ordinary lane.
"""
from __future__ import annotations

import ast
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from . import n25_b5_reconstruction_sources as base

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT/"proof/n25_full_count_source_plan.json"
PLAN_SHA256 = "18eb3f6bf6b3afe7a40490ad81eaa7f2f5e0f43ca892487fb82da2840bdf03a8"
BASE_PLAN_SHA256 = "6163a6692afd34403f848100cc647cbbee846f3a51f312847393a7c40338cbc0"
SCHEMA = "N25_FULL66_ORDINARY_COUNT_RESOURCE_SOURCE_PLAN_V1"
SCOPE = "CONDITIONAL_B5_ORDINARY_COUNT_100000_NODE_RESOURCE_EPOCH"
EPOCH = "COUNT_RESOURCE_EPOCH.json"
NODE_LIMIT = 100000
DEPTH_LIMIT = 128
MIB = 1024**2
TARGET = "76824784444199314310731654405729617052063596250011448874609/187500000000000000000000000000000000000000000000000000000000"
need = base.need
encoded = base.encoded
sha = base.sha
parsed = base.parsed


def targets():
    need(base.PLAN_SHA256 == BASE_PLAN_SHA256, "Exact frozen thirteen-capsule source plan")
    return tuple(t for t, r in base.profiles().items() if r["kind"] != "mixed-parent-v14")


def _plan():
    raw = base._regular(PLAN, 8*MIB)
    need(sha(raw) == PLAN_SHA256, "Externally pinned full66 ordinary resource epoch")
    data = parsed(raw)
    need(data["schema"] == SCHEMA and data["base_source_plan_sha256"] == BASE_PLAN_SHA256
         and tuple(data["profiles"]) == targets()
         and data["original_mathematical_code_executed"] is False
         and all(data[k] is False for k in base.FALSE_FLAGS), "Exactly eleven source-only ordinary profiles")
    return data


def profile(target):
    need(type(target) is str and target in targets(), "One ordinary B5 target; mixed protocols are separate")
    return deepcopy(_plan()["profiles"][target])


def _protocol(raw):
    """Prove the one assignment change by AST; do not execute either source."""
    tree = ast.parse(raw)
    assignment = [n for n in tree.body if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == "LIMIT" for t in n.targets)]
    need(len(assignment) == 1 and isinstance(assignment[0].value, ast.Constant)
         and type(assignment[0].value.value) is int and assignment[0].value.value == 10000,
         "One original literal10000-node assignment")
    text = raw.decode("utf-8")
    need(text.count("LIMIT=10000") == 1, "One exact resource-only source edit")
    changed = text.replace("LIMIT=10000", "LIMIT=100000", 1).encode("utf-8")
    assignment[0].value.value = NODE_LIMIT
    need(ast.dump(tree) == ast.dump(ast.parse(changed)), "Every non-LIMIT AST node unchanged")
    return changed


def _derive(target, payload):
    spec = base.profile(target)
    need(spec["kind"] in ("ordinary-v14", "quarter-v12") and payload.keys() == spec["output_files"].keys(),
         "Complete original ordinary source capsule")
    need(base._file_rows(payload) == spec["output_files"], "Exact frozen source capsule before resource edit")
    original = payload["count_protocol.py"]
    result = dict(payload)
    result.pop("FROZEN_DESIGN.json")
    base._add(result, "ORIGINAL_RECONSTRUCTION_FROZEN_DESIGN.json", payload["FROZEN_DESIGN.json"])
    base._add(result, "ORIGINAL_RESOURCE_BASE_COUNT_PROTOCOL.py", original)
    result["count_protocol.py"] = _protocol(original)
    epoch = dict(schema="N25_FULL66_ORDINARY_COUNT_RESOURCE_EPOCH_V1", target=target,
        scope=SCOPE, source_plan_sha256=BASE_PLAN_SHA256,
        base_design_sha256=spec["design_sha256"], base_checker_sha256=sha(original),
        checker_sha256=sha(result["count_protocol.py"]), contract_sha256=spec["contract_sha256"],
        kernel_manifest_sha256=spec["kernel_manifest_sha256"],
        original_node_limit=10000, node_limit=NODE_LIMIT, maximum_depth=DEPTH_LIMIT,
        exact_source_edit="Only the top-level LIMIT assignment10000->100000; all other AST nodes unchanged.",
        original_profile_acceptance_claimed=False, original_mathematical_code_executed=False,
        source_preparer_implements_full66_execution=False, **base.FALSE_FLAGS)
    base._add(result, EPOCH, encoded(epoch))
    base._add(result, "FROZEN_DESIGN.json", encoded(dict(
        schema="N25_FULL66_COUNT_RESOURCE_SOURCE_DESIGN_V1", files={n: sha(b) for n,b in result.items()},
        source_scope=SCOPE, original_design_acceptance_claimed=False, **base.FALSE_FLAGS)))
    base._imports(result)
    return result


def prepare(target, source_capsule, destination):
    """Build one new ordinary source capsule; native/forest execution is absent."""
    profile(target)
    base.verify_capsule(target, source_capsule)
    original = base.profile(target)
    payload = {n: base._regular(Path(source_capsule)/n) for n in original["output_files"]}
    result = _derive(target, payload)
    spec = profile(target)
    need(base._file_rows(result) == spec["files"], "Exact externally pinned resource capsule outputs")
    destination = Path(destination).absolute()
    base._no_link_ancestors(destination)
    need(not destination.exists(), "New resource capsule only; no overwrite")
    destination.mkdir(parents=True, exist_ok=False)
    for name, raw in result.items():
        with (destination/name).open("xb") as stream:
            stream.write(raw)
    verify(target, destination)
    return spec


def verify(target, capsule, *, outputs=False):
    spec = profile(target)
    capsule = Path(capsule)
    base._no_link_ancestors(capsule)
    need(capsule.is_dir(), "Regular ordinary resource capsule")
    expected = set(spec["files"])
    allowed = {f"COUNT{spec['index']}_FOREST.json", f"COUNT{spec['index']}_ACCEPTED.json"} if outputs else set()
    actual = {p.name for p in capsule.iterdir()}
    need(expected <= actual <= expected|allowed, "Exact source closure plus named optional native outputs only")
    data = {}
    for name, row in spec["files"].items():
        raw = base._regular(capsule/base._flat(name))
        need(len(raw) == row["bytes"] and sha(raw) == row["sha256"], "Exact ordinary resource source: "+name)
        data[name] = raw
    for name in actual-expected:
        base._regular(capsule/name, 128*MIB)
    manifest = parsed(data["FROZEN_DESIGN.json"])
    need(manifest["files"] == {n: sha(b) for n,b in data.items() if n != "FROZEN_DESIGN.json"}
         and all(manifest[k] is False for k in base.FALSE_FLAGS), "Complete false-acceptance resource source manifest")
    need(_protocol(data["ORIGINAL_RESOURCE_BASE_COUNT_PROTOCOL.py"]) == data["count_protocol.py"],
         "Only one source resource limit changed")
    base._imports(data)
    return spec


def native_header(target, capsule):
    spec = verify(target, capsule, outputs=True)
    kernel = parsed(base._regular(Path(capsule)/"KERNEL_COPY_MANIFEST.json"))["files"]
    return dict(schema=spec["native_schema"], n=25, index=spec["index"], target=TARGET,
        contract_sha256=spec["contract_sha256"], kernel_sha256=kernel, checker_sha256=spec["checker_sha256"])


def geometry(target, capsule, packet, *, checkpoint=False):
    """Check full closed geometry only; saved arithmetic is explicitly untrusted."""
    spec = verify(target, capsule, outputs=True)
    header = native_header(target, capsule)
    cfg = parsed(base._regular(Path(capsule)/"contract.json"))["rows"][0]
    if checkpoint:
        need(type(packet) is dict and set(packet) == {"schema","binding","roots","arithmetic_accepted"}
             and packet["schema"] == "UNTRUSTED_COUNT_SEARCH_CHECKPOINT_V1"
             and packet["arithmetic_accepted"] is False and type(packet["binding"]) is dict,
             "Exact untrusted search checkpoint")
        need(packet["binding"].get("design_sha256") == spec["design_sha256"]
             and base._same(packet["binding"].get("native_header"),header), "Current source/native checkpoint identity")
    else:
        need(type(packet) is dict and set(packet) == set(header)|{"roots"}
             and all(base._same(packet[k],v) for k,v in header.items()), "Exact source-bound candidate header")
    roots = packet["roots"]
    need(type(roots) is list and len(roots) == 26, "All26 original count roots")
    box = [list(map(Fraction,cfg["p"])), [Fraction(0),Fraction(cfg["Lambda"])],
           [Fraction(0),Fraction(1)],[Fraction(-1,2),Fraction(1,2)],[Fraction(0),Fraction(cfg["d0"])]]
    nodes=leaves=pending=splits=maximum_depth=0
    maximum_score=Fraction(0)
    statuses={}
    for k, root in enumerate(roots):
        need(type(root) is dict and set(root)=={"k","tree"} and type(root["k"]) is int and root["k"]==k,
             "Ordered literal count roots")
        stack=[(root["tree"],box,0)]
        while stack:
            node,current,depth=stack.pop();nodes+=1;maximum_depth=max(maximum_depth,depth)
            need(nodes<=NODE_LIMIT and depth<=DEPTH_LIMIT and type(node) is dict,"Finite original closed tree")
            kind=node.get("kind")
            if kind=="pending":
                need(checkpoint and set(node)=={"kind"},"Only checkpoint pending nodes carry no success claim")
                pending+=1
            elif kind=="leaf":
                need(set(node)=={"kind","box","decision","result"}
                     and base._same(node["box"],[[str(x) for x in pair] for pair in current])
                     and type(node["decision"]) is str and type(node["result"]) is dict,
                     "Reconstructed original closed leaf, untrusted complete payload")
                leaves+=1;statuses[node["decision"]]=statuses.get(node["decision"],0)+1
                if node["decision"]=="PASS_TARGET":
                    need(type(node["result"].get("score_upper")) is str,"Untrusted saved score has exact rational text")
                    maximum_score=max(maximum_score,Fraction(node["result"]["score_upper"]))
            else:
                need(kind=="split" and set(node)=={"kind","axis","cut","left","right"}
                     and type(node["axis"]) is int and 0<=node["axis"]<5 and type(node["cut"]) is str,
                     "Both closed children and literal split coordinate")
                axis=node["axis"];cut=Fraction(node["cut"])
                need(current[axis][0]<cut<current[axis][1],"Strict interior rational cut")
                lo,hi=deepcopy(current),deepcopy(current);lo[axis][1]=hi[axis][0]=cut
                stack.extend(((node["left"],lo,depth+1),(node["right"],hi,depth+1)));splits+=1
    need(nodes==2*(leaves+pending)-26,"Complete binary forest identity")
    return dict(roots=26,nodes=nodes,leaves=leaves,pending=pending,splits=splits,
                maximum_depth=maximum_depth,closed_statuses=statuses,maximum_score=str(maximum_score),
                arithmetic_accepted=False)
