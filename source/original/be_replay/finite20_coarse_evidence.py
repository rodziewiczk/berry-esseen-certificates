"""Pure readback of the internal original five-call coarse actual20 transaction."""
from __future__ import annotations
import math
from hashlib import sha256
from pathlib import Path,PurePosixPath,PureWindowsPath
import re
from . import finite20_coarse_sources as src
from .finite1039_count_evidence import same,mapped,terminal,inventory

SCOPE='ORIGINAL_COARSE_ACTUAL20_FIVE_CALL_BASIC_COMPONENT_V1'
OBSERVED='OBSERVED_COARSE_ACTUAL20_FIVE_CALL_COMPONENT_V1'
COMPLETED='COMPLETED_COARSE_ACTUAL20_FIVE_CALL_COMPONENT_V1'
CPU_SECONDS,WALL_SECONDS,MEMORY_BYTES=82800,82800,2048*src.MIB
FLAGS=('native_arithmetic_accepted','full_notebook58H_completed','actual20_sharp_verified',
       'predecessor_verified','owncap_verified','full_resource_count_join_verified','all_index_conclusion_verified')


def implementation():
    names=('finite20_coarse.py','finite20_coarse_sources.py','finite20_coarse_evidence.py',
           'finite1039_sources.py','finite1039_count_evidence.py','linux_supervisor.py','colab_batch.py')
    return {n:src.digest(src.ROOT/'be_replay'/n)for n in names}|dict(source_plan_sha256=src.PLAN_SHA256)


def original_path(request,relative):
    root=request['original_task_root'];cls=PureWindowsPath if re.match(r'^[A-Za-z]:',root)else PurePosixPath
    src.need(cls(root).is_absolute(),'One absolute original coarse task root');return str(cls(root)/'capsule'/relative)


def action_cwd(action):
    src.need(action in src.ACTIONS,'One fixed original action');return src.NATIVE if action.endswith('_construct')else src.AUDIT


def command(action,python):
    src.need(action in src.ACTIONS and type(python)is str and bool(python),'Original Python action')
    if action.endswith('_construct'):return [python,'-B','pilot.py',action[:2].upper()]
    return [python,'-B','-S','prepare.py']if action=='prepare'else[python,'-B','-S','replay.py',action[:2].upper()]


def finite(v):src.need(type(v)in(int,float)and math.isfinite(v)and v>=0,'Typed finite nonnegative execution duration');return v


