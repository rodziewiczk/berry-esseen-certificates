"""Both full original B3p30 supplemental resource calls and their pure reader.

The source-only port replaces just the obsolete four-log pathname loop by the
actual full parent export. Every mathematical statement, both complete support
rays,128 retained iterations and22 original corruption controls are unchanged.
"""
from __future__ import annotations
import ast,hashlib,json,shutil,sys
from pathlib import Path
from . import n25_full_join_sources as s,n25_parent_evidence as parent,n25_parents
from . import stopped_prefix as stopped,delivery_transport as tx
from .colab_batch import atomic_json

DIRECTORY='work/cutoff25_20261011/new_audit/supplemental_b3_p30_v1'
SCRIPT=DIRECTORY+'/protocol.py'
REQUEST='CURRENT_B3_PARENT_BINDING.json'
REVIEW='work/cutoff25_20261011/new_root/SUPPLEMENTAL_B3_P30_SOURCE_REVIEW_V1.json'
OUTPUTS=('SUPPLEMENTAL_PROOF.json','SUPPLEMENTAL_ACCEPTED.json')

def original(cache):return s.source(cache,SCRIPT[5:]).read_bytes()

def port(raw):
 text=raw.decode();tree=ast.parse(text);f=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='parents')
 loops=[n for n in f.body if isinstance(n,ast.For)and isinstance(n.target,ast.Tuple)
  and [x.id for x in n.target.elts if isinstance(x,ast.Name)]==['d','script','basename','prefix']]
 s.need(len(loops)==1,'One exact obsolete historical parent-capture loop')
 node=loops[0];lines=text.splitlines(keepends=True);before=''.join(lines[node.lineno-1:node.end_lineno])
 after="""    packet=read(ROOT/'CURRENT_B3_PARENT_BINDING.json')
    need(packet['schema']=='ACTUAL_COMPLETE_N25_B3_PARENT_TRANSPORT_BRIDGE_V1' and packet['historical_execution_relabelled'] is False,'actual completed parent evidence, not historical captures')
    need(packet['branch']=='b3' and packet['contact_allowance']=='5/16' and len(packet['stage_ledger_sha256'])==4,'all four original full parent actions')
    for name,value in packet['files_sha256'].items():
        path=ROOT/name;need(path.is_file() and sha(path)==value,'actual unchanged current source/proof/capture parent')
        bind(path)
"""
 current=''.join(lines[:node.lineno-1])+after+''.join(lines[node.end_lineno:])
 s.need(current.count(after)==1 and ast.dump(ast.parse(current.replace(after,before)),include_attributes=False)==ast.dump(tree,include_attributes=False),
  'Reverse projection preserves every original supplemental mathematical and control statement')
 return current.encode(),dict(schema='EXACT_CURRENT_B3_PARENT_CAPTURE_TRANSPORT_PORT_V1',original_sha256=hashlib.sha256(raw).hexdigest(),
  changed_sha256=hashlib.sha256(current.encode()).hexdigest(),only_original_parent_capture_loop_replaced=True,
  mathematical_support_retained_export_and_controls_unchanged=True,historical_execution_relabelled=False)

def implementation():
 return {n:s.digest(Path(__file__).parent/n)for n in('n25_full_join_supplement.py','n25_full_join_sources.py',
  'n25_parent_evidence.py','n25_parents.py','stopped_prefix.py','delivery_transport.py','action_supervisor.py')}|dict(source_plan=s.PLAN_SHA256)

def binding(task):
 task=Path(task);checked=parent.validate_completed(task/'parent',expected_branch='b3');capsule=task/'capsule'
 names=n25_parents.names('b3');actual=task/'parent'/checked['resource_capsule_relative'];root=capsule/'work/cutoff25_20261011/new_root'
 for kind in('initial','resource'):
  directory=names[kind+'_dir']
  s.need({p.name:s.digest(p)for p in(actual/directory).iterdir()if p.is_file()}==
   {p.name:s.digest(p)for p in(root/directory).iterdir()if p.is_file()},'Exact whole current accepted native parent capsule')
 files={p.relative_to(capsule).as_posix():s.digest(p)for p in(capsule/'parent_evidence').rglob('*')if p.is_file()}
 files.update({p.relative_to(capsule).as_posix():s.digest(p)for directory in(names['initial_dir'],names['resource_dir'])
  for p in(root/directory).iterdir()if p.is_file()})
 return dict(schema='ACTUAL_COMPLETE_N25_B3_PARENT_TRANSPORT_BRIDGE_V1',branch='b3',contact_allowance='5/16',
  stage_ledger_sha256=checked['stage_ledger_sha256'],files_sha256=files,original_parent_context=checked['original_task_root'],
  historical_execution_relabelled=False,global_predecessor_acquired=False)

