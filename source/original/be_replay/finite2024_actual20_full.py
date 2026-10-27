"""All40 original actual20 operations plus one explicit conditional scalar parent.

The three old launch-history composers use the complete original mathematical
interfaces with actual current52 evidence. Their transport is explicitly
ported; no old constructor capture is claimed current and no theorem flag is
inferred from a stopped0 process. Each action has its own23hour CPU/wall limit.
"""
from pathlib import Path
import ast,hashlib,json,shutil,sys,tempfile
from . import finite2024_actual20_adapter as a,finite2024_remaining_sources as s
from . import finite2024_remaining_epoch as epoch,finite2024_remaining_evidence as ev
from . import actual20_semantic_sources as extra,finite2024_fourier_sources as fs,finite2024_fourier_evidence as fe
from . import finite1920_feedback_sources as gs,finite1920_feedback_evidence as ge
from . import finite1039_sources as cs,finite1039_count_evidence as ce,stopped_prefix as prefix
from .finite1039_count_evidence import same
from . import finite2024_coupled_parent as coupled_parent
from .colab_batch import atomic_json
B='work/cutoff20_20261016/';C='work/continuation_cutoff20_20261016/'
ADDED=(
 ('high_rho_join',B+'root/high_rho_join_v1','check.py','JOINED.json','runs/cutoff20_20261016/root/high_rho_join01'),
 ('global20_auxiliary_feedback',B+'analytic/global20_aux_feedback_v2','check.py','JOINED.json','runs/cutoff20_20261016/analytic/global20_aux_feedback02'),
 ('feedback_premise_join',B+'analytic/feedback20_premise_join_v1','check.py','JOINED.json','runs/cutoff20_20261016/analytic/feedback20_premise_join01'),
 ('feedback_resource_join',B+'analytic/feedback_resources_join_v1','check.py','JOINED.json',None),
 ('coarse_scalar_map',B+'analytic/b0_all_inward_v1','map.py','MAPPED.json',None),
 ('coarse_coupled_map',B+'finite/coupled_noise_all_v1','map.py','MAPPED.json',None),
 ('feedback_scalar_map',B+'analytic/feedback_b0_scalar_map_v1','map.py','MAPPED.json','runs/cutoff20_20261016/analytic/feedback_b0_scalar_map01'),
 ('feedback_coupled_map',B+'analytic/feedback_b0_coupled_all_v1','map.py','MAPPED.json',None),
 ('feedback_bn_scalar_map',B+'root/feedback_bn_scalar_map_v1','map.py','MAPPED.json',None),
 ('independent_scalar_review',C+'analytic','review_scalar_moments.py','SCALAR_MOMENT_SOURCE_REVIEW.json',None),
 ('independent_bn_interfaces',C+'analytic','review_bn_interfaces.py','BN_RESOURCE_COUNT_INTERFACE_REVIEW.json',None))
REQUESTS={'global20_auxiliary_feedback':B+'analytic/global20_aux_feedback_v2/REQUEST.json',
 'coarse_scalar_map':B+'analytic/b0_all_inward_v1/REQUEST.json',
 'feedback_scalar_map':B+'analytic/feedback_b0_scalar_map_v1/REQUEST.json',
 'feedback_bn_scalar_map':B+'root/feedback_bn_scalar_map_v1/REQUEST.json'}
CAPTURE_PINS={'runs/cutoff20_20261016/'+n+'/metadata.json':pin for n,pin in(
 ('analytic/fourier_cover_readback01','d1aa8998e030ae4521d54ffabba21a43ecf974e93d1376e59f2c272efa9180cd'),
 ('analytic/supported1125_readback01','8b74eb2ccd862a36adf05399c4c51479a8d5fe6a891915bc8aa16c59fd4baee0'),
 ('root/high_rho_join01','6d606c21ffd5a2a1868ee2f06a1e7023f2909232c65f0cafd90b53f83e2d15f3'),
 ('analytic/global20_aux_feedback02','1f5590f735effb3890abacaa160e660893002c4486cb19726c200337ef893078'),
 ('analytic/feedback20_premise_join01','c424a40b311d4a91a0f2e20ce268cd211981a8c57b5e3ed2fbf8b06866441487'),
 ('analytic/feedback20_initial_b0_replay01','d72df68152826642446063659e60b46aa94c7c8148e1100add6a3993879aaa6c'),
 ('analytic/feedback_b0_scalar_map01','1db7a46c9d5bfaacac3da817c335f11b6ade24c7b8e22ecb6f65dded56b599d4'),
 ('analytic/feedback20_initial_bn_replay01','d0e213f286cd810e43641faec62448244570a6104d2cd71ed6969b091d979532'))}

