"""Full original B5 p24/p25 mixed acquisition, fresh primitives and acceptors.

Thirty complete original calls are retained, plus a separately completed D92
primitive transaction. Original native contracts/kernels are immutable. Only
explicit source/reference/capture metadata ports change; historical captures
are never relabelled as newly executed jobs. No kernel runs on import/readback.
"""
from __future__ import annotations
import hashlib,json,re,shutil,sys,uuid,zipfile
from copy import deepcopy
from pathlib import Path,PurePosixPath,PureWindowsPath
from . import n25_full_join_sources as s,n25_full_join_semantics as sem
from . import n25_mixed_sources as src,n25_mixed_contact as contact,n25_mixed_epoch as ports
from . import n25_mixed_dtask as dtask,n25_mixed_primitives as primitives,n25_mixed_stopped as stopped
from . import n25_b5_global_evidence as parent,n25_count_evidence as evidence,reference_graph_epoch as graph,delivery_transport as tx
from . import stopped_prefix as Dtransport
from .colab_batch import atomic_json,event

CONTEXT='MIXED_CONTEXT.json'
PARENT_BRIDGE='CURRENT_B5_PARENT_BINDING.json'
D_BRIDGE='CURRENT_FULL_D92_BINDING.json'
IMMUTABLE_PREFIXES=tuple(f'cutoff25_20261011/new_root/{kind}_b5_p{i}_{version}/'
 for i in(24,25,26)for kind,version in(('global_local_contact','v14'),('global_alpha_stoploss2','v12')))+(src.NATIVE24+'/',)
PRIMITIVE_PREFIXES=tuple('cutoff25_20261013/'+name+'/'for name in dtask.SOURCE_DIRS)
HEX=re.compile('[0-9a-f]{64}\\Z')

def implementation():
 names=sorted(p.name for p in Path(__file__).parent.glob('n25_mixed*.py'))
 names+=['n25_full_join_sources.py','n25_full_join_semantics.py','n25_b5_global_evidence.py',
  'n25_b5_global_sources.py','reference_graph_epoch.py','delivery_transport.py','stopped_prefix.py','action_supervisor.py']
 return {n:s.digest(Path(__file__).parent/n)for n in names}|dict(source_plan=s.PLAN_SHA256,mixed_action_plan=src.PIN)

class References(graph.References):
 """The same typed metadata algebra, including pure Windows source fixtures."""
 def __init__(self,*,old_root,new_root,context_literals=None):
  if not re.match('^[A-Za-z]:',new_root):super().__init__(old_root=old_root,new_root=new_root,context_literals=context_literals);return
  s.need(str(PurePosixPath(old_root))==old_root and old_root.startswith('/')and '..'not in PurePosixPath(old_root).parts,
   'Canonical independently pinned original root')
  p=PureWindowsPath(new_root);s.need(p.is_absolute()and '..'not in p.parts and str(p)==new_root,'One literal actual Windows fixture root')
  self.old_root,self.new_root=old_root,new_root;self.context=dict(context_literals or{});self.hashes={};self.roles={}
 def string(self,value):
  if value in self.hashes:return self.hashes[value]
  if value in self.context:return self.context[value]
  if value==self.old_root:return self.new_root
  if value.startswith(self.old_root+'/')and re.match('^[A-Za-z]:',self.new_root):
   rel=PurePosixPath(value).relative_to(PurePosixPath(self.old_root));s.need('..'not in rel.parts,'Contained literal old reference')
   return str(PureWindowsPath(self.new_root).joinpath(*rel.parts))
  return super().string(value)

