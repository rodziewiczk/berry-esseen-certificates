"""Native actual20 stage adapter for58H; no finite/global theorem acceptance.

The early sharp-premise join precedes feedback preparation. Every missing
historical capture is supplied by genuine current stopped evidence. Original
numeric constants, complete candidates,100-row resources and controls remain
unchanged; only separately recorded identity literals/graphs may be rebound.
"""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction as F
import json,re,shutil,zipfile
from . import finite2024_remaining_sources as src,finite2024_remaining_native as native
from . import finite2024_remaining_epoch as epoch,finite2024_remaining_evidence as ev
from . import finite2024_fourier_sources as fs,finite2024_fourier_evidence as fe
from . import delivery_transport as tx,stopped_prefix as prefix
from .finite1039_count_evidence import same
from .colab_batch import atomic_json

SHARP='work/cutoff20_20261016/root/sharp20_premise_join_v1'
RESOURCE_CAPTURES={
 'coarse_resources_construct':'runs/cutoff20_20261016/finite/sharp20_b0_resources_all_v1/construct01',
 'coarse_resources_accept':'runs/cutoff20_20261016/finite/sharp20_b0_resources_all_v1/accept01',
 'feedback_b0_resources_construct':'runs/cutoff20_20261016/finite/feedback20_b0_resources_construct01',
 'feedback_b0_resources_accept':'runs/cutoff20_20261016/finite/feedback20_b0_resources_accept01',
 'feedback_bn_resources_construct':'runs/cutoff20_20261016/fourier/feedback_bn_resources_v1/construct01',
 'feedback_bn_resources_accept':'runs/cutoff20_20261016/fourier/feedback_bn_resources_v1/accept01'}
RESOURCE_CAPTURE_PINS={
 RESOURCE_CAPTURES['feedback_b0_resources_construct']+'/metadata.json':'d75a0a85001603fd64f6d0eea286cd8b274fde84cf3c5275491db7d9beadf303',
 RESOURCE_CAPTURES['feedback_b0_resources_accept']+'/metadata.json':'56129630c6dd13107bfd70428b47231341152dfff0e2e5c1ada44bdbb6f26bff',
 RESOURCE_CAPTURES['feedback_bn_resources_construct']+'/metadata.json':'53dabe50e9378c6c6e83af76383a5b65dd42068c31097d4d1b677503aa8aa9b3',
 RESOURCE_CAPTURES['feedback_bn_resources_accept']+'/metadata.json':'cdb76bcf2253069d5af8c015b45ae44efce663e47d2f27164c09688eb5a4a5ea'}
def specs():
 result=[]
 for name,*_ in native.RECIPES:
  if name=='feedback_native_prepare':
   result.append(dict(id='early_sharp_premise_join',cwd=SHARP,argv=['{python}','-B','check.py'],
    outputs=[SHARP+'/JOINED.json'],created=[SHARP+'/JOINED.json']))
  r=native.recipe(name);a=dict(id=name,cwd=r['cwd'],argv=['{python}','-B',*r['arguments']],
   outputs=native.checkpoints(name),created=native.created_outputs(name))
  if name in native.CAPTURES:a['capture']=native.CAPTURES[name]
  if name in RESOURCE_CAPTURES:a['capture']=RESOURCE_CAPTURES[name]
  result.append(a)
 return result
def identity():
 return dict(source_plan_sha256=src.PLAN_SHA256,files={n:src.digest(src.ROOT/'be_replay'/n)for n in(
  'finite2024_actual20_adapter.py','finite2024_remaining_sources.py','finite2024_remaining_native.py',
  'finite2024_remaining_epoch.py','finite2024_remaining_evidence.py','finite2024_fourier_evidence.py')},
  full58H_semantic_scope_completed_by_this_adapter=False)
def all_created():return {n for a in specs()for n in a['created']}
def _parent_metadata(task,parent):
 """Alias a genuinely observed58D readback; preserve its actual argv/cwd."""
 checked=fe.validate_completed(parent);cfg=fs.family('auxiliary');report=fs.read(Path(parent)/'STAGE_OBSERVED.json')
 a=next(r for r in report['actions']if r['action']=='readback');o=a['observed'];d=Path(parent)/'executions/readback'
 launch=fs.read(d/'launch.json');sources=fs.read(Path(parent)/'SOURCES.json')['sources']
 return dict(schema='CURRENT_FULL58D_READBACK_CAPTURE_ALIAS_V1',command=launch['argv'],cwd=launch['cwd'],
  python=report['python_version'],returncode=o['returncode'],changed_inputs=[],input_sha256=sources,
  stdout_sha256=o['stdout_sha256'],stderr_sha256=o['stderr_sha256'],elapsed_seconds=o['elapsed_seconds'],
  current58D_stage_result_sha256=checked['stage_result_sha256'],
  current_supervisor_result_sha256=src.digest(d/'supervisor-result.json'),historical_capture_relabelled=False)