def specs():
 added={}
 for key,cwd,script,out,capture in ADDED:
  tail=['{python}','-B',script]+(['REQUEST.json']if key in('global20_auxiliary_feedback','coarse_scalar_map','feedback_scalar_map')else[])
  row=dict(id=key,cwd=cwd,argv=tail,outputs=[cwd+'/'+out],created=[cwd+'/'+out])
  if capture:row['capture']=capture
  added[key]=row
 result=[]
 for row in a.specs():
  row=dict(row)
  if row['id']=='feedback_native_prepare':result.extend(added[k]for k in('high_rho_join','global20_auxiliary_feedback'))
  if row['id']=='coarse_resources_construct':result.append(added['feedback_premise_join'])
  if row['id']in('feedback_b0_replay','feedback_bn_replay'):
   band='b0'if row['id']=='feedback_b0_replay'else'bn';row['capture']='runs/cutoff20_20261016/analytic/feedback20_initial_'+band+'_replay01'
  result.append(row)
 result.extend(added[k]for k,*_ in ADDED if k not in('high_rho_join','global20_auxiliary_feedback','feedback_premise_join'))
 scalar=dict(id='coupled_scalar_parent',cwd=coupled_parent.DIRECTORY,argv=['{python}','-B','CURRENT_PARENT.py'],
             outputs=[coupled_parent.RESULT],created=[coupled_parent.RESULT])
 result.insert(next(i for i,r in enumerate(result)if r['id']=='coarse_coupled_map'),scalar)
 for key in('B0','BN','GLOBAL'):
  result.append(dict(id='regional_'+key,cwd='',argv=['{python}','-B','-S','CURRENT_JOIN_'+key+'.py'],
   outputs=['CURRENT_JOIN_'+key+'.json'],created=['CURRENT_JOIN_'+key+'.json']))
 s.need(len(result)==41 and len({r['id']for r in result})==41,'All40 original calls plus one explicit five-contract conditional scalar parent')
 return result

def metadata(parent,*,feedback=False):
 parent=Path(parent);report=s.read(parent/'STAGE_OBSERVED.json');r=next(x for x in report['actions']if x['action']=='readback');o=r['observed'];launch=s.read(parent/'executions/readback/launch.json')
 return dict(schema='TRUTHFUL_CURRENT_UPSTREAM_READBACK_ALIAS_V1',command=launch['argv'],cwd=launch['cwd'],returncode=o['returncode'],
  changed_inputs=[],python=report['python_version'],input_sha256=s.read(parent/'SOURCES.json')['sources'],
  stdout_sha256=o['stdout_sha256'],stderr_sha256=o['stderr_sha256'],elapsed_seconds=o['elapsed_seconds'],
  supervisor_result_sha256=s.digest(parent/'executions/readback/supervisor-result.json'),historical_capture_relabelled=False)

def entry(context,key):
 return ('from pathlib import Path\nimport sys,hashlib\n'
  +'sys.path.insert(0,'+repr(context['runtime_root'])+')\nfrom be_replay import finite2024_actual20_math as worker\n'
  +'assert hashlib.sha256(Path(worker.__file__).read_bytes()).hexdigest()=='+repr(context['math_worker_sha256'])+'\n'
  +'worker.main(Path(__file__).resolve().parent.parent,'+repr(key)+')\n').encode()

