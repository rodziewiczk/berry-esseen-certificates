"""Strict data-reference epochs for the grouped58H protocol.

This module is stdlib metadata infrastructure. It never loads a mathematical
program. A reference epoch is not an acquisition of a historical PASS object.
The caller must separately validate the genuine parent execution and its whole
mathematical payload before registering it as a fresh mathematical parent.
"""
from __future__ import annotations

import ast
from copy import deepcopy
from hashlib import sha256
import io
import json
from pathlib import PurePosixPath
import re
import tokenize

HEX = re.compile(r"[0-9a-f]{64}\Z")
REFERENCE_ASSIGNMENTS = {
    "PINS", "PIN", "HASHES", "RESULTS", "INITIAL_SHA", "GATE_SHA", "pinned",
    "SOURCE_GATE_SHA", "GATE_PIN", "PREPARED_SHA", "SOURCE_PREPARED_SHA", "FIXED", "fixed", "CAPTURES", "REPLAY_SHA", "SPECS", "PREMISE_HASH", "EXPECTED_CANDIDATE", "EXPECTED", "CANDIDATE", "ACCEPTED",
}
REFERENCE_ASSIGNMENT_PATTERN = re.compile(r"(?:[A-Z][A-Z0-9_]*_)?(?:SHA(?:256)?|HASH|PINS?)\Z")


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    need(type(data) is bytes, "Ordinary immutable bytes")
    return sha256(data).hexdigest()


def dump(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "Duplicate JSON key")
        result[key] = value
    return result


def read(data):
    need(type(data) is bytes, "Immutable original/current JSON bytes")
    def invalid(_):
        raise ValueError("Nonfinite JSON constant")
    return json.loads(data.decode("utf-8"), object_pairs_hook=unique, parse_constant=invalid)


def path_parts(name):
    need(type(name) is str and name and "\\" not in name and "\0" not in name,
         "Canonical relative reference path")
    p = PurePosixPath(name)
    need(not p.is_absolute() and p.as_posix() == name and all(
        bit not in ("", ".", "..") and ":" not in bit for bit in p.parts),
        "Contained canonical relative reference path")
    return p.parts


def hash_map(value):
    need(type(value) is dict and value, "Nonempty complete reference map")
    for name, pin in value.items():
        path_parts(name)
        need(type(pin) is str and HEX.fullmatch(pin), "Exact lowercase SHA256 reference")
    return value


class References:
    """An explicit old identity to actual current-byte reference registry.

    Equal historical byte identities may have several canonical aliases. They
    may not silently turn into different new identities. A caller needing that
    split must specify and review a path-specific epoch instead.
    """
    def __init__(self):
        self.rows = {}

    def add(self, name, original_sha256, current_bytes, *, role, evidence_sha256=None):
        path_parts(name)
        need(type(original_sha256) is str and HEX.fullmatch(original_sha256), "Original external reference pin")
        need(role in ("unchanged_source", "conditional_archived_input", "validated_fresh_parent", "derived_metadata"),
             "Explicit reference role")
        if role == "validated_fresh_parent":
            need(type(evidence_sha256) is str and HEX.fullmatch(evidence_sha256), "Fresh parent requires a real evidence binding")
        current = digest(current_bytes)
        if role in ("unchanged_source", "conditional_archived_input"):
            need(current == original_sha256, "An archived/source identity may not impersonate new bytes")
        row = dict(original_sha256=original_sha256, current_sha256=current, role=role,
                   evidence_sha256=evidence_sha256)
        need(name not in self.rows or self.rows[name] == row, "No conflicting canonical reference")
        need(all(prior["original_sha256"] != original_sha256 or prior["current_sha256"] == current
                 for prior in self.rows.values()), "Ambiguous historical identity: path-specific epoch required")
        self.rows[name] = row
        self.substitutions()
        return current

    def substitutions(self):
        result = {}
        for row in self.rows.values():
            old, new = row["original_sha256"], row["current_sha256"]
            need(old not in result or result[old] == new, "Ambiguous historical identity: path-specific epoch required")
            result[old] = new
        return {old: new for old, new in result.items() if old != new}

    def graph(self, original):
        hash_map(original)
        need(set(original) <= set(self.rows), "Every original graph edge is explicitly accounted for")
        result = {}
        for name, pin in original.items():
            row = self.rows[name]
            need(row["original_sha256"] == pin, "No replaced original source commitment")
            result[name] = row["current_sha256"]
        return result


def _reference_context(node, parents):
    """Admit literal SHA data, never an arbitrary string in a math expression."""
    cursor = node
    while cursor in parents:
        cursor = parents[cursor]
        if isinstance(cursor, ast.Call) and isinstance(cursor.func, ast.Name) and cursor.func.id in ("capture", "captured", "completed_capture", "bind", "closure", "freeze"):
            return True
        if isinstance(cursor, ast.keyword):
            if cursor.arg is not None and re.search(r"(?:sha(?:256)?|hash|pin)\Z", cursor.arg, re.I) is not None:
                return True
            # A dict(...) keyword may live inside an explicitly named PINS or
            # SPECS assignment. Its enclosing identity guard still decides.
        if isinstance(cursor, ast.Assign):
            targets = [t.id for t in cursor.targets if isinstance(t, ast.Name)]
            return bool(targets) and all(t in REFERENCE_ASSIGNMENTS or REFERENCE_ASSIGNMENT_PATTERN.fullmatch(t) for t in targets)
        if isinstance(cursor, ast.For) and isinstance(cursor.target, ast.Tuple):
            # The original feedback join spells two fixed capture identities
            # as ``for band, metadata in [(band, SHA), ...]``. Only that exact
            # literal metadata table is admitted, never its executable body.
            names=[t.id for t in cursor.target.elts if isinstance(t, ast.Name)]
            table=cursor.iter
            return (names==['band','metadata'] and isinstance(table,(ast.List,ast.Tuple))
                    and any(item is node for item in ast.walk(table)) and bool(table.elts)
                    and all(isinstance(row,ast.Tuple) and len(row.elts)==2
                            and isinstance(row.elts[0],ast.Constant) and type(row.elts[0].value)is str
                            and isinstance(row.elts[1],ast.Constant) and type(row.elts[1].value)is str
                            and HEX.fullmatch(row.elts[1].value) for row in table.elts))
        if isinstance(cursor, ast.Compare):
            calls = [x for x in ast.walk(cursor) if isinstance(x, ast.Call)]
            return any(isinstance(call.func, ast.Name) and call.func.id in ("sha", "digest") for call in calls)
        if isinstance(cursor, (ast.Return, ast.Expr, ast.BinOp)):
            return False
    return False


