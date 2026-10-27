"""Scoped full66 stopped transport with a genuine original-cwd child relay.

This keeps the shared supervisor's checkpoint containment rule unchanged. The
outer cwd is the whole capsule; an independently pinned stdlib relay starts
the original program at its unchanged literal inner cwd. Both boundaries and
all complete original outputs are revalidated without rerunning a kernel.
"""
from __future__ import annotations
from datetime import datetime,timezone
import json,math,shutil,sys,tempfile,uuid,zipfile
from pathlib import Path
from . import delivery_transport as tx,action_supervisor as supervisor
from . import n25_count_evidence as evidence,n25_mixed_worker as worker
from .colab_batch import atomic_json,event,utc

CPU=WALL=82800
MEMORY=16*1024**3
DISK=16*1024**3
LOG=64*1024**2
SCHEMA='FULL66_GENUINE_TWO_BOUNDARY_STOPPED_PREFIX_V1'
PREFIX='MIXED_PREFIX.json'

def read(p):
 def unique(items):
  result={}
  for key,value in items:tx.need(key not in result,'No duplicate mixed transport key');result[key]=value
  return result
 return json.loads(Path(p).read_bytes(),object_pairs_hook=unique)
def hashes(p):return {n:r['sha256']for n,r in tx.inventory(p).items()}
def implementation():
 return {n:tx.digest(Path(__file__).parent/n)for n in('n25_mixed_stopped.py','n25_mixed_worker.py',
  'delivery_transport.py','action_supervisor.py')}
def original(context,*parts):
 cls=evidence.path_class(context['original_task_root']);return str(cls(context['original_task_root']).joinpath(*parts))
def mapped(task,value,context):
 cls=evidence.path_class(context['original_task_root']);rel=cls(value).relative_to(cls(context['original_task_root']))
 tx.need(rel.parts and '..'not in rel.parts,'Exact contained original mixed task context')
 return tx.ordinary(Path(task).joinpath(*rel.parts))
def command(context,spec):
 return [value.replace('{python}',context['python_executable']).replace('{capsule}',original(context,'capsule'))for value in spec['argv']]
def inner_name(spec):return 'transport/inner/'+spec['id']+'.json'
def request_name(spec):return 'transport/requests/'+spec['id']+'.json'
def output_names(spec):return list(spec['outputs'])+[inner_name(spec)]
def encoded(value):return(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()

def begin(task,*,adapter,context):
 task=tx.ordinary(task);c=task/'capsule'
 tx.need(c.is_dir()and not(task/PREFIX).exists(),'Exclusive complete mixed source task')
 context=dict(context,original_task_root=str(task),python_executable=sys.executable,python_version=sys.version)
 with zipfile.ZipFile(task/'INITIAL_CAPSULE.zip','x',zipfile.ZIP_DEFLATED,strict_timestamps=False)as z:
  for p in sorted(c.rglob('*')):
   tx.ordinary(p)
   if p.is_file():z.write(p,p.relative_to(c).as_posix())
  tx.zip_members(z,max_total=DISK,max_members=250000)
 state=dict(schema=SCHEMA,context=context,implementation=implementation(),adapter_identity=adapter.identity(),
  initial_capsule_sha256=tx.digest(task/'INITIAL_CAPSULE.zip'),initial_inventory=hashes(c),actions=[],
  only_complete_verified_actions_resumable=True,mathematical_acceptance=False)
 atomic_json(task/PREFIX,state);adapter.validate_initial(task,state);return state

def epoch(task,state,spec,adapter):
 changes,projection=adapter.epoch(task,state,spec)
 c=Path(task)/'capsule';before=hashes(c)
 for name,raw in changes.items():
  tx.parts(name);tx.need(type(raw)is bytes,'An exact derived source epoch consists of bytes')
 current=dict(before);current.update({n:__import__('hashlib').sha256(raw).hexdigest()for n,raw in changes.items()})
 context=state['context'];request=dict(schema='LITERAL_ORIGINAL_FULL66_MIXED_CHILD_REQUEST_V1',
  capsule=original(context,'capsule'),cwd=original(context,'capsule',spec['cwd']),command=command(context,spec),
  inner_capture=original(context,'capsule',inner_name(spec)),input_sha256=current,
  stdout_file=original(context,'executions',spec['id'],'stdout.txt'),
  stderr_file=original(context,'executions',spec['id'],'stderr.txt'))
 tx.need(request_name(spec)not in current,'Every original call has a unique immutable relay request')
 changes=dict(changes);changes[request_name(spec)]=encoded(request)
 return changes,projection

def guard():
 return dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,external_wall_seconds=float(WALL),
  per_process_RLIMIT_AS_bytes=MEMORY,per_process_RLIMIT_CPU_seconds=CPU,aggregate_kernel_memory_limit=False,
  aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=MEMORY,sampled_group_CPU_limit_seconds=CPU,
  sampled_group_CPU_includes_waited_descendants=True,sampled_file_limit_bytes=DISK,sampled_log_limit_bytes=LOG,
  descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)

