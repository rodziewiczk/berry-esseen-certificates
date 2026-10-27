"""58H complete actual20--24 acquisition and finite-only current conjunction.

Run in Colab after58A--G,52 and56K. All40 original actual20 calls plus one
explicit conditional scalar-parent call and all8 complete
100-panel band joins have genuine stopped evidence; each new call has separate
CPU/wall82800 limits. Complete verified prefix actions can resume, with all
original numerical domains/controls intact. No25+ tail or global proof flag.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
from copy import deepcopy
import hashlib,json,shutil,sys,traceback,uuid
from . import finite2024_remaining_sources as src,actual20_semantic_sources as extra
from . import finite2024_actual20_full as actual,finite2024_actual20_math as actual_math
from . import finite2124_full_join as bands,finite2124_core_sources as cores,finite2124_core as corer,finite2124_core_evidence as coree
from . import finite2124_high_sources as highs,finite2124_high as highr,finite2124_high_evidence as highe
from . import finite2024_fourier_sources as fs,finite2024_fourier as fr,finite2024_fourier_evidence as fe
from . import finite1920_feedback_sources as gs,finite1920_feedback as gr,finite1920_feedback_evidence as ge
from . import finite1039_sources as cs,finite1039_counts as cr,finite1039_count_evidence as ce
from . import finite1014_kappa_sources as ks,finite1014_kappa as kr,finite1014_kappa_evidence as ke
from . import finite2024_induction as induction,stopped_prefix as prefix,delivery_transport as tx,runtime_origin
from .finite1039_count_evidence import same
from .finite1014_join_evidence import ANALYTIC_PREMISES
from .colab_batch import atomic_json,event,utc
SCHEMA='COMPLETE58H_ACTUAL20_24_CURRENT_SESSION_V1'
COMPLETE='COMPLETE_CONDITIONAL_FINITE20_24'
FALSE=dict(global_proof_accepted=False,all_index_conclusion_verified=False,analytic_premises_acquired=False,cutoff20_proved=False)
READERS=dict(auxiliary=fe.validate_completed,universal=fe.validate_completed,supported=fe.validate_completed,
 feedback=ge.validate_completed,high=highe.validate_completed,scalar56K=ke.validate_completed)

def stage(root,key,hit):
 task,checked,export=hit
 return dict(key=key,task_relative=Path(task).relative_to(root).as_posix(),validated=checked,export=export)
def task_of(root,row):return src.ordinary(Path(root).joinpath(*src.parts(row['task_relative'])))
def import_inputs(root,durable,status):
 root=Path(root);durable=Path(durable);rows=[];missing=[]
 for key in fs.FAMILIES:
  hit=fr.restore_completed(durable/('finite2024-fourier-'+key)/'completed'/fs.PLAN_SHA256[:16],root/'imports'/key,key,root=root)
  if hit:rows.append(stage(root,key,hit))
  else:missing.append(key)
 for key,module,cache in(
  ('feedback',gr,durable/'finite1920-feedback/completed'/gs.PLAN_SHA256[:16]),
  ('high',highr,durable/'finite2124-highrho/completed'/highs.PLAN_SHA256[:16]),
  ('scalar56K',kr,durable/'finite1014-kappa/completed'/ks.PLAN_SHA256[:16])):
  hit=module.restore_completed(cache,root/'imports'/key,root=root)
  if hit:rows.append(stage(root,key,hit))
  else:missing.append(key)
 for n in range(21,25):
  for band in('B0','BN'):
   key=cores.case(n,band);cache=durable/('finite2124-core-'+band)/'completed'/cores.PLAN_SHA256[:16]/key
   hit=corer.restore_completed(cache,root/'imports/core',n,band,root=root)
   if hit:rows.append(stage(root,'core:'+key,hit))
   else:missing.append('core:'+key)
 for row in cs.jobs('n20_24'):
  cache=durable/'finite1039-counts-n20_24/completed'/cs.CATALOG_SHA256[:16]/cr.slug(row['job_id'])
  hit=cr.restore_stage(cache,root/'imports/counts',row,log_root=root)
  if hit:rows.append(stage(root,'count:'+row['job_id'],hit))
  else:missing.append('count:'+row['job_id'])
 status['imports']=rows;atomic_json(root/'SESSION_RESULT.json',status)
 event(root,'finite2024_complete_input_readback',available=len(rows),required=177,missing=len(missing));return missing

def inputs(root,status):
 by_key={r['key']:r for r in status['imports']};src.need(len(by_key)==len(status['imports'])==177,'Every current58H Fourier/support/scalar/INITIAL/resource/forest input')
 parents={};core={};counts={};wanted=set(READERS)
 for key,reader in READERS.items():
  r=by_key[key];task=task_of(root,r);checked=reader(task);src.need(same(checked,r['validated']),'Complete genuine current upstream input');parents[key]=dict(task=task,checked=checked)
 for n in range(21,25):
  for band in('B0','BN'):
   key='core:'+cores.case(n,band);wanted.add(key);r=by_key[key];task=task_of(root,r);checked=coree.validate_completed(task,expected_n=n,expected_band=band)
   src.need(same(checked,r['validated']),'Whole current four-call original core producer');core[n,band]=dict(task=task,checked=checked)
 for row in cs.jobs('n20_24'):
  key='count:'+row['job_id'];wanted.add(key);r=by_key[key];task=task_of(root,r);checked=ce.validate_completed(task)
  src.need(same(checked,r['validated']),'Full original native source/forest/leaf acceptance without old reader-version reintegration');counts[row['job_id']]=dict(task=task,checked=checked,row=row)
 src.need(set(by_key)==wanted,'No omitted or extra full58H input');return parents,core,counts

def parent_interfaces(parents,core):
 packets={}
 for key in fs.FAMILIES:
  p=parents[key];packets[key]=fs.read(p['task']/'capsule'/fs.result_path(fs.family(key)))
 aux,universal,supported=(packets[k]for k in fs.FAMILIES)
 src.need(aux['n']==list(range(19,25))and F(aux['per_n_upper']['19'])<F(262,625)
  and all(F(aux['per_n_upper'][str(n)])<F(419,1000)for n in range(20,25)),
  'Original licensed GLOBAL19 route and complete actual20--24 owncaps, never sample-size monotonicity')
 q=max(F(0),20*(F(aux['per_n_upper']['19'])-F(819,2000)));src.need(q<F(21,100),'Actual original q21/100 source bound')
 ce_lower=F(40973218,10**8);src.need(ce_lower<actual_math.exact_native_target(),'Original strict CE enclosure, not a rounded upper approximation')
 narrow_q=max(F(0),20*(F(aux['per_n_upper']['19'])-ce_lower))
 src.need(narrow_q<F(19,100),'Strong original GLOBAL19/CE enclosure licenses the narrow BN19/100 allowance')
 feedback=gs.read(parents['feedback']['task']/'capsule'/gs.RESULT);feedback_edges=[]
 for band,qcap,owncap in(('B0',F(29,250),F(831,2000)),('BN',F(23,500),F(103,250))):
  values=feedback['per_band_per_n_upper'][band];allowance=max(F(0),20*(F(values['19'])-ce_lower))
  src.need(allowance<qcap and F(values['20'])<owncap,'Same-law19 and actual20 feedback independently license both original literal premises')
  feedback_edges.append(dict(band=band,same_law19_upper=values['19'],owncap20_upper=values['20'],derived_contact_allowance=str(allowance),
   retained_q=str(qcap),retained_owncap=str(owncap),GLOBAL_sharp19_inferred=False))
 src.need(universal['n']==supported['n']==list(range(20,25))and universal['rho']==['6/5','19/10']
  and supported['rho']==['9/8','6/5']and supported['support_absolute_upper']=='3'
  and max(F(universal['normalized_upper_max']),F(universal['external_tail_upper']),F(supported['uniform_upper']))<F(4097,10000),
  'All literal actual indices in current universal/supported Fourier and full published19/10+ tail')
 hp=parents['high']['task']/'capsule'/highs.NATIVE;hc,ha=highs.read(hp/'CANDIDATE.json'),highs.read(hp/'ACCEPTED.json')
 induction.high(hc,ha,actual_math.exact_native_target())
 # The high-support native stage retains old Fourier packets. Full current
 # Fourier stages license the same or stronger actual numerical theorem.
 # Every original high support ray, interval and strict target remains exact.
 high_rows=[]
 for n in range(21,25):
  for band in('B0','BN'):
   checked=core[n,band]['checked']['summary'];req=checked['request'];rho,radius=cores.BANDS[band]
   src.need(req==dict(n=n,nmax=n,K='0',q='0',owncap='419/1000',band=band,rho_interval=rho,radius=radius,grid=[12,12,6,3]),
    'Actual literal-index closed INITIAL domain, equality-inclusive predecessor and q0')
   src.need(F(aux['per_n_upper'][str(n)])<F(req['owncap']),'Genuine same-index owncap strictly licenses retained INITIAL cap')
   high_rows.append(dict(n=n,band=band,owncap=aux['per_n_upper'][str(n)],q='0',global_predecessor=n-1,
    current_core_stage_sha256=core[n,band]['checked']['stage_result_sha256']))
 scalar=parents['scalar56K'];src.need(scalar['checked']['summary']['kappa']=='62/625','Actual completed whole scalar kappa certificate')
 scalar_files={};prefix_name='work/cutoff25_rethink_20261015/scale_analytic/kappa_62_625_v1/'
 for key in fs.FAMILIES:
  for name in('CERTIFICATE.json','controls.py','kernel.py','PROOF.txt'):
   a=scalar['task']/'capsule'/name;b=parents[key]['task']/'capsule'/prefix_name/name
   src.need(a.read_bytes()==b.read_bytes(),'Retained entire scalar source/certificate equals actual complete56K execution');scalar_files[prefix_name+name]=src.digest(a)
 return dict(actual20_predecessor_license='complete original GLOBAL19 auxiliary ceiling',actual20_conservative_q=str(q),actual20_narrow_q=str(narrow_q),
  actual20_same_law_feedback=feedback_edges,original_strict_CE_lower=str(ce_lower),
  actual21_24_interfaces=high_rows,current_universal_fourier_stage_sha256=parents['universal']['checked']['stage_result_sha256'],
  current_supported_fourier_stage_sha256=parents['supported']['checked']['stage_result_sha256'],
  current_high_support_stage_sha256=parents['high']['checked']['stage_result_sha256'],current_scalar_stage_sha256=scalar['checked']['stage_result_sha256'],
  current_scalar_files_sha256=scalar_files,historical_Fourier_or_scalar_captures_claimed_current=False)

def finite_induction(base,band_results,hc,ha,base_sha,band_shas):
 return induction.ledger(base,band_results,hc,ha,actual_math.exact_native_target(),base_sha,band_shas)
def induction_controls(base,band_results,hc,ha,base_sha,band_shas):
 cases=[('missing band',lambda z:z[1].pop((23,'BN'))),('wrong base index',lambda z:z[0].update(n=True)),
  ('missing original forest',lambda z:z[0].update(count_forests=48)),('lost base rho seam',lambda z:z[0]['rho_cover'][1].__setitem__(0,'111/100')),
  ('false global promotion',lambda z:z[0].update(global_proof_accepted=True)),('wrong immediate predecessor',lambda z:z[1][22,'B0'].update(predecessor_n=20)),
  ('selected law predecessor',lambda z:z[1][21,'BN'].update(predecessor_global_sharp_required=False)),('missing whole panel',lambda z:z[1][24,'B0']['panels'].pop()),
  ('lost final endpoint',lambda z:z[1][23,'BN']['panels'][-1]['p'].__setitem__(1,'999/1000')),('wrong native actual root census',lambda z:next(p for p in z[1][21,'BN']['panels']if'statistics'in p)['statistics'].update(nodes=0)),
  ('missing actual high index',lambda z:z[2]['actual_n'].pop()),('false support allowance',lambda z:z[2]['rows'][1]['proof'].update(q_contact='1/100')),
  ('missing signed high ray',lambda z:z[2]['rows'][2]['proof']['ray_rows'].pop()),('missing native high control',lambda z:z[3]['negative_controls'].pop())]
 result=[]
 for label,change in cases:
  bad=deepcopy([base,band_results,hc,ha]);change(bad)
  try:finite_induction(*bad,base_sha,band_shas)
  except(ValueError,KeyError,TypeError,IndexError):result.append(label)
  else:raise ValueError('Invalid finite-only actual20--24 induction accepted: '+label)
 return result

def validate_batch(root,status):
 root=Path(root);src.need(status['schema']==SCHEMA and all(status[k]is False for k in FALSE),'Explicit conditional finite-only58H scope')
 parents,core,counts=inputs(root,status);interfaces=parent_interfaces(parents,core)
 ar=status['actual20'];task=task_of(root,ar);checked=actual.validate_completed(task);src.need(same(checked,ar['validated']),'All41 genuine full actual20 calls')
 # Require this exact session's actual inputs, not another upstream export
 # that happens to state the same bound.
 request=src.read(task/'CURRENT_FULL_INPUTS.json')
 for key in('auxiliary','universal','supported','feedback'):
  src.need(same(request['parents'][key]['validated'],parents[key]['checked']),'Actual20 consumes the same genuine current Fourier input')
 for rec in request['counts']:src.need(same(rec['validated'],counts[rec['job_id']]['checked']),'Every actual20 forest matches the global finite session')
 result={};shas={};seen=set()
 for record in status['bands']:
  case=(record['n'],record['band']);src.need(case in core and case not in seen,'Exactly the full8 original band actions');seen.add(case)
  path=task_of(root,record);checked=bands.validate_completed(path);src.need(same(checked,record['validated']),'Complete real100-panel source/current COUNT join')
  req=src.read(path/'CURRENT_BAND_INPUTS.json');src.need(same(req['core_validated'],core[case]['checked']),'Same whole actual current INITIAL/resource parent')
  for rec in req['count_inputs']:src.need(same(rec['validated'],counts[rec['job_id']]['checked']),'Same full actual current native forest, all original leaves')
  result[case]=src.read(path/'capsule/CURRENT_BAND_RESULT.json');shas[case]=src.digest(path/'capsule/CURRENT_BAND_RESULT.json')
 src.need(seen==set(core),'No skipped actual21--24 band');base=src.read(task/'capsule/CURRENT_JOIN_GLOBAL.json')
 hp=parents['high']['task']/'capsule'/highs.NATIVE;hc,ha=highs.read(hp/'CANDIDATE.json'),highs.read(hp/'ACCEPTED.json')
 base_sha=src.digest(task/'capsule/CURRENT_JOIN_GLOBAL.json');steps=finite_induction(base,result,hc,ha,base_sha,shas)
 controls=induction_controls(base,result,hc,ha,base_sha,shas)
 return dict(schema='COMPLETE_CURRENT_CONDITIONAL_FINITE20_24_CHAIN_V2',finite_indices=list(range(20,25)),actual20_original_actions=40,
  actual20_total_actions=41,additional_conditional_scalar_parent_actions=1,
  band_join_actions=8,whole_original_forests=163,probability_panels=1000,parent_interfaces=interfaces,induction_steps=steps,
  induction_negative_controls=controls,actual20_sha256=base_sha,conditional_finite_chain_verified=True,incoming25_plus_tail_used=False,
  analytic_premises=list(ANALYTIC_PREMISES),**FALSE)
def validate_completed(root):
 root=Path(root);status=src.read(root/'SESSION_RESULT.json',limit=128*src.MIB)
 src.need(status['state']==COMPLETE and status['conditional_finite_chain_verified']is True,'Full58H finite-only session, never one ordinary sublane')
 checked=validate_batch(root,status);src.need(same(checked,status['finite_summary']),'Entire conditional finite conjunction independently reproduced')
 return dict(session_result_sha256=src.digest(root/'SESSION_RESULT.json'),summary=checked,conditional_finite_chain_verified=True,**FALSE)

def prefix_validator(task):return prefix.validate(task,adapter=actual.Adapter())

def compatible_actual_prefix(task,parents,counts):
 checked=prefix_validator(task);request=src.read(Path(task)/'CURRENT_FULL_INPUTS.json')
 src.need(set(request['parents'])=={'auxiliary','universal','supported','feedback'}and all(
  same(request['parents'][key]['validated'],parents[key]['checked'])for key in request['parents']),
  'Cached actual20 prefix uses the same whole current Fourier epochs')
 records={r['job_id']:r for r in request['counts']};selected={key:item for key,item in counts.items()if item['row']['n']==20}
 src.need(len(records)==len(request['counts'])==49 and set(records)==set(selected)and all(
  same(records[key]['validated'],selected[key]['checked'])for key in records),
  'Cached actual20 prefix uses all same current49 native forest epochs')
 return checked

def compatible_band(task,n,band,core,counts):
 checked=bands.validate_completed(task);request=src.read(Path(task)/'CURRENT_BAND_INPUTS.json')
 src.need((checked['n'],checked['band'])==(n,band)and(request['n'],request['band'])==(n,band)
  and same(request['core_validated'],core[n,band]['checked']),'Cached complete band uses the same current INITIAL/resource epoch')
 records={r['job_id']:r for r in request['count_inputs']};selected={key:item for key,item in counts.items()if(item['row']['n'],item['row']['band'])==(n,band)}
 src.need(len(records)==len(request['count_inputs'])and set(records)==set(selected)and all(
  same(records[key]['validated'],selected[key]['checked'])for key in records),
  'Cached complete band uses every same current native forest epoch')
 return checked

def execute_actual(root,durable,source,supplement,parents,counts,work_root):
 cache=Path(durable)/'finite2024-join/verified-actual20-prefixes'/src.PLAN_SHA256[:16]/extra.PIN[:16]
 hit=tx.restore(cache,Path(root)/'restored-actual20',validator=lambda task:compatible_actual_prefix(task,parents,counts),log=lambda name,**kw:event(root,name,**kw))
 if hit:
  if hit[1]['all_original_actions_completed']is True:
   return hit[0],actual.validate_completed(hit[0]),hit[2]
  task,checked=prefix.resume_origin(hit[0],adapter=actual.Adapter(),work_root=work_root);export=hit[2]
  context=prefix.read(task/'PREFIX.json')['context']
  src.need(context['python_executable']==sys.executable and context['python_version']==sys.version,
   'Completed prefix retained; executing further original capture-bound actions requires its originating interpreter profile. Complete results remain readable.')
  restored_runtime=runtime_origin.ensure_recorded_runtime(context,active_root=src.ROOT)
  event(root,'actual20_recorded_runtime_namespace_ready',**restored_runtime)
 else:
  task=Path(root)/'actual20';actual.prepare(source,supplement,task,parents={k:parents[k]['task']for k in('auxiliary','universal','supported','feedback')},
   count_tasks={key:item['task']for key,item in counts.items()if item['row']['n']==20});export=None
 while len(prefix.read(task/'PREFIX.json')['actions'])<len(actual.specs()):
  next_action=actual.specs()[len(prefix.read(task/'PREFIX.json')['actions'])]['id']
  event(root,'actual20_complete_action_preparing',action=next_action,phase='source_and_current_parent_binding',
   per_action_cpu_seconds=82800,per_action_wall_seconds=82800,shared_batch_deadline=False)
  prefix.advance(task,adapter=actual.Adapter(),root=root)
  export=tx.save(task,cache,validator=prefix_validator,label='actual20-verified-prefix')
  event(root,'actual20_complete_action_prefix_saved',completed_actions=len(prefix.read(task/'PREFIX.json')['actions']),total_actions=len(actual.specs()),**export)
 checked=actual.validate_completed(task)
 if not task.is_relative_to(root):
  out=Path(root)/'actual20-current';shutil.copytree(task,out);task=out
  src.need(same(actual.validate_completed(task),checked),'Portable entire actual20 result survives export path change')
 return task,checked,export

def run_colab(*,durable_root,work_root='/content/berry-esseen-runs',archives='/content/berry-esseen-archives',backup_interval=60):
 stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
 root=Path(work_root).resolve()/'finite2024-join'/stamp;root.mkdir(parents=True,exist_ok=False);durable=Path(durable_root)/'finite2024-join'/stamp
 status=dict(schema=SCHEMA,state='INCOMPLETE',started_utc=utc(),imports=[],actual20=None,bands=[],conditional_finite_chain_verified=False,**FALSE)
 atomic_json(root/'SESSION_RESULT.json',status);backup=tx.Backups(root,durable,backup_interval);backup.start()
 try:
  missing=import_inputs(root,durable_root,status)
  if missing:status.update(state='WAITING',missing=missing)
  else:
   parents,core,counts=inputs(root,status);parent_interfaces(parents,core)
   assets=src.obtain_assets(archives,progress=lambda name,**kw:event(root,name,**kw))
   source=src.prepare_cache(assets,Path(work_root)/'finite2024-remaining-source-cache'/src.PLAN_SHA256[:16],progress=lambda name,**kw:event(root,name,**kw))
   supplement=extra.prepare(assets,Path(work_root)/'finite2024-dynamic-source-cache'/extra.PIN[:16])
   hit=execute_actual(root,durable_root,source,supplement,parents,counts,Path(work_root).resolve());status['actual20']=stage(root,'actual20',hit);atomic_json(root/'SESSION_RESULT.json',status)
   for n in range(21,25):
    for band in('B0','BN'):
     key=cores.case(n,band);cache=Path(durable_root)/'finite2024-join/completed-bands'/src.PLAN_SHA256[:16]/key
     hit=tx.restore(cache,root/'band-stages',validator=lambda task:compatible_band(task,n,band,core,counts),log=lambda name,**kw:event(root,name,**kw))
     if hit:src.need((hit[1]['n'],hit[1]['band'])==(n,band),'Exact selected full band cache')
     else:
      task=root/'band-stages'/key;bands.prepare(source,task,n,band,core_task=core[n,band]['task'],
       count_tasks={k:item['task']for k,item in counts.items()if(item['row']['n'],item['row']['band'])==(n,band)})
      checked=bands.execute_prepared(task,n,band,root=root);hit=(task,checked,tx.save(task,cache,validator=bands.validate_completed,label=key))
     status['bands'].append(dict(n=n,band=band,**stage(root,key,hit)));atomic_json(root/'SESSION_RESULT.json',status)
   summary=validate_batch(root,status);status.update(state=COMPLETE,finite_summary=summary,conditional_finite_chain_verified=True)
   atomic_json(root/'SESSION_RESULT.json',status);validate_completed(root)
 except BaseException as error:
  status.update(state='INCOMPLETE',error=type(error).__name__+': '+str(error),conditional_finite_chain_verified=False)
  (root/'ERROR.txt').write_text(traceback.format_exc(),encoding='utf-8');event(root,'finite2024_full_join_incomplete',error=status['error'])
 finally:
  status['finished_utc']=utc()
  try:backup.close()
  except BaseException as error:status.update(state='INCOMPLETE',backup_error=str(error),conditional_finite_chain_verified=False)
  bundle=tx.final_bundle(root,durable,Path(work_root)/'finite2024-local-exports'/stamp,status)
 return dict(status=status,bundle=bundle,work=str(root))
