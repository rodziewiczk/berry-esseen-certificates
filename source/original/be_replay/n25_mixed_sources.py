"""Literal complete original mixed recipes and a source-only portable closure.

Historical streams are not staged as current captures. Exact original output
JSONs remain separate comparison vectors. Every actual mixed arithmetic result
must be acquired through a stopped action before its SHA can enter an epoch.
"""
from __future__ import annotations
import ast,hashlib,json
from pathlib import Path
from . import n25_full_join_sources as s,n25_mixed_contact as contact

PLAN=s.ROOT/'proof/n25_mixed_full_action_plan.json'
PIN='4961b6422ae510c2bc6bd1dcb53cf36565f7872887453bdb02dc818172e3d986'
OLD_ROOT='/Users/bkolodziejek/Downloads/BE_Codex_Handoff'
OLD_PYTHON='/Users/bkolodziejek/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
BASE='work/cutoff25_20261013/'
RUNTIME_DIRS=(
 'archive_audit/mixed_sparse_source_v1','low/mixed2_static_pointwise_v1',
 'archive_audit/mixed3_saved_scalar_v1','low/mixed4_grid_pointwise_v1',
 'low/p24_static_pointwise_v1','low/coupled_chord_discovery_v1',
 'root/coupled_chord_v1','root/coupled_third_moment_boxes_v1',
 'low/pointwise_inward_defect_v2','root/local_contact_rho_regional_v1')
NATIVE24='cutoff25_20261011/new_audit/fixed_law24_b5_p24_eps01_v1'
CANDIDATES=(
 'cutoff25_20261013/root/mixed_e24_b5p24_v1/MIXED_E24_UNACCEPTED_FOREST.json',
 'cutoff25_20261013/root/coarsened_complete_p25_v1/UNACCEPTED_FOREST.json')
OPAQUE_HISTORY=frozenset((
 'cutoff25_20261013/low/coupled_chord_discovery_v1/IMPORTS_CHECKED.json',
 'cutoff25_20261013/low/mixed_fast1_independent_review_v1/fixtures01/own_time/foreign.json'))
SOURCE_HISTORY=frozenset((
 'cutoff25_20261013/low/p24_static_pointwise_v1/pre_collection_indent_fix/e_registry.py',
 'cutoff25_20261013/low/tighter_ratio_rho_v1/halfline_feedback.py'))

def plan():
 s.need(s.digest(PLAN)==PIN,'Exact30-call full original mixed action plan')
 p=s.read(PLAN);actions=p['actions'];source_plan=s.plan()
 s.need(p['schema']=='FULL66_THIRTY_ORIGINAL_MIXED_ACTIONS_V1'and p['source_plan_sha256']==s.PLAN_SHA256
  and p['additional_required_D92']is True and len(actions)==30 and len({x['id']for x in actions})==30
  and p['original_programs_executed']is False and p['historical_acceptance_is_fresh']is False,
  'Every full original source action plus a separate mandatory current D92 proof')
 for row in actions:
  s.need(source_plan['files'][row['script_member']]['sha256']==row['script_sha256']
   and source_plan['files'][row['output_reference_member']]['sha256']==row['output_reference_sha256'],
   'Every original whole program and mathematical comparison vector has an external source pin')
 return p

def specs(capsule):
 rows=[];capsule=Path(capsule)
 for original in plan()['actions']:
  row={k:original[k]for k in('id','cwd','argv','outputs','created')};row['argv']=list(row['argv'])
  if 'capture'in original:row['capture']=original['capture']
  for i,arg in enumerate(row['argv']):
   if arg=='{C_acquisition_capture_directory}':row['argv'][i]=str(capsule/'runs/cutoff25_20261013/root/pointwise_local_acquisition01')
   elif arg=='{F_acquisition_capture_directory}':row['argv'][i]=str(capsule/'runs/cutoff25_20261013/archive_audit/p25_grid_pointwise_acquisition01')
  rows.append(row)
 return rows

