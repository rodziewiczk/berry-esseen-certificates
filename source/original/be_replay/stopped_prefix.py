"""Immutable stopped-action prefixes for protocols with native absolute cwd.

An adapter supplies the exact original recipes and full pure source/output
validators. This transport never accepts mathematics. Each source epoch, whole
checkpoint and genuine compatibility capture is retained; validation rebuilds
the state at each stop instead of checking an earlier call against later files.
"""
from datetime import datetime,timezone
from pathlib import Path
import json,shutil,sys,tempfile,uuid,zipfile
from . import delivery_transport as tx,action_supervisor
from . import finite69_remaining as stopped
from .finite1039_count_evidence import same
from .colab_batch import atomic_json,event,utc

SCHEMA='IMMUTABLE_GENUINE_STOPPED_ACTION_PREFIX_V1'
def read(p):
 def unique(items):
  result={}
  for k,v in items:tx.need(k not in result,'No duplicate action-prefix metadata');result[k]=v
  return result
 return json.loads(Path(p).read_bytes(),object_pairs_hook=unique)
def hashes(p):return {n:r['sha256']for n,r in tx.inventory(p).items()}
def implementation():
 return {n:tx.digest(Path(__file__).parent/n)for n in('stopped_prefix.py','finite69_remaining.py','delivery_transport.py','action_supervisor.py')}
def begin(task,*,adapter,context):
 task=tx.ordinary(task);tx.need((task/'capsule').is_dir()and not(task/'PREFIX.json').exists(),'Exclusive already source-prepared native transaction')
 context=dict(context,original_task_root=str(task),python_executable=sys.executable,python_version=sys.version)
 initial=task/'INITIAL_CAPSULE.zip'
 with zipfile.ZipFile(initial,'x',zipfile.ZIP_DEFLATED,strict_timestamps=False)as z:
  for p in sorted((task/'capsule').rglob('*')):
   tx.ordinary(p)
   if p.is_file():z.write(p,p.relative_to(task/'capsule').as_posix())
  tx.zip_members(z)
 state=dict(schema=SCHEMA,context=context,implementation=implementation(),adapter_identity=adapter.identity(),
  initial_capsule_sha256=tx.digest(initial),initial_inventory=hashes(task/'capsule'),actions=[],
  only_complete_verified_actions_resumable=True,mathematical_acceptance=False)
 atomic_json(task/'PREFIX.json',state);adapter.validate_initial(task,state)
 return state
def _capture(task,spec,item,context):
 d=Path(task)/'executions'/spec['id'];o=item['observed']
 return dict(schema='GENUINE_STOPPED_NATIVE_COMPATIBILITY_CAPTURE_V1',
  command=stopped.argv(context,spec,context),cwd=stopped.original(context,spec['cwd']),
  python=context['python_version'],returncode=o['returncode'],changed_inputs=[],input_sha256=item['flat_input_sha256'],
  started_utc=item['started_utc'],finished_utc=item['finished_utc'],elapsed_seconds=o['elapsed_seconds'],
  stdout_sha256=o['stdout_sha256'],stderr_sha256=o['stderr_sha256'],
  capture_bridge=dict(schema='EXACT_CURRENT_OUTER_LAUNCH_AND_SOURCE_BINDING_V1',
   launch_sha256=tx.digest(d/'launch.json'),supervisor_result_sha256=tx.digest(d/'supervisor-result.json'),
   complete_input_files_sha256=item['input_inventory'],original_task_root=context['original_task_root'],
   historical_execution_relabelled=False,proof_accepted=False))
def _copy_outputs(source_task,target_task,spec):
 src=Path(source_task);dest=Path(target_task);original_cwd=Path('capsule')/spec['cwd']
 for n in spec['outputs']:
  rel=Path('capsule')/n;copy=src/'executions'/spec['id']/'checkpoints'/rel.relative_to(original_cwd)
  p=dest/rel
  if p.exists():
   tx.need(n not in spec.get('created',spec['outputs'])and p.read_bytes()==copy.read_bytes(),
    'An input checkpoint is the complete unchanged input, never an overwritten output')
   continue
  tx.need(n in spec.get('created',spec['outputs']),'Only a declared genuinely new output can enter the next immutable prefix')
  p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(copy,p)
