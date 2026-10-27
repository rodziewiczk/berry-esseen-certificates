"""Public transport for fixed, unchanged native numerical source packages.

No authority, signatures, old captures or cloud services are inputs. A completed
slice is conditional arithmetic, never an assertion of the thirteen-role theorem.
"""
from pathlib import Path, PurePosixPath
from hashlib import sha256
import argparse
import json
import os
import signal
import subprocess
import sys
import time
import zipfile

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    def unique(items):
        out = {}
        for k, v in items:
            need(k not in out, 'Duplicate JSON field')
            out[k] = v
        return out
    return json.loads(Path(path).read_bytes(), object_pairs_hook=unique,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError('Nonfinite JSON')))


def write(path, value):
    with Path(path).open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')


def digest(path):
    h = sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def contained(root, name):
    need(type(name) is str and '\\' not in name and ':' not in name,
         'Portable relative member')
    p = PurePosixPath(name)
    need(p.parts and not p.is_absolute() and '..' not in p.parts and p.as_posix() == name,
         'Canonical contained member')
    result = root.joinpath(*p.parts)
    need(result.resolve().is_relative_to(root.resolve()), 'Member escapes its source directory')
    return result


def manifest():
    d = read(HERE / 'TASKS.json')
    need(d['schema'] == 'be.public-native-resource-tasks/1', 'Fixed public task schema')
    return d


def verify_package(task):
    package = HERE / task['archive']
    need(package.is_file() and not package.is_symlink() and digest(package) == task['archive_sha256'],
         'Missing or changed original source archive: ' + task['archive'])
    with zipfile.ZipFile(package) as z:
        need(len(z.namelist()) == len(set(z.namelist())) and set(z.namelist()) == set(task['files']),
             'Exact complete source archive inventory')
        for info in z.infolist():
            contained(HERE, info.filename)
            need(not info.is_dir() and ((info.external_attr >> 16) & 0o170000) != 0o120000,
                 'Ordinary source archive files only')
            need(sha256(z.read(info)).hexdigest() == task['files'][info.filename],
                 'Original source/member hash differs: ' + info.filename)
    need(task['entry'] in task['files'], 'Original entry belongs to the full source closure')
    return package


def source_inventory(root):
    out = {}
    for p in root.rglob('*'):
        need(not p.is_symlink(), 'No source symlinks')
        if p.is_file():
            out[p.relative_to(root).as_posix()] = digest(p)
    return out


