"""Whole-export admission and resumable constituent execution for full66.

The twenty-nine inputs are full sessions or the original nine direct exports, never
historical PASS metadata. Each reader is called again after ZIP relocation.
This module does not import an original mathematical kernel.
"""
from __future__ import annotations
import json
from pathlib import Path
from . import n25_full_join_sources as s, n25_full_join_inputs as inputs
from . import finite_join_session_import as transport
from .colab_batch import atomic_json, event


def specifications():
    rows = []
    for branch in ('b0', 'b1', 'b2'):
        rows.append(dict(key='counts:'+branch, kind='retained', branch=branch,
                         folder='n25-retained-'+branch+'/runs'))
    for branch in ('b3', 'b4', 'lower-b5', 'middle-b4', 'middle-b5', 'upper-high-beta3'):
        rows.append(dict(key='extra:'+branch, kind='extra', branch=branch,
                         folder='n25-retained-extra-'+branch+'/runs'))
    rows.append(dict(key='upper10', kind='upper', branch='upper-retained-graph',
                     folder='n25-upper10-upper-retained-graph/runs'))
    for branch in ('b0', 'b1', 'b2'):
        rows.append(dict(key='parent:'+branch, kind='b012', branch=branch,
                         folder='n25-parents-'+branch+'/runs'))
    for branch in ('b4', 'b5'):
        rows.append(dict(key='middle:'+branch, kind='middle', branch=branch,
                         folder='middle-n25-'+branch+'/runs'))
    rows += [dict(key='parent:b5', kind='b5', branch='b5', folder='n25-global-parents-b5/runs'),
             dict(key='high:beta3', kind='high-beta3', branch='beta3', folder='high-beta3-acquisition/runs'),
             dict(key='acquisitions40', kind='acquisitions40', folder='n25-acquisitions'),
             dict(key='recovered11', kind='recovered11', folder='n25-recovered-original/runs'),
             dict(key='predecessor58H', kind='predecessor58H', folder='finite2024-join')]
    s.need(len(rows) == 20 and len({r['key'] for r in rows}) == 20,
           'Exact twenty whole constituent sessions in addition to nine original exports')
    return rows


def admit(specification, root):
    kind = specification['kind']
    if kind in ('retained', 'extra', 'upper'):
        return inputs.retained(root, specification['branch'], kind=kind)
    if kind in ('b012', 'middle', 'b5', 'high-beta3'):
        return inputs.acquisition(root, kind, specification['branch'])
    if kind == 'acquisitions40':
        return inputs.acquisitions40(root)
    if kind == 'recovered11':
        return inputs.recovered11(root)
    if kind == 'predecessor58H':
        from .finite2024_join import validate_completed
        return validate_completed(root)
    raise ValueError('Unknown full66 constituent identity')


def portable(value, root):
    """Store actual frame paths relative to this export; preserve capture strings."""
    if isinstance(value, Path):
        resolved = s.tx.ordinary(value)
        relative = resolved.relative_to(Path(root).resolve()).as_posix()
        s.need(relative == '.' or all(p not in ('', '.', '..') for p in relative.split('/')),
               'Contained normalized admitted frame path')
        return {'relative_file': relative}
    if type(value) is dict:
        s.need(all(type(k) is str for k in value), 'Portable named full-input fields')
        return {k: portable(v, root) for k, v in value.items()}
    if type(value) in (list, tuple):
        return [portable(v, root) for v in value]
    s.need(value is None or type(value) in (str, int, bool, float), 'Portable admitted data')
    return value


def signature(value, root):
    # No numerical proof is inferred from this digest. It only binds the exact
    # output of the full reader that must be called again by readback().
    result = portable(value, root)
    json.dumps(result, allow_nan=False)
    return result


def reference(root, key, task, checked, export):
    task = s.tx.ordinary(task)
    return dict(key=key, root_relative=task.relative_to(Path(root).resolve()).as_posix(),
                admitted=signature(checked, task), export=export)