def parent_files(task,request):
 """Independently regenerate all actual aliases from full upstream readers."""
 task=Path(task);files={};proofs={};verified={}
 def put(name,source,pin):
  s.parts(name);raw=source if type(source)is bytes else Path(source).read_bytes()
  if name in files:s.need(files[name]==raw,'Consistent whole current upstream aliases')
  files[name]=raw;proofs[name]=pin
 for key,reader in(('auxiliary',fe.validate_completed),('universal',fe.validate_completed),('supported',fe.validate_completed),('feedback',ge.validate_completed)):
  record=request['parents'][key];parent=task.joinpath(*s.parts(record['task_relative']));checked=reader(parent)
  s.need(same(checked,record['validated']),'Entire current genuine actual20 parent, never a recorded PASS alone');verified[key]=checked
  if key!='feedback':s.need(checked['family']==key,'Literal Fourier parent family')
  audit=gs.AUDIT if key=='feedback'else fs.family(key)['audit'];result=gs.RESULT if key=='feedback'else fs.result_path(fs.family(key))
  marker=checked['stage_result_sha256']
  for p in(parent/'capsule').rglob('*'):
   s.ordinary(p)
   if p.is_file():put(p.relative_to(parent/'capsule').as_posix(),p,marker)
  put(audit+'/READBACK.json',parent/'capsule'/result,marker)
  capture='runs/cutoff20_20261016/analytic/'+{'auxiliary':'auxiliary19_24','universal':'fourier_cover','supported':'supported1125','feedback':'same_law1920_cover'}[key]+'_readback01'
  put(capture+'/metadata.json',(json.dumps(metadata(parent),indent=2)+'\n').encode(),marker)
  for stream in('stdout','stderr'):put(capture+'/'+stream+'.txt',parent/'executions/readback'/(stream+'.txt'),marker)
 selected={r['job_id']:r for r in cs.jobs('n20_24')if r['n']==20};records={r['job_id']:r for r in request['counts']}
 s.need(len(records)==len(request['counts'])==49 and set(records)==set(selected),'All49 exact actual20 forests, including every closed piece')
 for key,row in records.items():
  parent=task.joinpath(*s.parts(row['task_relative']));checked=ce.validate_completed(parent)
  s.need(same(checked,row['validated']),'Full current native forest, every original leaf/control and stopped acceptance')
  for p in(parent/'capsule').rglob('*'):
   s.ordinary(p)
   if p.is_file():put('work/'+p.relative_to(parent/'capsule').as_posix(),p,checked['stage_result_sha256'])
 return files,proofs,verified

def original_files(task):
 result={n:dict(r,location='originals')for n,r in s.plan()['original_files'].items()}
 for n,r in extra.plan().items():s.need(n not in result,'Disjoint exact dynamic original source supplement');result[n]=dict(r,location='supplement')
 return result

def initial_files(task,request,context):
 files={};owned={n for r in specs()for n in r['created']};deferred=set(REQUESTS.values())|{coupled_parent.REQUEST,coupled_parent.DRIVER}
 for n,row in original_files(task).items():
  if n not in owned|deferred:files[n]=(Path(task)/row['location']/n).read_bytes()
 parents,proofs,_=parent_files(task,request)
 for n,raw in parents.items():
  if n not in owned|deferred:files[n]=raw
 files['CURRENT_UPSTREAM_STAGES.json']=(json.dumps(request,indent=2)+'\n').encode()
 for key in('B0','BN','GLOBAL'):files['CURRENT_JOIN_'+key+'.py']=entry(context,key)
 # Always filter the merged namespace at the final boundary as well. Whole
 # upstream capsules contain explicitly historical scalar maps/reviews; none
 # may become a fresh output owned by this41-call transaction.
 files={n:raw for n,raw in files.items()if n not in {name for spec in specs()for name in spec['created']}}
 return files,proofs

