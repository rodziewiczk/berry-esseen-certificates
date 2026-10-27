"""Complete original actual20 interfaces and closed49-forest union.

Original math/control definitions load only inside the explicit Colab worker.
The clean reader uses independently sealed full mathematical reference objects,
then revalidates every actual native/root/leaf/current-parent transaction.
"""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import hashlib,importlib.util,json,sys
from . import finite2024_actual20_full as full,finite2024_remaining_sources as s,actual20_semantic_sources as extra
from . import finite1039_sources as cs,finite1039_count_evidence as ce
from . import finite2024_remaining_evidence as ev
from .finite1039_count_evidence import same
from .finite2124_full_join_worker import canonical
from .finite2024_join_scalar import exact_native_target
B,C=full.B,full.C
REFERENCE_PIN='f33e0182844ecc3982f68bbaf47a492013f43a67ab22163017fc4cd4118d66bf'
MODULES=(('review_scalar_moments',C+'analytic/review_scalar_moments.py'),('review_bn_interfaces',C+'analytic/review_bn_interfaces.py'),
 ('original_b0_union_contracts',C+'b0/union_contracts_v1.py'),('original_closed20_scope',B+'finite/feedback_b0_family_v1/scope.py'),
 ('original_closed40_scope',B+'finite/subpanel_count_v1/compose_v3.py'),
 ('geometry_audit',C+'bn/full_union_v6/geometry_audit.py'),('resource_scope',C+'bn/full_union_v6/resource_scope.py'),
 ('original_bn_full_union',C+'bn/full_union_v6/assemble.py'))
def dump(x):return(json.dumps(x,indent=2)+'\n').encode()
def modules(capsule):
 out={};old=list(sys.path)
 try:
  for name,n in MODULES:
   p=Path(capsule)/n;s.ordinary(p);sys.path.insert(0,str(p.parent));spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec)
   sys.modules[name]=m;spec.loader.exec_module(m);s.need(Path(m.__file__).resolve()==p.resolve(),'Whole original interface module origin');out[name]=m
 finally:sys.path[:]=old
 return out

def interface(c,band,i,contract,mods):
 c=Path(c);u=mods['original_b0_union_contracts'];bn=mods['review_bn_interfaces']
 generation='feedback'if band=='BN'or i>=41 else'coarse'
 family='fourier/feedback_bn_resources_v1'if band=='BN'else'finite/'+('feedback20_b0_resources_v1'if generation=='feedback'else'sharp20_b0_resources_all_v1')
 resource=c/(B+family);row=s.read(resource/f'rows/{i:03d}.json')
 if band=='B0':
  mapper='feedback_b0_scalar_map_v1'if generation=='feedback'else'b0_all_inward_v1'
  scalar=s.read(c/(B+'analytic/'+mapper+'/MAPPED.json'))['rows'][i]
  coupled_rows=s.read(c/(B+('analytic/feedback_b0_coupled_all_v1'if generation=='feedback'else'finite/coupled_noise_all_v1')+'/MAPPED.json'))['rows']
  coupled=next((x for x in coupled_rows if x['index']==i),None)
  if generation=='feedback':
   proof=dict(inward=scalar,coupled=coupled);result=u.verify_contract(contract,row,scalar,coupled)
   validate=lambda x:u.verify_contract(x,row,scalar,coupled)
  else:
   inward=s.read(c/(B+f'finite/sharp20_b0_counts_all_v1/capsule{i}/INWARD_DERIVATION.json'))
   proof=dict(inward=inward,scalar=scalar,coupled=coupled if i==40 else None);result=u.verify_old(contract,row,inward,scalar,coupled if i==40 else None)
   validate=lambda x:u.verify_old(x,row,inward,scalar,coupled if i==40 else None)
  changes=[('n',21),('K','1'),('p',['0','1']),('Lambda','0'),('gap_charge','1000'),('sign_premise',{})]
 else:
  family='feedback_bn_count_v1'if i in(37,42)else'feedback_bn_remaining_v1'
  proof=s.read(c/(B+f'fourier/{family}/capsule{i}/SCALAR_DERIVATION.json'));base=bn.base(row);bn.scalar(base,proof)
  expected=deepcopy(base);expected.update(rho_lower=proof['rho_floor'],acquired_p_lower=proof['acquired_p_lower'],acquired_lambda_upper=proof['acquired_lambda_upper'])
  margins=bn.validate_native(contract,row,proof,expected);result=dict(index=i,original_Lambda=expected['Lambda'],
   acquired_lambda_upper=expected['acquired_lambda_upper'],rho_lower=expected['rho_lower'],acquired_p_lower=expected['acquired_p_lower'],signed_quadratic_margins=margins)
  validate=lambda x:bn.validate_native(x,row,proof,expected)
  changes=[('n',True),('n',21),('index',True),('p',['0','1']),('D','0'),('Lambda','0'),('gap_charge','1000'),
   ('acquired_lambda_upper','0'),('rho_lower','1'),('acquired_mean',['0','0']),('sign_premise',{})]
 controls=[]
 for field,value in changes:
  bad=deepcopy(contract);bad['rows'][0][field]=value
  try:validate(bad)
  except(ValueError,KeyError,TypeError):controls.append(field)
  else:raise ValueError('Original whole simultaneous native interface mutation accepted')
 s.need(contract['resource_row_sha256']==s.digest(resource/f'rows/{i:03d}.json'),'Entire unchanged original physical row')
 return dict(band=band,index=i,generation=generation,resource_relative=B+('fourier/feedback_bn_resources_v1'if band=='BN'else'finite/'+('feedback20_b0_resources_v1'if generation=='feedback'else'sharp20_b0_resources_all_v1')),
  current_row_sha256=s.digest(resource/f'rows/{i:03d}.json'),whole_physical_row_canonical_sha256=canonical(row),
  whole_original_contract_cfg_canonical_sha256=canonical(contract['rows'][0]),whole_scalar_proof=proof,
  mathematical_interface=result,negative_controls=controls,historical_parent_hashes_rewritten=False)

