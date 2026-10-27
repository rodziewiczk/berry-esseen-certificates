"""Stream fresh original COUNT verification over untrusted candidate blobs.

--resume reuses the candidate data and output parent only. It NEVER reuses a
saved PASS; every selected job receives a new directory and native execution.
"""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import uuid


def pin(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--manifest', type=Path, default=here / 'MANIFEST.json')
    parser.add_argument('--worker', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--jobs', type=int, default=1, help='dynamic concurrent native jobs')
    parser.add_argument('--job-id', action='append', help='optional exact job IDs; default all')
    parser.add_argument('--timeout', type=int, default=1800)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    if args.jobs < 1 or args.timeout < 1:
        parser.error('positive jobs and timeout required')
    manifest = json.loads(args.manifest.read_bytes())
    if manifest['schema'] != 'be.public-untrusted-count-candidates/1':
        parser.error('unsupported candidate manifest')
    rows = manifest['jobs']
    selected = sorted(set(args.job_id) if args.job_id else rows)
    if not selected or any(job not in rows for job in selected):
        parser.error('unknown or empty candidate selection')
    if args.output.exists() and not args.resume:
        parser.error('output exists; --resume allows data reuse but reruns every job')
    worker = args.worker.resolve(strict=True)
    worker_sha = pin(worker)
    args.output.mkdir(parents=True, exist_ok=True)
    run = args.output.resolve() / ('run-' + uuid.uuid4().hex)
    run.mkdir()
    data_root = args.manifest.resolve().parent

    def verify(job_id):
        row = rows[job_id]
        meta = row['candidate']
        candidate = (data_root / meta['path']).resolve(strict=True)
        if data_root not in candidate.parents or candidate.stat().st_size != meta['bytes'] or pin(candidate) != meta['sha256']:
            raise ValueError('whole candidate SHA/size/path mismatch: ' + job_id)
        directory = run / job_id
        # Isolated Python omits the script directory. Explicitly add only the
        # selected public worker's directory for its capsule_worker dependency.
        bootstrap = ("import runpy,sys;from pathlib import Path;"
                     "p=Path(sys.argv[1]).resolve();sys.path.insert(0,str(p.parent));"
                     "sys.argv=sys.argv[1:];runpy.run_path(str(p),run_name='__main__')")
        command = [sys.executable, '-I', '-B', '-c', bootstrap, str(worker), 'verify', job_id,
                   '--directory', str(directory), '--candidate', str(candidate),
                   '--timeout', str(args.timeout)]
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 timeout=args.timeout + 60, check=False)
        log = run / (job_id + '.adapter.log')
        log.write_bytes(process.stdout + b'\nSTDERR\n' + process.stderr)
        return {'job_id': job_id, 'exit_code': process.returncode,
                'fresh_native_success': process.returncode == 0,
                'candidate_sha256': meta['sha256'], 'directory': directory.name,
                'log_sha256': pin(log), 'saved_pass_reused': False}

    results, failures = [], 0
    with (run / 'RESULTS.jsonl').open('x', encoding='utf-8') as stream:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
            futures = {executor.submit(verify, job): job for job in selected}
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                except Exception as exc:
                    result = {'job_id': futures[future], 'fresh_native_success': False,
                              'error': str(exc), 'saved_pass_reused': False}
                failures += not result['fresh_native_success']
                results.append(result)
                line = json.dumps(result, sort_keys=True)
                stream.write(line + '\n')
                stream.flush()
                print(line, flush=True)
    unchanged = pin(worker) == worker_sha
    summary = {'schema': 'be.public-fresh-count-batch/1', 'selected_jobs': len(selected),
               'completed_jobs': len(results), 'failed_jobs': failures,
               'worker_sha256': worker_sha, 'worker_unchanged': unchanged,
               'candidate_manifest_sha256': pin(args.manifest),
               'saved_pass_reused': False, 'all_index_full_pass': False,
               'global_theorem_accepted': False,
               'scope': 'Fresh conditional numerical COUNT verification only.'}
    (run / 'SUMMARY.json').write_text(json.dumps(summary, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, sort_keys=True))
    return 0 if not failures and unchanged else 1


if __name__ == '__main__':
    raise SystemExit(main())