def prepare(cache,task,*,auxiliary_task,owned_outputs=None):
 task=src.ordinary(task);src.need(not task.exists(),'Exclusive native actual20 transaction');task.mkdir(parents=True)
 src.verify_cache(cache);shutil.copytree(cache,task/'originals');src.verify_cache(task/'originals')
 checked=fe.validate_completed(auxiliary_task)
 src.need(checked['family']=='auxiliary','Complete actual19--24 auxiliary58D parent')
 shutil.copytree(auxiliary_task,task/'inputs/58D');aux=task/'inputs/58D';cfg=fs.family('auxiliary')
 c=task/'capsule';c.mkdir();pins={}
 # All historical numerical outputs owned by this transaction are absent.
 # Other archived JSON remains explicitly conditional source/provenance data.
 owned=all_created()|set(owned_outputs or())
 for n,row in src.plan()['original_files'].items():
  if n in owned:continue
  p=c/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Path(cache)/n,p);pins[n]=row['sha256']
 parent_pins={}
 for p in(aux/'capsule').rglob('*'):
  src.ordinary(p)
  if not p.is_file():continue
  n=p.relative_to(aux/'capsule').as_posix();dest=c/n;dest.parent.mkdir(parents=True,exist_ok=True)
  # An actual58D input may occupy an old reference name. Its complete genuine
  # upstream reader, not an arbitrary changed SHA, admits those exact bytes.
  shutil.copyfile(p,dest);pins[n]=src.digest(p);parent_pins[n]=pins[n]
 result=cfg['audit']+'/READBACK.json';p=c/result;p.parent.mkdir(parents=True,exist_ok=True)
 shutil.copyfile(aux/'capsule'/fs.result_path(cfg),p);pins[result]=src.digest(p);parent_pins[result]=pins[result]
 capture='runs/cutoff20_20261016/analytic/auxiliary19_24_readback01';dest=c/capture;dest.mkdir(parents=True,exist_ok=False)
 for stream in('stdout','stderr'):shutil.copyfile(aux/'executions/readback'/(stream+'.txt'),dest/(stream+'.txt'))
 atomic_json(dest/'metadata.json',_parent_metadata(task,aux))
 for name in('metadata.json','stdout.txt','stderr.txt'):
  n=capture+'/'+name;pins[n]=src.digest(c/n);parent_pins[n]=pins[n]
 aux_packet=src.read(c/result)
 src.need(aux_packet['n']==list(range(19,25))and aux_packet['finite_rho']==['1','19/10']
  and F(aux_packet['uniform_upper'])<F(262,625)and F(aux_packet['per_n_upper']['20'])<F(419,1000),
  'Actual all-law auxiliary ceilings license both original coarse and narrow native domains')
 atomic_json(task/'PREPARATION.json',dict(schema='GENUINE_CURRENT58H_NATIVE_ACTUAL20_PREPARATION_V1',
  source_plan_sha256=src.PLAN_SHA256,actual58D=checked,parent_files_sha256=parent_pins,initial_files_sha256=pins,
  full58H_completed=False,actual20_sharp_verified=False,all_index_conclusion_verified=False))
 return task
def _initial_files(task):
 p=src.read(Path(task)/'PREPARATION.json');src.need(p['schema']=='GENUINE_CURRENT58H_NATIVE_ACTUAL20_PREPARATION_V1'
  and p['source_plan_sha256']==src.PLAN_SHA256 and all(p[k]is False for k in('full58H_completed','actual20_sharp_verified','all_index_conclusion_verified')),
  'Exact nonaccepting preparation')
 checked=fe.validate_completed(Path(task)/'inputs/58D');src.need(same(checked,p['actual58D']),'Complete current58D execution evidence')
 cfg=fs.family('auxiliary');parent=Path(task)/'inputs/58D';pins={}
 for f in(parent/'capsule').rglob('*'):
  src.ordinary(f)
  if f.is_file():pins[f.relative_to(parent/'capsule').as_posix()]=src.digest(f)
 pins[cfg['audit']+'/READBACK.json']=src.digest(parent/'capsule'/fs.result_path(cfg))
 capture='runs/cutoff20_20261016/analytic/auxiliary19_24_readback01'
 for stream in('stdout','stderr'):pins[capture+'/'+stream+'.txt']=src.digest(parent/'executions/readback'/(stream+'.txt'))
 pins[capture+'/metadata.json']=epoch.digest((json.dumps(_parent_metadata(task,parent),indent=2)+'\n').encode())
 src.need(pins==p['parent_files_sha256'],'Every genuine parent alias and whole actual stopped readback stream')
 expected={n:r['sha256']for n,r in src.plan()['original_files'].items()if n not in all_created()};expected.update(pins)
 src.need(expected==p['initial_files_sha256'],'Only full original source inputs and whole genuine current58D aliases')
 return expected
