"""Public actual20/41 native entry points; no authority keys or PASS imports."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, platform, shutil, subprocess, sys, time, zipfile

HERE = Path(__file__).resolve().parent
MANIFEST_SHA256 = '21005346208478384d737650cd96dd97b394d833991303733a8b43ec8d36d08c'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def read(path):
    def unique(items):
        result = {}
        for k, v in items:
            need(k not in result, 'Duplicate JSON key')
            result[k] = v
        return result
    return json.loads(Path(path).read_bytes(), object_pairs_hook=unique)

def write(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2, sort_keys=True, allow_nan=False) + '\n',
                          encoding='utf-8', newline='\n')

def safe(name):
    p = PurePosixPath(name)
    need(not p.is_absolute() and p.as_posix() == name and all(x not in ('', '.', '..')
         and ':' not in x and '\\' not in x for x in p.parts), 'Contained canonical archive member')
    return p.parts

def manifest():
    need(sha(HERE / 'SOURCE-MANIFEST.json') == MANIFEST_SHA256, 'Pinned entire source manifest')
    m = read(HERE / 'SOURCE-MANIFEST.json')
    for name, row in m['archives'].items():
        p = HERE.joinpath(*safe(name))
        need(p.is_file() and not p.is_symlink() and p.stat().st_size == row['bytes']
             and sha(p) == row['sha256'], 'Exact whole public source/input archive: ' + name)
    return m

def extract(z, name, target, expected=None):
    raw = z.read(name)
    if expected:
        need(len(raw) == expected['bytes'] and hashlib.sha256(raw).hexdigest() == expected['sha256'],
             'Whole immutable source/input: ' + name)
    p = Path(target).joinpath(*safe(name))
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as stream:
        stream.write(raw)
    return p

def runtime(target, m):
    target.mkdir()
    with zipfile.ZipFile(HERE / 'sources/runtime.zip') as z:
        need(set(z.namelist()) == set(m['runtime_files']) and len(z.namelist()) == len(m['runtime_files']),
             'Closed original runtime source projection')
        for name, row in m['runtime_files'].items():
            extract(z, name, target, row)
    sys.path.insert(0, str(target))
    from be_replay import finite2024_actual20_full as full
    from be_replay import finite2024_coupled_parent as coupled
    return full, coupled

def source_cache(target, full):
    """Reconstruct all exact original-byte references, not an accepted stage."""
    originals, supplement = target / 'originals', target / 'supplement'
    originals.mkdir(); supplement.mkdir()
    with zipfile.ZipFile(HERE / 'sources/original-source-cache.zip') as z:
        catalog = json.loads(z.read('CURRENT2024-SOURCE-CACHE.json'))
        for role, dest in (('originals', originals), ('supplement', supplement)):
            for name, row in catalog['selections'][role].items():
                raw = z.read('current2024-source-cas/' + row['sha256'])
                need(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'],
                     'Whole original source-cache object')
                p = dest.joinpath(*safe(name)); p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(raw)
    src = full.s
    marker = dict(schema=src.SCHEMA, source_plan_sha256=src.PLAN_SHA256,
                  files_sha256=src._expected_files(), original_mathematical_code_executed=False,
                  numerical_acquisition_verified=False, full_notebook58H_completed=False,
                  all_index_conclusion_verified=False)
    (originals / 'ORIGINALS.json').write_bytes(src.dump(marker))
    src.verify_cache(originals); full.extra.verify(supplement)
    return originals, supplement

def profile():
    return dict(python=sys.version, executable=str(Path(sys.executable).resolve()),
                executable_sha256=sha(sys.executable), platform=platform.platform(),
                optimize=sys.flags.optimize, fresh_observation=True,
                legacy_runtime_profile_required=False, numerical_only=True, full_pass=False)

def scalar(out, full, coupled, timeout):
    """Execute the complete original five-contract scalar/control program."""
    task = out / 'scalar-task'; task.mkdir(); cap = task / 'capsule'; cap.mkdir()
    rows = full.original_files(task)
    names = {coupled.SCRIPT, coupled.HELPER, coupled.RESULT,
             coupled.DIRECTORY + '/PROOF.txt', coupled.B + 'root/inward_quadratic_noise_v1/PROOF.txt'}
    names |= {coupled.contract_path(b, i) for b, i in coupled.CASES}
    with zipfile.ZipFile(HERE / 'sources/original-source-cache.zip') as z:
        for name in sorted(names):
            row = rows[name]; raw = z.read('current2024-source-cas/' + row['sha256'])
            need(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'],
                 'Exact whole selected scalar reference')
            p = task / row['location'] / name; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(raw)
            if name != coupled.RESULT:
                p = cap / name; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(raw)
    prepared = coupled.prepare(task)
    command = [sys.executable, '-I', '-B', str(HERE / 'path_abi.py'), str(cap / coupled.DRIVER)]
    started = time.monotonic()
    with (out / 'stdout.txt').open('wb') as stdout, (out / 'stderr.txt').open('wb') as stderr:
        p = subprocess.Popen(command, cwd=cap / coupled.DIRECTORY, stdout=stdout, stderr=stderr,
                             start_new_session=os.name != 'nt')
        try:
            p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            if os.name == 'nt':
                p.kill()
            else:
                import signal
                os.killpg(p.pid, signal.SIGKILL)
            p.wait()
            raise ValueError('Scalar timeout; no numerical acceptance')
    need(p.returncode == 0 and (out / 'stderr.txt').stat().st_size == 0,
         'Actual complete native scalar process, zero return code and empty stderr')
    checked = coupled.validate(task, (out / 'stdout.txt').read_text('utf-8'))
    result = dict(schema='public-actual41-scalar-numerical-replay/1', argv=command,
                  returncode=p.returncode, seconds=time.monotonic()-started,
                  source_epoch=prepared, full_original_reader=checked,
                  stdout_sha256=sha(out/'stdout.txt'), stderr_sha256=sha(out/'stderr.txt'),
                  profile=profile(), scope='Five exact conditional scalar contracts only',
                  actual41_completed=False, upstream_numerical_parents_acquired=False, full_pass=False)
    write(out / 'RESULT.json', result)
    return result

def original_protocol(out, full, inputs, stop_after):
    """Expose the original strict full-stage API; never cast public COUNT JSON."""
    need(sys.platform == 'linux', 'The unchanged full stopped-action supervisor requires Linux')
    packet = read(inputs)
    need(set(packet) == {'parents', 'counts'} and set(packet['parents']) ==
         {'auxiliary', 'universal', 'supported', 'feedback'}, 'Four literal complete upstream stage directories')
    selected = {r['job_id'] for r in full.cs.jobs('n20_24') if r['n'] == 20}
    need(set(packet['counts']) == selected and len(selected) == 49,
         'All49 literal original COUNT stage directories, never a partial/result-only map')
    originals, supplement = source_cache(out, full)
    task = out / 'task'
    # prepare calls all four complete Fourier/feedback readers and every whole
    # COUNT reader. No earlier observation, signature or boolean is sufficient.
    state = full.prepare(originals, supplement, task,
                         parents={k:Path(v).resolve() for k,v in packet['parents'].items()},
                         count_tasks={k:Path(v).resolve() for k,v in packet['counts'].items()})
    while len(state['actions']) < stop_after:
        state = full.prefix.advance(task, adapter=full.Adapter(), root=out)
    checked = full.validate_completed(task) if stop_after == 41 else full.prefix.validate(task, adapter=full.Adapter())
    result = dict(schema='public-actual41-original-protocol-replay/1',
                  actions=len(state['actions']), original_reader=checked, profile=profile(),
                  source_epoch='Original full protocol; see README for later continuation/source epochs',
                  public_output_bridge_implemented=False, final_current_source_epoch_equivalence=False,
                  numerical_only=True, full_pass=False)
    write(out/'RESULT.json', result)
    return result

def main():
    need(__debug__ and sys.dont_write_bytecode and not sys.flags.optimize,
         'Run with python -I -B, without optimization')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode', choices=('inspect', 'scalar', 'original-protocol'))
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--inputs', type=Path)
    p.add_argument('--timeout', type=int, default=120)
    p.add_argument('--stop-after', type=int, default=41)
    args = p.parse_args()
    need(0 < args.timeout <= 82800 and 0 <= args.stop_after <= 41, 'Bounded explicit controls')
    out=args.output.resolve(); need(not out.exists(), 'Fresh exclusive output directory'); out.mkdir(parents=True)
    m=manifest(); full,coupled=runtime(out/'runtime', m)
    if args.mode == 'inspect':
        result=dict(schema='public-actual41-source-inspection/1', tasks=full.specs(),
                    original_operations=40, explicit_scalar_parent=1, profile=profile(),
                    numerical_program_executed=False, full_pass=False)
        write(out/'RESULT.json', result)
    elif args.mode == 'scalar':
        result=scalar(out,full,coupled,args.timeout)
    else:
        need(args.inputs is not None, '--inputs is required for the full original protocol')
        result=original_protocol(out,full,args.inputs,args.stop_after)
    print(json.dumps({k:v for k,v in result.items() if k in
          ('schema','returncode','actions','actual41_completed','full_pass')},sort_keys=True))

if __name__ == '__main__':
    main()
