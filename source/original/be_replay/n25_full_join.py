"""Full66: all remaining original n25 acquisitions and the current finite join.

Whole completed exports are revalidated and reused. Missing earlier inputs are
WAITING; a failed new action is INCOMPLETE. Neither is a completed theorem.
Original numerical programs run only in supervised Linux children.
"""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib, json, sys, traceback, uuid
from pathlib import Path
from . import n25_full_join_sources as source, n25_full_join_runtime as runtime
from . import n25_full_join_evidence as evidence
from . import n25_full_join_supplement as supplement, n25_b3_p34 as p34
from . import stopped_prefix as prefix, delivery_transport as transport, runtime_origin
from .colab_batch import atomic_json, event, utc

SCHEMA = 'FULL66_COMPLETE_CURRENT_N25_SESSION_V1'
COMPLETE = 'COMPLETE_CONDITIONAL_N25_FULL66'
FALSE = dict(full_n25_verified=False, all_index_conclusion_verified=False,
             global_proof_accepted=False, universal_analytic_inputs_acquired=False)


def key(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     allow_nan=False).encode()).hexdigest()


def task_at(root, record):
    source.need(type(record) is dict and set(record) == {'task_relative', 'validated'},
                'An exact full component reference')
    return source.path(root, record['task_relative'])


def component_record(root, task, checked):
    return dict(task_relative=Path(task).relative_to(root).as_posix(), validated=checked)


def compatible_supplement(task, parent_task):
    checked = prefix.validate(task, adapter=supplement.Adapter())
    old = supplement.parent.validate_completed(Path(task)/'parent', expected_branch='b3')
    current = supplement.parent.validate_completed(parent_task, expected_branch='b3')
    source.need(evidence.m.same(old, current), 'Same whole current B3 parent for a reusable complete action prefix')
    return checked


def execute_supplement(root, durable_root, cache, parent_task, *, work_root):
    parent_checked = supplement.parent.validate_completed(parent_task, expected_branch='b3')
    epoch = key(dict(implementation=supplement.implementation(), parent=parent_checked))
    directory = Path(durable_root)/'n25-full66/supplemental-b3-p30'/epoch
    log = lambda name, **fields: event(root, name, **fields)
    hit = transport.restore(directory, Path(root)/'supplement-imports',
                            validator=lambda task: compatible_supplement(task, parent_task), log=log)
    if hit:
        task, checked, _ = hit
        if checked['all_original_actions_completed'] is True:
            return task, supplement.validate_completed(task)
        task, _ = prefix.resume_origin(task, adapter=supplement.Adapter(), work_root=work_root)
        context = prefix.read(task/'PREFIX.json')['context']
        source.need(context['python_executable'] == sys.executable and context['python_version'] == sys.version,
                    'A partial prefix resumes only in its original recorded interpreter profile')
        runtime_origin.ensure_recorded_runtime(context, active_root=source.ROOT)
    else:
        task = Path(root)/'supplemental-b3-p30'
        supplement.prepare(cache, task, parent_task=parent_task)
    while len(prefix.read(task/'PREFIX.json')['actions']) < 2:
        prefix.advance(task, adapter=supplement.Adapter(), root=root)
        saved = transport.save(task, directory, validator=lambda path: compatible_supplement(path, parent_task),
                               label='full-original-b3-p30-prefix')
        event(root, 'full66_supplement_prefix_saved', **saved)
    return task, supplement.validate_completed(task)


def validate_completed(root):
    root = source.tx.ordinary(root)
    status = source.read(root/'SESSION_RESULT.json')
    source.need(status['schema'] == SCHEMA and status['state'] == COMPLETE
                and status['full_notebook66_completed'] is True
                and status['conditional_n25_chain_completed'] is True
                and all(status[k] is False for k in FALSE), 'Whole conditional full66 completion, with explicit universal-premise scope')
    p34_task = task_at(root, status['p34']); supplement_task = task_at(root, status['supplement'])
    mixed_task = task_at(root, status['mixed'])
    source.need(evidence.m.same(p34.validate_completed(p34_task), status['p34']['validated']), 'Entire original B3p34 acceptance readback')
    source.need(evidence.m.same(supplement.validate_completed(supplement_task), status['supplement']['validated']),
                'Both original full supplemental constructions/acceptances read back')
    from . import n25_mixed_runner as mixed
    source.need(evidence.m.same(mixed.validate_completed(mixed_task), status['mixed']['validated']),
                'Every complete original mixed action and fresh D92 primitive read back')
    checked = evidence.conjunction(root, status['imports'], p34_task=p34_task,
                                   supplement_task=supplement_task, mixed_task=mixed_task)
    source.need(evidence.m.same(checked, status['finite_summary']), 'Entire1900-panel/20-piece current conjunction independently reproduced')
    return dict(session_result_sha256=source.digest(root/'SESSION_RESULT.json'),
                conditional_n25_chain_completed=True, summary=checked, **FALSE)


