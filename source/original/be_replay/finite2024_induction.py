"""Finite20--24 ledger port. Only current base/band identity schemas changed.
No original producer imports, sample-size monotonicity or incoming25+ tail.
"""
"""Exact semantic checks only, no support/resource/count score oracle."""
from fractions import Fraction as F
from hashlib import sha256
import json
def need(ok,msg):
 if not ok:raise ValueError(msg)
def typed_indices(values,expected):need(type(values)is list and all(type(n)is int for n in values)and values==expected,'literal complete actual indices')
def exact_hash(o):return sha256(json.dumps(o,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def base20(o):
 need(o['schema']=='COMPLETE_CURRENT_ACTUAL20_CONDITIONAL_REGIONAL_CONJUNCTION_V1' and type(o['n'])is int and o['n']==20 and o['K']=='0'and o['target']=='CE','complete current conditional actual20 base')
 need(o['conditional_actual20_verified']is True and o['retained_analytic_framework_required']is True and o['global_proof_accepted']is False,'explicit conditional base boundary')
 need(o['rho_cover']==[['1','11/10'],['11/10','9/8'],['9/8','infinity']]and o['p']==['0','1']and o['closed_seams']==['11/10','9/8'],'all original same-law domains and closed seams')
 need(type(o['count_forests'])is int and o['count_forests']==49 and type(o['probability_panels'])is int and o['probability_panels']==200,'every complete original base panel and count forest')
def band(o,n,b,target):
 ranges={'B0':['1','11/10'],'BN':['11/10','9/8']}
 need(o['schema']=='CURRENT_COMPLETE_ACTUAL21_24_CONDITIONAL_BAND_V1'and type(o['n'])is int and o['n']==n and o['K']=='0'and o['target']=='CE'and o['band']==b,'literal actual band theorem')
 need(o['rho_interval']==ranges[b]and o['p_interval']==['0','1']and o['exact_native_target']==str(target),'same full domain and exact strict target')
 need(o['conditional_band_excluded']is True and type(o['predecessor_n'])is int and o['predecessor_n']==n-1 and o['predecessor_global_sharp_required']is True,'global predecessor implication')
 for k in('predecessor_verified','global_bound_proved','cutoff20_proved','historical_dependency_graph_reproduced'):need(o[k]is False,'native false flags preserved '+k)
 need(o['numerical_resource_or_leaf_oracle_calls']==0 and type(o['numerical_resource_or_leaf_oracle_calls'])is int,'composition only')
 need(type(o['panels'])is list and len(o['panels'])==100,'all100 original closed panels');leaves=nodes=0;maximum=F(0)
 for i,p in enumerate(o['panels']):
  need(type(p['index'])is int and p['index']==i and p['p']==[str(F(i,100)),str(F(i+1,100))],'ordered full closed p coverage')
  need(p['disposition']in('EXCLUDED_BY_FRESH_RESOURCE','EXCLUDED_BY_STRICT_SCALAR_MOMENT','EXCLUDED_BY_FRESH_NATIVE_FULL_COUNT'),'no unresolved outcome')
  if p['disposition']=='EXCLUDED_BY_FRESH_NATIVE_FULL_COUNT':
   s=p['statistics'];need(type(s['leaves'])is int and type(s['nodes'])is int and s['leaves']>=n+1 and s['nodes']==2*s['leaves']-(n+1)and F(s['maximum_score'])<target,'full actual n+1 roots and strict bound');leaves+=s['leaves'];nodes+=s['nodes'];maximum=max(maximum,F(s['maximum_score']))
 need(o['total_count_leaves']==leaves and type(o['total_count_leaves'])is int and o['total_count_nodes']==nodes and type(o['total_count_nodes'])is int and F(o['maximum_recorded_count_score'])==maximum,'actual finite totals')
 for j in range(101):
  q=F(j,100);owners=[p['index']for p in o['panels']if F(p['p'][0])<=q<=F(p['p'][1])];need(owners==([0]if j==0 else[99]if j==100 else[j-1,j]),'closed p seam')
 return leaves,nodes

def high(c,a,target):
 need(c['status']=='CONDITIONAL_ACTUAL21_24_HIGH_RHO_EXCLUSION_CANDIDATE'and a['status']=='PASS_FRESH_ACTUAL21_24_HIGH_RHO_REDUCTION_CONDITIONAL_ON_SHARP_PREDECESSORS','complete high-rho conditional theorem')
 for o in(c,a):
  typed_indices(o['actual_n'],[21,22,23,24]);need(o['excluded_rho']==['9/8','infinity']and o['remaining_rho']==['1','9/8']and o['remaining_upper_endpoint_open']is True,'closed high-rho seam')
  for k in('global_predecessors_verified','historical_fourier_replayed','sharp20_proved','cutoff20_proved'):need(o[k]is False,'retained high-rho limitations')
 need(c['strict_fourier_target']=='4097/10000'and F(c['exact_CE_lower'])==target and F(4097,10000)<target,'strict common high-rho score')
 need(type(a['fresh_support_calls'])is int and a['fresh_support_calls']==4 and len(a['negative_controls'])==len(set(a['negative_controls']))==10,'complete four-index fresh acceptance')
 need(len(c['rows'])==4,'all four literal supports')
 for n,row in zip(range(21,25),c['rows']):
  req=row['request'];proof=row['proof'];need(req==dict(n=n,K='0',q='0',rho_upper='6/5',radius='3',sign=0,mesh=10),'literal actual support request')
  need(type(proof['n'])is int and proof['n']==n and proof['K']==proof['q_contact']=='0'and proof['radius']=='3'and proof['rho_upper']=='6/5'and proof['beta_interval']==[str(-F(row['beta_upper'])),row['beta_upper']],'same actual support domain')
  need(type(proof['support_sign'])is int and proof['support_sign']==0 and [x['sign']for x in proof['ray_rows']]==[-1,1],'both support rays retained')
  beta=F(row['beta_upper']);need(0<beta<1 and (1+beta*beta)**2>=F(6,5)**2*(1-beta*beta),'exact Cauchy beta enclosure')

def ledger(base,bands,candidate,accepted,target,base_sha,band_shas):
 base20(base);high(candidate,accepted,target);previous=dict(n=20,conditional_global_sharp=True,base_certificate_sha256=base_sha);steps=[]
 need(set(bands)=={(n,b)for n in range(21,25)for b in('B0','BN')},'all eight actual band statements')
 for n in range(21,25):
  need(previous['n']==n-1 and previous['conditional_global_sharp']is True,'preceding complete global theorem, never monotonicity')
  totals=[band(bands[n,b],n,b,target)for b in('B0','BN')]
  step=dict(n=n,global_predecessor=n-1,predecessor_statement_sha256=exact_hash(previous),predecessor_discharged_within_conditional_chain=True,conditional_global_sharp=True,closed_rho_ranges=[['1','11/10'],['11/10','9/8'],['9/8','infinity']],B0_certificate_sha256=band_shas[n,'B0'],BN_certificate_sha256=band_shas[n,'BN'],high_rho_actual_index=n,total_low_rho_count_leaves=sum(x[0]for x in totals),total_low_rho_count_nodes=sum(x[1]for x in totals),conclusion=f'C{n}<CE under the same retained unrestricted-witness framework as the complete actual20 base.')
  steps.append(step);previous=step
 return steps