def parent_bridge(task):
 task=Path(task);checked=parent.validate_completed(task/'parent');base=parent.root(task/'parent');capsule=task/'capsule'
 files={}
 for stage in parent.sources.stages():
  folder=stage['folder'];source=base/folder;target=capsule/'work/cutoff25_20261011'/folder
  actual={p.name:s.digest(p)for p in source.iterdir()if p.is_file()}
  s.need(all((target/name).is_file()and s.digest(target/name)==pin for name,pin in actual.items()),
   'Every whole current accepted INITIAL/resource source and complete output is unchanged')
  # The source closure also preserves the independently pinned historical
  # SCALAR_SUPPORT_PREFLIGHT comparison vector. It is not an acquired parent
  # and never enters this current-fact bridge.
  files.update({(target/name).relative_to(capsule).as_posix():pin for name,pin in actual.items()})
 extensions={};cache=task/'originals'
 # Independently reconstruct all literal original contact implications. The
 # original source plan and cryptographic p24 recovery are checked elsewhere
 # before originals are admitted; this mathematical view never rewrites them.
 for index in(24,25,26):
  new=f'cutoff25_20261011/new_root/global_local_contact_b5_p{index}_v14'
  old=f'cutoff25_20261011/new_root/global_alpha_stoploss2_b5_p{index}_v12'
  cfg=s.read(cache/new/'contract.json')['rows'][0];original=s.read(cache/old/'contract.json')['rows'][0]
  expected=deepcopy(original);expected.update(local_contact_allowance='5/16',local_contact_premise=deepcopy(sem.CONTACT))
  s.need(sem.same(cfg,expected),'Every current native cfg is exactly its original guards and literal attained-contact premise')
  additions=s.read(cache/new/'LOCAL_CONTACT_V14_ADDITIONS.json')
  for name,pin in s.read(cache/new/'KERNEL_COPY_MANIFEST.json')['files'].items():
   p=capsule/'work'/new/name;s.need(s.digest(p)==pin,'Every entire immutable original mixed native helper')
   files[p.relative_to(capsule).as_posix()]=pin
  for name in('contract.json','KERNEL_COPY_MANIFEST.json','count_protocol.py','SOURCE_PORT.json'):
   p=capsule/'work'/new/name;s.need(p.read_bytes()==(cache/new/name).read_bytes(),'Native contracts, checkers and source history are never metadata-ported')
   files[p.relative_to(capsule).as_posix()]=s.digest(p)
  extensions[str(index)]=dict(capsule='work/'+new,contact_allowance='5/16',premise=deepcopy(sem.CONTACT),finite_feedback_rounds=3,
   rho_upper_rounding_denominator=10**9,original_cfg_sha256=graph.canonical(original),
   new_contract_sha256=s.digest(cache/new/'contract.json'),additions_manifest_sha256=s.digest(cache/new/'LOCAL_CONTACT_V14_ADDITIONS.json'))
 return dict(schema='CURRENT_COMPLETE_ORIGINAL_B5_PARENT_AND_CONTACT_BINDING_V1',initial_covers=13,probability_panels=100,
  contact_allowance='5/16',contact_extensions=extensions,files_sha256=files,parent_readback=checked,
  global_predecessor_license_acquired=False,historical_capture_relabelled=False)

