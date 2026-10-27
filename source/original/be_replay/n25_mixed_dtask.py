"""Source preparation, bounded execution and pure readback of full D92.

This action is separate from the original zero-new-scalar D registry writer.
It binds that writer's every selected saved claim to an entire fresh primitive
replay. Source preparation and completed validation never import a kernel.
"""
from __future__ import annotations
import json,shutil,sys,uuid
from pathlib import Path
from . import n25_full_join_sources as s,n25_mixed_primitives as primitives
from . import n25_recovery_sources as recovery,delivery_transport as tx
from . import n25_b5_global_evidence as b5,n25_full_join_semantics as sem
from . import stopped_prefix as stopped
from .colab_batch import atomic_json

BASE='work/cutoff25_20261013/'
OUTPUT='FULL_D92_PRIMITIVES.json'
REQUEST='D92_REQUEST.json'
SOURCE_DIRS=(
 'archive_audit/normalized_defect_frontier_v1','archive_audit/support_coupled_frontier_v1',
 'archive_audit/joint_contact_preflight_v1','archive_audit/affine_contact_cell_v1',
 'archive_audit/normalized_defect_rho_v1','archive_audit/pointwise_finished_prefix_v1',
 'low/pointwise_inward_defect_v2','low/tighter_ratio_rho_v1','b5/defect_rho_cap_v1')
COLLECTION='cutoff25_20261013/archive_audit/saved_scalar_rectangle_acquisition_v1/CONDITIONAL_RECTANGLES.json'

def original_name(value):
 value=value.replace('\\','/')
 if '/work/cutoff25_'in value:value=value.split('/work/',1)[1]
 elif value.startswith('work/'):value=value[5:]
 s.need(value.startswith('cutoff25_'),'One original n25 primitive reference');return value

def source_members():
 result={}
 for name,row in s.plan()['files'].items():
  if (any(name.startswith('cutoff25_20261013/'+d+'/')and '/'not in name[len('cutoff25_20261013/'+d+'/'):]for d in SOURCE_DIRS)
      and name.endswith(('.py','.txt','.tex'))):result[name]=row
 return result

def parent_binding(parent_task):
 checked=b5.validate_completed(parent_task);root=b5.root(parent_task);stages=b5.sources.stages()
 initial=root/stages[0]['folder']/stages[0]['proof'];resource=root/stages[1]['folder']/stages[1]['proof']
 ip,rp=s.read(initial),s.read(resource)
 s.need(ip['support']['q']=='5/16'and len(rp['rows'])==100 and len(ip['stages'])==12,
  'All original13 INITIAL covers and100 conditional resource acquisitions')
 return dict(summary=checked,initial_sha256=s.digest(initial),resource_sha256=s.digest(resource),
  initial_relative=initial.relative_to(parent_task).as_posix(),resource_relative=resource.relative_to(parent_task).as_posix(),
  contact_allowance='5/16',global_predecessor_license_acquired=False)