def closed_parts(i,objects,scope,scope40):
 """All14 original union controls, including typed/root/target mutations."""
 m=len(objects);s.need(m in(1,2,4),'Exactly the original complete one/two/four-piece panel')
 if m==1:
  s.need(objects[0]['forest'].get('subpanel')is None and objects[0]['receipt'].get('subpanel')is None,'Full native probability panel')
  return []
 first=objects[0]['forest'];tag='_SUBPANEL_'+str(m)+'_0'
 if first['schema'].startswith('ACTUAL20_SHARP_B0_P40_SUBPANEL_'):
  prep=dict(n=20,index=40,parts=m,original_p=['2/5','41/100'],
   rows=[dict(subpanel=x['forest']['subpanel'],directory=f'parts{m}/part{j}')for j,x in enumerate(objects)],
   original_contract_sha256=first['contract_sha256'],kernel_sha256=first['kernel_sha256'])
  scope40.validate_scopes(prep,objects,m);return scope40.mutation_controls(prep,objects,m)
 s.need(first['schema'].endswith(tag)and objects[0]['receipt']['status'].endswith(tag),'Literal original native subpanel labels')
 prep=dict(n=20,index=i,parts=m,original_p=[str(F(i,100)),str(F(i+1,100))],
  rows=[dict(subpanel=x['forest']['subpanel'])for x in objects],original_contract_sha256=first['contract_sha256'],kernel_sha256=first['kernel_sha256'],
  base_schema=first['schema'][:-len(tag)],base_status=objects[0]['receipt']['status'][:-len(tag)])
 scope.validate_union(prep,objects);return scope.mutation_controls(prep,objects)

