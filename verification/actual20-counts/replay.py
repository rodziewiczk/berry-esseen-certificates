"""Fixed actual20 COUNT execution and explicit mathematical namespace bridge."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,math,os,platform,shutil,subprocess,sys,time,zipfile
HERE=Path(__file__).resolve().parent
MANIFEST_SHA256='f9d4bcaecc9bca4d39c0426e278707e0b1afa617198662faf9b3870a1d6fd67d'
def need(ok,message):
 if not ok:raise ValueError(message)
def sha(path):
 with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def read(path):
 def unique(items):
  result={}
  for k,v in items:need(k not in result,'Duplicate JSON key');result[k]=v
  return result
 return json.loads(Path(path).read_bytes(),object_pairs_hook=unique)
def write(path,value):Path(path).write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
def parts(name):
 p=PurePosixPath(name)
 need(type(name)is str and p.parts and not p.is_absolute() and p.as_posix()==name and all(x not in('.','..') and ':' not in x and '\\' not in x and '\0' not in x for x in p.parts),'Contained canonical relative path')
 return p.parts
def manifest():
 need(sha(HERE/'SOURCE-MANIFEST.json')==MANIFEST_SHA256,'Pinned entire source manifest')
 m=read(HERE/'SOURCE-MANIFEST.json')
 for name,r in m['archives'].items():
  p=HERE.joinpath(*parts(name));need(not p.is_symlink() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'Complete pinned source archive')
 need(sha(HERE/'JOBS.json')==m['jobs_sha256'],'Complete fixed49 registry')
 return m
def materialize(archive,target,selected):
 need(not target.exists(),'Fresh exclusive materialization');target.mkdir(parents=True)
 with zipfile.ZipFile(HERE/archive) as z:
  need(len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(selected),'Closed exact archive inventory')
  for name,r in selected.items():
   raw=z.read(name);need(len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256'],'Whole original source byte')
   p=target.joinpath(*parts(name));p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
def load_runtime(target,m):
 materialize('runtime.zip',target,m['runtime_files']);sys.path.insert(0,str(target))
 from be_replay import finite1039_sources as src,finite1039_count_evidence as ce
 return src,ce
def rows(src):
 selected=[r for r in src.jobs('n20_24') if r['n']==20]
 need(len(selected)==49 and selected==read(HERE/'JOBS.json')['jobs'],'Every exact original n20 job, including every closed piece')
 return {r['job_id']:r for r in selected}
def inventory(root):
 result={}
 for p in sorted(root.rglob('*')):
  need(not p.is_symlink() and not(getattr(p,'is_junction',lambda:False)()),'Ordinary output inventory')
  if p.is_file():result[p.relative_to(root).as_posix()]=dict(bytes=p.stat().st_size,sha256=sha(p))
 return result
def mathematical_summary(task,row,ce):
 """Entire unchanged original reader; checkpoint describes an actual copied file."""
 output=task/'capsule'/ce.src.output_relative(row);capture=task/'execution/checkpoints'/row['output']
 observed=dict(checkpoints=[dict(source_path=str(output),exists=True,trusted_certificate=False,path=str(capture),bytes=capture.stat().st_size,sha256=sha(capture))])
 # summarize's mathematical checks are independent of platform supervisor policy.
 return ce.summarize(task,row,(task/'stdout.txt').read_text('utf-8'),observed,str(task),python_executable=sys.executable,python_version=sys.version)
def replay(out,row,src,ce,timeout):
 cache=out/'source-cache';m=manifest();materialize('count-sources.zip',cache,m['source_files'])
 task=out/'task';src.prepare_job(row['job_id'],cache,task)
 command=[sys.executable,'-B','-S',str(task/'capsule'/row['directory']/row['script']),*row['arguments']]
 cwd=task/'capsule'/row['directory'];launch=dict(argv=command,cwd=str(cwd),python_version=sys.version,platform=platform.platform(),timeout_seconds=timeout,guard_scope='DIRECT_SUBPROCESS_WALL_TIMEOUT_ONLY',kernel_cpu_or_memory_limit_claimed=False,historical_launch_claimed=False)
 write(task/'launch.json',launch);started=time.monotonic()
 with (task/'stdout.txt').open('wb') as stdout,(task/'stderr.txt').open('wb') as stderr:
  child=subprocess.Popen(command,cwd=cwd,stdout=stdout,stderr=stderr)
  try:code=child.wait(timeout=timeout)
  except subprocess.TimeoutExpired:
   child.kill();child.wait();write(task/'PROCESS.json',dict(returncode=child.returncode,timed_out=True,elapsed_seconds=time.monotonic()-started,full_pass=False));raise ValueError('Fresh acceptor exceeded explicit wall timeout')
 write(task/'PROCESS.json',dict(returncode=code,timed_out=False,elapsed_seconds=time.monotonic()-started,full_pass=False))
 need(code==0 and (task/'stderr.txt').stat().st_size==0,'Actual original acceptor exited0 with empty stderr')
 src.verify_job(task,row)
 output=task/'capsule'/src.output_relative(row)
 capture=task/'execution/checkpoints'/row['output'];capture.parent.mkdir(parents=True);shutil.copyfile(output,capture)
 summary=mathematical_summary(task,row,ce)
 result=dict(schema='PUBLIC_ACTUAL20_COUNT_MATH_V1',job_id=row['job_id'],source_manifest_sha256=MANIFEST_SHA256,summary=summary,artifacts=inventory(task),fresh_original_acceptor_executed=True,original_native_stage_protocol=False,parent_acquisitions_verified=False,full_pass=False)
 write(out/'RESULT.json',result);return result
def validate_portable(out,row,src,ce):
 out=Path(out).resolve();result=read(out/'RESULT.json');task=out/'task'
 need(result['schema']=='PUBLIC_ACTUAL20_COUNT_MATH_V1' and result['job_id']==row['job_id'] and result['source_manifest_sha256']==MANIFEST_SHA256 and result['fresh_original_acceptor_executed']is True and result['original_native_stage_protocol']is False and result['parent_acquisitions_verified']is False and result['full_pass']is False,'Explicit public mathematical evidence epoch')
 need(ce.same(result['artifacts'],inventory(task)),'Complete actual source/output/capture/launch inventory')
 src.verify_job(task,row);launch=read(task/'launch.json');process=read(task/'PROCESS.json')
 command=[sys.executable,'-B','-S',str(task/'capsule'/row['directory']/row['script']),*row['arguments']]
 need(launch['argv']==command and launch['cwd']==str(task/'capsule'/row['directory']) and launch['python_version']==sys.version and launch['guard_scope']=='DIRECT_SUBPROCESS_WALL_TIMEOUT_ONLY' and launch['kernel_cpu_or_memory_limit_claimed']is False and launch['historical_launch_claimed']is False,'Exact honestly observed fresh portable command/context')
 need(type(process['returncode'])is int and process['returncode']==0 and process['timed_out']is False and type(process['elapsed_seconds'])in(int,float) and math.isfinite(process['elapsed_seconds']) and process['elapsed_seconds']>=0 and (task/'stderr.txt').stat().st_size==0,'Whole successful actual process capture')
 need(ce.same(mathematical_summary(task,row,ce),result['summary']),'Entire original mathematical/control/source receipt re-read')
 return result
def count_files(outputs,src,ce,*,native=False):
 """All49 semantic bridge. Does not mint native STAGE or authority metadata."""
 selected=rows(src);need(type(outputs)is dict and set(outputs)==set(selected),'All49 literal actual20 outputs required')
 files={};checked={}
 for key,row in selected.items():
  out=Path(outputs[key]).resolve()
  if native:
   value=ce.validate_completed(out);need(value['job_id']==key,'Exact original native-stage job');cap=out/'capsule'
  else:value=validate_portable(out,row,src,ce);cap=out/'task/capsule'
  checked[key]=value
  for p in cap.rglob('*'):
   src.ordinary(p)
   if p.is_file():
    name='work/'+p.relative_to(cap).as_posix();raw=p.read_bytes()
    need(name not in files or files[name]==raw,'Consistent complete COUNT namespace')
    files[name]=raw
 return files,checked
def main():
 parser=argparse.ArgumentParser();parser.add_argument('mode',choices=('inspect','replay','original-stage','bridge'));parser.add_argument('--output',required=True);parser.add_argument('--job');parser.add_argument('--inputs');parser.add_argument('--native-inputs',action='store_true');parser.add_argument('--timeout',type=float,default=120)
 a=parser.parse_args();need(not sys.flags.optimize,'Unoptimized source execution required');need(math.isfinite(a.timeout) and a.timeout>0,'Finite positive timeout');m=manifest()
 # Reject selection errors before creating output or importing mathematical code.
 selection={r['job_id']:r for r in read(HERE/'JOBS.json')['jobs']}
 if a.mode in('replay','original-stage'):need(a.job in selection,'One exact n20 job from the fixed49 registry')
 else:need(a.job is None,'Job is only valid for one-job execution')
 if a.mode=='bridge':need(a.inputs is not None,'Complete49 map required')
 else:need(a.inputs is None and not a.native_inputs,'Input map is only valid for bridge')
 out=Path(a.output).resolve();need(not out.exists(),'Fresh exclusive output directory');out.mkdir(parents=True);src,ce=load_runtime(out/'runtime',m);selected=rows(src)
 if a.mode=='inspect':
  materialize('count-sources.zip',out/'source-cache',m['source_files']);write(out/'RESULT.json',dict(jobs=list(selected),source_files=len(m['source_files']),source_manifest_sha256=MANIFEST_SHA256,arithmetic_executed=False,full_pass=False))
 elif a.mode=='replay':replay(out,selected[a.job],src,ce,a.timeout)
 elif a.mode=='original-stage':
  need(sys.platform=='linux','Original exact stopped-stage protocol requires Linux')
  need(a.timeout==120,'Original native stage uses its unchanged43200 CPU/54000 wall policy; omit --timeout')
  materialize('count-sources.zip',out/'source-cache',m['source_files'])
  from be_replay import finite1039_counts as worker
  checked=worker.execute(out/'stage',selected[a.job],out/'source-cache',log_root=out)
  write(out/'RESULT.json',dict(schema='PUBLIC_ORIGINAL_ACTUAL20_COUNT_STAGE_V1',validated=checked,stage=str(out/'stage'),source_manifest_sha256=MANIFEST_SHA256,full_pass=False))
 else:
  files,checked=count_files(read(a.inputs),src,ce,native=a.native_inputs);cap=out/'count-namespace';cap.mkdir()
  for name,raw in files.items():p=cap.joinpath(*parts(name));p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
  write(out/'RESULT.json',dict(schema='PUBLIC_ACTUAL20_ALL49_MATHEMATICAL_NAMESPACE_V1',jobs=checked,namespace=inventory(cap),source_manifest_sha256=MANIFEST_SHA256,original_native_stage_protocol=a.native_inputs,parent_acquisitions_verified=False,actual20_41_operations_completed=False,full_pass=False))
 print(json.dumps(dict(output=str(out),mode=a.mode,full_pass=False)))
if __name__=='__main__':
 try:main()
 except Exception as error:print(type(error).__name__+': '+str(error),file=sys.stderr);sys.exit(2)