def validate_initial(task,state):
 src.verify_cache(Path(task)/'originals');expected=_initial_files(task)
 src.need(expected==state['initial_inventory'],'Complete initial source/parent inventory')
 src.need(not(set(expected)&all_created()),'No old native own output may be admitted as current')
 return expected
def copy_validation_context(task,virtual):
 for folder in('originals','inputs'):shutil.copytree(Path(task)/folder,Path(virtual)/folder)
 shutil.copyfile(Path(task)/'PREPARATION.json',Path(virtual)/'PREPARATION.json')
def _reference_map(task,state,extra=None):
 c=Path(task)/'capsule';p=src.plan();proofs=dict(state.get('extra_reference_proofs',{}));derived=set(state.get('additional_derived',[]));preparation=src.read(Path(task)/'PREPARATION.json')
 action_specs=state.get('context',{}).get('full_action_specs',specs())
 if state.get('context',{}).get('full_actual20'):
  from .finite2024_actual20_full import original_files
  p=dict(p,original_files=original_files(task))
 for name in preparation['parent_files_sha256']:proofs[name]=preparation['actual58D']['stage_result_sha256']
 for item in state['actions']:
  derived.update(item['source_changes']);evidence=src.digest(Path(task)/'executions'/item['action']/'supervisor-result.json')
  spec=next(a for a in action_specs if a['id']==item['action'])
  for n in spec['created']:proofs[n]=evidence
  if 'capture'in spec:
   for s in('metadata.json','stdout.txt','stderr.txt'):proofs[spec['capture']+'/'+s]=evidence
 if extra:
  derived.update(extra['source_changes'])
  evidence=src.digest(Path(task)/'executions'/extra['action']/'supervisor-result.json')
  for n in next(a for a in action_specs if a['id']==extra['action'])['created']:proofs[n]=evidence
 refs=epoch.References()
 for n,pin in prefix.hashes(c).items():
  old=p['original_files'].get(n,{}).get('sha256')or p['historical_execution_edges_requiring_genuine_current_replacement'].get(n,{}).get('pin')or RESOURCE_CAPTURE_PINS.get(n)or state.get('context',{}).get('full_capture_pins',{}).get(n)or pin
  if n in proofs:role='validated_fresh_parent'
  elif n in derived:role='derived_metadata'
  else:role='unchanged_source'if n.endswith(('.py','.txt','.diff','.md'))else'conditional_archived_input'
  refs.add(n,old,(c/n).read_bytes(),role=role,evidence_sha256=proofs.get(n))
 return refs
def epoch_changes(task,state):
 """Deterministic metadata only; never evaluate the original math source."""
 c=Path(task)/'capsule';originals=Path(task)/'originals';source_plan=src.plan();known_created={n for a in state.get('context',{}).get('full_action_specs',specs())for n in a['created']}
 full=state.get('context',{}).get('full_actual20',False)
 if full:
  from .finite2024_actual20_full import original_files,port_source,REQUESTS
  source_plan=dict(source_plan,original_files=original_files(task));known_created.update(REQUESTS.values())
 parent=set(src.read(Path(task)/'PREPARATION.json')['parent_files_sha256'])|set(state.get('extra_reference_proofs',{}));changes={};reports={}
 # Fixed-point expansion of source-only identities. Numeric output/parent
 # packets are never rewritten by this preparation pass.
 for unused in range(len(source_plan['original_files'])+1):
  refs=_reference_map(task,state);did=False
  for n,row in source_plan['original_files'].items():
   if n in known_created or n in parent or not(c/n).is_file():continue
   original=src.ordinary((Path(task)/row['location'] if full else originals)/n).read_bytes()
   src.need(len(original)==row['bytes']and epoch.digest(original)==row['sha256'],'Every independently pinned source epoch original')
   current=None;report=None
   if n.endswith('.py'):
    if full:
     from . import finite2024_coupled_parent as coupled_parent
     if n in(coupled_parent.SCRIPT,coupled_parent.HELPER):
      src.need(epoch.digest(original)==coupled_parent.SOURCE_SHA,'Original byte-identical scalar contractor/helper')
      if(c/n).read_bytes()!=original:
       (c/n).write_bytes(original);changes[n]=epoch.digest(original);did=True
      continue
    substitutions=refs.substitutions();used=set(re.findall(rb'[0-9a-f]{64}',original))
    selected={old:new for old,new in substitutions.items()if old.encode()in used}
    try:current,report=epoch.rewrite_reference_literals(original,selected)if selected else(original,dict(original_sha256=epoch.digest(original),current_sha256=epoch.digest(original),literal_edits=[],mathematical_source_body_changed=False))
    except ValueError as error:raise ValueError('Source epoch '+n+': '+str(error))from error
    if full:current,port=port_source(n,current,context=state['context']);report=dict(report,current_sha256=epoch.digest(current),explicit_current_transport_port=port)
   elif n.endswith('.json'):
    packet=epoch.read(original)
    if type(packet)is dict and 'files_sha256'in packet and set(packet['files_sha256'])<=set(refs.rows):
     fields=[k for k,v in packet.items()if k!='files_sha256'and k.endswith('sha256')and type(v)is str and epoch.HEX.fullmatch(v)]
     try:current,report=epoch.derive_graph_packet(original,refs,scalar_reference_fields=fields)
     except ValueError as error:raise ValueError('Source graph epoch '+n+': '+str(error))from error
     if same(epoch.read(current),packet):
      # Keep byte-identical shared source aliases when no identity changed.
      # JSON pretty-printing is not a reason to invalidate a source/cache pin.
      current=original;report=None
   if current is not None and(c/n).read_bytes()!=current:
    (c/n).write_bytes(current);changes[n]=epoch.digest(current);reports[n]=report;did=True
  if not did:return dict(schema='ACTUAL20_CURRENT_METADATA_SOURCE_EPOCH_V1',files_sha256=changes,reports=reports,
   mathematical_source_body_changed=False,historical_execution_relabelled=False)
  # The next registry construction admits only this exact independently
  # reproducible epoch, rather than an arbitrary mutable source file.
  # Derived names are explicitly carried for the following pass.
  state=dict(state,additional_derived=sorted(set(state.get('additional_derived',[]))|set(changes)))
 raise ValueError('Source reference epoch did not stabilize; a typed action boundary is required')
