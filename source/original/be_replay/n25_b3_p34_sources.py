"""One newly selected original B3p34 forest, outside the preserved 17-job batch.

The historical catalog excluded this available candidate because its regional
hard link was unresolved. Full66 has the separately pinned complete B3 selector
and checks the current resource implication itself. Source preparation is not
numerical acceptance and does not change the old extra-count selection.
"""
from __future__ import annotations

import ast
from copy import deepcopy
import json
from pathlib import Path
import shutil

from . import count_task as common, delivery_transport as tx
from . import retained_n25_extra_sources as original
from . import n25_full_join_sources as full

CATALOG = 'n25_retained_b34_catalog.json'
CATALOG_PIN = '38fdf0a66ea6dbdea196c146d2cf4955e75996db0a4f1e43a269756ad4201b7a'
SELECTOR = ('cutoff25_20261011/new_low/full_lower_local_rho_feedback_v1/'
            'SELECTION_B3_COMPLETE_V1.json')
SELECTOR_PIN = '59ff23e9326639e65e14448874cb3bf004173af06596bf03a8e5d2843494fc9c'
MEMBER = 'cutoff25_20261011/new_root/global_alpha_stoploss2_b3_p34_v12'
MANIFEST = 'SOURCES.json'
PREPARATION = 'SOURCE_PREPARATION.json'
EPOCH = 'FULL66_B3P34_SOURCE_EPOCH.json'
base = original.base
EXECUTION_CONTRACT = 'FULL66_B3P34_NEW_TRUSTED_NATIVE_REPLAY_NO_HISTORICAL_ACCEPTANCE'
CATALOG_SHA256 = original.sha(original.encoded(dict(
    catalog_sha256=CATALOG_PIN, selector_sha256=SELECTOR_PIN,
    full_source_plan_sha256=full.PLAN_SHA256, target='b3-p34')))


def job():
    raw = (common.ROOT / 'proof' / CATALOG).read_bytes()
    common.need(original.sha(raw) == CATALOG_PIN, 'Exact original B3/B4 catalog')
    catalog = json.loads(raw, object_pairs_hook=common.unique)
    rows = [r for r in catalog['jobs'] if r['target_id'] == 'b3-p34']
    common.need(len(rows) == 1, 'One original available B3p34 candidate')
    row = original._normalize(rows[0])
    common.need(row['capsule_member_prefix'].rstrip('/') == MEMBER
                and row['branch'] == 'b3' and row['index'] == 34
                and row['leaf_count'] == 3877 and row['node_count'] == 7728,
                'Exact complete original B3p34 census and native capsule')
    row['selection_evidence'] = dict(
        member=SELECTOR, sha256=SELECTOR_PIN, mode='global_count',
        selection_is_not_numerical_acceptance=True)
    # The obsolete design is not a mathematical input to the native loader.
    # Its old pin remains catalog provenance; the independently sealed current
    # source epoch never needs to pretend that historical design was accepted.
    row['source_file_rows'] = [item for item in row['source_file_rows']
                               if item['filename'] != 'FROZEN_DESIGN.json']
    row['historical_design_omitted_as_noninput_provenance'] = True
    return row


def jobs(branch):
    common.need(branch == 'b3', 'Only the fixed B3p34 branch')
    return [job()]


def _selected(row):
    common.need(original.encoded(row) == original.encoded(job()),
                'Exactly the new independently selected original B3p34 job')
    return row


def _selector(cache):
    raw = full.source(cache, SELECTOR).read_bytes()
    common.need(original.sha(raw) == SELECTOR_PIN, 'Exact complete B3 selector')
    return _selector_bytes(raw)


def _selector_bytes(raw):
    common.need(original.sha(raw) == SELECTOR_PIN, 'Independent full selector SHA')
    obj = json.loads(raw, object_pairs_hook=common.unique)
    choice = obj['panels']['34']
    common.need(choice['p_interval'] == ['17/50', '7/20']
                and choice['choice']['mode'] == 'global_count'
                and len(choice['choice']['counts']) == 1
                and choice['choice']['counts'][0]['capsule'] == 'work/' + MEMBER,
                'Literal whole p34 selection, not a regional PASS label')
    return choice


def _epoch(row, expected):
    return dict(schema='FULL66_B3P34_ORIGINAL_SOURCE_EPOCH_V1',
                catalog_sha256=CATALOG_SHA256, job_id=row['job_id'],
                files_sha256={n: r['sha256'] for n, r in sorted(expected.items())},
                selector_sha256=SELECTOR_PIN, execution_contract=EXECUTION_CONTRACT,
                historical_acceptance_used=False, mathematical_source_bytes_changed=False,
                old_extra17_selection_changed=False, fresh_arithmetic_replayed=False,
                historical_design_omitted_as_noninput_provenance=True)


