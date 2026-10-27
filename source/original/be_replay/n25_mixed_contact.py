"""Pure reconstruction of each unchanged original V12 -> V14 contact edge.

No native producer, scalar kernel or old execution is imported. The original
three textual checker edits are projected as a pure string/AST function; the
whole contract, disjoint additions, manifests and source-port graph are read
from independently pinned original bytes. Current parent arithmetic is a
separate input to the mixed task's whole stopped-evidence reader.
"""
from __future__ import annotations
import ast,hashlib,json
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
from . import n25_full_join_sources as s,n25_full_join_semantics as sem
from .reference_graph_epoch import canonical

PRODUCER='cutoff25_20261011/new_low/local_contact_v14_native_v1/prepare.py'
CENTRAL='cutoff25_20261013/b5/local_contact_v14_combined'
REVIEW='cutoff25_20261013/archive_audit/LOCAL_CONTACT_V14_INDEPENDENT_REVIEW.json'

def original_bytes(cache,name,plan):
 row=plan['files'].get(name);p=s.path(cache,name)
 s.need(row is not None and p.is_file(),'Whole independently pinned original contact input: '+name)
 raw=p.read_bytes();s.need(len(raw)==row['bytes']and hashlib.sha256(raw).hexdigest()==row['sha256'],
  'Exact entire contact input after one fully pinned plan read: '+name)
 return raw

def member(value):
 value=str(value).replace('\\','/')
 if '/work/cutoff25_'in value:value=value.split('/work/',1)[1]
 elif value.startswith('work/'):value=value[5:]
 s.need(value.startswith(('cutoff25_20261011/','cutoff25_20261013/')),'One literal original contact-source identity')
 s.tx.parts(value);return value

def recovered_original24(cache):
 """Recover only bytes whose original SHA is independently pinned already.

 The p24 V12 directory was omitted from the archives. Its immutable V14 port
 preserves every kernel byte and every original cfg field. The neighboring
 original p25 contract supplies the common four-parent metadata, status and
 scope. A recovery is admitted ONLY if the entire resulting bytes match the
 old SHA committed by the already externally pinned original SOURCE_PORT.
 """
 old='cutoff25_20261011/new_root/global_alpha_stoploss2_b5_p24_v12'
 new='cutoff25_20261011/new_root/global_local_contact_b5_p24_v14'
 plan=s.plan()
 def raw(name):return original_bytes(cache,name,plan)
 def read(name):return json.loads(raw(name),object_pairs_hook=s.base.unique)
 port=read(new+'/SOURCE_PORT.json');contract=read(new+'/contract.json')
 before=read('cutoff25_20261011/new_root/global_alpha_stoploss2_b5_p25_v12/contract.json')
 cfg=deepcopy(contract['rows'][0]);s.need(cfg.pop('local_contact_allowance')=='5/16'
  and sem.same(cfg.pop('local_contact_premise'),sem.CONTACT),'Exactly the two original explicit contact fields')
 before['index']=24;before['rows']=[cfg]
 recovered={old+'/contract.json':(json.dumps(before,indent=2)+'\n').encode()}
 additions=read(new+'/LOCAL_CONTACT_V14_ADDITIONS.json');manifest=read(new+'/KERNEL_COPY_MANIFEST.json')
 for name in list(additions['files'])+['LOCAL_CONTACT_V14_ADDITIONS.json']:
  s.need(name in manifest['files'],'All explicitly disjoint additions exist');manifest['files'].pop(name)
 recovered[old+'/KERNEL_COPY_MANIFEST.json']=(json.dumps(manifest,indent=2)+'\n').encode()
 text=raw(new+'/count_protocol.py').decode()
 edits=[('from local_contact_v14 import cell35,validate_premise','from rho_signed_moment_tightener import cell35'),
  ('LOW25_B5_GLOBAL_LOCAL_CONTACT_V14_PANEL24_RIGHT_HALF_CLOSED_COUNT_FOREST_V1','LOW25_B5_GLOBAL_ALPHA_STOPLOSS2_V12_PANEL24_RIGHT_HALF_CLOSED_COUNT_FOREST_V1'),
  (" cfg=contract['rows'][0]\n validate_premise(cfg)\n"," cfg=contract['rows'][0]\n")]
 for current,original in edits:s.need(text.count(current)==1,'Three unique inverse source-only checker edits');text=text.replace(current,original)
 ast.parse(text);recovered[old+'/count_protocol.py']=text.encode()
 for name,field in [('contract.json','source_contract_sha256'),('KERNEL_COPY_MANIFEST.json','source_kernel_manifest_sha256'),('count_protocol.py','source_checker_sha256')]:
  value=hashlib.sha256(recovered[old+'/'+name]).hexdigest()
  s.need(value==port[field]and value in plan['historical_reference_pins'][old+'/'+name],
   'Every entire reconstructed original file equals its independently pinned historical bytes: '+name)
 for name,pin in manifest['files'].items():
  value=raw(new+'/'+name);s.need(hashlib.sha256(value).hexdigest()==pin,'Every original helper is preserved byte-for-byte')
  recovered[old+'/'+name]=value
 return recovered