def _write_capture(task,spec,item,context,*,source_task):
 if 'capture'not in spec:return
 root=Path(task);out=root/'capsule'/spec['capture'];out.mkdir(parents=True,exist_ok=False)
 for stream in('stdout','stderr'):shutil.copyfile(Path(source_task)/'executions'/spec['id']/(stream+'.txt'),out/(stream+'.txt'))
 atomic_json(out/'metadata.json',_capture(task,spec,item,context))
def advance(task,*,adapter,root):
 """Run exactly the next full original call; failed work is never committed."""
 task=tx.ordinary(task);state=read(task/'PREFIX.json');adapter.validate_live(task,state)
 ordinal=len(state['actions']);spec=adapter.specs()[ordinal];context=state['context'];before=hashes(task/'capsule')
 delta=adapter.prepare_action(task,state,spec)
 after_epoch=hashes(task/'capsule');changed={n:p for n,p in after_epoch.items()if before.get(n)!=p}
 tx.need(set(before)<=set(after_epoch),'A source epoch cannot silently delete a prior native result')
 epochs=task/'source_epochs'/spec['id'];epochs.mkdir(parents=True,exist_ok=False)
 for n in changed:
  p=epochs/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(task/'capsule'/n,p)
 item=dict(action=spec['id'],source_epoch=delta,source_changes=changed,input_inventory=after_epoch,
  flat_input_sha256=adapter.capture_inputs(task,spec),started_utc=utc())
 atomic_json(task/'ACTION_INCOMPLETE.json',item)
 tx.need(all(not(task/'capsule'/n).exists()for n in spec.get('created',spec['outputs'])),'Every requested new native output is fresh')
 execution=task/'executions'/spec['id']
 event(root,'original_action_started',action=spec['id'],cpu_seconds=82800,wall_seconds=82800,
  action_budget_is_batch_budget=False,completed_prefix_actions=ordinal,total_actions=len(adapter.specs()))
 with tx.Follow(root,execution,spec['id']):
  observed=action_supervisor.run(stopped.argv(context,spec,context),cwd=task/'capsule'/spec['cwd'],output_dir=execution,
   mode='untrusted_search',cpu_seconds=82800,wall_seconds=82800,memory_bytes=stopped.MEMORY_BYTES,
   disk_bytes=stopped.DISK_BYTES,log_bytes=stopped.LOG_BYTES,sample_seconds=.2,heartbeat_seconds=20,
   checkpoint_paths=[task/'capsule'/n for n in spec['outputs']])
 item.update(observed=observed,finished_utc=utc());atomic_json(task/'ACTION_INCOMPLETE.json',item)
 stdout=stopped.transport(task,context,spec,item,context)
 actual=hashes(task/'capsule');tx.need(set(actual)==set(after_epoch)|set(spec.get('created',spec['outputs']))
  and all(actual[n]==p for n,p in after_epoch.items()),'Every source stayed fixed during the actual call; no undeclared output')
 item['validated_output']=adapter.validate_output(task,state,spec,item,stdout)
 _write_capture(task,spec,item,context,source_task=task)
 item['after_inventory']=hashes(task/'capsule');state['actions'].append(item)
 atomic_json(task/'PREFIX.json',state);(task/'ACTION_INCOMPLETE.json').unlink()
 event(root,'original_action_committed_to_complete_prefix',action=spec['id'],completed_prefix_actions=len(state['actions']))
 return state