def d_bridge(task):
 task=Path(task);checked=dtask.validate_completed(task/'d92');capsule=task/'capsule';copy=capsule/'current_d92_evidence'
 s.need(stopped.hashes(copy)==stopped.hashes(task/'d92'),'Entire actual D92 export is retained byte-for-byte, including original capture namespaces')
 request=s.read(task/'d92/capsule'/dtask.REQUEST);result=s.read(task/'d92/capsule'/dtask.OUTPUT)
 context=s.read(task/'d92/PREFIX.json')['context'];rows=[];all_aliases={}
 def alias(origin):
  cls=evidence.path_class(context['original_capsule'])
  rel=cls(origin).relative_to(cls(context['original_capsule']))
  s.need(rel.parts and rel.parts[0]=='work'and '..'not in rel.parts,'Every original imported primitive helper is inside its actual own capsule')
  name=Path(*rel.parts).as_posix();p=capsule/name
  original=dtask.mapped(task/'d92',origin,context);s.need(p.is_file()and p.read_bytes()==original.read_bytes(),'A declared relocated module alias preserves every actual original byte')
  return name,s.digest(p)
 for expected,record in zip(request['claims'],result['claims']):
  proof=s.read(dtask.mapped(task/'d92',record['result'],context));statement=expected['statement'];aliases={}
  for row in proof['prefix']['imported_workspace_modules'].values():
   name,pin=alias(row['path']);s.need(pin==row['sha256'],'Actual observed isolated prefix source origin');aliases[name]=pin
  for kind in('chain_imports_before','chain_imports_after'):
   for row in proof[kind].values():
    name,pin=alias(row['path']);s.need(pin==row['sha256'],'Actual observed original feedback source origin');all_aliases[name]=pin
  all_aliases.update(aliases)
  prefix={k:v for k,v in proof['prefix'].items()if k not in('source_sha256','imported_workspace_modules')}
  rows.append(dict(claim_id=statement['claim_id'],source_target_id=statement['source_target_id'],panel=statement['panel'],k=statement['k'],
   box=statement['box'],original_cfg=statement['original_cfg'],selected_method=statement['selected_method'],chain=proof['chain'],
   full_fresh_prefix_mathematical_view=prefix,actual_prefix_original_module_aliases=aliases,
   actual_original_prefix_module_observations=proof['prefix']['imported_workspace_modules']))
 return dict(schema='CURRENT_FULL92_GENUINE_PRIMITIVE_TRANSPORT_BRIDGE_V1',complete_original_D92_primitive_readback=True,
  original_D92_readback=checked,files_sha256={p.relative_to(capsule).as_posix():s.digest(p)for p in copy.rglob('*')if p.is_file()},
  claims=rows,unchanged_original_module_aliases=all_aliases,compatibility_view_is_derived_not_a_capture=True,
  historical_capture_relabelled=False,full66_complete=False)

def _raws(task):
 manifest=s.read(Path(task)/CONTEXT);result={};p=s.plan()
 for name,pin in manifest['original_files'].items():
  path=Path(task)/'originals'/name;s.need(path.is_file()and s.digest(path)==pin,'Every entire independently pinned original mixed input')
  if name in p['files']:s.need(pin==p['files'][name]['sha256'],'Whole source belongs to the sealed original archive plan')
  else:s.need(pin in p['historical_reference_pins'].get(name,[]),'Only exact independently SHA-recovered original source is additional')
  result[name]=path.read_bytes()
 return result

def _prune(value,available,*,removed,path=()):
 if type(value)is dict:
  out={}
  for key,item in value.items():
   if type(key)is str and type(item)is str and HEX.fullmatch(item):
    logical=src.logical(key)
    old_capture=key.startswith(src.OLD_ROOT+'/runs/')or key.startswith('runs/')or key.endswith(('.metadata.json','.stdout.txt','.stderr.txt'))
    old_local=(key[len(src.OLD_ROOT)+1:]if key.startswith(src.OLD_ROOT+'/')else key if key.startswith('work/')else None)
    if old_capture or(logical is not None and 'work/'+logical not in available)or(old_local is not None and old_local not in available):
     removed.append(dict(path=list(path)+[key],old_sha256=item,reason='retired_historical_transport_identity_not_a_current_fact'));continue
   out[key]=_prune(item,available,removed=removed,path=path+(key,))
  return out
 if type(value)is list:return[_prune(x,available,removed=removed,path=path+(i,))for i,x in enumerate(value)]
 return value

