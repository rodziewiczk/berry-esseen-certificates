"""Exact same-law resource/COUNT implications and the closed20-piece union.

No original numerical kernel is imported. A caller must first supply complete
fresh source/capture-validated acquisitions and full native tree acceptances.
These predicates prove their conditional interfaces, not universal analysis.
"""
from __future__ import annotations
from copy import deepcopy
from fractions import Fraction as F
from math import isqrt
import json
from pathlib import Path
from . import n25_full_join_sources as s,n25_count_evidence as evidence

same=evidence.same
LOWER=('1','11/10','6/5','13/10','7/5','3/2','33/20')
MIDDLE=('-13/20','0','4/25','321/1000','2/5','12/25','14/25','307827/500000')
HIGH=('-640471/1000000','0','321/1000','2/5','12/25','14/25','640471/1000000')
TAIL='459061/250000'
CE_FLOOR=F(40973218,10**8)
TARGET=F(76824784444199314310731654405729617052063596250011448874609,
 187500000000000000000000000000000000000000000000000000000000)
CONTACT=dict(schema='ATTAINED_POSITIVE_CLOSED_CONTACT_V1',sample_size=25,
 same_unrestricted_attained_witness=True,positive_closed_threshold=True,score_at_least_CE=True)
RESOURCE_FIELDS=(('D','D'),('d0','d0'),('lambda_max','Lambda'),('H_minus','Hminus'),('H_plus','Hplus'),
 ('radius_minus','radius_minus'),('radius_plus','radius_plus'),('outer0','outer0'),('outer1','outer1'))
PRICES=(('charge_b','binary_charge'),('charge_g','gap_charge'),('charge_h','noise_charge'))

def rational(x):
 s.need(type(x)in(str,int,F)and(type(x)is not str or len(x)<20000),'Exact rational, never float/bool')
 return F(x)
def dec(x):
 if type(x)is str:
  try:return F(x)
  except ValueError:return x
 if type(x)is dict:return{k:dec(v)for k,v in x.items()}
 if type(x)is list:return[dec(v)for v in x]
 return x
def enc(x):
 if type(x)is F:return str(x)
 if type(x)is dict:return{k:enc(v)for k,v in x.items()}
 if type(x)in(list,tuple):return[enc(v)for v in x]
 return x
def T(rho):
 r=rational(rho);s.need(r>=1,'Physical third absolute moment')
 return min(F(469,1000),F(3322,10000)*(1+F(429,1000)/r),F(3031,10000)*(1+F(646,1000)/r))

def scalar_licenses():
 from .finite2024_join_scalar import exact_native_target,verify_projection
 target_source=verify_projection()
 middle=25*(T('33/20')-CE_FLOOR);high=25*(T('7/4')-CE_FLOOR)
 s.need(middle==F(441991,2000000)and high==F(1366497,14000000),'Exact same-law universal predecessor allowances')
 margins=[]
 for rho,beta in[(F(7,4),F(MIDDLE[-1])),(F(7,4),F(13,20)),(F(TAIL),F(HIGH[-1]))]:
  margin=(1+beta*beta)**2-rho*rho*(1-beta*beta)
  s.need(0<beta<1 and margin>0,'Strict signed-second-moment ceiling, both signs')
  margins.append(dict(rho=str(rho),beta=str(beta),margin=str(margin)))
 s.need(T(TAIL)==F(1880920391,4590610000)<CE_FLOOR<TARGET and TARGET==exact_native_target(),
        'Inclusive universal rho tail and strict original count target')
 return dict(middle_contact=str(middle),high_contact=str(high),middle_owncap=str(T('33/20')),
  high_owncap=str(T('7/4')),beta_ceiling_margins=margins,tail_lower_included=TAIL,
  tail_upper=str(T(TAIL)),CE_lower_bound=str(CE_FLOOR),native_target=str(TARGET),
  exact_target_arithmetic_source_sha256=target_source,
  native_target_construction='Original Machin alternating-series pi upper bound and two downward exact integer square roots; the standard identities imply native_target<=CE.',
  CE_scalar_lemma_acquired=False,
  beta_definition='E[X*abs(X)]',normalization='sqrt(25)/rho; D is the total nD weighted defect, raw phase H is signed',
  published_iid_T_inputs_acquired=False)