def restore_inputs(root, durable_root, *, progress=None):
    from . import n25_collect as seven
    root = s.tx.ordinary(root); durable_root = s.tx.ordinary(durable_root)
    log = progress or (lambda name, **fields: event(root, name, **fields))
    direct, missing_direct = seven.collect(durable_root, root / 'seven', progress=log)
    records = []
    for key in seven.JOBS:
        if key not in direct:
            continue
        row = direct[key]
        task = s.path(root / 'seven', row['task_relative'])
        checked = inputs.seven_direct(task, key)
        s.need(inputs.same(checked, row['report']), 'Same fully revalidated direct export')
        records.append(reference(root, 'seven:'+key, task, checked,
                                 dict(path=row['zip_path'], sha256=row['zip_sha256'])))
    missing = ['seven:'+r['job'] for r in missing_direct]
    for spec in specifications():
        hit = transport.restore_latest(
            s.path(durable_root, spec['folder']), root/'imports'/spec['key'].replace(':', '-'),
            validator=lambda path, spec=spec: signature(admit(spec, path), path), log=log)
        if hit is None:
            missing.append(spec['key'])
        else:
            task, checked, exported = hit
            # checked is already the portable output of the actual full reader.
            records.append(dict(key=spec['key'], root_relative=task.relative_to(root).as_posix(),
                                admitted=checked, export=exported))
    atomic_json(root/'FULL66_INPUTS.json', dict(
        schema='TWENTY_NINE_COMPLETE_FULL66_CONSTITUENT_EXPORTS_V1', required=29,
        records=records, missing=missing))
    return records, missing


def readback(root, records, *, require_complete=True):
    from . import n25_collect as seven
    specs = {r['key']: r for r in specifications()}
    expected = {'seven:'+key for key in seven.JOBS} | set(specs)
    s.need(type(records) is list and all(type(r) is dict for r in records), 'Full input records')
    keys = [r['key'] for r in records]
    s.need(len(set(keys)) == len(keys) and set(keys) <= expected, 'No duplicate or unexpected whole input')
    if require_complete:
        s.need(set(keys) == expected and len(keys) == 29, 'Every twenty-nine complete current input is present')
    admitted = {}
    for row in records:
        s.need(set(row) == {'key', 'root_relative', 'admitted', 'export'}, 'Exact full input reference')
        path = s.path(root, row['root_relative']); key = row['key']
        checked = inputs.seven_direct(path, key[6:]) if key.startswith('seven:') else admit(specs[key], path)
        s.need(inputs.same(signature(checked, path), row['admitted']),
               'Whole current input was independently reproduced after relocation: '+key)
        admitted[key] = dict(root=path, value=checked)
    return admitted


def execute_missing_components(missing, *, durable_root, work_root, archives,
                               backup_interval=60, progress=lambda *a, **k: None):
    """Independent components continue even if another component fails.

    Their own verified stage caches survive. A missing external prerequisite
    remains WAITING; a failed constituent is explicitly returned as a failure.
    """
    from . import n25_acquisitions, n25_upper_counts, n25_recovered_batch
    calls = {
        'acquisitions40': lambda: n25_acquisitions.run_colab(
            durable_root=durable_root, work_root=work_root, archives=archives,
            backup_interval=backup_interval),
        'upper10': lambda: n25_upper_counts.run_colab(
            'upper-retained-graph', durable_root=durable_root, work_root=work_root,
            backup_interval=backup_interval),
        'recovered11': lambda: n25_recovered_batch.run_colab(
            durable_root=durable_root, work_root=work_root, backup_interval=backup_interval),
    }
    results, failures = {}, {}
    spec_by_key = {r['key']: r for r in specifications()}
    for key in calls:
        if key not in missing:
            continue
        try:
            progress('full66_component_started', component=key, shared_batch_deadline=False)
            result = calls[key]()
            # A returned success flag is insufficient; re-open the complete work.
            checked = admit(spec_by_key[key], result['work'])
            results[key] = dict(work=str(result['work']), bundle=str(result['bundle']),
                                admitted=signature(checked, result['work']))
            progress('full66_component_completed', component=key)
        except Exception as error:
            failures[key] = type(error).__name__+': '+str(error)
            progress('full66_component_incomplete', component=key, error=failures[key])
    return results, failures