def compute(task,band):
 task=Path(task);c=task/'capsule';request=s.read(task/'CURRENT_FULL_INPUTS.json');full.parent_files(task,request);mods=modules(c)
 selected={r['job_id']:r for r in cs.jobs('n20_24')if r['n']==20 and r['band']==band};records={r['job_id']:r for r in request['counts']}
 by_index={};inputs={};seen=set();total_leaves=total_nodes=0;maximum=F(0)
 for key,spec in selected.items():
  rec=records[key];parent=task.joinpath(*s.parts(rec['task_relative']));checked=ce.validate_completed(parent);s.need(same(checked,rec['validated']),'All native fresh mathematical acceptances')
  folder=parent/'capsule'/spec['directory'];s.need(s.digest(folder/spec['contract_name'])==spec['contract_sha256']and s.digest(folder/spec['candidate'])==spec['candidate_sha256'],'Entire immutable original count inputs')
  contract=s.read(folder/spec['contract_name']);forest=s.read(folder/spec['candidate'],limit=128*s.MIB);receipt=s.read(parent/checked['summary']['receipt_relative'])
  item=interface(c,band,spec['index'],contract,mods);stats=receipt['statistics'];s.need(F(stats['maximum_score'])<F(forest['target'])==exact_native_target(),'Exact original strict score and rigorous CE target')
  resource=c/item['resource_relative'];item.update(job_id=key,contract_sha256=spec['contract_sha256'],current_count_stage_sha256=checked['stage_result_sha256'],statistics=stats,
   native_p=forest.get('subpanel',{}).get('p',contract['rows'][0]['p']),subpanel=forest.get('subpanel'),
   current_candidate_sha256=s.digest(resource/'CANDIDATE.json'),current_acceptance_sha256=s.digest(resource/'ACCEPTED.json'),
   historical_candidate_sha256=contract['resource_candidate_sha256'],historical_acceptance_sha256=contract['resource_replay_sha256'])
  by_index.setdefault(spec['index'],[]).append(dict(item=item,forest=forest,receipt=receipt));inputs[key]=item
 panels=[];map_folder=B+('root/feedback_bn_scalar_map_v1'if band=='BN'else'analytic/feedback_b0_scalar_map_v1')
 mapped=s.read(c/(map_folder+'/MAPPED.json'))
 family=B+('fourier/feedback_bn_resources_v1'if band=='BN'else'finite/feedback20_b0_resources_v1')
 candidate=s.read(c/(family+'/CANDIDATE.json'));s.need(len(candidate['rows'])==len(mapped['rows'])==100,'Whole original100-panel probability domain')
 for i,desc in enumerate(candidate['rows']):
  row=s.read(c/(family+'/'+desc['path']));s.need(desc['index']==i and s.digest(c/(family+'/'+desc['path']))==desc['sha256'],'Whole actual resource row')
  panel=dict(index=i,p=[str(F(i,100)),str(F(i+1,100))],resource_row_sha256=desc['sha256'])
  if row['result']['excluded']:
   s.need(i not in by_index and row['status']=='EXCLUDED_BY_SAME_LAW_RESOURCE','No missing forest can masquerade as exclusion');panel['method']='RESOURCE'
  elif i==(34 if band=='BN' else 36):
   scalar=mapped['rows'][i];s.need(F(scalar['rho_floor'])>F('9/8'if band=='BN'else'11/10'),'Strict original all-law scalar contradiction')
   if band=='BN':mods['review_bn_interfaces'].scalar(mods['review_bn_interfaces'].base(row),None)
   panel.update(method='STRICT_SCALAR',scalar_proof=scalar)
  else:
   pieces=sorted(by_index[i],key=lambda x:F(x['item']['native_p'][0]));cursor=F(i,100)
   for x in pieces:
    p=x['item']['native_p'];s.need(F(p[0])==cursor<F(p[1])<=F(i+1,100),'Every closed piece, no gap/overlap/duplicate');cursor=F(p[1]);seen.add(x['item']['job_id'])
    stats=x['receipt']['statistics'];total_leaves+=stats['leaves'];total_nodes+=stats['nodes'];maximum=max(maximum,F(stats['maximum_score']))
   s.need(cursor==F(i+1,100),'Full final closed probability endpoint')
   controls=closed_parts(i,pieces,mods['original_closed20_scope'],mods['original_closed40_scope'])
   if band=='BN':
    descriptors=[dict(index=i,p=x['item']['native_p'],contract_sha256=x['forest']['contract_sha256'],
     kernel_sha256=x['forest']['kernel_sha256'],target=x['forest']['target'])for x in pieces]
    mods['original_bn_full_union'].validate_cover(i,descriptors)
    controls+=['BN: '+name for name in mods['original_bn_full_union'].cover_controls(i,descriptors)]
   panel.update(method='FULL_NATIVE_COUNT',pieces=[x['item']for x in pieces],closed_union_controls=controls)
  panels.append(panel)
 s.need(seen==set(selected)and len(panels)==100,'Every actual20 full forest and all100 panels')
 return dict(schema='COMPLETE_CURRENT_ACTUAL20_ORIGINAL_REGIONAL_MATH_V1',n=20,band=band,rho=['1','11/10']if band=='B0'else['11/10','9/8'],
  p=['0','1'],panels=panels,count_forests=len(selected),count_panels=len(by_index),count_leaves=total_leaves,count_nodes=total_nodes,maximum_score=str(maximum),
  original_interface_source_sha256={n:s.digest(c/relative)for n,relative in MODULES},
  every_original_count_acceptance_revalidated=True,historical_constructor_captures_claimed_current=False,conditional_region_excluded=True,global_proof_accepted=False)