def prepare(cache,task,*,parent_task,archive=recovery.DEFAULT_ARCHIVE):
 task=tx.ordinary(task);s.need(not task.exists(),'Exclusive full D primitive epoch');capsule=task/'capsule';capsule.mkdir(parents=True)
 parent=task/'parent';shutil.copytree(parent_task,parent);binding=parent_binding(parent)
 for name,row in source_members().items():
  path=capsule/'work'/name;path.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(s.source(cache,name),path)
 with recovery.RecoveryArchive(archive)as asset:
  for index in(24,25,26):
   target=f'b5-p{index}-mixed-parent-v14-original'if index in(24,25)else'b5-p26-v14-original'
   profile=recovery.profile(target);dest=capsule/'work'/profile['member_prefix'].rstrip('/')
   # Primitive replay needs the complete original source/contract, not an
   # ordinary forest. Do not unpack/census a122MB forest just to obtain98
   # already independently pinned source files.
   dest.mkdir(parents=True,exist_ok=True)
   for name,row in profile['files'].items():(dest/name).write_bytes(asset.read(profile['member_prefix']+name,row))
   rp=s.read(parent/binding['resource_relative']);cfg=s.read(dest/'contract.json')['rows'][0]
   sem.resource_interface(rp['rows'][index]['result'],cfg,rho=['3/2','33/20'],index=index)
 collection=s.read(s.source(cache,COLLECTION));claims=[];reference=capsule/'references';reference.mkdir()
 for i,statement in enumerate(collection['statements']):
  n=original_name(statement['source_result_path']);source=s.source(cache,n)
  s.need(s.digest(source)==statement['source_result_sha256'],'Exact original whole saved chain/prefix candidate')
  p=reference/(str(i).zfill(3)+'-original-result.json');shutil.copyfile(source,p);point=None
  if statement['source_pointwise_path']is not None:
   name=original_name(statement['source_pointwise_path']);old=s.source(cache,name)
   s.need(s.digest(old)==statement['source_pointwise_sha256'],'Whole original selected pointwise candidate collection')
   point=reference/(str(i).zfill(3)+'-original-pointwise.json');shutil.copyfile(old,point)
  claims.append(dict(statement=statement,reference_result=str(p),reference_pointwise=None if point is None else str(point)))
 shutil.copyfile(s.source(cache,COLLECTION),reference/'ORIGINAL_D_COLLECTION.json')
 sources={str(p):s.digest(p)for sub in('work','references')for p in(capsule/sub).rglob('*')if p.is_file()}
 request=dict(schema='CURRENT_SAME_LAW_FULL92_D_PRIMITIVE_REQUEST_V1',workspace=str(capsule),sources=sources,claims=claims,
  original_collection_sha256=s.digest(s.source(cache,COLLECTION)),parent_binding=binding,
  historical_scalar_candidates_are_fresh=False,all_claim_primitives_must_be_recomputed=True)
 atomic_json(capsule/REQUEST,request)
 context=dict(unit='66.D92',runtime_root=str(s.ROOT),implementation=implementation(),original_capsule=str(capsule))
 (capsule/'REPLAY_D92.py').write_bytes(worker_source(context))
 atomic_json(task/'D92_CONTEXT.json',context)
 stopped.begin(task,adapter=Adapter(),context=context);return task

def implementation():
 return {n:s.digest(Path(__file__).parent/n)for n in('n25_mixed_dtask.py','n25_mixed_primitives.py','n25_full_join_sources.py',
  'n25_full_join_semantics.py','n25_recovery_sources.py','n25_count_evidence.py','n25_b5_global_evidence.py',
  'n25_b5_global_sources.py','delivery_transport.py','stopped_prefix.py','action_supervisor.py',
  'finite69_remaining.py','finite2024_join_scalar.py')}|dict(source_plan=s.PLAN_SHA256,recovery_source_plan=recovery.PLAN_SHA256)

def worker_source(context):
 from .n25_count_evidence import path_class
 origin=path_class(context['original_capsule'])(context['original_capsule'])
 return ("import sys\nsys.path.insert(0,"+repr(context['runtime_root'])+")\nfrom be_replay.n25_mixed_primitives import run\n"
  +"run("+repr(str(origin/REQUEST))+","+repr(str(origin/OUTPUT))+")\n").encode()

def output_names(request):
 names=[OUTPUT]
 for i,item in enumerate(request['claims']):
  stem=str(i).zfill(3);base='FULL_D92_PRIMITIVES/'+stem
  names += [base+'-input.json',base+'-result.json',base+'.stdout.txt',base+'.stderr.txt',
   base+'-result.prefix-input.json',base+'-result.prefix.stdout.txt',base+'-result.prefix.stderr.txt']
  if item['statement']['selected_method']=='POINTWISE_EMPTY':names += [base+'-result.pointwise-input.json',
   base+'-result.pointwise.stdout.txt',base+'-result.pointwise.stderr.txt']
 return names