def prepare(cache,supplement,task,*,parents,count_tasks):
 s.need(set(parents)=={'auxiliary','universal','supported','feedback'},'All four original actual20 upstream Fourier families')
 task=Path(task).resolve();owned={n for spec in specs()for n in spec['created']}|set(REQUESTS.values())|{coupled_parent.REQUEST,coupled_parent.DRIVER}
 a.prepare(cache,task,auxiliary_task=parents['auxiliary'],owned_outputs=owned);extra.verify(supplement);shutil.copytree(supplement,task/'supplement')
 request=dict(schema='COMPLETE_CURRENT_ACTUAL20_INPUTS_V1',parents={},counts=[],historical_constructor_captures_claimed_current=False,global_proof_accepted=False)
 for key,parent in parents.items():
  out=task/'inputs'/key;shutil.copytree(parent,out);checked=(ge if key=='feedback'else fe).validate_completed(out)
  request['parents'][key]=dict(task_relative=out.relative_to(task).as_posix(),validated=checked)
 selected={r['job_id']for r in cs.jobs('n20_24')if r['n']==20};s.need(set(count_tasks)==selected,'No missing49-forest actual20 import')
 for i,key in enumerate(sorted(selected)):
  out=task/'inputs/counts'/str(i);shutil.copytree(count_tasks[key],out);checked=ce.validate_completed(out)
  request['counts'].append(dict(job_id=key,task_relative=out.relative_to(task).as_posix(),validated=checked))
 atomic_json(task/'CURRENT_FULL_INPUTS.json',request)
 from . import finite2024_actual20_math as math_worker
 context=dict(full_actual20=True,full_action_specs=specs(),full_capture_pins=CAPTURE_PINS,runtime_root=str(s.ROOT),math_worker_sha256=s.digest(math_worker.__file__),full_bridge_sha256=s.digest(__file__),
  dynamic_sources_sha256=extra.PIN,full58H_completed=False,global_proof_accepted=False)
 files,_=initial_files(task,request,context)
 for n,raw in files.items():
  path=task/'capsule'/n;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
 expected={n:hashlib.sha256(raw).hexdigest()for n,raw in files.items()}
 s.need(prefix.hashes(task/'capsule')==expected,'Exact initial materialization; every owned scalar/native output originally absent')
 return prefix.begin(task,adapter=Adapter(),context=context)