def prepare(cache,task,*,parent_task):
 task=tx.ordinary(task);s.need(not task.exists(),'Exclusive supplemental source epoch');capsule=task/'capsule';capsule.mkdir(parents=True)
 shutil.copytree(parent_task,task/'parent');checked=parent.validate_completed(task/'parent',expected_branch='b3')
 actual=task/'parent'/checked['resource_capsule_relative'];base=capsule/'work/cutoff25_20261011/new_root';base.mkdir(parents=True)
 for directory in(n25_parents.names('b3')['initial_dir'],n25_parents.names('b3')['resource_dir']):shutil.copytree(actual/directory,base/directory)
 shutil.copytree(task/'parent',capsule/'parent_evidence')
 raw=original(cache);folder=capsule/DIRECTORY;folder.mkdir(parents=True)
 (task/'original-protocol.py').write_bytes(raw);(task/'original-PROOF.txt').write_bytes(s.source(cache,DIRECTORY[5:]+'/PROOF.txt').read_bytes())
 changed,projection=port(raw);(folder/'protocol.py').write_bytes(changed);(folder/'PROOF.txt').write_bytes((task/'original-PROOF.txt').read_bytes())
 atomic_json(capsule/REQUEST,binding(task));mapping={str(p):s.digest(p)for p in capsule.rglob('*')if p.is_file()}
 review=dict(status='ROOT_REVIEWED_SUPPLEMENTAL_B3_P30_RESOURCES_V1',source_sha256=mapping,
  transport_epoch=projection,original_source_is_preserved=True,review_is_source_transport_not_mathematical_acceptance=True)
 atomic_json(capsule/REVIEW,review);atomic_json(task/'SUPPLEMENT_CONTEXT.json',dict(implementation=implementation(),projection=projection))
 stopped.begin(task,adapter=Adapter(),context=dict(unit='66.B3p30-supplement',implementation=implementation(),original_workspace=str(capsule)))
 return task