def transport(task,state,spec,item):
 context=state['context'];d=Path(task)/'executions'/spec['id'];o=read(d/'supervisor-result.json')
 tx.need(evidence.same(o,item['observed'])and o['status']=='completed'and type(o['returncode'])is int
  and o['returncode']==0 and o['reason']is None and o['mode']=='untrusted_search'
  and o['proof_accepted']is False and type(o['sample_count'])is int and o['sample_count']>0
  and evidence.same(o['guard_scope'],guard()),'Actual successful whole-capsule supervisor, honest16GB/23h policy')
 for name in('elapsed_seconds','maximum_sampled_group_RSS_bytes','maximum_sampled_group_CPU_seconds'):
  tx.need(type(o[name])in(int,float)and math.isfinite(o[name])and o[name]>=0,'Actual finite execution observation')
 launch=read(d/'launch.json');expected=dict(argv=[context['python_executable'],'-B','-S',
  original(context,'capsule','transport/launch_mixed_action.py'),original(context,'capsule',request_name(spec))],
  cwd=original(context,'capsule'),output_dir=original(context,'executions',spec['id']),mode='untrusted_search',
  wall_seconds=float(WALL),cpu_seconds=CPU,memory_bytes=MEMORY,disk_bytes=DISK,log_bytes=LOG,
  sample_seconds=.2,heartbeat_seconds=20.,checkpoint_paths=[original(context,'capsule',n)for n in output_names(spec)])
 tx.need(evidence.same(launch,expected),'Exact outer launch, limits, interpreter and every full original checkpoint')
 for stream in('stdout','stderr'):
  p=d/(stream+'.txt');tx.need(mapped(task,o[stream+'_path'],context)==p and tx.digest(p)==o[stream+'_sha256']
   and p.stat().st_size<=LOG,'Entire actual supervisor '+stream)
 tx.need((d/'stderr.txt').stat().st_size==0,'Successful original child stderr must be empty')
 tx.need(type(o['checkpoints'])is list and len(o['checkpoints'])==len(output_names(spec)),
  'All original outputs and actual inner capture stopped together')
 for row,name in zip(o['checkpoints'],output_names(spec)):
  source=Path(task)/'capsule'/name;copy=d/'checkpoints'/name
  tx.need(set(row)=={'source_path','exists','trusted_certificate','path','bytes','sha256'}and row['exists']is True
   and row['trusted_certificate']is False and mapped(task,row['source_path'],context)==source
   and mapped(task,row['path'],context)==copy and type(row['bytes'])is int
   and row['bytes']==source.stat().st_size==copy.stat().st_size and row['sha256']==tx.digest(source)==tx.digest(copy),
   'Every complete original result and real inner capture equals its actual stopped bytes')
 inner=read(Path(task)/'capsule'/inner_name(spec));request=Path(task)/'capsule'/request_name(spec)
 tx.need(inner['schema']=='GENUINE_FULL66_ORIGINAL_INNER_CHILD_CAPTURE_V1'
  and inner['command']==command(context,spec)and inner['cwd']==original(context,'capsule',spec['cwd'])
  and type(inner['returncode'])is int and inner['returncode']==0 and inner['python']==context['python_version']
  and inner['python_executable']==context['python_executable']and inner['request_sha256']==tx.digest(request)
  and inner['historical_execution_relabelled']is False and inner['proof_accepted']is False,
  'Genuine exact original inner cwd/argv/interpreter, never an invented historical execution')
 tx.need(evidence.same(inner['input_sha256'],read(request)['input_sha256'])
  and all(item['input_inventory'].get(n)==pin for n,pin in inner['input_sha256'].items()),
  'Every real original-child input is in the full outer immutable launch inventory')
 for stream in('stdout','stderr'):tx.need(inner[stream+'_sha256']==o[stream+'_sha256'],'Exact whole original inner/outer stream equality')
 tx.need(type(inner['elapsed_seconds'])in(int,float)and math.isfinite(inner['elapsed_seconds'])and inner['elapsed_seconds']>=0,
  'Actual finite original child elapsed time')
 return(d/'stdout.txt').read_text('utf-8'),inner