def _held(task,state):
 capsule=Path(task)/'capsule';result=set()
 def walk(obj):
  if type(obj)is dict:
   for key,value in obj.items():
    if key in('source_sha256','files_sha256')and type(value)is dict:
     for name,pin in value.items():
      if type(name)is str and type(pin)is str:
       try:p=stopped.mapped(task,name,state['context'])
       except(ValueError,TypeError):continue
       if p.is_relative_to(capsule)and p.is_file()and s.digest(p)==pin:result.add(p.relative_to(capsule).as_posix())
    walk(value)
  elif type(obj)is list:
   for x in obj:walk(x)
 for item in state['actions']:
  spec=next(x for x in src.plan()['actions']if x['id']==item['action'])
  for name in spec['outputs']:walk(s.read(capsule/name))
 return result

def _epoch(task,state,spec):
 capsule=Path(task)/'capsule';originals=_raws(task);context=state['context'];oldroot=src.OLD_ROOT
 newroot=stopped.original(context,'capsule');refs=References(old_root=oldroot,new_root=newroot,
  context_literals={src.OLD_PYTHON:context['python_executable'],
   'work/optimized301_20260927/tools/log_command.py':'transport/launch_mixed_action.py'})
 available=stopped.hashes(capsule);held=_held(task,state);mutable={};reports={}
 # Current facts are registered ONLY after their complete independent reader.
 bridge=parent_bridge(task);parent_pin=graph.canonical(bridge['parent_readback']);source_plan=s.plan()
 for name,pin in bridge['files_sha256'].items():
  logical=name.removeprefix('work/');old=source_plan['files'].get(logical,{}).get('sha256')
  pins=[old]if old else source_plan['historical_reference_pins'].get(logical,[])
  for prior in pins:refs.add(prior,pin,role='validated_current_result',evidence_sha256=parent_pin)
 for item in state['actions']:
  row=next(x for x in src.plan()['actions']if x['id']==item['action'])
  refs.add(row['output_reference_sha256'],s.digest(capsule/row['outputs'][0]),role='validated_current_result',
   evidence_sha256=item['validated_output']['receipt_sha256'])
 for name,raw in originals.items():
  rel='work/'+name;p=capsule/rel
  protected=(rel in bridge['files_sha256']or name.startswith(IMMUTABLE_PREFIXES)
   or(name.startswith(PRIMITIVE_PREFIXES)and name.endswith('.py'))or name in src.OPAQUE_HISTORY or name in src.SOURCE_HISTORY)
  if protected or rel in held:
   current=p.read_bytes();old=hashlib.sha256(raw).hexdigest();new=hashlib.sha256(current).hexdigest()
   if old!=new:refs.add(old,new,role='derived_source_metadata'if name.endswith('.py')else'derived_graph_metadata')
   continue
  if name.endswith('.json'):
   removed=[];value=json.loads(raw,object_pairs_hook=s.base.unique);value=_prune(value,available,removed=removed)
   projected=raw if not removed else graph.dump(value);reports[name]=dict(retired_historical_transport_edges=removed)
  else:projected=raw
  mutable[name]=projected
 current,report=ports.reference_epoch(mutable,refs)
 changes={}
 for name,raw in current.items():
  rel='work/'+name
  if not(capsule/rel).is_file()or(capsule/rel).read_bytes()!=raw:changes[rel]=raw
 return changes,dict(schema='FULL66_EXPLICIT_CURRENT_MIXED_STAGE_SOURCE_EPOCH_V1',original_program_projection=report,
  retired_historical_transport=reports,already_acquired_source_files_frozen=sorted(held),
  mathematical_native_contracts_and_kernels_changed=False,historical_execution_relabelled=False)

def _mathematical_view(obj):
 if type(obj)is dict:return{k:_mathematical_view(v)for k,v in obj.items()if k not in('seconds','source_sha256','files_sha256','module_origins')}
 if type(obj)is list:return[_mathematical_view(x)for x in obj]
 return obj

