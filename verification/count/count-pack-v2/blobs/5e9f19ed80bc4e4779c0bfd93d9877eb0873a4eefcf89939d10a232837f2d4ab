"""Untrusted fresh DFS for fourteen source-pinned flat COUNT interfaces.

No numerical candidate, receipt or historical split tree is read. All leaf
decisions come from the original exact evaluator. The unchanged full native
acceptor must independently reconstruct and replay the emitted forest.
"""
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def construct(index, here):
    here = Path(here).resolve()
    recipe = json.loads((here / "PRODUCER-RECIPE.json").read_bytes())
    require(type(index) is int and index in recipe["indices"], "One exact selected panel")
    require(recipe["historical_candidate_input"] is False, "Source-only fresh discovery")
    sources = recipe["original_source_files"]
    for name, pin in sources.items():
        require(sha256((here / name).read_bytes()).hexdigest() == pin, "Pinned original source")
    spec = importlib.util.spec_from_file_location("_strict154_native_checker", here / "accept_strict.py")
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    cfg = native.fixed(index) if recipe["fixed_provider"] == "fixed" else native.FIX
    evaluator = getattr(native, recipe["cell_function"])
    target = F(native.TARGET)
    require(target > 0, "Positive exact native target")
    dimensions = recipe["dimensions"]
    root = ((F(index, 100), F(index + 1, 100)), (F(0), F(cfg["Lambda"])),
            (F(0), F(1)), (-F(1, 2), F(1, 2)))
    if dimensions == 5:
        root += ((F(0), F(cfg["d0"])),)
    require(dimensions in (4, 5) and all(a < b for a, b in root), "Full exact closed root")
    widths = tuple(b - a for a, b in root)
    weights = tuple(F(x) for x in recipe["split_weights"])
    require(len(weights) == dimensions and all(x > 0 for x in weights), "Explicit positive search weights")
    start = time.monotonic()
    splits, leaves = [], []
    visited, maximum = 0, F(0)
    output = here / f"candidate_{index}.json"
    require(not output.exists(), "No previous candidate")
    for k in range(recipe["n"] + 1):
        stack = [((), root)]
        while stack:
            path, box = stack.pop()
            visited += 1
            require(visited <= recipe["max_nodes"] and len(path) <= recipe["depth_limit"]
                    and time.monotonic() - start <= recipe["wall_seconds"],
                    "BOUNDED_CONSTRUCTION_NOT_COMPLETE")
            args = dict(pl=box[0][0], pu=box[0][1], lo=box[1][0], hi=box[1][1],
                        al=box[2][0], ah=box[2][1], k=k, ul=box[3][0], uh=box[3][1])
            if dimensions == 5:
                args.update(a0l=box[4][0], a0h=box[4][1])
            if recipe["configuration_call_mode"] == "expanded_keyword_arguments":
                decision = evaluator(**cfg, **args)
            else:
                decision = evaluator(cfg, **args)
            require(type(decision) is dict, "Exact evaluator record")
            node = dict(k=k, path=list(path))
            if "score_upper" in decision and 0 <= F(decision["score_upper"]) < target:
                leaves.append(dict(node, status=recipe["pass_status"], score_upper=decision["score_upper"]))
                maximum = max(maximum, F(decision["score_upper"]))
            elif "score_upper" not in decision and decision.get("status") in recipe["empty_statuses"]:
                leaves.append(dict(node, status=decision["status"], score_upper=None))
            else:
                require(len(path) < recipe["depth_limit"], "BOUNDED_CONSTRUCTION_NOT_COMPLETE")
                # Source-family physical scales avoid over-refining the
                # small inward-gap coordinate. This changes search order only.
                scales = (F(1, 1000), F(3, 500), F(3, 20), F(1, 50), F(1))
                priority = [weights[i] * (box[i][1] - box[i][0]) / scales[i] for i in range(dimensions)]
                priority[2] *= max(box[1][1] / root[1][1], F(1, 10000))
                axis = max(range(dimensions), key=lambda i: priority[i])
                cut = sum(box[axis]) / 2
                require(box[axis][0] < cut < box[axis][1], "Proper exact midpoint")
                left, right = list(box), list(box)
                left[axis], right[axis] = (box[axis][0], cut), (cut, box[axis][1])
                splits.append(dict(node, axis=axis))
                # LIFO: visit left before right; preserve both closed children.
                stack.append((path + (1,), tuple(right)))
                stack.append((path + (0,), tuple(left)))
            if visited % 1000 == 0:
                print("FRESH_COUNT_SEARCH", index, k, visited, len(leaves), flush=True)
    packet = dict(schema=recipe["candidate_schema"], index=index,
                  root=[[str(x) for x in interval] for interval in root],
                  splits=splits, leaves=leaves, visited=visited,
                  maximum_score=str(maximum), target_lower=str(target),
                  status=recipe["candidate_status"])
    packet[recipe["contract_field"]] = native.CONTRACT_HASH
    # Original complete structural checker; numerical acceptance is separate.
    contexts = native.structure(packet, index)
    require(len(contexts) == len(leaves), "Whole original structural replay")
    for name, pin in sources.items():
        require(sha256((here / name).read_bytes()).hexdigest() == pin, "Original source unchanged")
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(packet, indent=2) + "\n")
    print("STORED_FRESH_COUNT_NOT_ACCEPTED", index, visited, len(leaves), str(maximum), flush=True)


if __name__ == "__main__":
    require(len(sys.argv) == 2 and sys.argv[1].isdigit(), "One literal panel argument")
    construct(int(sys.argv[1]), Path(__file__).resolve().parent)