def capture(task,state,spec,item,inner):
 if 'capture'not in spec:return
 task=Path(task);out=task/'capsule'/spec['capture'];out.mkdir(parents=True,exist_ok=False)
 d=task/'executions'/spec['id']
 for stream in('stdout','stderr'):shutil.copyfile(d/(stream+'.txt'),out/(stream+'.txt'))
 record=dict(schema='GENUINE_FULL66_ORIGINAL_CHILD_COMPATIBILITY_CAPTURE_V1',command=inner['command'],cwd=inner['cwd'],
  python=inner['python'],returncode=inner['returncode'],changed_inputs=[],input_sha256=item['flat_input_sha256'],
  started_utc=inner['started_utc'],finished_utc=inner['finished_utc'],elapsed_seconds=inner['elapsed_seconds'],
  stdout_sha256=inner['stdout_sha256'],stderr_sha256=inner['stderr_sha256'],
  capture_bridge=dict(schema='GENUINE_ORIGINAL_CHILD_UNDER_WHOLE_CAPSULE_SUPERVISOR_V1',
   outer_launch_sha256=tx.digest(d/'launch.json'),outer_supervisor_sha256=tx.digest(d/'supervisor-result.json'),
   inner_capture_sha256=tx.digest(task/'capsule'/inner_name(spec)),original_task_root=state['context']['original_task_root'],
   complete_outer_input_inventory=item['input_inventory'],historical_execution_relabelled=False,proof_accepted=False))
 atomic_json(out/'metadata.json',record)

def advance(task,*,adapter,root):
 task=tx.ordinary(task);state=read(task/PREFIX);adapter.validate_initial(task,state)
 tx.need(hashes(task/'capsule')==(state['actions'][-1]['after_inventory']if state['actions']else state['initial_inventory']),
  'Only the exact last complete mixed prefix can advance')
 spec=adapter.specs(state['context'])[len(state['actions'])];changes,report=epoch(task,state,spec,adapter)
 epoch_dir=task/'source_epochs'/spec['id'];epoch_dir.mkdir(parents=True,exist_ok=False)
 for name,raw in changes.items():
  p=epoch_dir/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
  dest=task/'capsule'/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
 item=dict(action=spec['id'],source_epoch=report,source_changes={n:tx.digest(epoch_dir/n)for n in changes},
  input_inventory=hashes(task/'capsule'),flat_input_sha256=adapter.capture_inputs(task,spec),started_utc=utc())
 atomic_json(task/'ACTION_INCOMPLETE.json',item)
 tx.need(all(not(task/'capsule'/n).exists()for n in output_names(spec)),'Exclusive genuinely new native results and inner capture')
 context=state['context'];execution=task/'executions'/spec['id']
 event(root,'full66_original_mixed_action_started',action=spec['id'],completed_actions=len(state['actions']),
  total_actions=len(adapter.specs(context)),cpu_seconds=CPU,wall_seconds=WALL,memory_bytes=MEMORY)
 with tx.Follow(root,execution,spec['id']):
  o=supervisor.run([context['python_executable'],'-B','-S',str(task/'capsule/transport/launch_mixed_action.py'),
   str(task/'capsule'/request_name(spec))],cwd=task/'capsule',output_dir=execution,mode='untrusted_search',
   cpu_seconds=CPU,wall_seconds=WALL,memory_bytes=MEMORY,disk_bytes=DISK,log_bytes=LOG,sample_seconds=.2,
   heartbeat_seconds=20,checkpoint_paths=[task/'capsule'/n for n in output_names(spec)])
 item.update(observed=o,finished_utc=utc());atomic_json(task/'ACTION_INCOMPLETE.json',item)
 stdout,inner=transport(task,state,spec,item);actual=hashes(task/'capsule')
 tx.need(set(actual)==set(item['input_inventory'])|set(output_names(spec))
  and all(actual[n]==pin for n,pin in item['input_inventory'].items()),'Every actual immutable input and all original side effects are accounted for')
 item['validated_output']=adapter.validate_output(task,state,spec,item,stdout)
 capture(task,state,spec,item,inner);item['after_inventory']=hashes(task/'capsule');state['actions'].append(item)
 atomic_json(task/PREFIX,state);(task/'ACTION_INCOMPLETE.json').unlink()
 event(root,'full66_original_mixed_action_committed',action=spec['id'],completed_actions=len(state['actions']))
 return state

