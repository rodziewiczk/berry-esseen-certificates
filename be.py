"""Public Berry--Esseen replay front door and full-pass verification driver.

Validates all 13 upper-bound roles, the lower approximation, the global equality
C_* = C_E, and every fresh native numerical execution receipt in
verification-results/, or streams individual native numerical runners unchanged.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import uuid

FOUNDATION_STAGES = ('n2-scalars', 'n2-primary', 'n2-independent', 'n3-scalars',
                     'n3-identities', 'n3-full', 'root4-two-pass')
EXPECTED_ROLES = [
    'N1', 'G2', 'G3', 'G4', 'C5-one-free', 'projected-C69', 'projected-C1019',
    'current-C2024', 'current-C25', 'current-C2639', 'current-C4042',
    'current-C4348', 'independent-tail49',
]


def emit(value):
    print(json.dumps(value, sort_keys=True, ensure_ascii=True), flush=True)


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        while chunk := f.read(1048576):
            h.update(chunk)
    return h.hexdigest()


def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


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
        'finite_collectors': ('verification/finite-collectors/replay.py',),
        'actual20_counts': ('verification/actual20-counts/replay.py',),
        'actual20_scalar': ('verification/actual20/replay.py',),
        'n1_worker': ('verification/count/capsule_worker.py', 'verification/n1/capsule_worker.py', 'work/public-replay-v1/capsule_worker.py'),
        'n1_source': ('verification/count/capsules/N1-dual', 'verification/n1/capsules/N1-dual', 'work/public-replay-v1/capsules/N1-dual'),
        'n1_candidate': ('verification/count/witnesses/N1-dual.json', 'verification/n1/witnesses/N1-dual.json', 'work/public-replay-v1/witnesses/N1-dual.json'),
    }


def verify_all_receipts(root):
    """Cryptographically and structurally verify all completed verification receipts."""
    vr = root / 'verification-results'
    obligations = []
    verified = {}

    # 1. N1 dual certificate
    n1_path = vr / 'n1/N1-dual-result.json'
    if not n1_path.is_file():
        n1_path = vr / 'n1/RESULT.json'
    if n1_path.is_file():
        n1 = load_json(n1_path)
        n1_ok = (
            (n1.get('schema') == 'be.public-fresh-numerical-witness-result/1'
             and n1.get('actual_execution', {}).get('returncode') == 0
             and n1.get('fresh_arithmetic_checker_executed') is True
             and n1.get('whole_original_checker_result', {}).get('status') == 'EXACT_DUAL_POLYNOMIAL_CERTIFICATE_VERIFIED')
            or (n1.get('exit_code') == 0 and n1.get('saved_pass_reused') is False)
        )
        if n1_ok:
            verified['N1'] = {'status': 'VERIFIED', 'receipt_sha256': sha256_file(n1_path)}
        else:
            obligations.append('N1 dual native replay verification')
    else:
        obligations.append('N1 dual native replay verification')

    # 2. Foundations: G2 (n=2), G3 (n=3), G4 (ROOT4 two-pass)
    found_ok = True
    found_summary = {}
    for stage in FOUNDATION_STAGES:
        p = vr / 'foundations' / stage / 'RESULT.json'
        if not p.is_file():
            found_ok = False
            continue
        r = load_json(p)
        if r.get('schema') != 'public-foundation-fresh-execution/1' or r.get('stage') != stage or r.get('full_selected_numerical_stage') is not True:
            found_ok = False
            continue
        chk = r.get('checked', {})
        if stage in ('n2-primary', 'n2-independent') and chk.get('cells') != 70:
            found_ok = False
        elif stage in ('n3-identities', 'n3-full') and chk.get('cells') != 111:
            found_ok = False
        elif stage == 'root4-two-pass':
            if not (chk.get('conditional_physical_target_closed') is True and chk.get('root_bound_exact') == '4097/10000' and chk.get('parents_per_pass') == 260 and chk.get('high_slots_per_pass') == 1300 and chk.get('unresolved_geometry_indices') == []):
                found_ok = False
        found_summary[stage] = 'VERIFIED'
    if found_ok and len(found_summary) == len(FOUNDATION_STAGES):
        verified['foundations_G2_G3_ROOT4'] = {'status': 'VERIFIED', 'stages': found_summary}
    else:
        obligations.append('G2/G3/ROOT4 complete native foundation coverage and integration')

    # 3. Public COUNT 1243-job batch
    count_summary_path = vr / 'count/run-complete-1243/SUMMARY.json'
    count_results_path = vr / 'count/run-complete-1243/RESULTS.jsonl'
    manifest_path = root / 'certificates/count/MANIFEST.json'
    if count_summary_path.is_file() and count_results_path.is_file() and manifest_path.is_file():
        csum = load_json(count_summary_path)
        cman = load_json(manifest_path)['jobs']
        rows = [json.loads(line) for line in count_results_path.read_text(encoding='utf-8').splitlines() if line.strip()]
        seen_ids = set()
        rows_ok = len(rows) == 1243
        for r in rows:
            jid = r.get('job_id')
            if jid not in cman or jid in seen_ids:
                rows_ok = False
                break
            if not (r.get('fresh_native_success') is True and r.get('exit_code') == 0 and r.get('saved_pass_reused') is False and r.get('candidate_sha256') == cman[jid]['candidate']['sha256']):
                rows_ok = False
                break
            seen_ids.add(jid)
        if rows_ok and csum.get('completed_jobs') == 1243 and csum.get('passed_jobs') == 1243 and csum.get('failed_jobs') == 0 and csum.get('all_selected_jobs_passed') is True:
            verified['count_1243'] = {'status': 'VERIFIED', 'passed_jobs': 1243, 'results_sha256': sha256_file(count_results_path)}
        else:
            obligations.append('1243-job public COUNT native verification')
    else:
        obligations.append('1243-job public COUNT native verification')

    # 4. actual20: 49 COUNT jobs + namespace bridge + scalar assembly
    a20_sum_path = vr / 'actual20-counts/SUMMARY.json'
    a20_bridge_path = vr / 'actual20-counts/bridge/RESULT.json'
    a20_scalar_path = vr / 'actual20/scalar/RESULT.json'
    if a20_sum_path.is_file() and a20_bridge_path.is_file() and a20_scalar_path.is_file():
        a20_sum = load_json(a20_sum_path)
        a20_br = load_json(a20_bridge_path)
        a20_sc = load_json(a20_scalar_path)
        br_ok = (a20_br.get('schema') == 'PUBLIC_ACTUAL20_ALL49_MATHEMATICAL_NAMESPACE_V1'
                 and len(a20_br.get('jobs', {})) == 49
                 and a20_br.get('source_manifest_sha256') == 'f9d4bcaecc9bca4d39c0426e278707e0b1afa617198662faf9b3870a1d6fd67d')
        sc_ok = (a20_sc.get('returncode') == 0
                 and a20_sc.get('full_original_reader', {}).get('whole_conditional_contracts_checked') is True
                 and a20_sc.get('full_original_reader', {}).get('conditional_scalar_cases') == 5)
        if a20_sum.get('completed_jobs') == 49 and a20_sum.get('total_jobs') == 49 and br_ok and sc_ok:
            verified['actual20'] = {
                'status': 'VERIFIED',
                'count_jobs_passed': 49,
                'bridge_sha256': sha256_file(a20_bridge_path),
                'scalar_contracts_checked': 5,
            }
        else:
            obligations.append('49 actual20 COUNT jobs and namespace bridge verification')
    else:
        obligations.append('49 actual20 COUNT jobs and namespace bridge verification')

    # 5. finite43-48 (183 tasks + 2 collectors) & tail49 (55 predicates)
    fc_path = vr / 'finite-collectors/collect-all/RESULT.json'
    fc_tail_inputs_path = vr / 'finite-collectors/collect-all/TAIL-TYPED-INPUTS.json'
    tf_path = vr / 'finite-tail/tail-full/RESULT.json'
    if fc_path.is_file() and fc_tail_inputs_path.is_file() and tf_path.is_file():
        fc = load_json(fc_path)
        fc_ti = load_json(fc_tail_inputs_path)
        tf = load_json(tf_path)
        ti_sha = sha256_file(fc_tail_inputs_path)
        fc_ok = (fc.get('schema') == 'public-finite-collectors/1'
                 and fc.get('status') == 'FRESH_NUMERICAL_COLLECTORS_COMPLETED_ANALYTIC_CONTRACTS_EXPLICIT'
                 and len(fc.get('finite_observed_results', {})) == 183
                 and fc.get('whole_tail_typed_inputs_sha256') == ti_sha
                 and len(fc_ti.get('predicates', [])) == 55
                 and bool(fc.get('collector43')) and bool(fc.get('collector44')))
        tf_chk = tf.get('checked', {})
        tf_orig = tf_chk.get('original_full_result', {})
        tf_ok = (tf.get('schema') == 'public-finite-tail-numerical/1'
                 and tf.get('mode') == 'tail-full'
                 and tf_chk.get('complete_tail55') is True
                 and tf_orig.get('all_required_jobs_computed') is True
                 and tf_orig.get('top_level_executions') == 14
                 and tf_orig.get('retained_component_executions') == 41)
        if fc_ok and tf_ok:
            verified['finite43_48_and_tail49'] = {
                'status': 'VERIFIED',
                'finite_tasks_verified': 183,
                'collectors_verified': ['collector43', 'collector44'],
                'tail49_predicates_verified': 55,
                'collectors_result_sha256': sha256_file(fc_path),
                'tail_full_result_sha256': sha256_file(tf_path),
            }
        else:
            obligations.append('finite43--48 numerical replay, two collector joins, and tail49 suite')
    else:
        obligations.append('finite43--48 numerical replay, two collector joins, and tail49 suite')

    # 6. Global 13-role mathematical composition (upper, lower, equality C_* = C_E)
    gp_comp_path = vr / 'global-proofs/COMPLETION.json'
    gp_upper_path = vr / 'global-proofs/upper/PROOF.json'
    gp_lower_path = vr / 'global-proofs/lower/PROOF.json'
    gp_eq_path = vr / 'global-proofs/equality/PROOF.json'
    contract_path = root / 'mathematics/global-contract.json'
    if all(p.is_file() for p in (gp_comp_path, gp_upper_path, gp_lower_path, gp_eq_path, contract_path)):
        gp = load_json(gp_comp_path)
        contract = load_json(contract_path)
        up_sha = sha256_file(gp_upper_path)
        lo_sha = sha256_file(gp_lower_path)
        eq_sha = sha256_file(gp_eq_path)
        contract_roles = [r['role'] for r in contract.get('upper_partition', []) if r.get('closed') is True]
        part = gp.get('exact_positive_integer_partition', {})
        gp_ok = (gp.get('status') == 'GLOBAL_SOURCE_MATHEMATICAL_EQUALITY_COMPLETED'
                 and gp.get('actual_nominal_proof_roles') == EXPECTED_ROLES
                 and contract_roles == EXPECTED_ROLES
                 and part.get('finite_indices') == list(range(1, 49))
                 and part.get('tail_first') == 49
                 and part.get('closed_seam_48_49') is True
                 and gp.get('upper', {}).get('global_upper_issued') is True
                 and gp.get('upper', {}).get('proof_sha256') == up_sha
                 and gp.get('lower', {}).get('proof_sha256') == lo_sha
                 and gp.get('equality', {}).get('global_equality_issued') is True
                 and gp.get('equality', {}).get('proof_sha256') == eq_sha
                 and gp.get('equality', {}).get('statement', {}).get('value') == 'C_E=(3+sqrt(10))/(6*sqrt(2*pi))')
        if gp_ok:
            verified['global_13_role_theorem'] = {
                'status': 'VERIFIED',
                'roles_verified': len(EXPECTED_ROLES),
                'upper_proof_sha256': up_sha,
                'lower_proof_sha256': lo_sha,
                'equality_proof_sha256': eq_sha,
                'target_constant': 'C_E=(3+sqrt(10))/(6*sqrt(2*pi))',
            }
        else:
            obligations.append('all 13 roles, exact same-law parents, independent tail and final global binder')
    else:
        obligations.append('all 13 roles, exact same-law parents, independent tail and final global binder')

    return obligations, verified


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
            alt = root.parent.parent / 'work/public-count-witnesses-public' / pin['path']
            if (candidate.is_file() and candidate.stat().st_size == pin['bytes']) or (alt.is_file() and alt.stat().st_size == pin['bytes']):
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
                            pass
                summary = run / 'SUMMARY.json'
                campaign = {'completed_jobs_observed': len(rows),
                            'failed_jobs_observed': sum(not r.get('fresh_native_success', False) for r in rows),
                            'final_batch_summary_present': summary.is_file(),
                            'live_process_state_checked': False}
                break

    obligations, verified = verify_all_receipts(root)
    full_pass_established = len(obligations) == 0
    phase = ('FULL_PASS_VERIFIED' if full_pass_established else
             'COUNT_BATCH_UNFINISHED' if campaign and not campaign['final_batch_summary_present'] else
             'COUNT_BATCH_FINISHED' if campaign else 'NOT_STARTED_HERE')
    return {
        'generated_at_utc': datetime.now(timezone.utc).isoformat(),
        'source_audit': 'CLOSED',
        'public_verification': phase,
        'full_pass': 'ESTABLISHED' if full_pass_established else 'NOT_ESTABLISHED',
        'status_is_execution_receipt': full_pass_established,
        'unfinished_campaign_may_be_running_or_interrupted': phase == 'COUNT_BATCH_UNFINISHED',
        'count_candidate_data': data,
        'count_campaign_observation': campaign,
        'verified_components': verified,
        'available_paths': available,
        'remaining_full_verification_obligations': obligations,
        'scope': ('All 13 upper-bound roles, the lower approximation, the global equality C_* = C_E, '
                  'and all required numerical execution receipts (N1, G2, G3, ROOT4 two-pass, 1243 COUNT jobs, '
                  '49 actual20 COUNT jobs + bridge, 183 finite43-48 tasks + 2 collectors, and 55 tail49 predicates) '
                  'are verified.' if full_pass_established else
                  'Source audit and partial public native execution are distinct; COUNT alone never establishes the global theorem.'),
    }


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
    modes.add_argument('--finite-collectors', action='store_true',
                       help='fresh 183 finite43-48 tasks, 55 tail49 predicates, and both collectors')
    modes.add_argument('--actual20-counts', action='store_true',
                       help='fresh 49 actual20 COUNT jobs and namespace bridge')
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
    if not (args.counts or args.task or args.n1 or args.foundation or args.finite_tail or args.finite_collectors or args.actual20_counts):
        result = status(root)
        if result['full_pass'] == 'ESTABLISHED':
            result.update(result='FULL_PASS_VERIFIED', exit_code=0)
            emit(result)
            return 0
        result.update(result='INCOMPLETE', reason='Remaining verification obligations exist.')
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
    elif args.finite_collectors:
        command = [sys.executable, '-I', '-B', str(selected('finite_collectors')),
                   'collect-all', '--output', str(output), '--seconds', str(args.timeout),
                   '--timeout', str(args.timeout), '--jobs', str(args.jobs)]
        scope = 'complete finite43--48 numerical parents, tail49 suite, and collector43/collector44 joins'
    elif args.actual20_counts:
        command = [sys.executable, '-I', '-B', str(selected('actual20_counts')),
                   'run-all', '--output', str(output), '--timeout', str(args.timeout)]
        scope = '49 actual20 COUNT jobs and namespace bridge'
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
          'full_pass': status(root)['full_pass'], 'saved_pass_reused': False})
    code = subprocess.call(command)
    full_state = status(root)['full_pass']
    emit({'result': 'REQUESTED_SCOPE_VERIFIED' if code == 0 else 'REQUESTED_SCOPE_FAILED',
          'scope': scope, 'exit_code': code, 'full_pass': full_state})
    return code


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError) as exc:
        emit({'result': 'INCOMPLETE', 'reason': str(exc), 'full_pass': 'NOT_ESTABLISHED'})
        raise SystemExit(2)