def references():
 p=s.ROOT/'proof/actual20_full_interface_references.json';s.need(s.digest(p)==REFERENCE_PIN,'Whole independently checked49 original actual20 interface reference table')
 r=s.read(p);s.need(r['schema']=='IMMUTABLE49_ACTUAL20_FULL_INTERFACE_REFERENCES_V1'and r['current_execution_acquired']is False and r['global_proof_accepted']is False,'Reference data is not an execution result')
 return r

def validate(task,key,stdout):
 task=Path(task);c=task/'capsule';request=s.read(task/'CURRENT_FULL_INPUTS.json');full.parent_files(task,request)
 path=c/('CURRENT_JOIN_'+key+'.json');r=s.read(path);reference=references()
 s.need(stdout.splitlines()[-1]=='COMPLETE_CURRENT_ACTUAL20_REGION '+key+' '+s.digest(path),'Actual stopped full original regional output terminal')
 if key=='GLOBAL':
  expected=global_join(task);s.need(same(r,expected),'Whole actual20 B0/BN/high-rho current conjunction');return dict(region='GLOBAL',conditional_actual20_verified=True,global_proof_accepted=False)
 s.need(set(r)==set(reference['region_shapes'][key])and r['schema']=='COMPLETE_CURRENT_ACTUAL20_ORIGINAL_REGIONAL_MATH_V1'
  and r['n']==20 and type(r['n'])is int and r['band']==key and r['rho']==(['1','11/10']if key=='B0'else['11/10','9/8'])
  and r['p']==['0','1']and r['every_original_count_acceptance_revalidated']is True and r['conditional_region_excluded']is True
  and r['historical_constructor_captures_claimed_current']is False and r['global_proof_accepted']is False,'Full exact original regional domain and conditional scope')
 s.need(len(r['panels'])==100,'Every closed original probability panel')
 records={x['job_id']:x for x in request['counts']};selected={x['job_id']:x for x in cs.jobs('n20_24')if x['n']==20 and x['band']==key}
 used=set();leaves=nodes=0;maximum=F(0);count_panels=0
 for i,(row,ref)in enumerate(zip(r['panels'],reference['panels'][key])):
  s.need(row['index']==i and type(row['index'])is int and row['p']==[str(F(i,100)),str(F(i+1,100))]and row['method']==ref['method']
   and row['resource_row_sha256']==ref['resource_row_sha256'],'Whole exact original100-panel disposition')
  current_resource=c/(B+('fourier/feedback_bn_resources_v1'if key=='BN'else'finite/feedback20_b0_resources_v1'))
  current_row=current_resource/f'rows/{i:03d}.json';s.need(s.digest(current_row)==ref['resource_row_sha256'],'Whole genuinely current original reference physical row')
  if row['method']=='RESOURCE':s.need(set(row)==set(ref)and s.read(current_row)['result']['excluded']is True,'Real original resource exclusion')
  elif row['method']=='STRICT_SCALAR':s.need(same(row,ref),'Whole independently checked strict scalar certificate')
  else:
   count_panels+=1;s.need(set(row)==set(ref)and len(row['pieces'])==len(ref['pieces'])and row['closed_union_controls']==ref['closed_union_controls'],
    'All original closed pieces and the full14 original union corruption controls')
   for piece,old in zip(row['pieces'],ref['pieces']):
    job=piece['job_id'];s.need(job in selected and job not in used,'Exactly one use of every full selected actual20 native forest');used.add(job)
    spec=selected[job];rec=records[job];parent=task.joinpath(*s.parts(rec['task_relative']));checked=ce.validate_completed(parent)
    s.need(same(checked,rec['validated']),'Every current full original acceptance revalidated')
    folder=parent/'capsule'/spec['directory'];s.need(s.digest(folder/spec['contract_name'])==spec['contract_sha256']and s.digest(folder/spec['candidate'])==spec['candidate_sha256'],'Immediate whole native forest/contract identities')
    contract=s.read(folder/spec['contract_name']);forest=s.read(folder/spec['candidate'],limit=128*s.MIB);receipt=s.read(parent/checked['summary']['receipt_relative'])
    dynamic={'current_count_stage_sha256','statistics','current_candidate_sha256','current_acceptance_sha256'}
    s.need(set(piece)==set(old)and same({k:v for k,v in piece.items()if k not in dynamic},{k:v for k,v in old.items()if k not in dynamic}),
     'Entire independently reconstructed original simultaneous physical/scalar proof, all fields and both signed margins')
    resource=c/piece['resource_relative'];s.need(s.digest(resource/f'rows/{i:03d}.json')==piece['current_row_sha256']==contract['resource_row_sha256']
     and canonical(s.read(resource/f'rows/{i:03d}.json'))==piece['whole_physical_row_canonical_sha256']
     and piece['current_count_stage_sha256']==checked['stage_result_sha256']and piece['current_candidate_sha256']==s.digest(resource/'CANDIDATE.json')
     and piece['current_acceptance_sha256']==s.digest(resource/'ACCEPTED.json')and piece['historical_candidate_sha256']==contract['resource_candidate_sha256']
     and piece['historical_acceptance_sha256']==contract['resource_replay_sha256']and same(piece['statistics'],receipt['statistics'])
     and piece['subpanel']==forest.get('subpanel')and piece['native_p']==forest.get('subpanel',{}).get('p',contract['rows'][0]['p'])
     and F(receipt['statistics']['maximum_score'])<F(forest['target'])==exact_native_target(),'Current full parent binding with every original historical header retained')
    leaves+=receipt['statistics']['leaves'];nodes+=receipt['statistics']['nodes'];maximum=max(maximum,F(receipt['statistics']['maximum_score']))
 s.need(used==set(selected)and r['count_forests']==len(used)and r['count_panels']==count_panels and r['count_leaves']==leaves
  and r['count_nodes']==nodes and F(r['maximum_score'])==maximum,'Every full original forest, exact complete node/leaf/score census')
 s.need(r['original_interface_source_sha256']=={n:s.digest(c/relative)for n,relative in MODULES},'All whole current original mathematical/control source files')
 return dict(region=key,panels=100,count_forests=len(used),count_panels=count_panels,count_leaves=leaves,conditional_region_excluded=True,global_proof_accepted=False)