def rewrite_reference_literals(original, substitutions):
    """Replace only registered literal reference SHA values in Python source.

    No numerical constant, branch, function, import, guard, count or formula is
    dropped. The complete reverse-normalized AST must equal the original AST.
    The original bytes remain a separately sealed provenance artifact.
    """
    need(type(original) is bytes and type(substitutions) is dict, "Original source and exact reference map")
    for old, new in substitutions.items():
        need(type(old) is str and HEX.fullmatch(old) and type(new) is str and HEX.fullmatch(new) and old != new,
             "Only changed literal SHA256 identities")
    text = original.decode("utf-8")
    tree = ast.parse(text)
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    allowed = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and type(node.value) is str and node.value in substitutions:
            need(_reference_context(node, parents), "Reference replacement occurs outside a metadata identity guard")
            allowed[(node.lineno, node.col_offset)] = node.value
    tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
    lines = text.splitlines(keepends=True)
    starts = []
    position = 0
    for line in lines:
        starts.append(position)
        position += len(line)
    edits = []
    for token in tokens:
        if token.type != tokenize.STRING:
            continue
        try:
            value = ast.literal_eval(token.string)
        except (ValueError, SyntaxError):
            continue
        if type(value) is not str or value not in substitutions:
            continue
        need(token.start in allowed and allowed[token.start] == value, "One exact admitted SHA literal token")
        a, b = token.start, token.end
        begin, end = starts[a[0] - 1] + a[1], starts[b[0] - 1] + b[1]
        # SHA references use simple ASCII quoted literals. Retain their quote
        # convention and every byte outside the 64-character reference itself.
        need(token.string in (repr(value), '"' + value + '"'), "Simple original reference string")
        replacement = token.string[0] + substitutions[value] + token.string[-1]
        edits.append((begin, end, replacement, value, substitutions[value], a[0], a[1]))
    need(len(edits) == len(allowed), "All admitted reference positions rewritten exactly once")
    current = text
    for begin, end, replacement, *_ in reversed(edits):
        current = current[:begin] + replacement + current[end:]
    actual = ast.parse(current)
    expected = deepcopy(tree)
    for node in ast.walk(expected):
        if isinstance(node, ast.Constant) and (node.lineno, node.col_offset) in allowed:
            node.value = substitutions[node.value]
    need(ast.dump(actual, include_attributes=False) == ast.dump(expected, include_attributes=False),
         "Entire source semantics differ only at admitted reference literals")
    output = current.encode("utf-8")
    report = dict(schema="ACTUAL20_REFERENCE_SHA_SOURCE_EPOCH_V1", original_sha256=digest(original),
                  current_sha256=digest(output), literal_edits=[dict(line=e[5], column=e[6], old=e[3], new=e[4]) for e in edits],
                  mathematical_source_body_changed=False, historical_identity_impersonated=False,
                  original_mathematical_code_executed=False)
    return output, report


def derive_graph_packet(original, references, *, scalar_reference_fields=()):
    """Rebind only a declared graph and listed top-level reference identities.

    Status, all numerical rows, profiles, supports, caps, durations and every
    other payload byte value remain identical. This is not a new original
    mathematical acceptance or a fresh source-review execution.
    """
    need(isinstance(references, References), "Explicit actual reference registry")
    old = read(original)
    need(type(old) is dict and "files_sha256" in old, "Original complete graph packet")
    current = deepcopy(old)
    current["files_sha256"] = references.graph(old["files_sha256"])
    substitutions = references.substitutions()
    need(type(scalar_reference_fields) in (tuple, list) and len(set(scalar_reference_fields)) == len(scalar_reference_fields),
         "Exact declared scalar reference fields")
    for key in scalar_reference_fields:
        need(type(key) is str and key != "files_sha256" and key in old and type(old[key]) is str and HEX.fullmatch(old[key]),
             "Declared scalar field is a SHA identity, not a numerical parameter")
        current[key] = substitutions.get(old[key], old[key])
    preserved = {k: v for k, v in old.items() if k not in {"files_sha256", *scalar_reference_fields}}
    need(dump(preserved) == dump({k: v for k, v in current.items() if k not in {"files_sha256", *scalar_reference_fields}}),
         "Every non-reference payload field preserved")
    output = dump(current)
    report = dict(schema="ACTUAL20_GRAPH_PACKET_REFERENCE_EPOCH_V1", original_sha256=digest(original),
                  current_sha256=digest(output), original_graph=old["files_sha256"], current_graph=current["files_sha256"],
                  scalar_reference_fields=list(scalar_reference_fields), original_packet_nonreference_payload_preserved=True,
                  original_acceptance_replayed=False, mathematical_acquisition_verified=False,
                  historical_identity_impersonated=False)
    return output, report