def transport(task,request,action,observed,report):
    task=Path(task);directory=task/'executions'/action;root=request['original_task_root'];cwd=task/'capsule'/action_cwd(action)
    src.need(same(src.read(directory/'supervisor-result.json'),observed)
             and observed.get('status')=='completed'and type(observed.get('returncode'))is int and observed['returncode']==0
             and observed.get('reason')is None and observed.get('mode')=='untrusted_search'and observed.get('proof_accepted')is False
             and type(observed.get('sample_count'))is int and observed['sample_count']>0,'Actual stopped successful BASIC execution')
    for k in('elapsed_seconds','maximum_sampled_group_RSS_bytes','maximum_sampled_group_CPU_seconds'):finite(observed[k])
    launch=src.read(directory/'launch.json');outputs=src.output_paths(action)
    fields={'argv','cwd','output_dir','mode','wall_seconds','cpu_seconds','memory_bytes','checkpoint_paths',
            'disk_bytes','log_bytes','sample_seconds','heartbeat_seconds'}
    src.need(set(launch)==fields and same(launch['argv'],command(action,report['python_executable']))
             and mapped(task,launch['cwd'],root)==cwd and mapped(task,launch['output_dir'],root)==directory
             and launch['mode']=='untrusted_search'and type(launch['cpu_seconds'])is int and launch['cpu_seconds']==CPU_SECONDS
             and type(launch['memory_bytes'])is int and launch['memory_bytes']==MEMORY_BYTES
             and type(launch['wall_seconds'])in(int,float)and launch['wall_seconds']==WALL_SECONDS
             and type(launch['disk_bytes'])is int and launch['disk_bytes']==512*src.MIB
             and type(launch['log_bytes'])is int and launch['log_bytes']==16*src.MIB
             and launch['sample_seconds']==.2 and launch['heartbeat_seconds']==20
             and type(launch['checkpoint_paths'])is list
             and [mapped(task,v,root)for v in launch['checkpoint_paths']]==[task/'capsule'/n for n in outputs],
             'Literal original command/cwd/output requests and complete resource policy')
    scope=dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,
        external_wall_seconds=float(WALL_SECONDS),per_process_RLIMIT_AS_bytes=MEMORY_BYTES,
        per_process_RLIMIT_CPU_seconds=CPU_SECONDS,aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,
        sampled_group_RSS_limit_bytes=MEMORY_BYTES,sampled_group_CPU_limit_seconds=CPU_SECONDS,
        sampled_file_limit_bytes=512*src.MIB,sampled_log_limit_bytes=16*src.MIB,
        descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)
    src.need(same(observed['guard_scope'],scope),'Honest full BASIC scope, without native proof acceptance')
    captures={}
    for kind in('stdout','stderr'):
        p=mapped(task,observed[kind+'_path'],root)
        src.need(p==directory/(kind+'.txt')and p.is_file()and p.stat().st_size<=16*src.MIB
                 and src.digest(p)==observed[kind+'_sha256'],'Actual whole captured '+kind);captures[kind]=p
    src.need(captures['stderr'].stat().st_size==0,'Actual successful stderr is empty')
    copied=observed['checkpoints'];src.need(type(copied)is list and len(copied)==len(outputs),'Every whole original output captured')
    for row,name in zip(copied,outputs):
        p=task/'capsule'/name;q=directory/'checkpoints'/p.relative_to(cwd)
        src.need(set(row)=={'source_path','exists','trusted_certificate','path','bytes','sha256'}
                 and row['exists']is True and row['trusted_certificate']is False
                 and mapped(task,row['source_path'],root)==p and mapped(task,row['path'],root)==q
                 and p.is_file()and q.is_file()and type(row['bytes'])is int
                 and row['bytes']==p.stat().st_size==q.stat().st_size
                 and row['sha256']==src.digest(p)==src.digest(q),'Actual cwd-relative stopped whole-output copy')
    return captures['stdout'].read_text('utf-8')


def candidate(task,band):
    d=src.plan();cfg=d['cases'][band];c=Path(task)/'capsule';path=c/src.NATIVE/(band+'_RESULT.json');obj=src.read(path,limit=128*src.MIB)
    src.need(set(obj)==set(cfg['candidate_fields'])and obj['status']=='EXACT_SHARP20_CONDITIONAL_INITIAL_CANDIDATE_READY_FOR_RESOURCE_REVIEW'
             and type(obj['n'])is int and obj['n']==20 and obj['band']==band and obj['K']=='0'and obj['target']=='CE'
             and obj['q']==cfg['q']and obj['owncap']==cfg['owncap']and same(obj['rho_interval'],cfg['rho'])
             and obj['failure']is None and len(obj['stages'])==8 and len(obj['export']['panels'])==100
             and obj['stages'][0]['input_raw']is None and obj['stages'][0]['input_D']is None
             and same(obj['files_sha256'],d['source_graph']),'Whole complete original unseeded coarse INITIAL candidate')
    times=[]
    def without_times(value,path=()):
        if type(value)is dict:
            out={}
            for k,v in value.items():
                if k=='seconds'or path==()and k=='initial_seconds':finite(v);times.append(list(path+(k,)))
                else:out[k]=without_times(v,path+(k,))
            return out
        if type(value)is list:return[without_times(v,path+(i,))for i,v in enumerate(value)]
        return value
    facts=without_times(obj)
    src.need(sorted(times,key=lambda p:src.dump(p))==sorted(cfg['candidate_timing_paths'],key=lambda p:src.dump(p))
             and sha256(src.dump(facts)).hexdigest()==cfg['candidate_math_sha256'],
             'Every original mathematical candidate field matches, excluding only declared runtime durations')
    return obj


