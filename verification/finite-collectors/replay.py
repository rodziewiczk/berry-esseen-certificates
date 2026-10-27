"""Fresh finite43/44 numerical collectors, with explicit unproved analytic inputs."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
import argparse, copy, importlib, json, os, sys, time, uuid
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import upstream as up
need, digest, save, load = up.need, up.digest, up.save, up.load


def family_rows(data, row, rows):
    if Path(row.get('script', '')).name != 'bind_low42.py':
        return None
    family = 'central42_v2' if 'central42_v2' in row['cwd'] else 'left42_final'
    wanted = {r['task_id'] for r in data['low_rows'] if r['family'] == family}
    need(wanted <= set(rows), 'All fresh rows for the selected LOW family')
    return {key: rows[key] for key in sorted(wanted)}


@dataclass(frozen=True)
class Observed:
    """In-memory result of our own call; never reconstructed from external JSON."""
    task_id: str
    output: Path
    result_sha256: str


def finite_parent(native, observed, campaign, profile, root):
    need(type(observed) is Observed, 'An observed call in this execution is mandatory')
    task = observed.output
    need(task.parent == root / 'tasks' and task.name == observed.task_id,
         'The exact current private task directory')
    need(digest(task / 'TASK-COMPLETED.json') == observed.result_sha256, 'Unchanged observed complete result')
    request = native.guard(task)
    result = load(task / 'TASK-COMPLETED.json')
    row = native.definition(observed.task_id)
    command = [sys.executable, '-E', '-B', '-S', str(Path(native.__file__).parent / 'finite61_worker.py'),
               str(task / 'SOURCE-REQUEST.json')]
    process = result['process']; supervisor = process['supervisor']
    need(result['task_id'] == observed.task_id and result['campaign_id'] == campaign
         and request['campaign_id'] == campaign and result['runtime_profile_digest'] == profile
         and result['implementation'] == native.implementation()
         and result['source_manifest_sha256'] == native.MANIFEST_SHA
         and result['input_statement_digest'] == native.identity('task-inputs', request)
         and result['full_proof_pass'] is False and result['all_law_provider_populated'] is False,
         'Exact current task, source, inputs, runtime observation and conditional scope')
    need(process['command'] == command and type(supervisor['returncode']) is int
         and supervisor['returncode'] == 0 and supervisor['reason'] == 'completed'
         and supervisor['tree_cleanup_complete'] is True
         and digest(task / 'execution.log') == process['log_sha256'],
         'Actual whole successful subprocess receipt and complete capture')
    trace = native.common.parsed((task / 'SOURCE-READ-TRACE.json').read_bytes())
    need(native.common.sha(native.common.encoded(trace)) == result['source_read_trace_sha256']
         and trace['unexpected_reads'] == [] and set(trace['reads']) <= set(request['inputs']),
         'Whole actual source-read trace inside immutable inputs')
    if row['kind'] == 'native':
        report = native._stdout((task / 'execution.log').read_text(encoding='utf-8'), row['stdout_rule'])
        need(report == result['native_report'], 'Original complete typed mathematical output reader')
        return report
    need(result['outcome'] == 'FRESH_LOW_ROW_COMPUTED_NOT_ACCEPTED'
         and digest(task / 'LOW-ROW.json') == result['row_sha256'], 'Exact observed new LOW bytes')
    return None


def math_view(port, native, observed, root):
    work = root / 'math-view/work/below49_20261006'
    work.mkdir(parents=True)
    cache = Path(native.__file__).parent
    for name in port.DATA:
        p = work / name; p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(port._source(port.WORK_PREFIX + name, cache))
    byid = {r.task_id: r for r in observed}
    for row in native.manifest()['actions']:
        if Path(row['script']).name != 'bind_low42.py': continue
        family = 'central42_v2' if 'central42_v2' in row['cwd'] else 'left42_final'
        index = next(f['index_name'] for f in native.manifest()['low_families'] if f['family'] == family)
        task = byid[row['task_id']].output
        request = native.guard(task); name = row['cwd'] + '/' + index
        raw = (task / 'capsule' / name).read_bytes()
        need(native.common.sha(raw) == request['inputs'][name], 'Current fully replayed canonical LOW index')
        p = work / 'local' / family / index; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(raw)
    return work.parents[1]


def tail_inputs(tail, result, output):
    """Full original reader, followed by source-bound, whole typed outputs."""
    need(result['all_required_jobs_computed'] is True, 'Fresh full tail55 completed')
    source = output / 'original-BE49'; execution = output / 'native-full'
    tail.verify_sources(source); new, retained = tail.source_jobs(source)
    checked = tail.validate_full_result(source, execution, new, retained)
    need(all(result[k] == value for k, value in checked.items()), 'Original whole55 result reader agrees')
    tail.wrapper_captures(result['execution'])
    top = load(execution / 'result.json')['jobs']; children = load(execution / 'components/metadata.json')['jobs']
    specs = new + [dict(name=n, cwd=c, argv=[p]) for n,c,p in (
        ('finite_base','baseline/finite','accept_finite_base.py'),
        ('entry_schedule_mapping','baseline/entry','validate_schedule.py'),
        ('local_formula_mapping','baseline/local','check_consolidation.py'))]
    specs.append(dict(name=tail.TOP_NAMES[-1], cwd='.', argv=[tail.RUNNER]))
    predicates = []
    for group, records, definitions, directory in [('top', top, specs, execution), ('retained', children, retained, execution/'components')]:
        for row, definition in zip(records, definitions):
            tail.successful(row, directory, row['name'])
            text = (directory / (row['name']+'.stdout.txt')).read_text(encoding='utf-8')
            decoder = json.JSONDecoder(object_pairs_hook=tail.unique); objects = []
            for i, char in enumerate(text):
                if char != '{': continue
                try: value, end = decoder.raw_decode(text, i)
                except ValueError: continue
                if not text[end:].strip() and type(value) is dict: objects.append(value)
            # Some unchanged programs have exact terminal text instead of JSON;
            # preserve the full text and its digest rather than invent a schema.
            need(len(objects) <= 1, 'Unique complete terminal object where present')
            cwd = source / (('baseline/certificates/' if group == 'retained' else '') + definition['cwd'])
            program = cwd / definition['argv'][0]
            predicates.append(dict(group=group, name=row['name'], actual_record=row,
                complete_terminal_object=objects[0] if objects else None,
                complete_stdout=text, source_program_sha256=digest(program),
                fixed_input_manifest_sha256=tail.MANIFEST_SHA,
                source_job_definition=definition, analytic_license=None, all_law_claim=None))
    need(len(predicates) == 55, 'All14+41 complete original numerical predicates')
    return dict(original_reader=checked, predicates=predicates, full_pass=False,
                numerical_programs_launched_in_this_run=True, analytic_licenses_issued=False)


def compose(native, tail, observed, campaign, profile, root, tail_result):
    data = native.manifest()
    wanted = {r['task_id'] for key in ('actions', 'low_rows') for r in data[key]}
    need(len(observed) == 183 and {r.task_id for r in observed} == wanted, 'All and only183 observed current calls')
    reports = {r.task_id: finite_parent(native, r, campaign, profile, root) for r in observed}
    port = importlib.import_module('math_port')
    view = math_view(port, native, observed, root)
    jobs = [dict(run=r['id'][3:], report=reports[r['task_id']]) for r in data['actions'] if r['id'].startswith('44.')]
    outputs = {r['id'][3:]: reports[r['task_id']] for r in data['actions'] if r['id'].startswith('43.')}
    inputs = tail_inputs(tail, tail_result, root/'tail')
    save(root/'TAIL-TYPED-INPUTS.json', inputs)
    assumptions = port.required_typed_claims(Path(native.__file__).parent)
    result = dict(schema='public-finite-collectors/1', campaign_id=campaign,
        collector44=port._math44(view, jobs, Path(native.__file__).parent),
        collector43=port._math43(view, outputs, Path(native.__file__).parent),
        finite_observed_results={r.task_id: r.result_sha256 for r in observed},
        whole_tail_typed_inputs_sha256=digest(root/'TAIL-TYPED-INPUTS.json'),
        shared12_source='complete fresh original tail14+41 suite',
        required_analytic_and_same_law_contracts=assumptions,
        analytic_and_same_law_contracts_discharged=False,
        status='FRESH_NUMERICAL_COLLECTORS_COMPLETED_ANALYTIC_CONTRACTS_EXPLICIT',
        finite_projection_indices=list(range(43,49)), independent49plus_is_separate=True,
        all_law_provider_populated=False, full_pass=False, all_law_theorem_verified=False)
    return result


def run(args):
    need(sys.platform == 'linux', 'Full tail suite requires its unchanged Linux BASIC guard')
    output = args.output.resolve(); need(not output.exists(), 'Fresh exclusive full execution directory')
    need(1 <= args.jobs <= 64 and 1 <= args.seconds <= 64800 and 1 <= args.timeout <= 82800, 'Bounded positive budgets')
    output.mkdir(parents=True)
    before = dict(up.runtime(), collector_adapter_sha256=digest(__file__), math_port_sha256=digest(HERE/'math_port.py'))
    save(output/'RUNTIME-BEFORE.json', before); profile = digest(output/'RUNTIME-BEFORE.json')
    native, tail = up.backend(output); campaign = uuid.uuid4().hex
    deadline = time.monotonic()+args.seconds; rows = {}; observed = []
    data = native.manifest()
    def one(row):
        remaining = int(deadline-time.monotonic()); need(remaining > 0, 'Whole execution deadline')
        task = output/'tasks'/row['task_id']
        result = up.finite_one(native, row['task_id'], task, campaign, profile,
            min(args.timeout, remaining), family_rows(data, row, rows))
        print('COMPLETED '+row['task_id'], flush=True)
        return Observed(row['task_id'], task, result['result_sha256'])
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for item in pool.map(one, data['low_rows']): observed.append(item); rows[item.task_id] = str(item.output)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        observed.extend(pool.map(one, data['actions']))
    remaining = int(deadline-time.monotonic()); need(remaining > 0, 'Time remains for genuine tail55')
    tail_result = tail.run(output/'tail', archives=HERE/'sources', download=False, mode='basic',
        wall_seconds=remaining, cpu_seconds=remaining, heartbeat_seconds=30, memory_bytes=args.memory_mib*1048576)
    result = compose(native, tail, observed, campaign, profile, output, tail_result)
    after = dict(up.runtime(), collector_adapter_sha256=digest(__file__), math_port_sha256=digest(HERE/'math_port.py'))
    save(output/'RUNTIME-AFTER.json', after); need(before == after, 'Observed interpreter and adapter unchanged')
    save(output/'RESULT.json', result)
    return result


def main():
    need(__debug__ and not sys.flags.optimize, 'Unoptimized original arithmetic')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['collect-all','scalar-smoke'])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--jobs', type=int, default=1)
    parser.add_argument('--seconds', type=int, default=64800)
    parser.add_argument('--timeout', type=int, default=14400)
    parser.add_argument('--memory-mib', type=int, default=8192)
    args = parser.parse_args()
    if args.mode == 'scalar-smoke':
        args.mode='run'; args.task_id='61.native.43.scalar01'; args.rows=None; args.campaign_id=None
        up.run(args)
    else: run(args)
    print(json.dumps(dict(completed=True, result=str(args.output.resolve()/'RESULT.json'), full_pass=False)))


if __name__ == '__main__': main()