class Adapter:
 def identity(self):return dict(schema='FULL66_D92_FRESH_PRIMITIVE_ADAPTER_V1',**implementation())
 def specs(self):
  # Dynamic output inventory is materialized once by this bound context.
  s.need(hasattr(self,'_spec'),'D92 adapter must be bound to its exact request');return[self._spec]
 def bind(self,task):
  request=s.read(Path(task)/'capsule'/REQUEST)
  self._spec=dict(id='full92-D-primitives',cwd='',argv=['{python}','-B','-S','REPLAY_D92.py'],outputs=output_names(request))
  return self
 def validate_initial(self,task,state):
  self.bind(task);s.need(state['context']['implementation']==implementation(),'Exact complete primitive implementation')
  request=s.read(Path(task)/'capsule'/REQUEST);s.need(request['schema']=='CURRENT_SAME_LAW_FULL92_D_PRIMITIVE_REQUEST_V1'
   and request['historical_scalar_candidates_are_fresh']is False and request['all_claim_primitives_must_be_recomputed']is True,
   'Saved results are candidates, never fresh inputs')
  binding=parent_binding(Path(task)/'parent');s.need(evidence_same(binding,request['parent_binding']),'Actual whole B5 resource/INITIAL remains bound')
  expected=set(p.relative_to(Path(task)/'capsule').as_posix()for sub in('work','references')
   for p in(Path(task)/'capsule'/sub).rglob('*')if p.is_file())|{REQUEST,'REPLAY_D92.py'}
  s.need(set(state['initial_inventory'])==expected,'No extra initial primitive helper or omitted request/source')
  validate_request(task,request,state['context'])
  return request
 def validate_live(self,task,state):self.validate_initial(task,state)
 def prepare_action(self,task,state,spec):return dict(no_original_mathematical_source_edit=True)
 def validate_epoch(self,task,state,spec,item):self.validate_initial(task,state);s.need(item['source_changes']=={},'No primitive source mutation')
 def capture_inputs(self,task,spec):return {p.name:s.digest(p)for p in(Path(task)/'capsule').iterdir()if p.is_file()}
 def copy_validation_context(self,source,target):
  shutil.copytree(Path(source)/'parent',Path(target)/'parent');shutil.copyfile(Path(source)/'D92_CONTEXT.json',Path(target)/'D92_CONTEXT.json')
 def validate_output(self,task,state,spec,item,stdout):return validate_output(task,state['context'],stdout)

def evidence_same(a,b):
 from .n25_count_evidence import same
 return same(a,b)

def mapped(task,value,context):
 from . import n25_count_evidence as e
 origin=e.path_class(context['original_capsule'])(context['original_capsule'])
 rel=e.relative(value,origin);return s.tx.ordinary(Path(task)/'capsule'/rel)