class Adapter:
 def specs(self):return specs()
 def identity(self):
  return dict(source_plan_sha256=s.PLAN_SHA256,supplement_sha256=extra.PIN,
   files={n:s.digest(s.ROOT/'be_replay'/n)for n in('finite2024_actual20_full.py','finite2024_actual20_math.py','actual20_semantic_sources.py','finite2024_coupled_parent.py',
    'finite2024_actual20_adapter.py','finite2024_remaining_epoch.py','finite2024_remaining_evidence.py',
    'finite2024_fourier_evidence.py','finite1920_feedback_evidence.py','finite1039_count_evidence.py')})
 def enriched(self,task,state):
  request=s.read(Path(task)/'CURRENT_FULL_INPUTS.json');_,proofs,_=parent_files(task,request)
  return dict(state,extra_reference_proofs=proofs)
 def validate_initial(self,task,state):
  s.verify_cache(Path(task)/'originals');extra.verify(Path(task)/'supplement');ctx=state['context']
  s.need(ctx['full_actual20']is True and ctx['full_action_specs']==specs()and ctx['full_capture_pins']==CAPTURE_PINS and ctx['full_bridge_sha256']==s.digest(__file__)and ctx['dynamic_sources_sha256']==extra.PIN
   and ctx['full58H_completed']is False and ctx['global_proof_accepted']is False,'Entire41-operation actual20 conditional protocol')
  expected,_=initial_files(task,s.read(Path(task)/'CURRENT_FULL_INPUTS.json'),ctx)
  s.need(state['initial_inventory']=={n:hashlib.sha256(raw).hexdigest()for n,raw in expected.items()},'Whole original source and actual current parent inventory independently reproduced')
 def copy_validation_context(self,task,target):
  for n in('originals','supplement','inputs'):shutil.copytree(Path(task)/n,Path(target)/n)
  for n in('PREPARATION.json','CURRENT_FULL_INPUTS.json'):shutil.copyfile(Path(task)/n,Path(target)/n)
 def validate_live(self,task,state):
  s.need(state['adapter_identity']==self.identity(),'Exact complete actual20 implementation epoch')
  expected=state['actions'][-1]['after_inventory']if state['actions']else state['initial_inventory']
  s.need(prefix.hashes(Path(task)/'capsule')==expected,'Resume exclusively complete verified actual20 actions')
 def capture_inputs(self,task,spec):
  if spec['id']in{r['id']for r in a.specs()}:return a.capture_inputs(task,spec)
  folder=Path(task)/'capsule'/spec['cwd'];created=set(spec['created'])
  out={p.name:s.digest(p)for p in folder.iterdir()if p.is_file()and p.relative_to(Path(task)/'capsule').as_posix()not in created}
  return {spec['cwd']+'/'+n:pin for n,pin in out.items()}if spec['id'].startswith('feedback_bn_resources_')else out
 def prepare_action(self,task,state,spec):
  state=self.enriched(task,state);result=a.epoch_changes(task,state);capsule=Path(task)/'capsule';request=None
  key=spec['id']
  if key=='coupled_scalar_parent':
   generated=coupled_parent.prepare(task)
   result['coupled_scalar_parent_epoch']=generated
  if key in REQUESTS:
   if key=='global20_auxiliary_feedback':
    stem=B+'analytic/same_law1920_cover_review_v1/READBACK.json';capture='runs/cutoff20_20261016/analytic/same_law1920_cover_readback01/metadata.json'
    request=dict(supported_receipt_sha256=s.digest(capsule/stem),supported_metadata_sha256=s.digest(capsule/capture))
   else:
    folder={'coarse_scalar_map':'finite/sharp20_b0_resources_all_v1','feedback_scalar_map':'finite/feedback20_b0_resources_v1',
     'feedback_bn_scalar_map':'fourier/feedback_bn_resources_v1'}[key]
    cand,receipt=(s.digest(capsule/(B+folder+'/'+n))for n in('CANDIDATE.json','ACCEPTED.json'))
    request={'CANDIDATE.json':cand,'ACCEPTED.json':receipt}if key=='feedback_bn_scalar_map'else dict(candidate_sha256=cand,receipt_sha256=receipt)
   p=capsule/REQUESTS[key];p.parent.mkdir(parents=True,exist_ok=True);atomic_json(p,request)
   result['request_files_sha256']={REQUESTS[key]:s.digest(p)}
  return result
 def validate_epoch(self,task,state,spec,item):
  with tempfile.TemporaryDirectory(prefix='be-full-actual20-source-')as d:
   target=Path(d)/'task';target.mkdir();self.copy_validation_context(task,target);shutil.copytree(Path(task)/'capsule',target/'capsule');(target/'executions').mkdir()
   for prior in state['actions']:shutil.copytree(Path(task)/'executions'/prior['action'],target/'executions'/prior['action'])
   before=prefix.hashes(target/'capsule');expected=self.prepare_action(target,state,spec);after=prefix.hashes(target/'capsule')
   s.need(same(expected,item['source_epoch'])and{n:pin for n,pin in after.items()if before.get(n)!=pin}==item['source_changes'],
    'Every complete source/reference/current-request port independently reproduced')
 def validate_output(self,task,state,spec,item,stdout):
  state=self.enriched(task,state);key=spec['id']
  if key=='coupled_scalar_parent':return coupled_parent.validate(task,stdout)
  if key in{r['id']for r in a.specs()}:return a.validate_output(task,state,spec,item,stdout)
  if key.startswith('regional_'):
   from . import finite2024_actual20_math as math_worker
   return math_worker.validate(task,key.removeprefix('regional_'),stdout)
  refs=a._reference_map(task,state,item);name=spec['created'][0];packet=s.read(Path(task)/'capsule'/name)
  rows=original_files(task)
  if name in rows:
   root=Path(task)/rows[name]['location'];original=epoch.read((root/name).read_bytes())
   s.need(same(ev.mathematical_view(original,references=refs.substitutions(),original=True),ev.mathematical_view(packet)),
    'Every original scalar certificate, control, physical row and scope retained')
  s.need('files_sha256'in packet,'Complete original mathematical output with actual source closure')
  if key in('independent_scalar_review','independent_bn_interfaces'):
   # These two original final20 reviewers use ROOT=<capsule>/work and emit
   # paths relative to that exact namespace. Keep their original graph bytes;
   # explicitly bind the one known work-prefix translation, never search for
   # an arbitrary similarly named historical file.
   relative_refs=epoch.References();base=Path(task)/'capsule/work'
   for n in packet['files_sha256']:
    source=refs.rows.get('work/'+n);s.need(source is not None,'Exact original final20 review graph work-prefix edge')
    relative_refs.add(n,source['original_sha256'],(base/n).read_bytes(),role=source['role'],evidence_sha256=source['evidence_sha256'])
   ev.check_current_graph(base,packet,relative_refs)
  else:ev.check_current_graph(Path(task)/'capsule',packet,refs)
  s.need(all(packet.get(k,False)is False for k in('sharp20_proved','cutoff20_proved','global_sharp20_proved','all_index_conclusion_verified')),
   'An individual scalar/resource call cannot acquire sharp20 or the global proof')
  # Some originals print a whole summary, others a SHA marker or scalar rows.
  # All full output bytes are already tied to the actual stopped checkpoint.
  s.need(bool(stdout.strip()),'Actual original nonempty completion stream')
  return dict(action=key,output_sha256=s.digest(Path(task)/'capsule'/name),whole_original_semantic_payload_checked=True,
   complete_current_source_graph_checked=True,conditional_statement_only=True,global_proof_accepted=False)