def _capsule(row, capsule):
    _selected(row)
    capsule = tx.ordinary(capsule)
    expected, kernel = original._selection(
        row, original._regular(capsule / row['manifest_filename'], original.MAX_SOURCE))
    protocol = (capsule / 'count_protocol.py').read_bytes()
    common.need(b'FROZEN_DESIGN' not in protocol,
                'The unchanged native program does not consume omitted design provenance')
    wanted = set(expected) | {EPOCH}
    common.need(capsule.is_dir() and
                wanted <= {p.name for p in capsule.iterdir()} <=
                wanted | {row['acceptance_filename']}, 'Exact fixed B3p34 source capsule')
    records = []
    for name, item in sorted(expected.items()):
        p = tx.ordinary(capsule / name)
        raw = original._regular(p, original.MAX_FOREST if item['role'] == 'candidate'
                                else original.MAX_SOURCE)
        common.need(original.sha(raw) == item['sha256']
                    and (item['bytes'] is None or len(raw) == item['bytes']),
                    'Every original unchanged B3p34 source/candidate byte')
        records.append(dict(item, bytes=len(raw)))
    raw_epoch = original.encoded(_epoch(row, expected))
    common.need((capsule / EPOCH).read_bytes() == raw_epoch, 'Exact new B3p34 seal')
    records.append(dict(filename=EPOCH, member=None, bytes=len(raw_epoch),
                        sha256=original.sha(raw_epoch), role='new_source_epoch'))
    return records, kernel


def census(row, capsule):
    _, kernel = _capsule(row, capsule)
    tree = ast.parse((Path(capsule) / 'count_protocol.py').read_bytes())
    header = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'header')
    schema = next(k.value for k in header.body[0].value.keywords if k.arg == 'schema')
    return base._structure(dict(row, forest_schema=ast.literal_eval(schema)), capsule, kernel)


def _manifest(task):
    row = job()
    choice = _selector_bytes((Path(task) / 'B3_SELECTOR.json').read_bytes())
    capsules = tx.ordinary(Path(task) / 'capsules')
    common.need(capsules.is_dir() and {p.name for p in capsules.iterdir()} == {row['job_id']},
                'Only the dedicated B3p34 source job')
    records, _ = _capsule(row, Path(task) / row['capsule_relative'])
    census(row, Path(task) / row['capsule_relative'])
    return dict(schema='FULL66_B3P34_SOURCES_V1', branch='b3',
                catalog_sha256=CATALOG_SHA256, selector_sha256=SELECTOR_PIN,
                selected_choice=choice, execution_contract=EXECUTION_CONTRACT,
                historical_acceptance_used=False, old_extra17_selection_changed=False,
                jobs=[dict(job_id=row['job_id'], files=records)])


def prepare(cache, task):
    row = job()
    _selector(cache)
    task = tx.ordinary(task)
    common.need(not task.exists(), 'Exclusive dedicated B3p34 source task')
    manifest_raw = full.source(cache, MEMBER + '/' + row['manifest_filename']).read_bytes()
    expected, _ = original._selection(row, manifest_raw)
    capsule = task / row['capsule_relative']
    capsule.mkdir(parents=True)
    for name, item in sorted(expected.items()):
        raw = full.source(cache, item['member']).read_bytes()
        common.need(original.sha(raw) == item['sha256'], 'Independent archive and catalog agree')
        (capsule / name).write_bytes(raw)
    (capsule / EPOCH).write_bytes(original.encoded(_epoch(row, expected)))
    shutil.copyfile(full.source(cache, SELECTOR), task / 'B3_SELECTOR.json')
    manifest = _manifest(task)
    (task / MANIFEST).write_bytes(original.encoded(manifest))
    (task / PREPARATION).write_bytes(original.encoded(dict(
        schema='FULL66_B3P34_PREPARATION_V1', source_manifest_sha256=original.sha(
            original.encoded(manifest)), source_helper_sha256=common.digest(__file__),
        selected_jobs=1, selected_leaves=3877, source_plan_sha256=full.PLAN_SHA256,
        fresh_arithmetic_replayed=False, historical_acceptance_used=False)))
    return manifest


def verify(task):
    task = tx.ordinary(task)
    raw = (task / MANIFEST).read_bytes()
    manifest = _manifest(task)
    common.need(raw == original.encoded(manifest), 'Exact complete B3p34 source manifest')
    expected = dict(schema='FULL66_B3P34_PREPARATION_V1',
                    source_manifest_sha256=original.sha(raw),
                    source_helper_sha256=common.digest(__file__), selected_jobs=1,
                    selected_leaves=3877, source_plan_sha256=full.PLAN_SHA256,
                    fresh_arithmetic_replayed=False, historical_acceptance_used=False)
    common.need((task / PREPARATION).read_bytes() == original.encoded(expected),
                'Exact source-only dedicated preparation record')
    return manifest
