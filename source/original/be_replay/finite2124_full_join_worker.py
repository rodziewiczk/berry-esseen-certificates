"""58H: full current21--24 band worker; execute only as a Colab action.

Uses the original independent physical/scalar/coupled routines in full. Current
complete native acceptance replaces the old construct/accept launcher history;
the immutable forest, contract and historical parent hashes are never edited.
No mathematical module is loaded until run() is explicitly called.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json,sys
if __package__ in(None,''):
 sys.path.insert(0,str(Path(__file__).resolve().parents[1]));__package__='be_replay'
from fractions import Fraction as F
from copy import deepcopy
from . import finite2124_core_sources as core_src,finite2124_core_evidence as core_ev
from . import finite1039_sources as count_src,finite1039_count_evidence as count_ev
from . import finite2024_remaining_sources as sources
from .finite1039_count_evidence import same
from .finite2024_join_scalar import exact_native_target,verify_projection

REFERENCE_SHA256='fe0a5549cfe0f92c3c83971b6bd70e0a8ed2c19ae23293cb7ba7a8c386902cda'

MODULES=(
 ('review_scalar_moments','work/continuation_cutoff20_20261016/analytic/review_scalar_moments.py'),
 ('review_bn_interfaces','work/continuation_cutoff20_20261016/analytic/review_bn_interfaces.py'),
 ('monotone_actual','work/continuation_cutoff20_20261016/b0/bridge_counts_v3/monotone_actual.py'),
 ('overlay_actual','work/continuation_cutoff20_20261016/b0/bridge_counts_v3/overlay_actual.py'),
 ('coupled_math','work/continuation_cutoff20_20261016/b0/bridge_counts_v3/coupled_math.py'),
 ('coupled_actual','work/continuation_cutoff20_20261016/b0/bridge_counts_v3/coupled_actual.py'),
 ('contract_helpers','work/continuation_cutoff20_20261016/b0/bridge_counts_v3/contract_helpers.py'),
 ('review_actual_count_family','work/continuation_cutoff20_20261016/analytic/review_actual_count_family.py'))
def dump(x):return(json.dumps(x,indent=2)+'\n').encode()
def canonical(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
def references():
 path=sources.ROOT/'proof/finite2124_full_interface_references.json'
 need(sources.digest(path)==REFERENCE_SHA256,'Exact externally sealed114 immutable physical/scalar interface references')
 result=sources.read(path)
 need(result['schema']=='IMMUTABLE_ACTUAL21_24_114_INTERFACE_REFERENCE_CATALOG_V1'
  and result['original_source_plan_sha256']==sources.PLAN_SHA256 and len(result['references'])==114
  and result['current_execution_acquired']is False and result['global_proof_accepted']is False,'Reference data is not execution evidence')
 expected={r['job_id']for r in count_src.jobs('n20_24')if r['n']>20}
 need(set(result['references'])==expected,'Whole original114-forest interface domain')
 return result['references']
def _modules(cache):
 """Fixed original math sources, separate from all legacy capture consumers."""
 root=Path(cache).resolve();pins=sources.plan()['original_files'];out={};old_path=list(sys.path)
 try:
  for name,relative in MODULES:
   p=root/relative;need(relative in pins and sources.digest(p)==pins[relative]['sha256'],'Every complete original scalar/interface source byte')
   sys.path.insert(0,str(p.parent));spec=importlib.util.spec_from_file_location(name,p);module=importlib.util.module_from_spec(spec)
   sys.modules[name]=module;spec.loader.exec_module(module);need(Path(module.__file__).resolve()==p,'Actual original mathematical module origin')
   out[name]=module
 finally:sys.path[:]=old_path
 return out
def _relative(root,name):return sources.ordinary(Path(root).joinpath(*sources.parts(name)))
def run(root,n,band):
 need(__debug__ and sys.dont_write_bytecode and not sys.flags.optimize,'Ordinary-B full band worker')
 core_src.case(n,band);verify_projection();reference=references();root=Path(root).resolve();request=sources.read(root/'CURRENT_BAND_INPUTS.json')
 need(request['schema']=='CURRENT_FULL21_24_BAND_INPUTS_V1'and request['n']==n and type(request['n'])is int and request['band']==band,
  'One literal complete actual-index band')
 originals=root/'originals';sources.verify_cache(originals);modules=_modules(originals)
 h,audit=modules['contract_helpers'],modules['review_actual_count_family'];core=_relative(root,request['core_task_relative'])
 checked=core_ev.validate_completed(core);need(same(checked,request['core_validated']),'Complete genuine four-call current INITIAL/resource family')
 c=core/'capsule';folder=c/core_src.RESOURCE/core_src.case(n,band)
 candidate=core_src.read(folder/'CANDIDATE.json',128*core_src.MIB);accepted=core_src.read(folder/'ACCEPTED.json',128*core_src.MIB)
 need(candidate['n']==n and candidate['band']==band and candidate['q']==candidate['K']=='0'
  and candidate['owncap']=='419/1000'and len(candidate['rows'])==100 and same(accepted['rows'],candidate['rows']),
  'Whole same-law fresh resource inventory, q0 and actual INITIAL membership')
 selected={r['job_id']:r for r in count_src.jobs('n20_24')if(r['n'],r['band'])==(n,band)}
 inputs={r['job_id']:r for r in request['count_inputs']};need(set(inputs)==set(selected)and len(inputs)==len(request['count_inputs']),
  'Every and only selected full current COUNT transaction for this band')
 counts={};indices={}
 for key,row in selected.items():
  record=inputs[key];task=_relative(root,record['task_relative']);result=count_ev.validate_completed(task)
  need(same(result,record['validated']),'All native roots/leaves, exact sources, successful real stopped acceptance and original24 controls')
  need(row['index']not in indices,'One full forest per actual probability panel')
  counts[key]=dict(row=row,task=task,checked=result);indices[row['index']]=key
 result=[];used=set();leaves=nodes=controls=0;maximum=F(0)
 for i,desc in enumerate(candidate['rows']):
  need(type(desc['index'])is int and desc['index']==i and desc['path']==f'rows/{i:03d}.json','All100 whole canonical row descriptors')
  path=folder/desc['path'];need(sources.digest(path)==desc['sha256'],'Current complete physical resource row')
  row=core_src.read(path,128*core_src.MIB);need(row['n']==n and row['band']==band and row['index']==i and row['status']==desc['status'],
   'Same literal actual n/band/probability panel')
  panel=dict(index=i,p=[str(F(i,100)),str(F(i+1,100))],resource_row_sha256=sources.digest(path))
  if row['status']=='EXCLUDED_BY_SAME_LAW_RESOURCE':
   need(row['result']['excluded']is True and i not in indices,'A real resource exclusion, never a missing comparison')
   panel['disposition']='EXCLUDED_BY_FRESH_RESOURCE';result.append(panel);continue
  need(row['status']=='RESOURCE_ROW_ACQUIRED_FOR_COUNT'and row['result']['excluded']is False,'Only a completely acquired retained row')
  expected,derivation=h.mapped_contract(row,n,band,i);independent,margins=audit.base(row,n,band,i);raw=row['result']['result']
  if expected is None:
   need(i not in indices and derivation['status']=='EXCLUDED_BY_STRICT_ACTUAL_INWARD_MOMENT','Only the original strict scalar exclusion')
   floor,cap=audit.scalar(raw,derivation['scalar'],n,band,i);need(floor>F(raw['rho_hi']),'Independent strict whole scalar contradiction')
   panel.update(disposition='EXCLUDED_BY_STRICT_SCALAR_MOMENT',scalar_proof=derivation);result.append(panel);continue
  need(i in indices,'Every remaining whole probability panel has its actual complete native forest')
  key=indices[i];item=counts[key];spec=item['row'];capsule=item['task']/'capsule'/spec['directory']
  contract=count_src.read(capsule/spec['contract_name']);need(len(contract['rows'])==1 and same(contract['rows'],[expected]),
   'Entire original simultaneous physical/scalar contract, no relaxed domain or changed resource')
  floor,cap=audit.scalar(raw,derivation['scalar'],n,band,i);lo,hi=audit.m.folded(independent['p']);coupled=derivation['coupled']
  if 0<F(independent['d0'])<=lo:
   need(coupled is not None and coupled['coupled_inputs']=={k:independent[k]for k in('n','index','p','d0','Lambda','rho_upper')},'All original simultaneous coupled inputs')
   bound=audit.ns['coupled_check'](lo,hi,F(independent['d0']),F(independent['rho_upper']),F(independent['Lambda']),coupled['coupled_derivation'],n)
   bound=min(F(independent['Lambda']),audit.m.ceiling(bound,10**9));need(bound==F(coupled['coupled_lambda_upper']),'Independent complete coupled derivation')
   cap=min(cap,bound)
  else:need(coupled is None,'Original optional coupled gate')
  independent.update(rho_lower=str(floor),acquired_lambda_upper=str(cap))
  need(same(independent,expected)and derivation['signed_quadratic_margins']==margins,'Independent entire simultaneous physical/scalar contract and both signed phase margins')
  need(contract['n']==n and type(contract['n'])is int and contract['index']==i and type(contract['index'])is int and contract['band']==band
   and contract['K']=='0'and all(contract[k]is False for k in('predecessor_verified','global_bound_proved','cutoff20_proved')),'Exact original native conditional scope')
  original=reference[key];proof_sha=hashlib.sha256(dump(derivation)).hexdigest()
  need(spec['contract_sha256']==original['immutable_contract_sha256']and contract['resource_row_sha256']==original['reference_row_sha256']
   and contract['scalar_derivation_sha256']==original['whole_scalar_proof_sha256']
   and canonical(row)==original['reference_row_canonical_sha256']and canonical(derivation)==original['reference_scalar_canonical_sha256']
   and canonical(expected)==original['whole_contract_cfg_canonical_sha256'],
   'Whole immutable historical row/scalar/contract facts equal the current objects; only JSON serialization order may differ')
  # This binding deliberately retains both original parent header hashes.
  # Current full parent execution and the exact same physical row supply the
  # mathematical premise, without rewriting any completed COUNT contract.
  header=dict(historical_candidate_sha256=contract['resource_candidate_sha256'],historical_acceptance_sha256=contract['resource_replay_sha256'],
   current_candidate_sha256=sources.digest(folder/'CANDIDATE.json'),current_acceptance_sha256=sources.digest(folder/'ACCEPTED.json'),
   current_full_core_stage_sha256=checked['stage_result_sha256'],same_complete_physical_row=True,historical_hashes_rewritten=False,
   original_row_sha256=original['reference_row_sha256'],current_row_sha256=panel['resource_row_sha256'],
   original_scalar_sha256=original['whole_scalar_proof_sha256'],current_scalar_sha256=proof_sha,
   entire_row_and_scalar_canonical_equality_verified=True)
  receipt=count_src.read(item['task']/item['checked']['summary']['receipt_relative'])
  forest=count_src.read(capsule/spec['candidate'],limit=128*count_src.MIB);stats=receipt['statistics']
  need(F(4097,10000)<F(forest['target'])<=exact_native_target()and F(stats['maximum_score'])<F(forest['target']),
   'Whole native strict score below its unchanged exact target and the original rigorous CE lower enclosure')
  for field,value in [('n',True),('n',20),('Lambda','0'),('rho_lower','0'),('acquired_lambda_upper','0'),('sign_premise',{}),('acquired_mean',['0','0']),('p',['0','1'])]:
   bad=deepcopy(independent);bad[field]=value;need(not same(bad,contract['rows'][0]),'Original typed full-contract corruption control');controls+=1
  leaves+=stats['leaves'];nodes+=stats['nodes'];maximum=max(maximum,F(stats['maximum_score']));used.add(key)
  panel.update(disposition='EXCLUDED_BY_FRESH_NATIVE_FULL_COUNT',job_id=key,contract_sha256=spec['contract_sha256'],
   current_count_stage_sha256=item['checked']['stage_result_sha256'],scalar_proof_sha256=proof_sha,scalar_proof=derivation,
   statistics=stats,current_parent_binding=header)
  result.append(panel);print('FULL_CURRENT_INTERFACE',n,band,i,'PASS',flush=True)
 need(used==set(selected)and len(result)==100 and [r['index']for r in result]==list(range(100)),
  'All and only original full forests; whole closed probability cover including both endpoints')
 for i in range(99):need(result[i]['p'][1]==result[i+1]['p'][0],'Every closed original probability seam')
 return dict(schema='CURRENT_COMPLETE_ACTUAL21_24_CONDITIONAL_BAND_V1',n=n,band=band,K='0',target='CE',exact_native_target=str(exact_native_target()),rho_interval=core_src.BANDS[band][0],p_interval=['0','1'],
  panels=result,total_count_leaves=leaves,total_count_nodes=nodes,maximum_recorded_count_score=str(maximum),typed_contract_controls=controls,
  current_full_parent_stage_sha256=checked['stage_result_sha256'],full_original_interface_source_sha256={n:sources.digest(originals/rel)for n,rel in MODULES},
  historical_constructor_execution_claimed_current=False,current_full_count_acceptance_revalidated=True,
  conditional_band_excluded=True,predecessor_n=n-1,predecessor_global_sharp_required=True,predecessor_verified=False,
  global_bound_proved=False,cutoff20_proved=False,all_index_conclusion_verified=False,historical_dependency_graph_reproduced=False,numerical_resource_or_leaf_oracle_calls=0)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('root',type=Path);parser.add_argument('n',type=int);parser.add_argument('band',choices=('B0','BN'));args=parser.parse_args()
 output=run(args.root,args.n,args.band);path=args.root/'CURRENT_BAND_RESULT.json'
 need(not path.exists(),'Fresh complete original-domain band output');path.write_bytes(dump(output))
 print('CURRENT_FULL_BAND_COMPLETE',args.n,args.band,hashlib.sha256(path.read_bytes()).hexdigest(),flush=True)