def validate_request(task,request,context):
 """Reconstruct all92 source→claim edges from the externally pinned source."""
 capsule=Path(task)/'capsule';collection=capsule/'references/ORIGINAL_D_COLLECTION.json'
 s.need(request['workspace']==context['original_capsule']and context['unit']=='66.D92'
  and (capsule/'REPLAY_D92.py').read_bytes()==worker_source(context),
  'Exact complete declared primitive worker, import origin and originating request/output')
 s.need(s.digest(collection)==s.plan()['files'][COLLECTION]['sha256']==request['original_collection_sha256'],
  'Entire independent original92-statement collection is unchanged')
 original=s.read(collection)['statements'];s.need(len(original)==len(request['claims'])==92,'All92 original selected claims')
 expected_files={p.relative_to(capsule).as_posix():s.digest(p)for sub in('work','references')for p in(capsule/sub).rglob('*')if p.is_file()}
 current={mapped(task,p,context).relative_to(capsule).as_posix():h for p,h in request['sources'].items()}
 s.need(expected_files==current,'Whole original primitive/reference source inventory, no unbound comparison file')
 profiles={recovery.profile(t)['member_prefix'].rstrip('/'):recovery.profile(t)
  for t in('b5-p24-mixed-parent-v14-original','b5-p25-mixed-parent-v14-original','b5-p26-v14-original')}
 for name,pin in expected_files.items():
  if not name.startswith('work/'):continue
  member=name[5:];allowed=s.plan()['files'].get(member)
  if any(member.startswith(prefix+'/')for prefix in profiles):
   prefix=next(prefix for prefix in profiles if member.startswith(prefix+'/'));filename=member[len(prefix)+1:]
   allowed=profiles[prefix]['files'].get(filename)
  s.need(allowed is not None and allowed['sha256']==pin,'Every actual primitive/helper/native source has an external original pin')
 rp=s.read(Path(task)/'parent'/request['parent_binding']['resource_relative'])
 for want,entry in zip(original,request['claims']):
  s.need(evidence_same(want,entry['statement']),'Full literal original D statement, not a producer-selected replacement')
  ref=mapped(task,entry['reference_result'],context);s.need(request['sources'].get(entry['reference_result'])==want['source_result_sha256']==s.digest(ref),
   'Exact bound whole original scalar candidate, never an external/unbound path')
  if want['source_pointwise_path']is None:s.need(entry['reference_pointwise']is None,'No extra pointwise assumption')
  else:
   point=mapped(task,entry['reference_pointwise'],context)
   s.need(request['sources'].get(entry['reference_pointwise'])==want['source_pointwise_sha256']==s.digest(point),
    'Exact bound whole selected pointwise candidate')
  cfg=s.read(capsule/f"work/cutoff25_20261011/new_root/global_local_contact_b5_p{want['panel']}_v14/contract.json")['rows'][0]
  s.need(evidence_same(cfg,want['original_cfg']),'Same complete original conditional cfg')
  sem.resource_interface(rp['rows'][want['panel']]['result'],cfg,rho=['3/2','33/20'],index=want['panel'])
 return True