def validate_completed(task):
 state=prefix.read(Path(task)/'PREFIX.json')
 s.need([row['action']for row in state['actions']]==[row['id']for row in specs()],
  'All41 original/declarative actions are present in exact order, including the scalar parent')
 checked=prefix.validate(task,adapter=Adapter())
 s.need(checked['all_original_actions_completed']is True and len(state['actions'])==41,'All40 original actual20 operations and the explicit conditional scalar parent completed')
 return dict(schema='COMPLETE_CURRENT_ACTUAL20_CONDITIONAL_UNIT_V2',prefix_sha256=checked['prefix_sha256'],actions=41,original_actions=40,additional_conditional_scalar_parent_actions=1,
  regions=['B0','BN','9/8+'],native_forests=49,conditional_actual20_verified=True,global_proof_accepted=False)

# Only two legacy transport assertions need a port. The complete mathematical
# functions, mutations, numerical constants and all other statements are kept.
PORTS={B+'analytic/global20_aux_feedback_v2/check.py':(
 "completed_capture(NEW_CAPTURE, request['supported_metadata_sha256'], graph, NEW, 'readback.py', ['REQUEST.json'])",
 "current_supported_capture(ROOT, NEW_CAPTURE, request['supported_metadata_sha256'], graph)"),
 C+'analytic/review_bn_interfaces.py':(
 "need(contract['resource_candidate_sha256']==sha(cp)and contract['resource_replay_sha256']==sha(ap)and contract['resource_row_sha256']==sha(p)and contract['resource_row']=='work/cutoff20_20261016/fourier/feedback_bn_resources_v1/rows/'+f'{i:03d}.json'and contract['scalar_map_sha256']==sha(mp)and contract['scalar_derivation_sha256']==sha(sp)and contract['original_rho_scope']==['11/10','9/8'],'all exact native provenance edges')",
 "current_native_contract_bridge(ROOT.parent,contract,row,proof,kp,sp,mp,cp,ap)")}