class Adapter:
 def identity(self):return dict(schema='FULL66_COMPLETE_THIRTY_CALL_MIXED_ADAPTER_V1',**implementation())
 def specs(self,context):
  return src.specs(stopped.original(context,'capsule'))
 def validate_initial(self,task,state):
  task=Path(task);s.need(state['context']['implementation']==implementation(),'Exact current full mixed implementation epoch')
  originals=_raws(task);manifest=s.read(task/CONTEXT)
  s.need(set(originals)==set(manifest['source_closure']['files'])
   and all(hashlib.sha256(raw).hexdigest()==manifest['source_closure']['files'][name]for name,raw in originals.items()),
   'Every unchanged original source closure and cryptographic source recovery')
  for row in src.plan()['actions']:
   s.need(row['script_member']in originals and hashlib.sha256(originals[row['script_member']]).hexdigest()==row['script_sha256'],
    'All30 full original programs are present, never synthetic arithmetic replacements')
   p=task/'references'/(row['id']+'.json');s.need(s.digest(p)==row['output_reference_sha256'],
    'Original whole mathematical output is an immutable comparison vector only')
  c=task/'capsule';s.need((c/'transport/launch_mixed_action.py').read_bytes()==Path(stopped.worker.__file__).read_bytes(),
   'Exact independently pinned whole-capsule original-child relay')
  s.need(sem.same(s.read(c/PARENT_BRIDGE),parent_bridge(task))and sem.same(s.read(c/D_BRIDGE),d_bridge(task)),
   'Actual complete B5 parent and all92 primitive stopped evidence, not metadata self-attestation')
  return manifest
 def epoch(self,task,state,spec):return _epoch(task,state,spec)
 def capture_inputs(self,task,spec):
  return {p.name:s.digest(p)for p in(Path(task)/'capsule'/spec['cwd']).iterdir()if p.is_file()}
 def copy_validation_context(self,source,target):
  source=Path(source);target=Path(target)
  for name in('parent','d92','originals','references'):shutil.copytree(source/name,target/name)
  shutil.copyfile(source/CONTEXT,target/CONTEXT)
 def validate_output(self,task,state,spec,item,stdout):
  task=Path(task);capsule=task/'capsule';row=next(x for x in src.plan()['actions']if x['id']==spec['id'])
  actual=s.read(capsule/spec['outputs'][0]);old=s.read(task/'references'/(spec['id']+'.json'))
  s.need(actual['status']==row['expected_status'],'Exact complete original mixed action terminal scope')
  # The source epoch explicitly records all admitted path/SHA identities.
  roles=item['source_epoch']['original_program_projection']['registered_reference_graph']['references']['identity_roles']
  refs=References(old_root=src.OLD_ROOT,new_root=stopped.original(state['context'],'capsule'),
   context_literals={src.OLD_PYTHON:state['context']['python_executable']})
  for before,entry in roles.items():refs.add(before,entry['current'],role=entry['role'],evidence_sha256=entry['evidence_sha256'])
  expected=refs.value(old)
  s.need(sem.same(_mathematical_view(actual),_mathematical_view(expected)),
   'Every entire original mathematical field, tree result, statement, domain, scalar/native count and negative control is freshly reproduced')
  s.need(stdout.strip()and actual['status']in stdout,'Actual whole original stopped stdout contains its exact terminal')
  def bound(obj):
   if type(obj)is dict:
    for key,value in obj.items():
     if key in('source_sha256','files_sha256')and type(value)is dict:
      for name,pin in value.items():
       if not(type(name)is str and type(pin)is str and HEX.fullmatch(pin)):continue
       p=stopped.mapped(task,name,state['context'])if name.startswith(stopped.original(state['context'],'capsule'))else capsule.joinpath(*tx.parts(name))
       s.need(p.is_relative_to(capsule)and p.is_file()and s.digest(p)==pin,'Every actual whole original source/current-parent binding')
     bound(value)
   elif type(obj)is list:
    for value in obj:bound(value)
  bound(actual)
  summary=dict(action=spec['id'],receipt_sha256=s.digest(capsule/spec['outputs'][0]),status=actual['status'],
   whole_original_mathematical_payload_reproduced=True,historical_capture_relabelled=False,full66_complete=False)
  if spec['id']in('p24-full_acceptance','p25-full_acceptance'):
   index=24 if spec['id'].startswith('p24-')else 25;cfg=actual['original_cfg']
   binding=dtask.parent_binding(task/'parent');global_proof=s.read(task/'parent'/binding['resource_relative'])
   edge=sem.resource_interface(global_proof['rows'][index]['result'],cfg,rho=['3/2','33/20'],index=index)
   summary.update(index=index,same_original_cfg_current_resource_interface=True,resource_interface=edge,
    evidence_sha256=summary['receipt_sha256'],statistics=actual['statistics'])
  return summary

