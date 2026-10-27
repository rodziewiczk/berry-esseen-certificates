"""Current-proof index and exact physical-panel routing for full66.

Historical selectors select untrusted mathematical inputs. Only paths added by
an already completed, independently revalidated constituent can be consumed as
an acquired proof or native count here.
"""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
from fractions import Fraction as F
from . import n25_full_join_sources as s,n25_full_join_semantics as m

def member(value):
 value=str(value).replace('\\','/')
 if '/work/cutoff25_'in value:value=value.split('/work/',1)[1]
 elif value.startswith('work/'):value=value[5:]
 s.need(value.startswith(('cutoff25_20261011/','cutoff25_20261013/')),'Literal n25 original mathematical identity')
 s.tx.parts(value);return value.rstrip('/')

class ProofGraph:
 def __init__(self):self.files={};self.counts={};self.provenance={}
 def add(self,name,path,*,evidence_sha256):
  name=member(name);path=s.tx.ordinary(path)
  s.need(path.is_file()and type(evidence_sha256)is str and len(evidence_sha256)==64,'An actual fully revalidated constituent binds this file')
  row=dict(path=path,sha256=s.digest(path),evidence_sha256=evidence_sha256)
  s.need(name not in self.files or self.files[name]['sha256']==row['sha256'],'No conflicting current same-law artifact identity')
  self.files[name]=row;return row
 def add_tree(self,base,*,prefix='cutoff25_20261011',evidence_sha256,admitted_files):
  """Admit only the constituent reader's exact current output manifest.

  A neighboring historical proof or source candidate is not acquired merely
  because it is beside one completed export.
  """
  base=Path(base)
  s.need(type(admitted_files)is dict and admitted_files,'Exact separately revalidated mathematical output manifest')
  for name,pin in admitted_files.items():
   p=s.path(base,name);s.need(p.is_file()and s.digest(p)==pin,'Every admitted current output is actual bound bytes')
   self.add(prefix+'/'+name,p,evidence_sha256=evidence_sha256)
 def read(self,name):
  row=self.files.get(member(name));s.need(row is not None,'A current completed acquisition is required: '+str(name))
  s.need(s.digest(row['path'])==row['sha256'],'Current proof bytes unchanged');return s.read(row['path'])
 def proof(self,name):
  key=member(name);return self.read(key),self.files[key]
 def add_count(self,frame):
  key=member(frame['member']);s.need(key not in self.counts,'Exactly one selected full COUNT export per source capsule')
  cfg=s.read(frame['contract']);receipt=s.read(frame['native'])
  s.need(len(cfg['rows'])==1 and receipt['contract_sha256']==s.digest(frame['contract'])
   and receipt['forest_sha256']==s.digest(frame['forest']),'Actual accepted full contract and entire original forest')
  stats=receipt['statistics'];s.need(F(stats['maximum_score'])<m.TARGET and stats['leaves']==receipt['fresh_leaf_evaluations'],
   'Every original native leaf was freshly replayed below the unchanged strict target')
  pin=s.digest(frame['native']);self.counts[key]=dict(frame,cfg=cfg['rows'][0],receipt=receipt,evidence_sha256=pin)
  for p in(frame['contract'],frame['native'],frame['forest']):self.add(key+'/'+p.name,p,evidence_sha256=pin)
  return self.counts[key]
 def count(self,name):
  key=member(name);s.need(key in self.counts,'The complete current original count is missing: '+key);return self.counts[key]
 def inventory(self):return {name:{k:v for k,v in row.items()if k!='path'}for name,row in sorted(self.files.items())}

def resource_objects(obj):
 """Enumerate actual complete resource results, preserving their local profile."""
 found=[]
 def walk(x,profile=None):
  if type(x)is dict:
   profile=x.get('profile',profile)
   if {'excluded','result','raw_row','initial'}<=set(x)and x['excluded']is False:
    found.append((x,profile))
   for key,y in x.items():
    if key not in('source_sha256','files_sha256'):walk(y,profile)
  elif type(x)is list:
   for y in x:walk(y,profile)
 walk(obj);return found

def surviving_resource(global_row,local=None):
 if local is None:return global_row,None
 if 'rows'in local:
  index=global_row['result']['index'];s.need(type(index)is int,'Actual native resource panel index')
  rows=[r for r in local['rows']if r['index']==index]
  s.need(len(rows)==1,'One actual current selected local probability panel');local=dict(local,**rows[0])
 if local.get('excluded')is True:return None,local.get('profile')
 if 'survivor_resource'in local:return local['survivor_resource'],local.get('profile')
 terminal=local.get('terminal')
 if type(terminal)is dict:
  for key in('resource','survivor_resource','derivation'):
   if key in terminal:
    obj=terminal[key];return obj.get('derivation',obj),local.get('profile')
 cycles=local.get('cycles');s.need(type(cycles)is list and cycles,'Complete selected nonempty local feedback chain')
 last=cycles[-1];resource=last.get('resource');s.need(type(resource)is dict,'Final actual local resource acquisition')
 return resource.get('derivation',resource),last.get('profile',local.get('profile'))

def panel_counts(graph,choices,resource,*,rho,index,invariants=None):
 result=[]
 for choice in choices:
  actual=graph.count(choice['capsule']);cfg=actual['cfg']
  edge=m.resource_interface(resource,cfg,rho=rho,index=index,invariants=invariants)
  edge.update(source_capsule=member(choice['capsule']),native_evidence_sha256=actual['evidence_sha256'],
   leaves=actual['receipt']['statistics']['leaves'])
  result.append(edge)
 m.closed_partition([e['p']for e in result],[str(F(index,100)),str(F(index+1,100))]);return result