def global_join(task):
 c=Path(task)/'capsule';b0,bn=(s.read(c/('CURRENT_JOIN_'+k+'.json'))for k in('B0','BN'));high=s.read(c/(B+'root/high_rho_join_v1/JOINED.json'))
 s.need(b0['conditional_region_excluded']is bn['conditional_region_excluded']is True and b0['count_panels']==22 and bn['count_panels']==11
  and b0['count_forests']==30 and bn['count_forests']==19 and len(b0['panels'])==len(bn['panels'])==100,'Complete original B0+BN200-panel49-forest conjunction')
 s.need(high['excluded_rho']==['9/8','infinity']and high['remaining_rho']==['1','9/8']and high['remaining_upper_endpoint_open']is True
  and high['universal_rho_from']=='6/5'and high['supported_rho']==['9/8','6/5']and F(high['constant_check']['CE_lower'])>F(4097,10000),
  'Entire original high-rho/universal/published complement and exact strict CE enclosure')
 for n in('root/sharp20_premise_join_v1/JOINED.json','analytic/feedback20_premise_join_v1/JOINED.json','analytic/feedback_resources_join_v1/JOINED.json'):
  packet=s.read(c/(B+n));s.need(packet.get('cutoff20_proved',False)is False and packet['n']==20,'Same actual contrary witness, no global promotion')
 return dict(schema='COMPLETE_CURRENT_ACTUAL20_CONDITIONAL_REGIONAL_CONJUNCTION_V1',n=20,K='0',target='CE',
  rho_cover=[['1','11/10'],['11/10','9/8'],['9/8','infinity']],p=['0','1'],closed_seams=['11/10','9/8'],
  B0_sha256=s.digest(c/'CURRENT_JOIN_B0.json'),BN_sha256=s.digest(c/'CURRENT_JOIN_BN.json'),high_sha256=s.digest(c/(B+'root/high_rho_join_v1/JOINED.json')),
  count_forests=49,probability_panels=200,conditional_actual20_verified=True,retained_analytic_framework_required=True,global_proof_accepted=False)

def main(task,key):
 s.need(__debug__ and sys.dont_write_bytecode and not sys.flags.optimize,'Ordinary-B full original actual20 mathematical worker')
 result=global_join(task)if key=='GLOBAL'else compute(task,key);path=Path(task)/'capsule'/('CURRENT_JOIN_'+key+'.json')
 s.need(not path.exists(),'Fresh full original regional output');path.write_bytes(dump(result));print('COMPLETE_CURRENT_ACTUAL20_REGION',key,s.digest(path),flush=True)