def logical(value):
 if type(value)is not str:return None
 value=value.replace('\\','/')
 if value.startswith(OLD_ROOT+'/work/'):value=value[len(OLD_ROOT+'/work/'):]
 elif value.startswith('work/'):value=value[5:]
 if value.startswith(('cutoff25_20261011/','cutoff25_20261013/')):
  s.tx.parts(value);return value
 return None

def strings(value):
 if type(value)is str:yield value
 elif type(value)is dict:
  for key,item in value.items():yield key;yield from strings(item)
 elif type(value)is list:
  for item in value:yield from strings(item)

def closure(cache):
 """Close original source/JSON references without importing archived code.

 The omitted original p24 source is reconstructed only to pre-existing exact
 independent SHA pins. Runtime outputs and old capture streams are never
 treated as source inputs. Missing historical identities remain an explicit
 provenance list; an actual loaded module/output cannot use that exemption.
 """
 source_plan=s.plan();actions=plan()['actions'];outputs={r['output_reference_member']for r in actions}
 recovered=contact.recovered_original24(cache);selected={};missing={};queue=[]
 def add(name):
  if name in selected or name in outputs:return
  if name.endswith(('.metadata.json','.stdout.txt','.stderr.txt'))or Path(name).name in('metadata.json','stdout.txt','stderr.txt'):
   missing[name]=dict(role='HISTORICAL_CAPTURE_NEVER_CURRENT',sha256=source_plan['files'].get(name,{}).get('sha256'))
   return
  if name in recovered:raw=recovered[name]
  elif name in source_plan['files']:raw=contact.original_bytes(cache,name,source_plan)
  else:
   missing[name]=source_plan['historical_reference_pins'].get(name,[]);return
  selected[name]=raw;queue.append(name)
 directories={str(Path(r['script_member']).parent).replace('\\','/')for r in actions}
 directories.update('cutoff25_20261013/'+name for name in RUNTIME_DIRS)
 for folder in sorted(directories):
  for name in source_plan['files']:
   if name.startswith(folder+'/')and '/'not in name[len(folder)+1:]:add(name)
 for index in(24,25,26):
  _,files=contact.reconstruct(cache,index)
  for name in files:add(name[5:])
 for name in recovered:add(name)
 # The native24 checker is exercised by both complete sparse predecessor
 # checkers; it is not replaced by a pointwise/global24 theorem.
 for name in source_plan['files']:
  if name.startswith(NATIVE24+'/')and '/'not in name[len(NATIVE24)+1:]:add(name)
 for name in CANDIDATES:add(name)
 while queue:
  name=queue.pop();raw=selected[name];found=[]
  if name in OPAQUE_HISTORY:found=[]
  elif name.endswith('.json'):
   value=json.loads(raw,object_pairs_hook=s.base.unique);found=list(strings(value))
  elif name.endswith('.py'):
   try:tree=ast.parse(raw)
   except SyntaxError:
    s.need(name in SOURCE_HISTORY,
     'No selected runtime program may have a syntax error')
    # These exact archived draft bytes are source-history vectors only. The
    # current e_registry/ratio files have distinct pinned identities. Never
    # repair a draft in place or claim it was the runtime program.
    found=[]
   else:found=[n.value for n in ast.walk(tree)if isinstance(n,ast.Constant)and type(n.value)is str]
  for value in found:
   member=logical(value)
   if member:add(member)
 return selected,dict(schema='FULL66_SOURCE_ONLY_COMPLETE_MIXED_CLOSURE_V1',
  source_plan_sha256=s.PLAN_SHA256,action_plan_sha256=PIN,files={n:hashlib.sha256(raw).hexdigest()for n,raw in selected.items()},
  recovered_exact_original_files={n:hashlib.sha256(raw).hexdigest()for n,raw in recovered.items()},
  historical_unstaged_source_references=missing,historical_streams_relabelled=False,
  original_output_comparison_vectors_are_not_current_facts=True,mathematical_acceptance=False)