def run_colab(*, durable_root, work_root='/content/berry-esseen-runs',
              archives='/content/berry-esseen-archives', backup_interval=60):
    source.need(sys.platform.startswith('linux'), 'Original supervised mathematical execution requires the Linux runtime')
    from . import n25_mixed_runner as mixed
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    root = source.tx.ordinary(Path(work_root)/'n25-full66'/stamp); root.mkdir(parents=True, exist_ok=False)
    durable = Path(durable_root)/'n25-full66/runs'/stamp
    status = dict(schema=SCHEMA, state='INCOMPLETE', full_notebook66_completed=False,
                  conditional_n25_chain_completed=False, imports=[], missing=[], failures={},
                  shared_batch_deadline=False, **FALSE)
    log = lambda name, **fields: event(root, name, **fields)
    backups = transport.Backups(root, durable, backup_interval); backups.start()
    try:
        status['imports'], status['missing'] = runtime.restore_inputs(root, durable_root, progress=log)
        atomic_json(root/'SESSION_RESULT.json', status)
        completed, failures = runtime.execute_missing_components(
            status['missing'], durable_root=durable_root, work_root=work_root,
            archives=archives, backup_interval=backup_interval, progress=log)
        status['new_constituents'] = completed; status['failures'].update(failures)
        if completed:
            # Re-import each complete exported transaction using its original
            # bounded transport and actual full reader, including synchronization.
            status['imports'], status['missing'] = runtime.restore_inputs(root, durable_root, progress=log)
        admitted = runtime.readback(root, status['imports'], require_complete=False)
        assets = source.obtain(archives, progress=root)
        cache = source.prepare_cache(assets, Path(work_root)/'n25-full66-source-cache', progress=log)
        try:
            task, checked = p34.ensure(cache, root/'original-b3-p34',
                completed_cache=Path(durable_root)/'n25-full66/b3-p34-completed'/p34.sources.CATALOG_SHA256[:24], log_root=root)
            status['p34'] = component_record(root, task, checked)
            atomic_json(root/'SESSION_RESULT.json', status)
        except Exception as error:
            status['failures']['original-b3-p34'] = type(error).__name__+': '+str(error)
            log('full66_component_incomplete', component='original-b3-p34', error=status['failures']['original-b3-p34'])
        if 'seven:n25-parents-b3' in admitted:
            try:
                task, checked = execute_supplement(root, durable_root, cache,
                    admitted['seven:n25-parents-b3']['root'], work_root=work_root)
                status['supplement'] = component_record(root, task, checked)
                atomic_json(root/'SESSION_RESULT.json', status)
            except Exception as error:
                status['failures']['supplement'] = type(error).__name__+': '+str(error)
                log('full66_component_incomplete', component='supplement', error=status['failures']['supplement'])
        if 'parent:b5' in admitted:
            try:
                result = mixed.run_component(cache, root/'original-b5-mixed', durable_root=durable_root,
                    work_root=work_root, parent_task=admitted['parent:b5']['value']['task'], log_root=root)
                status['mixed'] = component_record(root, result['task'], result['validated'])
                atomic_json(root/'SESSION_RESULT.json', status)
            except Exception as error:
                status['failures']['mixed'] = type(error).__name__+': '+str(error)
                log('full66_component_incomplete', component='mixed', error=status['failures']['mixed'])
        if status['failures']:
            status['state'] = 'INCOMPLETE'
        elif status['missing']:
            status['state'] = 'WAITING_FOR_COMPLETE_CURRENT_INPUTS'
        else:
            source.need(all(k in status for k in ('p34','supplement','mixed')), 'Every full new constituent has actual complete evidence')
            status['finite_summary'] = evidence.conjunction(root, status['imports'],
                p34_task=task_at(root,status['p34']), supplement_task=task_at(root,status['supplement']),
                mixed_task=task_at(root,status['mixed']))
            status.update(state=COMPLETE, full_notebook66_completed=True, conditional_n25_chain_completed=True)
            atomic_json(root/'SESSION_RESULT.json', status)
            validate_completed(root)
    except BaseException as error:
        status.update(state='INCOMPLETE', full_notebook66_completed=False,
                      conditional_n25_chain_completed=False, error=type(error).__name__+': '+str(error))
        (root/'ERROR.txt').write_text(traceback.format_exc(), encoding='utf-8')
        log('full66_incomplete', error=status['error'])
    finally:
        try:
            backups.close()
        except Exception as error:
            status.update(state='INCOMPLETE', full_notebook66_completed=False,
                          conditional_n25_chain_completed=False, synchronization_error=str(error))
        status['finished_utc'] = utc(); atomic_json(root/'SESSION_RESULT.json', status)
        result = transport.final_bundle(root, durable, Path(work_root)/'n25-full66-local'/stamp, status)
    return dict(status=status, bundle=str(result), work=str(root))
