"""Public Berry--Esseen replay front door (partial native coverage).

No saved observation, source audit, or COUNT result is a global proof.
This wrapper streams the original public numerical runners unchanged.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import uuid

FOUNDATION_STAGES = ('n2-scalars', 'n2-primary', 'n2-independent', 'n3-scalars',
                     'n3-identities', 'n3-full', 'root4-two-pass')


def emit(value):
    print(json.dumps(value, sort_keys=True, ensure_ascii=True), flush=True)


def locate(root, *names):
    for name in names:
        path = root / name
        if path.exists():
            return path.resolve()
    raise FileNotFoundError('Required public file is missing: ' + ' or '.join(names))


def layout(root):
    return {
        'count_worker': ('verification/count/count_worker_v2.py', 'work/public-replay-v1/count_worker_v2.py'),
        'count_batch': ('verification/count/batch_verify.py', 'certificates/count/batch_verify.py', 'work/public-count-witnesses-public/batch_verify.py'),
        'count_data': ('certificates/count/MANIFEST.json', 'work/public-count-witnesses-public/MANIFEST.json'),
        'resources': ('verification/resources/generic_resource_batch.py', 'work/public-noncount-public/generic_resource_batch.py'),
        'foundations': ('verification/foundations/foundations.py',),
        'finite_tail': ('verification/finite-tail/replay.py',),
        'n1_worker': ('verification/count/capsule_worker.py', 'verification/n1/capsule_worker.py', 'work/public-replay-v1/capsule_worker.py'),
        'n1_source': ('verification/count/capsules/N1-dual', 'verification/n1/capsules/N1-dual', 'work/public-replay-v1/capsules/N1-dual'),
        'n1_candidate': ('verification/count/witnesses/N1-dual.json', 'verification/n1/witnesses/N1-dual.json', 'work/public-replay-v1/witnesses/N1-dual.json'),
    }


def status(root):
    available = {}
    for name, paths in layout(root).items():
        try:
            available[name] = str(locate(root, *paths).relative_to(root))
        except FileNotFoundError:
            available[name] = None
    data = None
    if available['count_data']:
        manifest_path = root / available['count_data']
        manifest = json.loads(manifest_path.read_bytes())
        present = 0
        for row in manifest.get('jobs', {}).values():
            pin = row['candidate']
            candidate = manifest_path.parent / pin['path']
            if candidate.is_file() and candidate.stat().st_size == pin['bytes']:
                present += 1
        required = manifest.get('required_jobs')
        data = {'required_jobs': required, 'available_jobs': present,
                'all_required_candidates_available': present == required,
                'manifest_declared_available_jobs': manifest.get('available_jobs'),
                'availability_is_not_arithmetic_verification': True}
    campaign = None
    for base in (root / 'verification-results/count', root / 'work/full-count-public-verification-v1'):
        if base.is_dir():
            runs = sorted(base.glob('run-*'), key=lambda p: p.stat().st_mtime, reverse=True)
            if runs:
                run = runs[0]
                results = run / 'RESULTS.jsonl'
                rows = []
                if results.is_file():
                    for line in results.read_text(encoding='utf-8').splitlines():
                        try:
                            rows.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass  # A live final line may still be in flight.
                summary = run / 'SUMMARY.json'
                campaign = {'completed_jobs_observed': len(rows),
                            'failed_jobs_observed': sum(not r.get('fresh_native_success', False) for r in rows),
                            'final_batch_summary_present': summary.is_file(),
                            'live_process_state_checked': False}
                break
    phase = ('COUNT_BATCH_UNFINISHED' if campaign and not campaign['final_batch_summary_present'] else
             'COUNT_BATCH_FINISHED' if campaign else 'NOT_STARTED_HERE')
    return {'generated_at_utc': datetime.now(timezone.utc).isoformat(),
            'source_audit': 'CLOSED', 'public_verification': phase,
            'full_pass': 'NOT_ESTABLISHED', 'status_is_execution_receipt': False,
            'unfinished_campaign_may_be_running_or_interrupted': phase == 'COUNT_BATCH_UNFINISHED',
            'count_candidate_data': data, 'count_campaign_observation': campaign,
            'available_paths': available,
            'remaining_full_verification_obligations': [
                'G2/G3/ROOT4 complete native foundation coverage and integration',
                'actual20 continuation: complete 41-step replay, public stage bridge and final source epochs',
                '49 actual20 COUNT jobs outside the selected 1243-job public registry',
                'finite43--48 numerical replay and two current collector joins',
                'tail49 complete numerical replay and current qualification',
                'all 13 roles, exact same-law parents, independent tail and final global binder'],
            'scope': 'Source audit and partial public native execution are distinct; COUNT alone never establishes the global theorem.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('action', choices=('status', 'verify'))
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent,
                        help='public project root; defaults to the directory containing be.py')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--counts', action='store_true')
    modes.add_argument('--task', help='an explicit generic native task, for example indexed40')
    modes.add_argument('--n1', action='store_true')
    modes.add_argument('--foundation', choices=FOUNDATION_STAGES,
                       help='fresh original G2/G3/ROOT4 numerical stage')
    modes.add_argument('--finite-tail', choices=('finite-all', 'tail-full'),
                       help='complete finite numerical parents or original tail suite')
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--timeout', type=int, default=1800)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--resume', action='store_true', help='COUNT data reuse only; all selected checks run afresh')
    args = parser.parse_args()
    if args.jobs < 1 or not 1 <= args.timeout <= 86400:
        parser.error('positive jobs and timeout between 1 and 86400 seconds required')
    root = args.root.resolve(strict=True)
    if args.action == 'status':
        emit(status(root))
        return 0
    if not (args.counts or args.task or args.n1 or args.foundation or args.finite_tail):
        result = status(root)
        result.update(result='INCOMPLETE', reason='The public driver does not yet cover the complete 13-role theorem.')
        emit(result)
        return 2
    if args.resume and not args.counts:
        parser.error('--resume applies only to --counts and never reuses saved PASS')
    paths = layout(root)
    selected = lambda name: locate(root, *paths[name])
    output = args.output or root / 'verification-results' / ('request-' + uuid.uuid4().hex)
    output = output.resolve()
    if args.counts:
        data = status(root)['count_candidate_data']
        if not data or not data['all_required_candidates_available']:
            parser.error('COUNT candidate files are missing; first run python tools/fetch_certificates.py --counts')
        command = [sys.executable, '-I', '-B', str(selected('count_batch')),
                   '--manifest', str(selected('count_data')), '--worker', str(selected('count_worker')),
                   '--output', str(output), '--jobs', str(args.jobs), '--timeout', str(args.timeout)]
        if args.resume:
            command.append('--resume')
        scope = 'complete conditional COUNT family only'
    elif args.finite_tail:
        command = [sys.executable, '-I', '-B', str(selected('finite_tail')),
                   args.finite_tail, '--output', str(output), '--seconds', str(args.timeout),
                   '--timeout', str(args.timeout), '--jobs', str(args.jobs)]
        scope = ('finite43--48 numerical parents; two collectors remain separate'
                 if args.finite_tail == 'finite-all' else 'original complete tail49 numerical suite')
    elif args.foundation:
        command = [sys.executable, '-I', '-B', str(selected('foundations')),
                   args.foundation, '--output', str(output), '--timeout', str(args.timeout)]
        scope = 'original foundation numerical stage: ' + args.foundation
    elif args.task:
        command = [sys.executable, '-I', '-B', str(selected('resources')), 'run',
                   '--task-id', args.task, '--output', str(output), '--seconds', str(args.timeout),
                   '--jobs', str(args.jobs)]
        scope = 'explicit original native resource task: ' + args.task
    else:
        command = [sys.executable, '-I', '-B', str(selected('n1_worker')), 'replay', 'N1-dual',
                   '--source', str(selected('n1_source')), '--candidate', str(selected('n1_candidate')),
                   '--output', str(output / 'N1-dual-result.json'), '--timeout', str(min(args.timeout, 600))]
        scope = 'N1 dual numerical certificate only'
    emit({'result': 'STARTING_FRESH_NATIVE_REPLAY', 'scope': scope, 'output': str(output),
          'full_pass': 'NOT_ESTABLISHED', 'saved_pass_reused': False})
    code = subprocess.call(command)  # inherit stdout/stderr for streaming progress
    emit({'result': 'REQUESTED_SCOPE_VERIFIED' if code == 0 else 'REQUESTED_SCOPE_FAILED',
          'scope': scope, 'exit_code': code, 'full_pass': 'NOT_ESTABLISHED'})
    return code


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError) as exc:
        emit({'result': 'INCOMPLETE', 'reason': str(exc), 'full_pass': 'NOT_ESTABLISHED'})
        raise SystemExit(2)