def profile_license(profile,*,rho,beta=None,lower=False,support=None,predecessor_allowance=None):
 s.need(type(profile)is dict and type(profile['n'])is int and profile['n']==25 and F(profile['barrier'])==0,
        'Same actual-n25 zero-barrier profile')
 inv=profile['invariants'];lo,hi=map(F,rho)
 s.need(F(inv['rho_lo'])==lo and F(inv['rho'])==hi,'Exact whole incoming closed arbitrary-law moment domain')
 if beta is not None:
  s.need(F(inv['beta_lo'])<=F(beta[0])<=F(beta[1])<=F(inv['beta_hi']),
         'The acquired profile contains the entire stated signed beta piece')
 q=F(5,16)if lower else 25*(T(lo)-CE_FLOOR)
 cap=F(profile['cap'])
 if lower:
  s.need(type(support)is dict and predecessor_allowance is not None and F(predecessor_allowance)<=q
   and F(support['q'])==q and F(support['owncap'])==cap and cap>=min(F(support['smoothing_upper']),T(lo)),
   'Actual INITIAL smoothing/owncap certificate and an independently acquired same-law predecessor allowance')
  full=support['full_support']
  s.need(type(full['n'])is int and full['n']==25 and full['K']=='0'and F(full['q_contact'])==q
   and F(full['rho_upper'])==hi and [r['sign']for r in full['ray_rows']]==[-1,1]
   and F(full['radius'])==F(profile['radius'])and all(all(F(r[k])<0 for k in
    ('coefficient_at_R','contact_derivative_at_R','contact_derivative_slope_at_R','contact_upper'))for r in full['ray_rows']),
   'Both complete strict support rays for the same current lower witness/profile')
 else:s.need(cap>=T(lo),'Universal same-law cap fits the actual profile')
 return dict(n=25,rho=list(rho),beta=beta,contact_allowance=str(q),
  same_unrestricted_attained_positive_closed_witness=True,analytic_license_is_conditional=True)

def initial_license(proof,*,rho,beta=None,lower=False,predecessor_allowance=None):
 profile=proof['profile']
 result=profile_license(profile,rho=rho,beta=beta,lower=lower,support=proof.get('support'),
  predecessor_allowance=predecessor_allowance)
 if not lower:
  q=25*(T(rho[0])-CE_FLOOR)
  s.need(F(proof['contact_allowance'])==q and F(proof['universal_own_cap'])==T(rho[0])
   and F(proof['CE_lower'])==CE_FLOOR and F(proof['CE_lower_verified'])==TARGET,
   'Exact current upper/middle same-law contact, owncap and CE licenses')
  supports=proof['initial_signed_support'];s.need(type(supports)is list and len(supports)==2,
   'Both actual support orientations are needed before the finite cover')
  for sign,full in zip((-1,1),supports):
   s.need(full['n']==25 and type(full['n'])is int and full['K']=='0'and full['support_sign']==sign
    and F(full['q_contact'])==q and F(full['rho_upper'])==F(rho[1])
    and [r['sign']for r in full['ray_rows']]==[sign]
    and F(full['radius'])==F(profile['radius_minus'if sign==-1 else'radius_plus'])
    and list(map(F,full['beta_interval']))==list(map(F,beta))
    and all(F(full['ray_rows'][0][k])<0 for k in('coefficient_at_R','contact_derivative_at_R','contact_derivative_slope_at_R','contact_upper')),
    'Complete strict signed support ray for the same whole incoming moment/profile domain')
 return result

