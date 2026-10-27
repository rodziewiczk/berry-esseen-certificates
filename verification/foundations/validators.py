# Whole output validators copied from the original qualified workers.
from pathlib import Path
from fractions import Fraction
from hashlib import sha256
import re
from types import SimpleNamespace
def need(ok,code,message):
    if not ok:raise ValueError(code+": "+message)
def file_sha(path):
    h=sha256()
    with Path(path).open("rb")as stream:
        while b:=stream.read(1048576):h.update(b)
    return h.hexdigest()
common=SimpleNamespace(need=need,file_sha=file_sha,MIB=1048576)
EPOCH_SHA="63f409204df8b1a786ce049dfdd1868f6b7fb736fc4053729b228f7675ce3a90"
def validate_output(stage, text, witnesses):
    lines = text.splitlines()
    common.need(not any(line.startswith(("REJECTED", "PARTIAL_INTEGER_CHECK_ONLY")) for line in lines),
                "small_rejection", "No rejected or partial source computation")
    if stage in ("n2-scalars", "n3-scalars"):
        marker = "SOURCE_SCALARS_COMPLETED " + stage
        common.need(lines == [marker], "small_scalars", "Actual original exact scalar function returned")
        return dict(scalar_function_completed=True)
    if stage == "n3-identities":
        marker = "ACCEPTED_ALL_INITIAL_IDENTITIES cells=111 orthants=444 exact_grid_identities=95904"
        common.need(lines.count(marker) == 1, "small_identity_count", "All111*4*216 exact identities")
        return dict(cells=111, orthants=444, exact_grid_identities=95904)
    patterns = {
        "n2-primary": (r"CHECKED (\d+) (\d+) (\d+)", r"ACCEPTED_ALL_70_TENSOR_CELLS (\d+) (\d+)", 70),
        "n2-independent": (r"INTEGER_CHECK (\d+): triangles=(\d+), leaves=(\d+), moment_boxes=(\d+)",
                           r"ACCEPTED_ALL_70_BY_INDEPENDENT_INTEGER_CHECK (\d+) (\d+) (\d+)", 70),
        "n3-full": (r"CELL (\d+) \[([^,]+),([^\]]+)\] nodes=(\d+) leaves=(\d+) depth=(\d+) moment_boxes=(\d+) sha256=([0-9a-f]{64})",
                    r"ACCEPTED_FULL_N3 (\d+) (\d+) (\d+) (\d+)", 111),
    }
    row_pattern, total_pattern, count = patterns[stage]
    rows = [match for line in lines if (match := re.fullmatch(row_pattern, line))]
    totals = [match for line in lines if (match := re.fullmatch(total_pattern, line))]
    common.need([int(row[1]) for row in rows] == list(range(count)) and len(totals) == 1,
                "small_complete_cells", "Every ordered cell and one complete final source result")
    if stage == "n2-primary":
        computed = [sum(int(row[2]) for row in rows), sum(int(row[3]) for row in rows)]
    elif stage == "n2-independent":
        computed = [sum(int(row[i]) for row in rows) for i in (2, 3, 4)]
    else:
        computed = [111] + [sum(int(row[i]) for row in rows) for i in (4, 5, 7)]
        previous = None
        for index, row in enumerate(rows):
            lo, hi = Fraction(row[2]), Fraction(row[3])
            common.need(lo < hi and (previous is None or lo == previous), "small_n3_seams", "Consecutive exact threshold cells")
            common.need(row[8] == witnesses[f"{index:03d}.json"]["sha256"], "small_n3_cell_hash", "Actual source witness bytes percell")
            previous = hi
        common.need(Fraction(rows[0][2]) == Fraction(-7, 2) and previous == Fraction(3, 2),
                    "small_n3_range", "Full closed threshold scope")
    common.need([int(value) for value in totals[0].groups()] == computed,
                "small_dynamic_census", "Actual new percell sums; no historical node marker required")
    return dict(cells=count, actual_totals=computed, ordered_cell_results=[row[0] for row in rows])

def validate_root4(module, output, result):
    common.need(result.get("schema") == "ROOT4_TWO_FRESH_FULL_PASSES_V1"
                and result.get("source_epoch_sha256") == EPOCH_SHA
                and result.get("all_required_stages_computed") is True
                and len(result.get("stages", [])) == 2,
                "root4_full_passes", "Both complete actual native passes, not a previous status label")
    capsule = Path(output) / "capsule"; module.verify_capsule(capsule)
    candidate = capsule / module.OUTPUT_NAME
    common.need(candidate.is_file() and not candidate.is_symlink()
                and candidate.stat().st_size <= 48 * common.MIB, "root4_actual_candidate", "Actual complete fresh ROOT4 artifact")
    candidate_pin = common.file_sha(candidate); checked = []
    for name, row in zip(("produce", "replay"), result["stages"]):
        common.need(row.get("stage") == name and row.get("completed") is True
                    and row.get("native_guard_verified") is True
                    and row.get("receipt_sha256") == candidate_pin,
                    "root4_stage_binding", "Actual fresh producer and byte-preserving replay")
        observation = row["observed"]
        common.need(module.guard_verified(observation, capsule), "root4_inner_guard", "Original guard still enforced, never replaced by a Boolean")
        terminal = module.terminal_packet(observation)
        common.need(terminal == row["terminal_result"], "root4_actual_capture", "Reopened actual observed native output")
        checked.append(module.validate_terminal(terminal, name, capsule))
    common.need(checked[0]["summary"] == checked[1]["summary"]
                and checked[0]["root_bound_exact"] == checked[1]["root_bound_exact"],
                "root4_replay_agreement", "All full mathematical outputs agree")
    closed = all(row["conditional_target_closed"] for row in checked)
    common.need(result.get("conditional_physical_root_verified") is closed
                and result.get("all_law_C4_verified") is False,
                "root4_conditional_scope", "Physical-class result only; analytic parents remain explicit")
    return dict(candidate_sha256=candidate_pin, candidate_bytes=candidate.stat().st_size,
                root_bound_exact=checked[1]["root_bound_exact"], conditional_physical_target_closed=closed,
                parents_per_pass=260, high_slots_per_pass=1300,
                unresolved_geometry_indices=checked[1]["unresolved_geometry_indices"])