def prepare(cache,task,*,parent_task,d92_task):
 task=tx.ordinary(task);s.need(not task.exists(),'Exclusive full original mixed task');capsule=task/'capsule';capsule.mkdir(parents=True)
 shutil.copytree(parent_task,task/'parent');shutil.copytree(d92_task,task/'d92');dtask.validate_completed(task/'d92')
 raw,closure=src.closure(cache)
 for name,value in raw.items():
  for base in(task/'originals',capsule/'work'):
   p=base/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(value)
 for stage in parent.sources.stages():
  folder=stage['folder'];source=parent.root(task/'parent')/folder;dest=capsule/'work/cutoff25_20261011'/folder
  dest.mkdir(parents=True,exist_ok=True)
  for p in source.iterdir():
   if p.is_file():shutil.copyfile(p,dest/p.name)
 shutil.copytree(task/'d92',capsule/'current_d92_evidence')
 p=capsule/'transport/launch_mixed_action.py';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(Path(stopped.worker.__file__).read_bytes())
 (task/'references').mkdir()
 for row in src.plan()['actions']:shutil.copyfile(s.source(cache,row['output_reference_member']),task/'references'/(row['id']+'.json'))
 atomic_json(task/CONTEXT,dict(schema='FULL66_COMPLETE_ORIGINAL_MIXED_TASK_CONTEXT_V1',source_closure=closure,
  original_files={name:hashlib.sha256(value).hexdigest()for name,value in raw.items()},implementation=implementation()))
 atomic_json(capsule/PARENT_BRIDGE,parent_bridge(task));atomic_json(capsule/D_BRIDGE,d_bridge(task))
 stopped.begin(task,adapter=Adapter(),context=dict(unit='66.full-mixed',implementation=implementation()))
 return task

def validate_prefix(task):return stopped.validate(task,adapter=Adapter())
def validate_completed(task):
 checked=validate_prefix(task);s.need(checked['all_original_actions_completed']is True,'All30 complete original mixed source actions')
 state=stopped.read(Path(task)/stopped.PREFIX);panels={str(item['validated_output']['index']):item['validated_output']for item in state['actions']if 'index'in item['validated_output']}
 s.need(set(panels)=={'24','25'},'Both whole original E24 and finite coupled ABCDF25 mixed acceptances')
 return dict(checked,mixed_panels=panels,d92_summary=dtask.validate_completed(Path(task)/'d92'),
  full66_complete=False,full_n25_verified=False,all_index_conclusion_verified=False)

def _save(task,directory):
 checked=validate_prefix(task);directory=tx.ordinary(directory);directory.mkdir(parents=True,exist_ok=True)
 name=str(checked['completed_actions']).zfill(2)+'-'+uuid.uuid4().hex[:12]+'-mixed-complete.zip';out=directory/name
 with zipfile.ZipFile(out,'x',zipfile.ZIP_DEFLATED,strict_timestamps=False)as z:
  for p in sorted(Path(task).rglob('*')):
   tx.ordinary(p)
   if p.is_file():z.write(p,p.relative_to(task).as_posix())
  tx.zip_members(z,max_total=stopped.DISK,max_members=250000)
 pin=s.digest(out);out.with_suffix('.zip.sha256').write_text(pin+'  '+out.name+'\n',encoding='ascii');return dict(path=str(out),sha256=pin)

