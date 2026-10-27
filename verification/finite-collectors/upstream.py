"""Fresh original finite43--48 / tail49 numerical execution; no private authority."""
from pathlib import Path
from hashlib import sha256
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse, importlib, json, os, platform, signal, subprocess, sys, time, uuid, zipfile
HERE=Path(__file__).resolve().parent
sys.dont_write_bytecode=True

def need(ok,msg):
    if not ok:raise ValueError(msg)

def digest(p):
    h=sha256()
    with Path(p).open('rb')as f:
        while b:=f.read(1048576):h.update(b)
    return h.hexdigest()

def save(p,x):Path(p).write_text(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n',encoding='utf-8')

def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))

def backend(output):
    spec=load(HERE/'SOURCE-MANIFEST.json');pack=HERE/'sources/backend.zip'
    need(digest(pack)==spec['backend_sha256'],'Exact public source backend')
    target=output/'backend';target.mkdir()
    with zipfile.ZipFile(pack)as z:
        for e in z.infolist():
            rel=Path(e.filename);need(not rel.is_absolute() and '..'not in rel.parts and not e.is_dir(),'Contained source member')
            p=target/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(e))
    sys.path.insert(0,str(target/'finite61'));sys.path.insert(0,str(target/'snapshot'))
    return importlib.import_module('finite61_batch'),importlib.import_module('be_replay.tail49')

def runtime():return dict(python=sys.version,executable_sha256=digest(sys.executable),platform=platform.platform(),adapter_sha256=digest(__file__),legacy_HMAC_required=False,hermetic_runtime_claimed=False)