def capture_metadata(task,request,band,observed,report):
    action=band.lower()+'_construct';c=Path(task)/'capsule';path=c/src.NATIVE/(band+'_RESULT.json')
    obj=candidate(task,band);directory=Path(task)/'executions'/action
    stdout=(directory/'stdout.txt').read_text('utf-8')
    src.need(stdout.splitlines()[-1]==obj['status']+' '+band+' '+src.digest(path),'Actual completed original constructor terminal identity')
    return dict(capture_kind='GENUINE_STOPPED_OUTER_PROCESS_V1',command=command(action,report['python_executable']),
        cwd=original_path(request,src.NATIVE),input_sha256=request['sources'],python=report['python_version'],
        platform=report['platform'],returncode=0,elapsed_seconds=observed['elapsed_seconds'],changed_inputs=[],
        stdout_sha256=src.digest(directory/'stdout.txt'),stderr_sha256=src.digest(directory/'stderr.txt'),
        **{band+'_RESULT.json_sha256':src.digest(path)})


def bridge_record(task,request,band,observed,report):
    action=band.lower()+'_construct';directory=Path(task)/'executions'/action
    return dict(schema='ACTUAL20_CONSTRUCTOR_STOPPED_OUTER_CAPTURE_BRIDGE_V1',action=action,band=band,n=20,
        original_task_root=request['original_task_root'],source_plan_sha256=src.PLAN_SHA256,
        sources_sha256=request['sources'],launch_sha256=src.digest(directory/'launch.json'),
        supervisor_result_sha256=src.digest(directory/'supervisor-result.json'),
        metadata_sha256=src.digest(Path(task)/'capsule'/src.capture_directory(band)/'metadata.json'),
        whole_result_sha256=src.digest(Path(task)/'capsule'/src.NATIVE/(band+'_RESULT.json')),
        historical_capture_relabelled=False,native_arithmetic_accepted=False,**{f:False for f in FLAGS if f!='native_arithmetic_accepted'})


def verify_capture(task,request,band,observed,report):
    c=Path(task)/'capsule';directory=c/src.capture_directory(band);meta=capture_metadata(task,request,band,observed,report)
    src.need(same(src.read(directory/'metadata.json'),meta),'Truthful current outer capture metadata, not a fabricated child')
    for kind in('stdout','stderr'):
        src.need((directory/(kind+'.txt')).read_bytes()==(Path(task)/'executions'/(band.lower()+'_construct')/(kind+'.txt')).read_bytes(),
                 'Whole original outer stream preserved in the consumed capture')
    src.need(same(src.read(directory/'CAPTURE_BRIDGE.json'),bridge_record(task,request,band,observed,report)),
             'Explicit current whole-launch/source/result capture bridge')


def expected_prepared(task):
    c=Path(task)/'capsule';d=src.plan();graph=dict(d['source_graph']);candidates={}
    for name in d['copied_modules']:graph[src.AUDIT+'/engine/'+name]=d['source_graph'][src.NATIVE+'/'+name]
    for band in('B0','B1'):
        name=src.NATIVE+'/'+band+'_RESULT.json';capture=src.capture_directory(band)
        candidates[band]=dict(path=name,sha256=src.digest(c/name),capture=capture,metadata_sha256=src.digest(c/capture/'metadata.json'))
        graph[name]=src.digest(c/name)
        for leaf in('metadata.json','stdout.txt','stderr.txt'):graph[capture+'/'+leaf]=src.digest(c/capture/leaf)
    for leaf in('prepare.py','replay.py','PROOF.txt'):graph[src.AUDIT+'/'+leaf]=src.digest(c/src.AUDIT/leaf)
    return dict(status='PREPARED_IDENTICAL_INITIAL_WORK_COPIES_NO_NUMERICAL_EXECUTION',candidates=candidates,
                copied_modules=d['copied_modules'],files_sha256=graph)