def _restore(directory,destination,log):
 directory=Path(directory)
 if not directory.exists():return None
 for p in sorted(directory.glob('*-mixed-complete.zip'),reverse=True):
  try:
   tx.ordinary(p);pin=s.digest(p);s.need(p.stat().st_size<=4*1024**3 and p.with_suffix('.zip.sha256').read_text('ascii')==pin+'  '+p.name+'\n','Whole append-only mixed prefix ZIP and exactSHA')
   out=Path(destination)/('mixed-restored-'+uuid.uuid4().hex[:12]);out.mkdir(parents=True)
   with zipfile.ZipFile(p)as z:
    for row in tx.zip_members(z,max_total=stopped.DISK,max_members=250000):
     target=out.joinpath(*tx.parts(row.filename));target.parent.mkdir(parents=True,exist_ok=True)
     with z.open(row)as source,target.open('xb')as dest:shutil.copyfileobj(source,dest,tx.MIB)
   checked=validate_prefix(out);log('full66_mixed_prefix_revalidated',completed=checked['completed_actions'],cache=str(p));return out,checked
  except Exception as error:log('full66_mixed_cache_rejected',cache=str(p),error=type(error).__name__+': '+str(error))
 return None

def run_component(cache,task,*,durable_root,work_root,parent_task,log_root):
 task=tx.ordinary(task);base=tx.ordinary(work_root);parent_state=dtask.parent_binding(parent_task)
 key=graph.canonical(dict(implementation=implementation(),actual_parent=parent_state))[:24]
 durable=Path(durable_root)/'n25-full-mixed'/key;log=lambda name,**fields:event(log_root,name,**fields)
 hit=tx.restore(durable/'D92',task.parent/'D92-imports',validator=dtask.validate_completed,log=log)
 if hit:d92_task=hit[0]
 else:
  d92_task=task.parent/('D92-'+uuid.uuid4().hex[:8]);dtask.prepare(cache,d92_task,parent_task=parent_task)
  Dtransport.advance(d92_task,adapter=dtask.Adapter().bind(d92_task),root=log_root)
  dtask.validate_completed(d92_task);tx.save(d92_task,durable/'D92',validator=dtask.validate_completed,label='full92-primitives')
 restored=_restore(durable/'prefixes',task.parent/'mixed-imports',log)
 if restored:
  candidate,checked=restored;state=stopped.read(candidate/stopped.PREFIX)
  origin=tx.ordinary(state['context']['original_task_root'])
  s.need(origin.is_relative_to(base)and origin!=base and len(origin.relative_to(base).parts)>=3,
   'Resume only this recorded owned full-mixed native transaction beneath the configured runtime tree')
  if origin.exists():
   existing=stopped.read(origin/stopped.PREFIX)
   s.need(existing['context']==state['context']and existing['initial_capsule_sha256']==state['initial_capsule_sha256'],
    'Never replace an unrelated task while preserving interrupted numerical work')
   origin.rename(origin.with_name(origin.name+'-preserved-interrupted-'+uuid.uuid4().hex[:8]))
  origin.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(candidate,origin);active=origin
 else:active=prepare(cache,task,parent_task=parent_task,d92_task=d92_task)
 adapter=Adapter();saved=None
 while len(stopped.read(active/stopped.PREFIX)['actions'])<30:
  stopped.advance(active,adapter=adapter,root=log_root);saved=_save(active,durable/'prefixes')
 checked=validate_completed(active)
 if active!=task:
  s.need(not task.exists(),'Separate final current-session copy, without overwriting any owned evidence');shutil.copytree(active,task);checked=validate_completed(task)
 return dict(task=task,validated=checked,cache=saved)