class Adapter:
 def identity(self):return dict(schema='FULL66_B3P30_FIXED_SUPPLEMENT_ADAPTER_V1',**implementation())
 def specs(self):return[dict(id='supplement-'+action,cwd=DIRECTORY,argv=['{python}','-B','protocol.py',action],
  outputs=[DIRECTORY+'/'+name for name in OUTPUTS[:i+1]],created=[DIRECTORY+'/'+OUTPUTS[i]])for i,action in enumerate(('construct','accept'))]
 def validate_initial(self,task,state):
  task=Path(task);capsule=task/'capsule';s.need(state['context']['implementation']==implementation(),'Exact complete supplemental implementation')
  raw=(task/'original-protocol.py').read_bytes();s.need(hashlib.sha256(raw).hexdigest()==s.plan()['files'][SCRIPT[5:]]['sha256'],
   'Entire independently pinned original supplemental program')
  changed,projection=port(raw);s.need((capsule/SCRIPT).read_bytes()==changed,'Only the named current parent transport loop changes')
  s.need((task/'original-PROOF.txt').read_bytes()==(capsule/DIRECTORY/'PROOF.txt').read_bytes()
   and s.digest(task/'original-PROOF.txt')==s.plan()['files'][DIRECTORY[5:]+'/PROOF.txt']['sha256'],'Unchanged entire original supplemental proof')
  s.need(s.read(capsule/REQUEST)==binding(task),'Whole current full parent evidence readback')
  review=s.read(capsule/REVIEW);s.need(review['transport_epoch']==projection and review['review_is_source_transport_not_mathematical_acceptance']is True,
   'Truthful reviewed source-only metadata epoch')
  from .n25_count_evidence import path_class
  origin=path_class(state['context']['original_workspace'])(state['context']['original_workspace'])
  fixed={REQUEST,SCRIPT,DIRECTORY+'/PROOF.txt'}
  fixed.update(p.relative_to(capsule).as_posix()for p in(capsule/'parent_evidence').rglob('*')if p.is_file())
  for directory in(n25_parents.names('b3')['initial_dir'],n25_parents.names('b3')['resource_dir']):
   fixed.update(p.relative_to(capsule).as_posix()for p in(capsule/'work/cutoff25_20261011/new_root'/directory).iterdir()if p.is_file())
  expected={str(origin.joinpath(*tx.parts(n))):s.digest(capsule/n)for n in fixed}
  s.need(review['source_sha256']==expected,'Every source-only gate edge derives from the exact actual current parent and immutable program')
  allowed=fixed|{REVIEW}|{DIRECTORY+'/'+name for name in OUTPUTS[:len(state['actions'])]}
  s.need({p.relative_to(capsule).as_posix()for p in capsule.rglob('*')if p.is_file()}==allowed,
   'No additional import/helper/candidate besides the exact current source epoch')
  return projection
 def validate_live(self,task,state):self.validate_initial(task,state)
 def prepare_action(self,task,state,spec):return dict(source_transport_projection=self.validate_initial(task,state))
 def validate_epoch(self,task,state,spec,item):self.validate_initial(task,state);s.need(not item['source_changes'],'No later source mutation')
 def capture_inputs(self,task,spec):return {p.name:s.digest(p)for p in(Path(task)/'capsule'/DIRECTORY).iterdir()if p.is_file()}
 def copy_validation_context(self,source,target):
  shutil.copytree(Path(source)/'parent',Path(target)/'parent')
  for name in('original-protocol.py','original-PROOF.txt','SUPPLEMENT_CONTEXT.json'):shutil.copyfile(Path(source)/name,Path(target)/name)
 def validate_output(self,task,state,spec,item,stdout):
  capsule=Path(task)/'capsule';proof=s.read(capsule/DIRECTORY/OUTPUTS[0]);s.need(proof['schema']=='SUPPLEMENTAL_N25_B3_P30_FIXED_TWO_STEP_V1',
   'Full exact original supplemental proof')
  s.need(len(proof['supports'])==len(proof['steps'])==2 and [x['step']for x in proof['steps']]==[1,2],
   'Both full support rays and both64-iteration harmonic resource steps')
  if spec['id'].endswith('construct'):
   s.need(stdout.split()[0]=='SUPPLEMENTAL_FIXED_TWO_STEP_CONSTRUCTED','Original full construction terminal')
   return dict(proof_sha256=s.digest(capsule/DIRECTORY/OUTPUTS[0]),steps=2,supports=2,full66_complete=False)
  receipt=s.read(capsule/DIRECTORY/OUTPUTS[1]);labels=original_controls((Path(task)/'original-protocol.py').read_bytes())
  s.need(receipt['status']=='PASS_FRESH_SUPPLEMENTAL_N25_B3_P30_TWO_STEP_RESOURCES'and receipt['negative_controls']==labels
   and receipt['fresh_support_targets']==2 and receipt['fresh_retained_iterations']==128
   and receipt['proof_sha256']==s.digest(capsule/DIRECTORY/OUTPUTS[0])and receipt['checker_sha256']==s.digest(capsule/SCRIPT)
   and json.loads(stdout,object_pairs_hook=s.base.unique)==receipt,'All22 original controls and the whole actual native terminal/receipt')
  return dict(proof_sha256=s.digest(capsule/DIRECTORY/OUTPUTS[0]),receipt_sha256=s.digest(capsule/DIRECTORY/OUTPUTS[1]),
   negative_controls=labels,fresh_support_targets=2,fresh_retained_iterations=128,full66_complete=False)

def original_controls(raw):
 tree=ast.parse(raw);f=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='mutations')
 changes=next(n.value for n in f.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='changes'for t in n.targets))
 labels=[ast.literal_eval(n.elts[0])for n in changes.elts];s.need(len(labels)==len(set(labels))==22,'Every exact original supplemental corruption control')
 return labels

def validate_completed(task):
 checked=stopped.validate(task,adapter=Adapter());s.need(checked['all_original_actions_completed']is True,'Both full original supplemental calls')
 return dict(checked,output_sha256=s.digest(Path(task)/'capsule'/DIRECTORY/OUTPUTS[1]),supplemental_iterations=128,full66_complete=False)