def supervise(command,cwd,log,timeout):
    start=time.monotonic()
    with Path(log).open('xb')as f:
        child=subprocess.Popen(command,cwd=cwd,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,
            start_new_session=os.name!='nt',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name=='nt'else 0)
        try:
            while child.poll() is None:
                need(time.monotonic()-start<timeout,'Fresh numerical task wall limit')
                need(Path(log).stat().st_size<=16*1048576,'Native log limit')
                time.sleep(.1)
        except BaseException:
            if os.name=='nt':subprocess.run(['taskkill','/PID',str(child.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            else:os.killpg(child.pid,signal.SIGKILL)
            child.wait();raise
    if os.name!='nt':
        try:os.killpg(child.pid,0)
        except ProcessLookupError:pass
        else:os.killpg(child.pid,signal.SIGKILL);raise ValueError('Numerical child left a live descendant')
    return dict(returncode=child.returncode,reason='completed',elapsed_seconds=time.monotonic()-start,tree_cleanup_complete=True,
                resource_scope='observed task process; external host qualification separate')

def finite_one(native,task_id,directory,campaign,profile,timeout,rows=None):
    r=native.run(task_id,Path(native.__file__).parent,directory,campaign_id=campaign,
                 runtime_profile_digest=profile,rows=rows,timeout=timeout,supervisor=supervise)
    need(r['task_id']==task_id and r['full_proof_pass']is False,'Exact numerical scope')
    return dict(task_id=task_id,output=str(directory),outcome=r['outcome'],result_sha256=digest(directory/'TASK-COMPLETED.json'))

def tail_source(module,output):
    pack=HERE/'sources'/module.ARCHIVE_NAME
    need(pack.stat().st_size==module.ARCHIVE_BYTES and digest(pack)==module.ARCHIVE_SHA,'Exact whole1401-file original tail source/data')
    return module.prepare(pack,output/'source')

def tail_one(module,task_id,output,timeout):
    source=tail_source(module,output);new,retained=module.source_jobs(source);ids={r['name']:r for r in new}
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0');env.pop('PYTHONOPTIMIZE',None)
    if task_id.startswith('tail.new.'):
        row=ids[task_id.removeprefix('tail.new.')];cwd=source/row['cwd'];cmd=[sys.executable,'-B',*row['argv']]
    elif task_id.startswith('tail.mapping.'):
        maps={'finite_base':('baseline/finite','accept_finite_base.py'),'entry_schedule_mapping':('baseline/entry','validate_schedule.py'),'local_formula_mapping':('baseline/local','check_consolidation.py')}
        cwd0,script=maps[task_id.removeprefix('tail.mapping.')];cwd=source/cwd0;cmd=[sys.executable,'-B',script]
    else:
        cwd=source;cmd=[sys.executable,'-B',str(source/module.RUNNER),'--workspace-root',str(source/'baseline/certificates'),
             '--job-file',str(source/'retained_jobs.json'),'--output',str(output/'components')]
        if task_id!='tail.retained-all':
            name=task_id.removeprefix('tail.retained.');need(name in{r['name']for r in retained},'Exact retained task');cmd+=['--only',name]
    previous=dict(os.environ);os.environ.update(env)
    try:observed=supervise(cmd,cwd,output/'native.log',timeout)
    finally:os.environ.clear();os.environ.update(previous)
    need(observed['returncode']==0,'Actual original numerical checker failed; see native.log')
    module.verify_sources(source)
    if task_id.startswith('tail.retained'):
        meta=module.load(output/'components/metadata.json');expected=retained if task_id=='tail.retained-all'else[r for r in retained if r['name']==name]
        need(meta['status']=='PASS' and meta['selected_jobs']==len(expected) and meta['sources_unchanged']is True and
             meta['input_sha256']==meta['input_sha256_after'] and [r['name']for r in meta['jobs']]==[r['name']for r in expected],'Every selected original retained program and complete source snapshot')
        for actual,want in zip(meta['jobs'],expected):
            need(all(actual[k]==want[k]for k in('name','cwd','argv','source_run')),'Actual retained invocation')
            module.successful(actual,output/'components',actual['name'])
    return dict(task_id=task_id,actual_command=cmd,native_log_sha256=digest(output/'native.log'),source_manifest_sha256=module.MANIFEST_SHA,
                numerical_program_completed=True,complete_tail55=False)

def run(args):
    output=args.output.resolve();need(not output.exists(),'Fresh exclusive output directory')
    output.mkdir(parents=True);before=runtime();save(output/'RUNTIME-BEFORE.json',before)
    native,tail=backend(output);profile=digest(output/'RUNTIME-BEFORE.json');campaign=args.campaign_id or uuid.uuid4().hex
    if args.mode=='tail-full':
        r=tail.run(output/'native',archives=HERE/'sources',download=False,mode='basic',wall_seconds=args.seconds,
                   cpu_seconds=args.seconds,heartbeat_seconds=30,memory_bytes=args.memory_mib*1048576)
        need(r['all_required_jobs_computed']is True and r['top_level_executions']==14 and r['retained_component_executions']==41,'Whole original55 execution predicates and full output reader')
        checked=dict(numerical_predicates_completed=True,original_full_result=r,complete_tail55=True)
    elif args.mode=='finite-all':
        need(1<=args.jobs<=64,'Bounded worker count');deadline=time.monotonic()+args.seconds;data=native.manifest();results=[];rows={}
        def one(row):
            remaining=int(deadline-time.monotonic());need(remaining>0,'Global fresh-run deadline')
            task=output/'tasks'/row['task_id'];r=finite_one(native,row['task_id'],task,campaign,profile,min(args.timeout,remaining),rows if Path(row.get('script','')).name=='bind_low42.py'else None)
            print('COMPLETED '+row['task_id'],flush=True);return r
        with ThreadPoolExecutor(max_workers=args.jobs)as pool:
            for r in pool.map(one,data['low_rows']):results.append(r);rows[r['task_id']]=r['output']
        save(output/'LOW-ROW-MAP.json',rows)
        with ThreadPoolExecutor(max_workers=args.jobs)as pool:
            for r in pool.map(one,data['actions']):results.append(r)
        need(len(results)==183,'All152 fresh LOW producers and31 whole native acceptors')
        checked=dict(numerical_tasks_completed=183,results=results,collectors_completed=False,
                     remaining_collectors=data['collectors'],all_law_finite43_48=False)
    elif args.task_id.startswith('tail.'):
        checked=tail_one(tail,args.task_id,output/'task',args.timeout)
    else:
        rowmap=load(args.rows)if args.rows else None
        checked=finite_one(native,args.task_id,output/'task',campaign,profile,args.timeout,rowmap)
    after=runtime();save(output/'RUNTIME-AFTER.json',after);need(before==after,'Observed runtime/adapter unchanged')
    result=dict(schema='public-finite-tail-numerical/1',mode=args.mode,checked=checked,full_pass=False,
                current_execution_authentication='local observed process; external qualification remains separate',all_law_theorem_verified=False)
    save(output/'RESULT.json',result);return result

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('mode',choices=['list','run','finite-all','tail-full']);ap.add_argument('--task-id');ap.add_argument('--output',type=Path)
    ap.add_argument('--rows',type=Path);ap.add_argument('--campaign-id');ap.add_argument('--timeout',type=int,default=14400);ap.add_argument('--seconds',type=int,default=64800);ap.add_argument('--memory-mib',type=int,default=8192);ap.add_argument('--jobs',type=int,default=1)
    a=ap.parse_args()
    if a.mode=='list':print(json.dumps(load(HERE/'TASKS.json'),sort_keys=True));return
    need(a.output is not None and 1<=a.timeout<=82800 and 1<=a.seconds<=64800,'Explicit output and bounded time')
    if a.mode=='run':need(a.task_id in{r['task_id']for r in load(HERE/'TASKS.json')['tasks']if r.get('runnable')},'One declared runnable task')
    run(a);print(json.dumps(dict(completed=True,result=str(a.output.resolve()/'RESULT.json'),full_pass=False)))

if __name__=='__main__':main()