def validate_output(task,context,stdout):
 """Pure whole-result admission: no feedback/project/upper is imported."""
 from . import n25_count_evidence as e
 capsule=Path(task)/'capsule';request=s.read(capsule/REQUEST);result=s.read(capsule/OUTPUT)
 s.need(result['schema']=='FULL92_FRESH_ORIGINAL_D_PRIMITIVES_V1'and type(result['claim_count'])is int
  and result['claim_count']==len(result['claims'])==len(request['claims'])==92 and type(result['native_count_calls'])is int and result['native_count_calls']==0
  and result['all_feedback_prefix_normalized_and_selected_pointwise_recomputed']is True and result['full66_complete']is False,
  'Every92 original full primitive proofs, not a status-only saved D collection')
 validate_request(task,request,context)
 def local(value):return mapped(task,value,context)
 s.need(result['request_sha256']==s.digest(capsule/REQUEST)and evidence_same(result['source_sha256'],request['sources']),
  'One immutable exact primitive request/source epoch')
 for name,pin in request['sources'].items():s.need(s.digest(local(name))==pin,'Every actual original primitive source still exact')
 from .n25_count_evidence import path_class
 origin=path_class(context['original_capsule'])(context['original_capsule'])
 for ordinal,(expected,record)in enumerate(zip(request['claims'],result['claims'])):
  stem=str(ordinal).zfill(3);base=origin/'FULL_D92_PRIMITIVES';input_name=base/(stem+'-input.json');result_name=base/(stem+'-result.json')
  s.need(record['command']==[context['python_executable'],'-B','-S','-m','be_replay.n25_mixed_primitives','--claim',str(input_name),str(result_name)]
   and record['result']==str(result_name),'Exact actual per-claim isolated interpreter and original result slot')
  s.need(e.same(s.read(local(str(input_name))),dict(request=request,entry=expected))and record['input_sha256']==s.digest(local(str(input_name))),
   'Whole actual bound child input, without a dropped mathematical premise')
  for key in('stdout','stderr'):
   stream=local(str(base/(stem+'.'+key+'.txt')))
   s.need(record[key+'_sha256']==s.digest(stream),'Every complete actual child stream and recorded digest')
   if key=='stderr':s.need(stream.stat().st_size==0,'Empty successful child stderr')
   else:s.need(stream.read_text('utf-8').strip()=='D_CLAIM_COMPLETE','Actual exact claim-worker terminal')
  p=local(record['result']);proof=s.read(p);statement=expected['statement'];old=s.read(local(expected['reference_result']))
  s.need(record['claim_id']==statement['claim_id']and record['sha256']==s.digest(p)and type(record['returncode'])is int
   and record['returncode']==0 and proof['claim_id']==statement['claim_id']and proof['panel']==statement['panel']
   and proof['k']==statement['k']and e.same(proof['box'],statement['box'])and e.same(proof['original_cfg'],statement['original_cfg'])
   and proof['selected_method']==statement['selected_method']and type(proof['native_count_calls'])is int and proof['native_count_calls']==0
   and proof['schema']=='FULL_FRESH_SAME_CFG_D_SCALAR_CLAIM_V1'and proof['full_feedback_recomputed']is True
   and proof['full_prefix_recomputed']is True and proof['full_pointwise_recomputed']is(statement['selected_method']=='POINTWISE_EMPTY')
   and e.same(proof['sources_sha256'],request['sources']),
   'Exact current same-cfg/count closed D rectangle and actual child success')
  s.need(primitives.equivalent(proof['chain'],old['chain'])and primitives.equivalent(proof['prefix'],old['prefix_result'],root=True),
   'Whole freshly reproduced original chain and normalized scalar proof')
  prefix_input=local(str(result_name.with_suffix('.prefix-input.json')))
  s.need(e.same(s.read(prefix_input),dict(request=request,entry=expected,chain=proof['chain'],candidate=proof['chain']['candidate_cfg'])),
   'Fresh feedback output supplies every exact isolated scalar-prefix premise')
  prefix_stdout=local(str(result_name.with_suffix('.prefix.stdout.txt')));prefix_stderr=local(str(result_name.with_suffix('.prefix.stderr.txt')))
  s.need(prefix_stderr.stat().st_size==0 and e.same(s.read(prefix_stdout),proof['prefix']),
   'The entire fresh scalar prefix/normalized result is its actual stopped child output')
  s.need(e.same(proof['prefix']['source_sha256'],request['sources']),'Whole fresh prefix source inventory')
  origins=proof['prefix']['imported_workspace_modules']
  s.need(type(origins)is dict and origins and 'optimized_arithmetic'not in origins
   and origins['exact35_core']['path']==str(origin/f"work/cutoff25_20261011/new_root/global_local_contact_b5_p{statement['panel']}_v14/exact35_core.py")
   and origins['prefix_project']['path']==str(origin/'work/cutoff25_20261013/archive_audit/normalized_defect_frontier_v1/prefix_project.py'),
   'The original independent D review requires the actual isolated native scalar prefix module origins')
  allowed_prefix={str(origin/f"work/cutoff25_20261011/new_root/global_local_contact_b5_p{statement['panel']}_v14"),
   str(origin/'work/cutoff25_20261013/archive_audit/normalized_defect_frontier_v1'),
   str(origin/'work/cutoff25_20261013/archive_audit/normalized_defect_rho_v1')}
  for row in origins.values():
   s.need(request['sources'].get(row['path'])==row['sha256']==s.digest(local(row['path'])),
    'All isolated prefix/normalized module origins have the actual exact original source')
   s.need(str(e.path_class(row['path'])(row['path']).parent)in allowed_prefix,
    'Every actual original isolated prefix helper stays in exactly the three reviewed native/normalized directories')
  if statement['selected_method']=='POINTWISE_EMPTY':
   collection=s.read(local(expected['reference_pointwise']));matches=[r for r in collection['rows']
    if r['index']==statement['panel']and r['target']['id']==statement['source_target_id']]
   s.need(len(matches)==1 and e.same(proof['pointwise'],matches[0]['result']),'Whole fresh strict pointwise proof')
   point_input=local(str(result_name.with_suffix('.pointwise-input.json')))
   s.need(e.same(s.read(point_input),dict(request=request,entry=expected,row=dict(old,chain=proof['chain'],prefix_result=proof['prefix']))),
    'The pointwise worker consumes that exact fresh chain and complete prefix')
   ps=local(str(result_name.with_suffix('.pointwise.stdout.txt')));pe=local(str(result_name.with_suffix('.pointwise.stderr.txt')))
   point=s.read(ps);s.need(pe.stat().st_size==0 and point['status']=='POINTWISE_EMPTY'and e.same(point['result'],proof['pointwise']),
    'Full actual fresh pointwise output and strict contradiction')
   point_origins=point['imported_original_modules']
   s.need(type(point_origins)is dict and point_origins
    and point_origins['_n25_D_pointwise_interface']['path']==str(origin/'work/cutoff25_20261013/archive_audit/pointwise_finished_prefix_v1/interface.py')
    and point_origins['pointwise_inward_v2']['path']==str(origin/'work/cutoff25_20261013/low/pointwise_inward_defect_v2/pointwise_inward_v2.py'),
    'Actual isolated original pointwise interface and full strict cap module origins')
   for row in point_origins.values():
    s.need(request['sources'].get(row['path'])==row['sha256']==s.digest(local(row['path'])),'Every actual isolated pointwise module')
  else:s.need(proof['pointwise']is None,'No undeclared pointwise route replaces a selected prefix/normalized rule')
  for key in('chain_imports_before','chain_imports_after'):
   s.need(type(proof[key])is dict and proof[key],'Actual imported original-module origin audit')
   s.need(not set(proof[key])&{'affine_rays','affine_core_v2','cell'},
    'The original independent D source audit forbids the alternate affine/cell runtime modules')
   chain_dirs={str(origin/f"work/cutoff25_20261011/new_root/global_local_contact_b5_p{statement['panel']}_v14")}
   chain_dirs.update(str(origin/('work/cutoff25_20261013/archive_audit/'+name))for name in
    ('normalized_defect_frontier_v1','support_coupled_frontier_v1','joint_contact_preflight_v1','affine_contact_cell_v1'))
   ratio=str(origin/'work/cutoff25_20261013/low/tighter_ratio_rho_v1/ratio.py')
   for row in proof[key].values():
    s.need(request['sources'].get(row['path'])==row['sha256']==s.digest(local(row['path']))
     and(str(e.path_class(row['path'])(row['path']).parent)in chain_dirs or row['path']==ratio),
     'Every actual primitive module has the exact independently pinned path, SHA and reviewed helper directory')
 s.need(stdout.splitlines()[-1]=='FULL92_D_PRIMITIVES_COMPLETE '+s.digest(capsule/OUTPUT),'Actual whole original primitive terminal')
 return dict(schema='REVALIDATED_FULL92_FRESH_D_PRIMITIVES_V1',claims=92,output_sha256=s.digest(capsule/OUTPUT),
  full_feedback_prefix_normalized_pointwise_replayed=True,historical_scalar_acceptance_promoted=False,full66_complete=False)

def validate_completed(task):
 adapter=Adapter().bind(task);checked=stopped.validate(task,adapter=adapter)
 s.need(checked['all_original_actions_completed']is True,'Whole D92 primitive action completed')
 state=s.read(Path(task)/'PREFIX.json');return dict(checked,primitive_summary=state['actions'][-1]['validated_output'])
