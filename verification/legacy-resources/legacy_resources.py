"""Fresh public execution of fixed original C5/C6--9/C10--19 resource jobs.

The original native controllers and complete mathematical acceptors run
unchanged. Their numerical scopes remain conditional; no global PASS is issued.
"""
import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import uuid
import zipfile

HERE = Path(__file__).resolve().parent


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def physical(path):
    """Windows long-path I/O only; original native path metadata is unchanged."""
    path = Path(path).absolute()
    text = str(path)
    return Path('\\\\?\\' + text) if os.name == 'nt' and not text.startswith('\\\\') else path


def digest(path):
    h = hashlib.sha256()
    with physical(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def manifest():
    value = json.loads((HERE / 'MANIFEST.json').read_bytes())
    need(value['schema'] == 'be.public-legacy-native-tasks/1' and value['all_index_full_pass'] is False,
         'Exact public partial numerical task catalogue')
    return value


def package(data, destination=None):
    meta = data['package']
    path = HERE / meta['path']
    need(path.is_file() and not path.is_symlink() and path.stat().st_size == meta['bytes']
         and digest(path) == meta['sha256'], 'Whole original source/data package SHA and size')
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        need(len(names) == len(set(names)) == len(meta['files']) and set(names) == set(meta['files']),
             'Complete closed source/data inventory')
        for name in names:
            p = PurePosixPath(name)
            need(not p.is_absolute() and '..' not in p.parts and '\\' not in name and ':' not in name,
                 'Contained public source member')
            row = meta['files'][name]
            body = z.read(name)
            need(len(body) == row['bytes'] and hashlib.sha256(body).hexdigest() == row['sha256'],
                 'Every complete original source/data byte: ' + name)
            if destination is not None:
                target = physical(destination.joinpath(*p.parts))
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open('xb') as stream:
                    stream.write(body)


def unchanged(data, runtime):
    for name, row in data['package']['files'].items():
        path = physical(runtime.joinpath(*PurePosixPath(name).parts))
        need(path.is_file() and path.stat().st_size == row['bytes'] and digest(path) == row['sha256'],
             'Unchanged original runtime source/data: ' + name)


def prepare(data, row, output, archives, fetch, deps):
    need(not output.exists(), 'Exclusive new execution directory; no saved completion is reused')
    runtime = output / 'runtime'
    runtime.mkdir(parents=True)
    package(data, runtime)
    sys.path.insert(0, str(runtime))
    sys.path.insert(0, str(runtime / 'snapshot'))
    group = row['source_group']
    cache = output / 'source-cache'
    if row['adapter'] == 'n5_remaining':
        module = importlib.import_module('be_replay.n5_remaining_sources')
        directory = archives if archives is not None else output / 'archives'
        archive = module.obtain_archive(directory, download=fetch)
        module.prepare_cache(archive, cache)
    elif group in ('65.caps', '65.remaining'):
        importlib.import_module('resource65_source_cache').materialize(group, cache)
    elif group and group.endswith('.controls'):
        importlib.import_module('resource_controls_source_cache').materialize(
            group, runtime / 'resource-controls-extension', cache,
            manifest_sha256=data['controls_manifest_sha256'])
    elif group:
        importlib.import_module('resource_source_cache').materialize(
            group, cache, upstream_high=deps.get('57H.high'))
    else:
        cache.mkdir()
    unchanged(data, runtime)
    return runtime, cache


def portable_scalar(task):
    """New plain process transport; retain the complete original scalar math."""
    source = importlib.import_module('be_replay.finite1014_kappa_sources')
    evidence = importlib.import_module('be_replay.finite1014_kappa_evidence')
    request = source.prepare(task)
    command = evidence.command(request, sys.executable)
    process = subprocess.run(command, cwd=task / 'capsule', stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, timeout=120, check=False)
    (task / 'public-native.stdout.txt').write_bytes(process.stdout)
    (task / 'public-native.stderr.txt').write_bytes(process.stderr)
    need(process.returncode == 0 and not process.stderr, 'Complete original scalar process must finish successfully')
    source.verify(task)
    summary = evidence.scalar_outputs(task, request, json.loads(process.stdout))
    return {'whole_original_scalar_math_verified': True, 'summary': summary,
            'actual_returncode': process.returncode,
            'stdout_sha256': hashlib.sha256(process.stdout).hexdigest(),
            'transport': 'public ordinary subprocess; no historical supervisor identity claimed'}


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('mode', choices=('list', 'verify', 'prepare', 'run', 'replay'))
    parser.add_argument('--task')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--dependencies', type=Path, help='explicit original completed dependency task directories')
    parser.add_argument('--archives', type=Path, help='existing pinned original public C5 ZIP directory')
    parser.add_argument('--fetch', action='store_true', help='allow the original C5 source downloader; exact SHA remains required')
    args = parser.parse_args()
    need(__debug__ and not sys.flags.optimize and sys.dont_write_bytecode, 'Use unoptimized Python -B')
    data = manifest()
    if args.mode == 'list':
        print(json.dumps({'tasks': data['tasks'], 'remaining': data['remaining'], 'all_index_full_pass': False}, indent=2))
        return
    if args.mode == 'verify':
        package(data)
        print(json.dumps({'whole_package_verified': True, 'tasks': data['task_count'],
                          'native_calls': 0, 'all_index_full_pass': False}))
        return
    need(args.task in data['tasks'] and args.output is not None, 'Exact task and new output directory required')
    row = data['tasks'][args.task]
    need(row['runnable'], row.get('reason', 'Unsupported exact source route'))
    if args.mode in ('run', 'replay'):
        need(sys.platform == 'linux' or args.task == 'shared.kappa62_625',
             'Original complete resource controllers require Linux; only the explicit scalar transport is portable')
    deps = {} if args.dependencies is None else json.loads(args.dependencies.read_bytes())
    need(type(deps) is dict and all(type(k) is str and type(v) is str for k, v in deps.items()),
         'Explicit dependency directory map')
    deps = {k: Path(v).resolve(strict=True) for k, v in deps.items()}
    required = row.get('runtime_requires', [])
    need(all(k in deps for k in required), 'Required original dependencies missing: ' + ', '.join(k for k in required if k not in deps))
    output = args.output.resolve()
    own = digest(__file__)
    runtime, cache = prepare(data, row, output, args.archives, args.fetch, deps)
    if args.mode == 'prepare':
        print(json.dumps({'task': args.task, 'whole_source_inputs_prepared': True,
                          'native_calls': 0, 'all_index_full_pass': False}))
        return
    task = output / 'task'
    logs = output / 'logs'
    logs.mkdir()
    if args.task == 'shared.kappa62_625':
        checked = portable_scalar(task)
    elif row['adapter'] == 'n5_remaining':
        source = importlib.import_module('be_replay.n5_remaining_sources')
        controller = importlib.import_module('be_replay.n5_remaining')
        checked = controller.execute(task, source.job(row['job_id']), cache, log_root=logs)
    else:
        controller = importlib.import_module('resource_worker_v2')
        checked = controller.run(args.task, task, cache, dependencies=deps,
                                 campaign_id='public-native-' + uuid.uuid4().hex, log_root=logs)
    unchanged(data, runtime)
    need(digest(__file__) == own, 'Public dispatcher unchanged throughout native execution')
    result = {'schema': 'be.public-fresh-legacy-resource-execution/1',
              'task_id': args.task, 'source_package_sha256': data['package']['sha256'],
              'adapter_sha256': own, 'original_complete_controller_result': checked,
              'fresh_native_execution_completed': True, 'historical_authority_used': False,
              'same_law_parent_facts_acquired': False, 'saved_pass_reused': False,
              'all_index_full_pass': False, 'global_theorem_accepted': False}
    (output / 'PUBLIC-LEGACY-NATIVE-RESULT.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