def stop_tree(child):
    if child.poll() is not None:
        return
    if os.name == 'nt':
        subprocess.run(['taskkill', '/PID', str(child.pid), '/T', '/F'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    else:
        os.killpg(child.pid, signal.SIGKILL)
    child.wait()


def result_checks(task, report):
    need(report.get('status') == task['result_status'], 'Original complete numerical status required')
    for k, expected in task.get('equals', {}).items():
        need(type(report.get(k)) is type(expected) and report[k] == expected,
             'Original result field differs: ' + k)
    for k, expected in task.get('lengths', {}).items():
        need(type(report.get(k)) in (list, dict) and len(report[k]) == expected,
             'Incomplete original result collection: ' + k)
    for k in ('failed', 'failures', 'errors'):
        if k in report:
            need(report[k] in ([], {}), 'Original task retained a failure: ' + k)
    need(report.get('full_proof_pass', False) is False,
         'This adapter cannot issue an all-index proof claim')


def run(task_id, output, seconds=3600, jobs=1):
    tasks = manifest()['tasks']
    need(task_id in tasks, 'Unsupported native task: ' + task_id)
    task = tasks[task_id]
    need(task['supported'], task.get('reason', 'Task needs another explicit adapter'))
    need(type(seconds) is int and seconds > 1 and type(jobs) is int
         and 1 <= jobs <= task.get('max_jobs', 1), 'Finite timeout and supported parallelism')
    package = verify_package(task)
    output = Path(output).absolute()
    need(not output.exists(), 'Use a fresh output directory')
    output.mkdir(parents=True)
    source = output / 'source'
    source.mkdir()
    with zipfile.ZipFile(package) as z:
        for name in task['files']:
            p = contained(source, name)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(z.read(name))
    need(source_inventory(source) == task['files'], 'Full source closure after relocation')
    result_dir = output / 'native'
    argv = [sys.executable, '-B', '-S', str(source / task['entry']), 'run',
            '--task', str(result_dir), '--deadline', str(int(time.time()) + seconds)]
    if task.get('jobs_argument'):
        argv += ['--jobs', str(jobs)]
    env = os.environ.copy()
    for key in ('PYTHONPATH', 'PYTHONHOME', 'PYTHONOPTIMIZE', 'BE_FROZEN_SCIENTIFIC_SITE'):
        env.pop(key, None)
    env.update(PYTHONDONTWRITEBYTECODE='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
    observation = dict(schema='be.public-native-resource-observation/1', task_id=task_id,
                       archive_sha256=task['archive_sha256'], entry=task['entry'],
                       original_entry_sha256=task['files'][task['entry']],
                       argv=['python', '-B', '-S', 'source/' + task['entry'], 'run',
                             '--task', 'native', '--deadline', argv[8], *argv[9:]],
                       status='INCOMPLETE', full_proof_pass=False,
                       authentication_or_global_theorem_issued=False)
    child = None
    began = time.monotonic()
    try:
        with (output / 'stdout.txt').open('xb') as out, (output / 'stderr.txt').open('xb') as err:
            child = subprocess.Popen(argv, cwd=source, env=env, stdin=subprocess.DEVNULL,
                                     stdout=out, stderr=err, start_new_session=os.name != 'nt')
            try:
                rc = child.wait(timeout=seconds + 10)
            except subprocess.TimeoutExpired:
                stop_tree(child)
                raise ValueError('Native task timeout; partial outputs are not acceptance')
        observation['returncode'] = rc
        need(rc == 0 and (output / 'stderr.txt').stat().st_size == 0,
             'Original complete native execution failed; inspect captured stderr')
        report_path = result_dir / task.get('result_file', 'RESULT.json')
        need(report_path.is_file(), 'Missing complete original numerical result')
        report = read(report_path)
        result_checks(task, report)
        need(source_inventory(source) == task['files'], 'Original static source closure changed during execution')
        observation.update(status='COMPLETE_CONDITIONAL_NATIVE_SLICE',
                           native_status=report['status'], result_sha256=digest(report_path),
                           result_file='native/' + task.get('result_file', 'RESULT.json'))
    except Exception as error:
        observation['error'] = type(error).__name__ + ': ' + str(error)
        raise
    finally:
        if child is not None:
            stop_tree(child)
        observation.update(seconds=time.monotonic() - began,
                           stdout_sha256=digest(output / 'stdout.txt') if (output / 'stdout.txt').exists() else None,
                           stderr_sha256=digest(output / 'stderr.txt') if (output / 'stderr.txt').exists() else None)
        write(output / 'OBSERVATION.json', observation)
    return observation


def main():
    p = argparse.ArgumentParser(allow_abbrev=False)
    p.add_argument('mode', choices=('list', 'verify', 'run'))
    p.add_argument('--task-id')
    p.add_argument('--output', type=Path)
    p.add_argument('--seconds', type=int, default=3600)
    p.add_argument('--jobs', type=int, default=1)
    a = p.parse_args()
    need(__debug__ and not sys.flags.optimize, 'Ordinary Python required')
    d = manifest()
    if a.mode == 'list':
        print(json.dumps({k:dict(supported=v['supported'], entry=v['entry'],
                                reason=v.get('reason')) for k,v in d['tasks'].items()}, indent=2))
    elif a.mode == 'verify':
        selected = [a.task_id] if a.task_id else list(d['tasks'])
        for name in selected:
            need(name in d['tasks'], 'Unknown task')
            verify_package(d['tasks'][name])
        print(json.dumps(dict(verified_source_packages=len(selected), native_calls=0, full_proof_pass=False)))
    else:
        need(a.task_id is not None and a.output is not None, 'Explicit task and fresh output required')
        print(json.dumps(run(a.task_id, a.output, a.seconds, a.jobs), indent=2))


if __name__ == '__main__':
    main()