def validate(task,*,adapter):
 task=tx.ordinary(task);state=read(task/PREFIX);context=state['context'];specs=adapter.specs(context)
 tx.need(state['schema']==SCHEMA and evidence.same(state['implementation'],implementation())
  and evidence.same(state['adapter_identity'],adapter.identity())and state['only_complete_verified_actions_resumable']is True
  and state['mathematical_acceptance']is False and 0<=len(state['actions'])<=len(specs),
  'Exact whole scoped transport/source epoch and complete unskipped prefix')
 tx.need(tx.digest(task/'INITIAL_CAPSULE.zip')==state['initial_capsule_sha256'],'Entire initial full mixed source/parent capsule')
 adapter.validate_initial(task,state)
 with tempfile.TemporaryDirectory(prefix='be-full66-mixed-readback-')as temp:
  virtual=Path(temp)/'task';c=virtual/'capsule';c.mkdir(parents=True);adapter.copy_validation_context(task,virtual)
  with zipfile.ZipFile(task/'INITIAL_CAPSULE.zip')as z:
   for row in tx.zip_members(z,max_total=DISK,max_members=250000):
    p=c.joinpath(*tx.parts(row.filename));p.parent.mkdir(parents=True,exist_ok=True)
    with z.open(row)as source,p.open('xb')as target:shutil.copyfileobj(source,target,tx.MIB)
  tx.need(hashes(c)==state['initial_inventory'],'Whole independently pinned initial source inventory')
  prior=dict(state,actions=[])
  for spec,item in zip(specs,state['actions']):
   tx.need(item['action']==spec['id'],'No omitted, duplicate or reordered original mixed action')
   expected,report=epoch(virtual,prior,spec,adapter)
   tx.need(evidence.same(report,item['source_epoch'])and {n:__import__('hashlib').sha256(raw).hexdigest()for n,raw in expected.items()}==item['source_changes'],
    'Every metadata-only stage epoch is reconstructed from immutable sources and already validated current parents')
   tx.need(hashes(task/'source_epochs'/spec['id'])==item['source_changes'],'Entire actual derived stage epoch')
   for name,raw in expected.items():
    tx.need((task/'source_epochs'/spec['id']/name).read_bytes()==raw,'Exact expected stage bytes')
    p=c/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
   tx.need(hashes(c)==item['input_inventory']and evidence.same(adapter.capture_inputs(virtual,spec),item['flat_input_sha256']),
    'Every actual original input at this exact stopped stage')
   d=virtual/'executions'/spec['id'];shutil.copytree(task/'executions'/spec['id'],d)
   for name in output_names(spec):
    p=c/name;tx.need(not p.exists(),'A complete original output cannot overwrite any input');p.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(d/'checkpoints'/name,p)
   stdout,inner=transport(virtual,prior,spec,item)
   checked=adapter.validate_output(virtual,prior,spec,item,stdout)
   tx.need(evidence.same(checked,item['validated_output']),'Whole original native mathematical result and controls, never an earlier status flag')
   capture(virtual,prior,spec,item,inner);tx.need(hashes(c)==item['after_inventory'],'Every genuine compatibility capture and exact complete stopped state')
   prior['actions'].append(item)
  tx.need(hashes(task/'capsule')==hashes(c),'Final/live capsule is exactly its complete reconstructed prefix')
 return dict(schema='REVALIDATED_FULL66_GENUINE_TWO_BOUNDARY_PREFIX_V1',prefix_sha256=tx.digest(task/PREFIX),
  completed_actions=len(state['actions']),required_actions=len(specs),all_original_actions_completed=len(state['actions'])==len(specs),
  mathematical_acceptance=False)
