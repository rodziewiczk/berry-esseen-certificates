"""Full original B3p34 native acceptance inside full66, with complete-stage reuse.

This is not a new notebook. The existing 17-job extra-B3 batch is untouched.
The original trusted-native policy is retained: 12 hours CPU, 12h5m wall, 2GiB.
No original mathematical program executes when importing or validating this module.
"""
from pathlib import Path
from types import FunctionType

from . import count_task as common, retained_n25_extra as template
from . import n25_b3_p34_sources as sources, n25_b3_p34_evidence as evidence
from . import delivery_transport as tx
from .colab_batch import atomic_json

RESULT = 'B3P34_RESULT.json'


def bound_namespace():
    namespace = dict(vars(template))
    namespace.update(sources=sources, evidence=evidence, __file__=__file__)
    # Rebind a complete connected set so restore/save call the same private
    # pure validator; nothing in either original module is monkeypatched.
    for name in ('_ordinary', 'accept', '_cache_members', 'restore_stage', 'save_stage'):
        value = vars(template)[name]
        function = FunctionType(value.__code__, namespace, value.__name__,
                                value.__defaults__, value.__closure__)
        function.__kwdefaults__ = value.__kwdefaults__
        namespace[name] = function
    return namespace


_BOUND = bound_namespace()
accept = _BOUND['accept']
restore_stage = _BOUND['restore_stage']
save_stage = _BOUND['save_stage']


def validate_completed(task):
    task = tx.ordinary(task)
    sources.verify(task)
    result = common.read(task / RESULT, 4 * common.MIB)
    common.need(set(result) == {'schema', 'epoch_relative', 'summary'}
                and result['schema'] == 'COMPLETE_FULL66_B3P34_CONDITIONAL_ARITHMETIC_V1',
                'One complete dedicated original B3p34 result')
    relative = tx.parts(result['epoch_relative'])
    common.need(len(relative) == 1, 'Direct complete original native epoch')
    epoch = task / relative[0]
    checked = evidence.validate_stage(task, sources.job(), epoch)
    common.need(evidence.template.same(checked, result['summary']),
                'Whole original stopped native evidence is revalidated, not its flag')
    return checked


def ensure(cache, task, *, completed_cache=None, log_root=None, on_epoch=None):
    """Prepare or resume exactly one full native acceptance; never rerun extra17."""
    task = tx.ordinary(task)
    if not task.exists():
        sources.prepare(cache, task)
    else:
        sources.verify(task)
    if (task / RESULT).is_file():
        return task, validate_completed(task)
    selected = sources.job()
    restored = (restore_stage(task, selected, completed_cache, log_root=log_root)
                if completed_cache is not None else None)
    epoch, checked = restored if restored is not None else accept(
        task, selected, on_epoch=on_epoch)
    atomic_json(task / RESULT, dict(
        schema='COMPLETE_FULL66_B3P34_CONDITIONAL_ARITHMETIC_V1',
        epoch_relative=epoch.relative_to(task).as_posix(), summary=checked))
    checked = validate_completed(task)
    if completed_cache is not None and restored is None:
        save_stage(task, selected, epoch, completed_cache)
    return task, checked


def frame(task):
    """Return the same checked COUNT-frame ABI as the other full66 constituents."""
    task = tx.ordinary(task)
    checked = validate_completed(task)
    result = common.read(task / RESULT, 4 * common.MIB)
    capsule = task / result['epoch_relative'] / 'capsule'
    selected = sources.job()
    return dict(job_id=selected['job_id'], member=sources.MEMBER, task=task,
                capsule=capsule, row=selected, validated=checked,
                contract=capsule / 'contract.json',
                forest=capsule / selected['forest_filename'],
                native=capsule / selected['acceptance_filename'])
