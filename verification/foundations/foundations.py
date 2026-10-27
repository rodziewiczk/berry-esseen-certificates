"""Key-free fresh execution of the unchanged small-index and ROOT4 programs."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction
import argparse, importlib, json, os, platform, re, runpy, shutil, signal, subprocess, sys, time, zipfile

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(HERE))
SMALL_MANIFEST = '8ca0f5c30991b50c61fc998c7c873873c2ac7d2bde6611123ce74651e1a3c26b'
ROOT4_ZIP = 'edc8c644b22440b6a575a3417df39ae286f2ed9120892f9a29de3ff6d050bfe2'
STAGES = ('n2-scalars','n2-primary','n2-independent','n3-scalars','n3-identities','n3-full','n2-cell','root4-prepare','root4-two-pass')

def need(ok, message):
    if not ok: raise ValueError(message)

def digest(path):
    h=sha256()
    with Path(path).open('rb') as f:
        while b:=f.read(1024*1024): h.update(b)
    return h.hexdigest()

def write(path, value):
    Path(path).write_text(json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n',encoding='utf-8')

def inventory(root):
    return {p.relative_to(root).as_posix():dict(sha256=digest(p),bytes=p.stat().st_size)
            for p in sorted(Path(root).rglob('*')) if p.is_file()}

def unpack(name, target):
    manifest=json.loads((HERE/'MANIFEST.json').read_bytes()); spec=manifest['packages'][name]
    pack=HERE/spec['file'];need(digest(pack)==spec['sha256'],'Changed source package')
    with zipfile.ZipFile(pack) as z:
        need(len(z.namelist())==len(set(z.namelist()))==spec['members'],'Exact whole source inventory')
        for entry in z.infolist():
            rel=Path(entry.filename)
            need(not rel.is_absolute() and '..' not in rel.parts and not entry.is_dir(),'Contained regular source member')
            out=target/rel;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(z.read(entry))
    if name=='small':
        need(digest(target/'MANIFEST.json')==SMALL_MANIFEST,'Exact original189-source/witness manifest')
        native=json.loads((target/'MANIFEST.json').read_bytes())
        need(native['certificate_counts']=={'n2':70,'n3':111} and len(native['files'])==189,'Whole original70+111')
        actual=inventory(target)
        expected={r['path']:dict(bytes=r['bytes'],sha256=r['sha256'])for r in native['files']}
        need({k:v for k,v in actual.items()if k!='MANIFEST.json'}==expected,'Every original source and rational witness byte')
    else: need(digest(pack)==ROOT4_ZIP,'Exact original99-member ROOT4 source bundle')

def profile(cxx=False):
    result=dict(schema='public-current-foundation-runtime/1',python=sys.version,
                executable_sha256=digest(sys.executable),platform=platform.platform(),
                source_adapter_sha256=digest(__file__),scientific_packages_required=False,
                output_validator_sha256=digest(HERE/'validators.py'),source_manifest_sha256=digest(HERE/'MANIFEST.json'),
                legacy_authentication_required=False,hermetic_runtime_claimed=False)
    if cxx:
        compiler=shutil.which('g++');need(compiler is not None,'n3-full requires g++ and Boost headers on PATH')
        r=subprocess.run([compiler,'--version'],capture_output=True,text=True,check=True)
        result['compiler']=dict(executable_sha256=digest(compiler),version=r.stdout,
                                original_argv=['g++','-O2','-std=c++17','check_cube.cpp','-o','FRESH_BINARY'])
    return result

def _native(stage, source, task):
    """Subprocess entry: original functions/mains; no acceptance from old logs."""
    sys.dont_write_bytecode=True
    n=2 if stage.startswith('n2') else 3
    script=source/f'n{n}'/({'n2-independent':'independent_integer_check.py','n3-identities':'audit_initial_polynomials.py'}.get(stage,'tensor_certificate.py'if n==2 else'verify.py'))
    sys.path.insert(0,str(script.parent)); processes=[]; binary_hash=None
    def hook(event,args):
        nonlocal binary_hash
        if event!='subprocess.Popen':return
        cmd=args[1];need(stage=='n3-full' and isinstance(cmd,list),'Unexpected native subprocess')
        if cmd[0]=='g++':
            need(len(cmd)==6 and cmd[1:3]==['-O2','-std=c++17'] and Path(cmd[3])==script.parent/'check_cube.cpp' and cmd[4]=='-o','Original native compile argv')
        else:
            exe=Path(cmd[0]).resolve()
            if os.name=='nt' and not exe.is_file() and Path(str(exe)+'.exe').is_file():exe=Path(str(exe)+'.exe')
            need(exe.is_relative_to(task/'tmp') and exe.is_file(),'Fresh task-owned C++ kernel')
            h=digest(exe);need(binary_hash in(None,h),'Same fresh C++ kernel for every cell');binary_hash=h
            kept=task/'compiled-kernel';
            if not kept.exists():shutil.copyfile(exe,kept)
        processes.append(dict(argv=list(map(str,cmd)),binary_sha256=None if cmd[0]=='g++'else binary_hash))
    sys.addaudithook(hook)
    if stage in('n2-scalars','n3-scalars','n2-cell'):
        ns=runpy.run_path(str(script),run_name='public_original_function')
        if stage=='n2-cell':
            nodes,moments=ns['verify_one'](source/'n2/certificate/000.json',0)
            print('PUBLIC_ORIGINAL_COMPLETE_N2_CELL_000',nodes,moments,flush=True)
        else:
            ns['verify_reductions'if n==2 else'analytic_constants']()
            print('SOURCE_SCALARS_COMPLETED '+stage,flush=True)
    else:
        sys.argv=[str(script)]+(['check']if stage=='n2-primary'else[])
        runpy.run_path(str(script),run_name='__main__')
    write(task/'NATIVE-PROCESSES.json',dict(processes=processes,binary_sha256=binary_hash))

def run(stage, output, timeout=54000):
    need(__debug__ and not sys.flags.optimize,'Unoptimized Python required')
    output=Path(output).resolve();need(not output.exists(),'Fresh output directory required')
    output.mkdir(parents=True);start=time.monotonic();before_profile=profile(stage=='n3-full')
    write(output/'RUNTIME-BEFORE.json',before_profile)
    if stage.startswith('root4'):
        bundle=output/'bundle';unpack('root4',bundle);original=inventory(bundle)
        sys.path.insert(0,str(bundle/'snapshot'));module=importlib.import_module('be_replay.root4')
        need(Path(module.__file__).resolve()==bundle/'snapshot/be_replay/root4.py','Own exact bundled controller')
        if stage=='root4-prepare':
            epoch=module.prepare(output/'capsule');module.verify_capsule(output/'capsule')
            checked=dict(source_epoch=epoch,commands=[module.command(output/'capsule',s)for s in('produce','replay')],native_computation_executed=False)
        else:
            need(sys.platform=='linux','root4-two-pass uses the existing reviewed Linux resource-only epoch; no Windows-monitor bypass')
            result=module.run(output/'native',wall_seconds=timeout,heartbeat_seconds=60)
            from validators import validate_root4
            checked=validate_root4(module,output/'native',result)
            need(checked['conditional_physical_target_closed'] is True,'Completed UNKNOWN is not a proof')
        need(inventory(bundle)==original,'Original99 files unchanged')
    else:
        source=output/'source';unpack('small',source);original=inventory(source)
        tmp=output/'tmp';tmp.mkdir();env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUNBUFFERED='1',TMPDIR=str(tmp),TMP=str(tmp),TEMP=str(tmp))
        cmd=[sys.executable,'-I','-B',str(Path(__file__).resolve()),'_native',stage,str(source),str(output)]
        with (output/'native.log').open('wb')as f:
            child=subprocess.Popen(cmd,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,env=env,
                                   start_new_session=os.name!='nt',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name=='nt'else 0)
            try:code=child.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                if os.name=='nt':subprocess.run(['taskkill','/PID',str(child.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                else:os.killpg(child.pid,signal.SIGKILL)
                child.wait();raise
        need(code==0,'Original native checker failed; see native.log')
        text=(output/'native.log').read_text(encoding='utf-8')
        from validators import validate_output
        if stage=='n2-cell':
            need(re.search(r'^PUBLIC_ORIGINAL_COMPLETE_N2_CELL_000 \d+ \d+$',text,re.M) is not None,'Whole single-cell function completed')
            checked=dict(cells=1,full_n2=False)
        else:
            witnesses={p.name:dict(sha256=digest(p))for p in(source/f'n{stage[1]}/certificate').glob('*.json')}
            checked=validate_output(stage,text,witnesses)
        trace=json.loads((output/'NATIVE-PROCESSES.json').read_bytes())
        if stage=='n3-full':
            ps=trace['processes'];need(len(ps)==112 and sum(p['argv'][0]=='g++'for p in ps)==1 and trace['binary_sha256'],'One actual fresh compile and111 original C++ checks')
        need(inventory(source)==original,'All original source/witness files unchanged')
        checked['native_log_sha256']=digest(output/'native.log')
    after_profile=profile(stage=='n3-full');write(output/'RUNTIME-AFTER.json',after_profile)
    need(after_profile==before_profile,'Observed interpreter/compiler profile unchanged')
    result=dict(schema='public-foundation-fresh-execution/1',stage=stage,checked=checked,
                elapsed_seconds=time.monotonic()-start,runtime_sha256=digest(output/'RUNTIME-BEFORE.json'),
                full_selected_numerical_stage=stage not in('n2-cell','root4-prepare'),
                all_law_theorem_verified=False,full_pass=False)
    write(output/'RESULT.json',result);return result

def main():
    if len(sys.argv)>1 and sys.argv[1]=='_native':
        need(len(sys.argv)==5 and sys.argv[2]in STAGES,'Exact internal native invocation')
        _native(sys.argv[2],Path(sys.argv[3]).resolve(),Path(sys.argv[4]).resolve());return
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('stage',choices=STAGES);ap.add_argument('--output',required=True,type=Path);ap.add_argument('--timeout',type=int,default=54000)
    a=ap.parse_args();need(1<=a.timeout<=86400,'Explicit wall timeout up to24h')
    result=run(a.stage,a.output,a.timeout)
    print(json.dumps(dict(stage=result['stage'],completed=True,result=str(a.output.resolve()/'RESULT.json'),
                         full_selected_numerical_stage=result['full_selected_numerical_stage'],full_pass=False),sort_keys=True))

if __name__=='__main__':main()