def port_source(name,raw,context=None):
 if name not in PORTS:return raw,None
 before,after=PORTS[name];text=raw.decode();s.need(text.count(before)==1,'Exactly one original legacy transport assertion, no mathematical body substitution')
 changed=text.replace(before,after);tree=ast.parse(changed);reverse=ast.parse(changed.replace(after,before))
 s.need(ast.dump(reverse,include_attributes=False)==ast.dump(ast.parse(text),include_attributes=False),
  'All original math and control AST unchanged outside one declared current-parent transport bridge')
 context=context or dict(runtime_root=str(s.ROOT),full_bridge_sha256=s.digest(__file__))
 module_path=str(Path(context['runtime_root'])/'be_replay/finite2024_actual20_full.py')
 prelude=('import sys as _current_sys\nfrom pathlib import Path as _CurrentPath\nimport hashlib as _current_hashlib\n'
  +'_current_sys.path.insert(0,'+repr(context['runtime_root'])+')\nfrom be_replay import finite2024_actual20_full as _current_parent_bridge\n'
  +'assert _CurrentPath(_current_parent_bridge.__file__).resolve()==_CurrentPath('+repr(module_path)+')\n'
  +'assert _current_hashlib.sha256(_CurrentPath(_current_parent_bridge.__file__).read_bytes()).hexdigest()=='+repr(context['full_bridge_sha256'])+'\n'
  +'current_supported_capture=_current_parent_bridge.current_supported_capture\ncurrent_native_contract_bridge=_current_parent_bridge.current_native_contract_bridge\n')
 # No future imports occur in either fixed original. Retain their text exactly.
 output=(prelude+changed).encode();compile(output,name,'exec')
 return output,dict(schema='DECLARED_CURRENT_FULL_PARENT_TRANSPORT_PORT_V1',original_name=name,original_after_reference_epoch_sha256=hashlib.sha256(raw).hexdigest(),
  current_sha256=hashlib.sha256(output).hexdigest(),transport_replacements=1,entire_remaining_original_AST_preserved=True,
  historical_parent_hashes_rewritten=False,mathematical_acceptance_granted_by_port=False)

def current_supported_capture(root,directory,pin,graph):
 """Full genuine58G readback; never manufacture the old REQUEST argv/cwd."""
 root=Path(root);task=root.parent;request=s.read(task/'CURRENT_FULL_INPUTS.json');r=request['parents']['feedback'];parent=task.joinpath(*s.parts(r['task_relative']))
 checked=ge.validate_completed(parent);s.need(same(checked,r['validated']),'Full actual two-band19/20 Fourier producer and every control')
 source=parent/'capsule'/gs.RESULT;alias=root/(gs.AUDIT+'/READBACK.json')
 s.need(source.read_bytes()==alias.read_bytes(),'Whole current58G result at the separately declared original input alias')
 s.need(s.digest(directory/'metadata.json')==pin and s.read(directory/'metadata.json')==metadata(parent),'Truthful real outer launch/streams and entire original/current upstream stage')
 for stream in('stdout','stderr'):
  path=directory/(stream+'.txt');s.need(path.read_bytes()==(parent/'executions/readback'/(stream+'.txt')).read_bytes(),'Actual58G stopped readback streams')
  graph[path.relative_to(root).as_posix()]=s.digest(path)
 graph[(directory/'metadata.json').relative_to(root).as_posix()]=pin

def current_native_contract_bridge(root,contract,row,proof,kp,sp,mp,cp,ap):
 """Preserve immutable native headers, bind their entire current math facts."""
 root=Path(root);task=root.parent;request=s.read(task/'CURRENT_FULL_INPUTS.json');selected={r['job_id']:r for r in cs.jobs('n20_24')if r['n']==20}
 matches=[r for r in selected.values()if r['band']=='BN'and r['index']==row['index']and r['contract_sha256']==s.digest(kp)]
 s.need(matches and contract['resource_row_sha256']==s.digest(root/(B+'fourier/feedback_bn_resources_v1/rows/'+f"{row['index']:03d}.json"))
  and contract['resource_row']==B+'fourier/feedback_bn_resources_v1/rows/'+f"{row['index']:03d}.json"
  and contract['scalar_derivation_sha256']==s.digest(sp)and contract['original_rho_scope']==['11/10','9/8'],
  'Entire original physical/scalar proof, native scope and unchanged immutable header')
 by_id={r['job_id']:r for r in request['counts']}
 for spec in matches:
  rec=by_id[spec['job_id']];parent=task.joinpath(*s.parts(rec['task_relative']));checked=ce.validate_completed(parent)
  s.need(same(checked,rec['validated'])and s.digest(parent/'capsule'/spec['directory']/spec['contract_name'])==s.digest(kp),
   'Every current full native piece uses the entire immutable historical mathematical contract')
 # The surrounding unchanged original functions independently reconstruct the
 # whole scalar certificate/cfg and every signed quadratic, before this bridge.
 s.need(s.read(cp)['rows']==s.read(ap)['rows']and s.read(ap)['candidate_sha256']==s.digest(cp),
  'Actual newly acquired complete parent pair remains internally bound')