def validate_run(task,report):
    task=Path(task);request=src.verify_job(task);c=task/'capsule'
    src.need(report['schema']==OBSERVED and report['scope']==SCOPE and same(report['implementation'],implementation())
             and report['original_task_root']==request['original_task_root']
             and report['conditional_coarse_initial_arithmetic_completed']is False and all(report[f]is False for f in FLAGS)
             and [x['action']for x in report['actions']]==list(src.ACTIONS),'Exact five original calls and observed-false epoch')
    stdout={row['action']:transport(task,request,row['action'],row['observed'],report)for row in report['actions']}
    for i,band in enumerate(('B0','B1')):verify_capture(task,request,band,report['actions'][i]['observed'],report)
    prepared=src.read(c/src.AUDIT/'PREPARED.json');src.need(same(prepared,expected_prepared(task)),
        'Unchanged original preparation generated the complete current candidate/capture/source graph')
    src.need(same(terminal(stdout['prepare']),{k:v for k,v in prepared.items()if k!='files_sha256'}),'Whole captured original preparation terminal')
    receipts={}
    for band in('B0','B1'):
        obj=candidate(task,band);cfg=src.plan()['cases'][band];p=c/src.AUDIT/(band+'_REPLAY_CHECKED.json');r=src.read(p,limit=128*src.MIB)
        graph=dict(prepared['files_sha256']);graph[src.AUDIT+'/PREPARED.json']=src.digest(c/src.AUDIT/'PREPARED.json')
        src.need(set(r)==set(cfg['replay_fields'])and r['status']==cfg['replay_status']and type(r['n'])is int and r['n']==20
                 and r['band']==band and r['K']=='0'and r['target']=='CE'and same(r['rho'],cfg['rho'])
                 and type(r['full_signed_covers'])is int and r['full_signed_covers']==9
                 and type(r['signed_cells'])is int and r['signed_cells']==23328
                 and type(r['probability_panels'])is int and r['probability_panels']==100
                 and type(r['malformed_controls'])is int and r['malformed_controls']==14 and r['cutoff20_proved']is False
                 and r['candidate_sha256']==src.digest(c/src.NATIVE/(band+'_RESULT.json'))and same(r['files_sha256'],graph)
                 and same(r['profile'],obj['profile'])and same(r['final_invariants'],obj['final_invariants'])
                 and same(terminal(stdout[band.lower()+'_replay']),{k:v for k,v in r.items()if k!='files_sha256'}),
                 'Complete original nine-cover semantic replay and whole captured receipt')
        facts={k:v for k,v in r.items()if k not in('files_sha256','candidate_sha256')}
        src.need(sha256(src.dump(facts)).hexdigest()==cfg['replay_math_sha256'],'All original semantic facts retained under current genuine captures')
        receipts[band]=dict(candidate_sha256=src.digest(c/src.NATIVE/(band+'_RESULT.json')),receipt_sha256=src.digest(p),
            source_graph_sha256=sha256(src.dump(graph)).hexdigest(),rho=cfg['rho'],q=cfg['q'],owncap=cfg['owncap'])
    found={p.relative_to(c).as_posix()for p in c.rglob('*')if p.is_file()}
    src.need(found==set(request['sources'])|src.allowed_outputs(),'Exactly all original/current declared capsule files')
    return dict(schema='CONDITIONAL_COARSE_ACTUAL20_INITIAL_FACTS_V1',n=20,bands=receipts,
        original_actions=5,total_full_signed_covers=36,total_signed_cells=93312,full_replay_controls=28,
        source_plan_sha256=src.PLAN_SHA256,conditional_premises=['Same attained unrestricted positive closed contrary20 witness',
        'Licensed same-witness contact allowance<=21/100','Independently licensed actual20 owncap21/50',
        'Retained analytic support/INITIAL/interval kernel implications'],**{f:False for f in FLAGS})


def validate_completed(task, *,original_task_root=None):
    task=Path(task);request=src.verify_job(task);report=src.read(task/'STAGE_OBSERVED.json');complete=src.read(task/'STAGE_COMPLETED.json',limit=32*src.MIB)
    src.need(original_task_root is None or str(original_task_root)==request['original_task_root'],'One explicit original task context')
    summary=validate_run(task,report)
    src.need(complete['schema']==COMPLETED and complete['scope']==SCOPE and same(complete['implementation'],report['implementation'])
             and complete['observed_sha256']==src.digest(task/'STAGE_OBSERVED.json')and same(complete['summary'],summary)
             and same(complete['artifacts'],inventory(task))and complete['conditional_coarse_initial_arithmetic_completed']is True
             and all(complete[f]is False for f in FLAGS),'Whole complete coarse transaction, without full58H promotion')
    return dict(schema='REVALIDATED_COARSE_ACTUAL20_FIVE_CALL_COMPONENT_V1',summary=summary,
        stage_result_sha256=src.digest(task/'STAGE_COMPLETED.json'),source_plan_sha256=src.PLAN_SHA256,
        original_task_root=request['original_task_root'],conditional_coarse_initial_arithmetic_completed=True,**{f:False for f in FLAGS})