def validate(task,*,adapter):
 """Rebuild every stopped state; no original producer or oracle is executed."""
 task=tx.ordinary(task);state=read(task/'PREFIX.json');specs=adapter.specs();context=state['context']
 tx.need(state['schema']==SCHEMA and same(state['implementation'],implementation())
  and same(state['adapter_identity'],adapter.identity())and state['only_complete_verified_actions_resumable']is True
  and state['mathematical_acceptance']is False and 0<=len(state['actions'])<=len(specs),
  'Exact adapter/transport epoch and explicit nonaccepting immutable prefix')
 tx.need(tx.digest(task/'INITIAL_CAPSULE.zip')==state['initial_capsule_sha256'],'Whole initial source/canonical-parent archive SHA')
 adapter.validate_initial(task,state)
 with tempfile.TemporaryDirectory(prefix='be-complete-prefix-readback-')as temp:
  virtual=Path(temp)/'task';c=virtual/'capsule';c.mkdir(parents=True)
  # All other metadata/provenance/parent evidence is data supplied to the pure
  # adapter. No file from an archive is imported by the transport.
  adapter.copy_validation_context(task,virtual)
  with zipfile.ZipFile(task/'INITIAL_CAPSULE.zip')as z:
   for r in tx.zip_members(z):
    p=c.joinpath(*tx.parts(r.filename));p.parent.mkdir(parents=True,exist_ok=True)
    with z.open(r)as s,p.open('xb')as d:shutil.copyfileobj(s,d,tx.MIB)
  tx.need(hashes(c)==state['initial_inventory'],'Exact initial native source/parent inventory')
  prior=dict(state,actions=[])
  for spec,item in zip(specs,state['actions']):
   tx.need(item['action']==spec['id'],'No omitted, reordered or substituted original action')
   adapter.validate_epoch(virtual,prior,spec,item)
   expected=dict(hashes(c))
   epoch_dir=task/'source_epochs'/spec['id'];actual=hashes(epoch_dir)
   tx.need(actual==item['source_changes'],'Whole metadata-only source epoch inventory')
   for n,pin in actual.items():
    p=c/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(epoch_dir/n,p);expected[n]=pin
   tx.need(expected==item['input_inventory']==hashes(c),'Every actual immutable input at this exact stop')
   tx.need(same(adapter.capture_inputs(virtual,spec),item['flat_input_sha256']),
    'The original-consumed flat capture field is derived from the full actual immutable inputs')
   execution=virtual/'executions'/spec['id'];shutil.copytree(task/'executions'/spec['id'],execution)
   _copy_outputs(task,virtual,spec)
   stdout=stopped.transport(virtual,context,spec,item,context)
   tx.need(set(hashes(c))==set(expected)|set(spec.get('created',spec['outputs']))and all(tx.digest(c/n)==p for n,p in expected.items()),
    'Exact stopped source/output state without later artifacts')
   checked=adapter.validate_output(virtual,prior,spec,item,stdout)
   tx.need(same(checked,item['validated_output']),'Whole native mathematical output, source and original control readback')
   _write_capture(virtual,spec,item,context,source_task=virtual)
   tx.need(hashes(c)==item['after_inventory'],'Whole genuinely derived compatibility capture and completed state')
   prior['actions'].append(item)
  tx.need(hashes(task/'capsule')==hashes(c),'Live/final capsule equals the last complete verified state')
 return dict(schema='REVALIDATED_GENUINE_STOPPED_ACTION_PREFIX_V1',prefix_sha256=tx.digest(task/'PREFIX.json'),
  completed_actions=len(state['actions']),required_actions=len(specs),all_original_actions_completed=len(state['actions'])==len(specs),
  mathematical_acceptance=False)
def resume_origin(restored,*,adapter,work_root):
 """Restore actual original native cwd, preserving any interrupted remainder."""
 restored=tx.ordinary(restored);checked=validate(restored,adapter=adapter);state=read(restored/'PREFIX.json')
 origin=tx.ordinary(state['context']['original_task_root']);base=tx.ordinary(work_root)
 tx.need(origin.is_relative_to(base)and origin!=base and len(origin.relative_to(base).parts)>=3,
  'Only a recorded owned task beneath the configured runtime work tree can be resumed')
 if origin.exists():
  tx.need((origin/'PREFIX.json').is_file(),'Never replace an unrelated existing directory')
  current=read(origin/'PREFIX.json')
  tx.need(current['schema']==SCHEMA and current['context']==state['context']
   and current['initial_capsule_sha256']==state['initial_capsule_sha256'],'Same exclusive owned native transaction')
  saved=origin.with_name(origin.name+'-preserved-interrupted-'+uuid.uuid4().hex[:12]);origin.rename(saved)
 origin.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(restored,origin)
 tx.need(validate(origin,adapter=adapter)==checked,'Whole stopped evidence survives restoration to the actual original cwd')
 return origin,checked