def mean_floor(pl,pu,theta,retained):
 s.need(0<=pl<=pu<=1 and 0<=theta<=1 and retained>=0,'Physical variance/mean premises')
 square=(1-theta)*min(pl*(1-pl),pu*(1-pu));grid=10**12
 root=F(isqrt(square.numerator*grid*grid//square.denominator),grid)
 s.need(root*root<=square<(root+F(1,grid))**2,'Downward exact square-root enclosure')
 return max(root,retained)

def polymin(a,b,c,h):
 s.need(h>=0,'Nonnegative full signed threshold cap')
 values=[a,a+b*h+c*h*h]
 if c>0 and 0<-b/(2*c)<h:values.append(a-b*b/(4*c))
 return min(values)

def resource_interface(resource,cfg,*,rho,index,invariants=None):
 """Every physical field consumed by all219 selected ordinary contracts.

This is the exact signed quadratic-envelope implication used by the original
independent regional composers, together with their endpoint/beta/mean/theta
premises. It permits outward domination, never inward rounding.
 """
 allowed={'n','K','index','p','rho_lower','rho_upper','D','d0','Lambda','Hminus','Hplus',
  'radius_minus','radius_plus','outer0','outer1','binary_charge','gap_charge','noise_charge',
  'quadratics','sign_premise','acquired_beta','acquired_mean','acquired_theta_upper',
  'local_contact_allowance','local_contact_premise'}
 s.need(type(cfg)is dict and set(cfg)<=allowed and allowed-{'acquired_theta_upper','local_contact_allowance','local_contact_premise'}<=set(cfg),
        'Entire known simultaneous original count interface, no ignored mathematical fields')
 s.need(type(index)is int and type(cfg['index'])is int and cfg['index']==index and type(cfg['n'])is int
  and cfg['n']==25 and cfg['K']=='0','Literal actual index/barrier/panel')
 s.need(resource['excluded']is False,'Only a genuinely acquired same-law surviving resource')
 obj=dec(resource);r,raw,seed=obj['result'],obj['raw_row'],obj['initial'];lo,hi=map(F,rho)
 pl,pu=map(F,cfg['p']);base=[F(index,100),F(index+1,100)]
 s.need(base[0]<=pl<pu<=base[1]and all(x['pl']==base[0]and x['pu']==base[1]for x in(r,raw,seed)),
        'All simultaneous physical inputs concern the same closed probability panel')
 r=deepcopy(r);r['rho_hi']=min(r['rho_hi'],hi);r['pl'],r['pu']=pl,pu
 s.need(F(cfg['rho_lower'])==lo<=r['rho_lo']<=r['rho_hi']<=F(cfg['rho_upper'])and F(cfg['rho_upper'])<=hi,
        'Literal acquired rho floor and whole outgoing contract rho enclosure')
 comparisons=[]
 for source,target in RESOURCE_FIELDS:
  s.need(0<=r[source]<=F(cfg[target]),'Acquired physical upper bound '+target)
  if target in('d0','Lambda','radius_minus','radius_plus','outer0','outer1'):s.need(F(cfg[target])>0,'Positive original divisor/support')
  comparisons.append(dict(field=target,acquired=str(r[source]),target=cfg[target],direction='acquired<=target'))
 for source,target in PRICES:
  s.need(r[source]>=F(cfg[target])>=0,'Acquired signed simultaneous price '+target)
  comparisons.append(dict(field=target,acquired=str(r[source]),target=cfg[target],direction='acquired>=target'))
 planes=[];s.need(type(cfg['quadratics'])is list and cfg['quadratics']and r['quadratics'],'Nonempty complete phase envelopes')
 for sign in('plus','minus'):
  field='F'+sign;h=F(cfg['H'+sign])
  for i,q in enumerate(r['quadratics']):
   margins=[polymin(F(t['A'])-q['A'],F(t[field])-q[field],q['Qbudget']-F(t['Qbudget']),h)for t in cfg['quadratics']]
   value=max(margins);s.need(value>=0,'Each whole acquired signed plane dominated on its entire raw H interval')
   planes.append(dict(sign=sign,acquired=i,target=margins.index(value),margin=str(value)))
 sign=cfg['sign_premise'];s.need(set(sign)=={'schema','resource_status','conditional_means_zero','negative_endpoint_lower','positive_endpoint_lower'}
  and sign['schema']=='ACTUAL_SIGN_CONDITIONED_MARGINAL_V1'and sign['conditional_means_zero']is True,
  'Physical sign-conditioned marginal, no constrained optimizer substituted')
 endpoints={}
 for key,name in[('A','negative_endpoint_lower'),('B','positive_endpoint_lower')]:
  value=max(raw[key],seed[key]);s.need(0<F(sign[name])<=value,'Strict acquired endpoint floor')
  endpoints[name]=str(value)
 inv={}if invariants is None else dec(invariants)
 beta=[max(raw['beta_lo'],seed['beta_lo'],inv.get('beta_lo',F(-1))),
       min(raw['beta_hi_signed'],seed['beta'],inv.get('beta_hi',F(1)))]
 mean=[mean_floor(*base,raw['theta'],max(seed['mean_lo'],raw.get('mean_lo',seed['mean_lo']),inv.get('mean_lo',F(0)))),
       min(seed['mean_hi'],raw['mean_hi'],inv.get('mean_hi',seed['mean_hi']))]
 s.need(F(cfg['acquired_beta'][0])<=beta[0]<=beta[1]<=F(cfg['acquired_beta'][1])and
  F(cfg['acquired_mean'][0])<=mean[0]<=mean[1]<=F(cfg['acquired_mean'][1]),'Entire same-law signed beta and mean intervals')
 if 'acquired_theta_upper'in cfg:s.need(0<=raw['theta']<=F(cfg['acquired_theta_upper'])<1,'Whole acquired physical theta cap')
 contact=False
 if 'local_contact_allowance'in cfg or 'local_contact_premise'in cfg:
  s.need(cfg['local_contact_allowance']=='5/16'and same(cfg['local_contact_premise'],CONTACT),'Exactly the additional unrestricted attained closed-contact premise')
  contact=True
 return dict(schema='CURRENT_N25_COMPLETE_RESOURCE_COUNT_IMPLICATION_V1',index=index,p=cfg['p'],rho=list(rho),
  comparisons=comparisons,signed_quadratic_planes=planes,endpoint_floors=endpoints,
  acquired_beta=enc(beta),acquired_mean=enc(mean),additional_attained_contact=contact,
  same_law_and_orientation=True,universal_analytic_premise_acquired=False)

def closed_partition(pieces,whole):
 s.need(type(pieces)is list and pieces,'Nonempty literal closed partition')
 end=F(whole[0])
 for pair in pieces:
  s.need(type(pair)is list and len(pair)==2 and end==F(pair[0])<F(pair[1])<=F(whole[1]),'No missing closed seam, overlap ordering or reversed interval')
  end=F(pair[1])
 s.need(end==F(whole[1]),'Entire incoming interval, including last endpoint')
 return len(pieces)+1

def global_union(regions,*,predecessor):
 """Derive20 physical pieces; do not infer them from13 historical records."""
 licenses=scalar_licenses();expected=[]
 for i in range(6):expected.append(dict(id='lower-b'+str(i),rho=list(LOWER[i:i+2]),beta=None))
 for i in range(7):expected.append(dict(id='middle-'+str(i),rho=['33/20','7/4'],beta=list(MIDDLE[i:i+2])))
 for i in range(6):expected.append(dict(id='high-'+str(i),rho=['7/4',TAIL],beta=list(HIGH[i:i+2])))
 s.need(type(regions)is list and len(regions)==19 and [r['id']for r in regions]==[r['id']for r in expected],
        'All19 finite physical pieces in literal order, no missing/duplicate branch')
 for actual,wanted in zip(regions,expected):
  s.need(same({k:actual[k]for k in wanted},wanted)and actual['n']==25 and actual['K']=='0',
         'Every finite piece has the same literal mathematical scope')
  s.need([r['index']for r in actual['outcomes']]==list(range(100)),'All100 ordered closed probability-panel dispositions')
  for row in actual['outcomes']:
   s.need(row['p']==[str(F(row['index'],100)),str(F(row['index']+1,100))]
    and row['method']in('current_full_resource_exclusion','current_full_INITIAL_exclusion','current_full_local_exclusion',
                       'current_full_native_counts','current_full_mixed_E','current_full_mixed_ABCDF'),
          'Every physical panel has an actual admitted exclusion route')
   s.need(type(row['evidence_sha256'])is str and len(row['evidence_sha256'])==64,'Actual current complete evidence, never a status-only route')
   if row['method']=='current_full_native_counts':
    s.need(row['count_interfaces']and all(x['same_law_and_orientation']is True for x in row['count_interfaces']),
           'All native count premises have actual same-law resources')
    closed_partition([x['p']for x in row['count_interfaces']],row['p'])
 s.need(predecessor['n']==24 and predecessor['target']=='CE'and predecessor['conditional_finite_chain_verified']is True,
        'Complete current sharp24 conditional finite theorem licenses lower q25, under its retained universal premises')
 s.need(F(predecessor['derived_q25'])<=F(5,16),'Same-law deletion allowance, sharp24 is sufficient without a cycle')
 return dict(schema='COMPLETE_CURRENT_N25_CONDITIONAL_20_PIECE_UNION_V1',n=25,K='0',target='CE',finite_pieces=expected,
  universal_rho_tail=dict(id='universal-tail',rho_lower_included=TAIL,beta_unrestricted=True,strict_upper=licenses['tail_upper']),
  physical_pieces=20,lower_closed_rho_seams=list(LOWER),middle_closed_beta_seams=list(MIDDLE),high_closed_beta_seams=list(HIGH),
  scalar_licenses=licenses,predecessor=predecessor,same_unrestricted_attained_positive_closed_witness=True,
  both_discrepancy_orientations_via_initial_reflection=True,beta_is_signed_second_moment=True,
  conditional_C25_strictly_below_CE=True,universal_analytic_inputs_acquired=False,full_n25_verified=False,
  all_index_conclusion_verified=False)