def reconstruct(cache,index):
 s.need(type(index)is int and index in(24,25,26),'Exactly the three original mixed-resource panels')
 old=f'cutoff25_20261011/new_root/global_alpha_stoploss2_b5_p{index}_v12'
 new=f'cutoff25_20261011/new_root/global_local_contact_b5_p{index}_v14'
 plan=s.plan();recovered=recovered_original24(cache)if index==24 else{};files={}
 def raw(name):
  name=member(name);value=recovered[name]if name in recovered else original_bytes(cache,name,plan)
  files['work/'+name]=hashlib.sha256(value).hexdigest();return value
 def file_pin(name):raw(name);return files['work/'+member(name)]
 def read(name):return json.loads(raw(name),object_pairs_hook=s.base.unique)
 before,after=read(old+'/contract.json'),read(new+'/contract.json')
 s.need(type(before['rows'])is list and len(before['rows'])==1
  and type(after['rows'])is list and len(after['rows'])==1,'Entire one-row original and extended contracts')
 cfg=before['rows'][0];expected=deepcopy(cfg)
 s.need(type(cfg['n'])is int and cfg['n']==25 and type(cfg['index'])is int and cfg['index']==index
  and cfg['K']=='0'and cfg['p']==[str(F(index,100)),str(F(index+1,100))]
  and[cfg['rho_lower'],cfg['rho_upper']]==['3/2','33/20']
  and 'local_contact_allowance'not in cfg and 'local_contact_premise'not in cfg,
  'Literal original whole-panel n25 profile, not an already assumed contact extension')
 expected.update(local_contact_allowance='5/16',local_contact_premise=deepcopy(sem.CONTACT))
 s.need(sem.same(after['rows'][0],expected)and after['status']==
  'EXACT_GLOBAL_GUARDS_AND_LOCAL_CONTACT_RHO_FEEDBACK_CONDITIONAL_UNTIL_V8_COMPOSITION',
  'Exactly the original guards and the two explicit same-witness contact fields')
 oldmap=read(old+'/KERNEL_COPY_MANIFEST.json')['files'];newmap=read(new+'/KERNEL_COPY_MANIFEST.json')['files']
 additions=read(CENTRAL+'/LOCAL_CONTACT_V14_ADDITIONS.json')
 additions_pin=files['work/'+CENTRAL+'/LOCAL_CONTACT_V14_ADDITIONS.json']
 s.need(member(additions['source_directory'])==CENTRAL
  and not(set(additions['files'])|{'LOCAL_CONTACT_V14_ADDITIONS.json'})&set(oldmap),
  'Exact separately reviewed disjoint contact additions, with no native-helper replacement')
 want=dict(oldmap,**additions['files']);want['LOCAL_CONTACT_V14_ADDITIONS.json']=additions_pin
 s.need(sem.same(newmap,want)and file_pin(new+'/LOCAL_CONTACT_V14_ADDITIONS.json')==additions_pin,
  'Whole unchanged V12 manifest plus all and only the complete reviewed V14 additions')
 for name,pin in oldmap.items():
  s.need(hashlib.sha256(raw(old+'/'+name)).hexdigest()==hashlib.sha256(raw(new+'/'+name)).hexdigest()==pin,'Every entire original native helper remains byte-identical')
 for name,pin in additions['files'].items():
  s.need(hashlib.sha256(raw(CENTRAL+'/'+name)).hexdigest()==hashlib.sha256(raw(new+'/'+name)).hexdigest()==pin,'Every entire reviewed contact helper remains byte-identical')
 projected=s.functions(cache,PRODUCER,['checker'],context=dict(need=s.need,ast=ast))
 raw(PRODUCER)
 s.need(projected.checker(raw(old+'/count_protocol.py').decode(),5,index)==raw(new+'/count_protocol.py').decode(),
  'Exactly the original three-location pure native checker port, no new arithmetic')
 port=read(new+'/SOURCE_PORT.json')
 s.need(port['status']=='SOURCE_ONLY_V14_NATIVE_PORT_NOT_ACCEPTED'and member(port['source_native'])==old,
  'Original source preparation is preserved as provenance, never relabelled as an acceptance')
 old_root=port['source_native'].split('/work/',1)[0]
 def historical_capture(name,value):
  # The immutable SOURCE_PORT/REVIEW bytes themselves bind these entries.
  # Their absent old streams are deliberately NOT staged, rewritten, imported
  # or called current arithmetic. Every actual current parent and primitive
  # must instead pass its own complete stopped-output reader.
  if name.startswith(old_root+'/runs/'):
   rel=name[len(old_root)+1:];s.tx.parts(rel)
   s.need(type(value)is str and len(value)==64 and all(c in'0123456789abcdef'for c in value),
    'Exact historical capture identity is provenance only')
   return True
  return False
 expected_pins={
  'producer_sha256':PRODUCER,'source_review_sha256':str(Path(PRODUCER).parent/'ROOT_REVIEW.json').replace('\\','/'),
  'source_contract_sha256':old+'/contract.json','source_checker_sha256':old+'/count_protocol.py',
  'source_kernel_manifest_sha256':old+'/KERNEL_COPY_MANIFEST.json',
  'central_additions_manifest_sha256':CENTRAL+'/LOCAL_CONTACT_V14_ADDITIONS.json'}
 for field,name in expected_pins.items():s.need(port[field]==file_pin(name),'Every independently pinned original source-port edge '+field)
 for name,value in port['source_sha256'].items():
  if historical_capture(name,value):continue
  key=member(name)
  if key in plan['files']or key in recovered:s.need(file_pin(key)==value,'Whole unchanged original available source-port graph')
  else:s.need(value in plan['historical_reference_pins'].get(key,[]),'Absent historical provenance is kept explicitly unacquired, not a substituted current fact')
 for name,pin in before['source_inputs_sha256'].items():s.need(after['source_inputs_sha256'].get(name)==pin,'Every original acquired-parent graph edge remains in the immutable contract')
 for name,pin in port['source_sha256'].items():
  s.need(name.startswith(old_root+'/'),'Every immutable historical preparation edge is inside its exact original namespace')
  rel=name[len(old_root)+1:];s.tx.parts(rel)
  s.need(after['source_inputs_sha256'].get(rel)==pin,'The complete original preparation graph remains in the immutable contract, without relabelling its provenance')
 review=read(REVIEW)
 s.need(review['status']=='REVIEWED_CONDITIONAL_LOCAL_CONTACT_V14_SOURCE_AND_ANALYTIC_EDGE','Exact independent original source/analytic review')
 for name,value in review['source_sha256'].items():
  if historical_capture(name,value):continue
  key=member(name)
  if key in plan['files']or key in recovered:s.need(file_pin(key)==value,'Entire original available review source graph')
  else:s.need(value in plan['historical_reference_pins'].get(key,[]),'Missing historical review provenance is never called fresh evidence')
 for name,pin in additions['files'].items():
  s.need(review['source_sha256'].get(old_root+'/work/'+CENTRAL+'/'+name)==pin,
   'Original review pins every actual contact addition in its unchanged original namespace')
 return dict(capsule='work/'+new,contact_allowance='5/16',premise=deepcopy(sem.CONTACT),
  finite_feedback_rounds=3,rho_upper_rounding_denominator=10**9,original_cfg_sha256=canonical(cfg),
  new_contract_sha256=file_pin(new+'/contract.json'),additions_manifest_sha256=additions_pin),files