def resource_panels(global_proof,*,rho,profile=None):
 original_rows=global_proof['rows'];s.need(type(original_rows)is list and len(original_rows)==100,'Whole complete resource array')
 rows=[]
 for row in original_rows:
  if 'result'in row:
   s.need(set(row)in({'index','result'},{'index','input_source','result'}),
    'Original canonical resource-row descriptor with optional exact source provenance')
   rows.append(row)
  else:
   s.need(set(row)in({'index','derivation'},{'index','input_source','radius_minus','radius_plus','derivation'}),
    'One of the exact original quarter/beta resource descriptors')
   rows.append(dict(index=row['index'],result=row['derivation']))
 s.need(type(rows)is list and len(rows)==100
  and all(type(row['index'])is int and row['index']==i and type(row['result']['excluded'])is bool for i,row in enumerate(rows)),
  'Whole complete100-panel signed resource disposition')
 if profile is not None:s.need(m.same(global_proof['profile'],profile),'Same actual global profile')
 for i,row in enumerate(rows):
  if row['result']['excluded']is False:
   r=row['result'];s.need(all(F(z['pl'])==F(i,100)and F(z['pu'])==F(i+1,100)for z in(r['result'],r['raw_row'],r['initial'])),
    'All simultaneous physical resource objects have one closed p domain')
 return rows

def full_feedback_region(identity,rho,beta,proof,*,proof_pin,incoming_initial):
 license=m.initial_license(incoming_initial,rho=rho,beta=beta)
 s.need(m.same(proof['profile'],incoming_initial['profile']),'One whole actual INITIAL/global/local feedback profile')
 rows=proof['rows'];s.need(type(rows)is list and len(rows)==100 and all(type(r['index'])is int
  and r['index']==i and r['excluded']is True and type(r['cycles'])is list for i,r in enumerate(rows)),
  'The complete actual mixed-feedback acceptor excludes every100 closed panels')
 s.need(proof['schema']=='EXACT_HIGH25_MIXED_BETA1_FEEDBACK_PROOF_V1','Literal original high-beta1 full feedback theorem')
 out=[dict(index=i,p=[str(F(i,100)),str(F(i+1,100))],method='current_full_local_exclusion',evidence_sha256=proof_pin)for i in range(100)]
 return dict(id=identity,n=25,K='0',rho=list(rho),beta=beta,outcomes=out,full_mixed_feedback_proof_sha256=proof_pin,profile_license=license)

def region_from_rows(identity,rho,beta,global_proof,*,proof_pin,graph,selections,incoming_initial,
                     predecessor_allowance=None,locals=None,mixed=None):
 """All100 current outcomes, with exact surviving local and COUNT routes."""
 lower=identity.startswith('lower-')
 license=m.initial_license(incoming_initial,rho=rho,beta=beta,lower=lower,predecessor_allowance=predecessor_allowance)
 rows=resource_panels(global_proof,rho=rho,profile=incoming_initial['profile']);out=[];locals={}if locals is None else locals;mixed={}if mixed is None else mixed
 for i,row in enumerate(rows):
  entry=dict(index=i,p=[str(F(i,100)),str(F(i+1,100))],evidence_sha256=proof_pin)
  if row['result']['excluded']is True:entry['method']='current_full_resource_exclusion'
  else:
   local_record=locals.get(i);local=None
   if local_record is not None:
    s.need(set(local_record)=={'proof','evidence_sha256'}and type(local_record['evidence_sha256'])is str
     and len(local_record['evidence_sha256'])==64,'Actual full selected local acceptance evidence')
    local=local_record['proof'];entry['evidence_sha256']=local_record['evidence_sha256']
    s.need(m.same(local['profile'],incoming_initial['profile']),
     'Every current local exclusion or survivor starts from the whole same actual incoming rho/beta profile')
   resource,profile=surviving_resource(row['result'],local)
   if resource is None:entry['method']='current_full_local_exclusion'
   elif i in mixed:
    actual=mixed[i];s.need(actual['index']==i and actual['same_original_cfg_current_resource_interface']is True,
     'A complete actual mixed acceptance, acquired registries and same-law original resource interface')
    entry.update(method='current_full_mixed_E'if i==24 else'current_full_mixed_ABCDF',mixed=actual,
     evidence_sha256=actual['evidence_sha256'])
   else:
    s.need(str(i)in selections,'Every actual surviving physical panel has a selected closed COUNT cover')
    chosen=selections[str(i)];chosen=chosen.get('choice',chosen);choices=chosen['counts']
    edges=panel_counts(graph,choices,resource,rho=rho,index=i,invariants=None if profile is None else profile.get('invariants'))
    entry.update(method='current_full_native_counts',count_interfaces=edges)
  out.append(entry)
 return dict(id=identity,n=25,K='0',rho=list(rho),beta=beta,outcomes=out,
  full_global_proof_sha256=proof_pin,all_100_p_intervals_closed=True,profile_license=license)

def empty_initial_region(identity,rho,beta,proof,*,proof_pin):
 license=m.initial_license(proof,rho=rho,beta=beta)
 stages=proof['stages'];s.need(type(stages)is list and stages,'Whole original finite INITIAL derivation')
 final=stages[-1].get('cover',stages[-1]);s.need(type(final['active'])is int and final['active']==0,
  'The complete actual last signed cover is empty, not merely one panel or one sign')
 panels=final['panels'];s.need(len(panels)==100 and all(type(p['cells'])is int and p['cells']==0 for p in panels),
  'Every one of100 closed panels is empty in the final full cover')
 out=[dict(index=i,p=[str(F(i,100)),str(F(i+1,100))],method='current_full_INITIAL_exclusion',evidence_sha256=proof_pin)for i in range(100)]
 return dict(id=identity,n=25,K='0',rho=list(rho),beta=beta,outcomes=out,full_initial_proof_sha256=proof_pin,profile_license=license)
