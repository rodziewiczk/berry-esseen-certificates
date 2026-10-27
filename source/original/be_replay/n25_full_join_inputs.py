"""Full pure admission of already completed n25 constituent exports.

Every full numerical reader is called again; stored revalidation summaries,
old PASS records and search checkpoints cannot replace actual stopped evidence.
"""
from __future__ import annotations
from pathlib import Path
from . import n25_full_join_sources as s,n25_count_evidence as exact

same=exact.same

def locate(root,name):return s.path(root,name)

def retained(root,branch,*,kind='retained'):
 if kind=='retained':
  from . import retained_n25_sources as src,retained_n25_evidence as ev
 elif kind=='extra':
  from . import retained_n25_extra_sources as src,retained_n25_extra_evidence as ev
 elif kind=='upper':
  from . import n25_upper_counts_sources as src,n25_upper_counts_evidence as ev
 else:raise ValueError('One literal retained-count evidence family')
 root=Path(root);task=root/'task';rows=src.jobs(branch);src.verify(task);status=s.read(root/'SESSION_RESULT.json')
 stages=status['stages'];s.need(type(stages)is list and len(stages)==len(rows)
  and status['state']=='selected_retained_count_arithmetic_accepted'and status['completed_jobs']==len(rows)
  and status['completed_leaves']==sum(j['leaf_count']for j in rows),'Whole complete selected native count batch')
 output=[]
 for row,item in zip(rows,stages):
  s.need(item['job_id']==row['job_id'],'Every original selected job in exact order')
  epoch=locate(task,item['epoch']);checked=ev.validate_stage(task,row,epoch)
  s.need(same(checked,item['evidence']),'Freshly reproduced whole evidence summary, not self-attestation')
  capsule=epoch/'capsule';output.append(dict(job_id=row['job_id'],member=row['capsule_member_prefix'].rstrip('/'),
    task=task,capsule=capsule,row=row,validated=checked,contract=capsule/'contract.json',
    native=capsule/row['acceptance_filename'],forest=capsule/row['forest_filename']))
 return output

def seven(root):
 from . import n25_collect as old
 d=s.read(Path(root)/'SESSION_RESULT.json');record=s.read(Path(root)/'N25_INTERFACES.json')if(Path(root)/'N25_INTERFACES.json').exists()else None
 # A collector can be recreated from preserved constituent imports, but cannot
 # merely trust the collector's saved flag. Its exact original inputs are read.
 if record is None:
  candidates=list(Path(root).glob('*INTERFACE*.json'))
  s.need(len(candidates)==1,'Actual complete seven-interface collector report');record=s.read(candidates[0])
 s.need(record['selected_interfaces_verified']is True and set(record['imports'])==set(old.JOBS),'All seven counts and both actual parents')
 counts,parents,_=old.validators();imports={}
 for key,item in record['imports'].items():
  task=locate(root,item['task_relative'])
  checked,_=old.validate_count_export(task,key,counts)if key in old.COUNTS else(parents.validate_completed(task,expected_branch=key[-2:]),parents)
  old.validate_scope(key,checked);s.need(same(checked,item['report']),'Every actual preserved count/parent export is revalidated')
  imports[key]=dict(item,report=checked)
 edges,pending=old.interfaces(imports,root,progress=lambda *a,**k:None);s.need(not pending and same(edges,record['interfaces']),'All seven same-law exact resource interfaces')
 old.cover(edges);return record,imports

def seven_direct(root,key):
 from . import n25_collect as old
 counts,parents,_=old.validators();task=Path(root)
 checked,_=old.validate_count_export(task,key,counts)if key in old.COUNTS else(parents.validate_completed(task,expected_branch=key[-2:]),parents)
 old.validate_scope(key,checked);return checked

def acquisition(root,kind,branch):
 """Return full current INITIAL/resource/local actions and actual proof paths."""
 if kind=='b012':
  from . import n25_b012_acquisition_sources as src,n25_b012_acquisition_evidence as ev
  stages=src.stages(branch);validate=lambda t:ev.validate_prefix(t,branch,len(stages));native_root=ev.root
 elif kind=='middle':
  from . import middle_n25_acquisition_sources as src,middle_n25_acquisition_evidence as ev
  stages=src.stages(branch);validate=lambda t:ev.validate_completed(t,branch);native_root=ev.root
 elif kind=='b5':
  from . import n25_b5_global_sources as src,n25_b5_global_evidence as ev
  stages=src.stages(branch);validate=ev.validate_completed;native_root=ev.root
 elif kind=='high-beta3':
  from . import high_beta3_acquisition_sources as src,high_beta3_acquisition_evidence as ev
  stages=src.stages();validate=ev.validate_completed;native_root=ev.root
 else:raise ValueError('One exact current n25 acquisition family')
 root=Path(root);task=root/'task';checked=validate(task);base=native_root(task)
 proof_rows=[]
 for stage in stages:
  name=stage.get('proof');receipt=stage.get('receipt')
  if name:proof_rows.append(dict(stage=stage,proof=base/stage['folder']/name,
    receipt=base/stage['folder']/receipt if receipt else None))
 return dict(kind=kind,branch=branch,task=task,base=base,validated=checked,proofs=proof_rows)

def acquisitions40(root):
 from . import n25_acquisitions as run,n25_full_acquisition_sources as src
 root=Path(root);d=s.read(root/'SESSION_RESULT.json');s.need(d['state']=='COMPLETE_CONDITIONAL_40_ACTION_ACQUISITION_COMPONENT'
  and [r['family']for r in d['families']]==list(src.families()),'All ten original complete acquisition families')
 result={}
 for r in d['families']:
  task=locate(root,r['task_relative']);checked=run.validate_prefix(task,require_complete=True)
  s.need(same(checked,r['validated']),'Entire current40-action component readback')
  result[r['family']]=dict(task=task,base=run.family_root(task),validated=checked)
 return result

def recovered11(root):
 from . import n25_recovery_sources as src,n25_recovered_counts_evidence as ev
 root=Path(root);d=s.read(root/'SESSION_RESULT.json');targets=src.targets()
 s.need(d['state']=='COMPLETE_ELEVEN_CONDITIONAL_ORIGINAL_B5_ACCEPTANCES'
  and [r['target']for r in d['stages']]==list(targets),'All11 original B5 acceptances, with no discovery substitution')
 result=[]
 for r in d['stages']:
  task=root/'tasks'/r['target'];epoch=locate(root,r['epoch']);checked=ev.validate_stage(task,r['target'],epoch)
  s.need(same(checked,r['validated']),'Full original B5 source/capture/native-guard evidence')
  profile=src.profile(r['target'],ordinary=True);capsule=epoch/'capsule'
  result.append(dict(job_id=r['target'],member=profile['member_prefix'].rstrip('/'),task=task,capsule=capsule,
   validated=checked,contract=capsule/'contract.json',forest=capsule/profile['candidate']['filename'],
   native=capsule/profile['historical_receipt']['filename']))
 return result