def prepare_action(task,state,spec):return epoch_changes(task,state)
def validate_epoch(task,state,spec,item):
 # Work on a temporary copy so comparison cannot change the rebuilt prefix.
 import tempfile
 with tempfile.TemporaryDirectory(prefix='be-actual20-source-projection-')as d:
  target=Path(d)/'task';target.mkdir();copy_validation_context(task,target);shutil.copytree(Path(task)/'capsule',target/'capsule')
  (target/'executions').mkdir()
  for prior in state['actions']:shutil.copytree(Path(task)/'executions'/prior['action'],target/'executions'/prior['action'])
  expected=epoch_changes(target,state)
  src.need(same(expected,item['source_epoch'])and expected['files_sha256']==item['source_changes'],
   'Whole independently reconstructed current source/graph epoch, every original mathematical field preserved')
def capture_inputs(task,spec):
 if spec['id']=='early_sharp_premise_join':return {p.name:src.digest(p)for p in(Path(task)/'capsule'/SHARP).iterdir()if p.is_file()}
 inputs=native.capture_input_map(Path(task)/'capsule',spec['id'])
 if spec['id'].startswith('feedback_bn_resources_'):inputs={spec['cwd']+'/'+name:pin for name,pin in inputs.items()}
 return inputs
def validate_live(task,state):
 src.need(state['adapter_identity']==identity(),'Exact native actual20 implementation profile')
 expected=state['actions'][-1]['after_inventory']if state['actions']else state['initial_inventory']
 src.need(prefix.hashes(Path(task)/'capsule')==expected,'Only a complete verified prefix may advance')
def validate_output(task,state,spec,item,stdout):
 # A stopped0 process is still not a theorem. Full output/source/control
 # validation precedes the compatibility capture and committed-prefix marker.
 refs=_reference_map(task,state,item)
 if spec['id']=='early_sharp_premise_join':
  name=SHARP+'/JOINED.json';packet=src.read(Path(task)/'capsule'/name)
  result=ev.check_packet(Path(task)/'originals',name,packet,references=refs);ev.check_current_graph(Path(task)/'capsule',packet,refs)
  src.need(packet['negative_controls']==12 and packet['cutoff20_proved']is False and packet['resource_rows']==5,
   'Whole original early premise join and all12 controls, without a sharp/global result')
  src.need(stdout.splitlines()[-1].split()[1]==src.digest(Path(task)/'capsule'/name),'Actual original premise-join terminal identity')
  return result
 result=ev.check_native_output(Path(task)/'originals',Path(task)/'capsule',spec['id'],stdout,refs)
 if spec['id']in('coarse_b0_construct','coarse_b1_construct','narrow_construct','feedback_b0_construct','feedback_bn_construct'):
  name=spec['created'][0];packet=src.read(Path(task)/'capsule'/name)
  src.need(stdout.splitlines()[-1]==packet['status']+' '+packet['band']+' '+src.digest(Path(task)/'capsule'/name),
   'Exact whole current native INITIAL terminal, literal band and candidate SHA')
 for n in spec['created']:
  if n.endswith('.py'):native.generated_code_identity(Path(task)/'originals',Path(task)/'capsule',n)
 return result
