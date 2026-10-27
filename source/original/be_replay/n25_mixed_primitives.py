"""Full fresh primitives for all92 saved D claims (Linux child execution only).

The historical D acquirer checks saved scalar chains, not their arithmetic.
This separate action recomputes feedback, the literal native scalar prefix,
normalized moment cap and, where selected, the full pointwise cap. Original
mathematical modules are loaded only inside the explicitly launched worker.
Importing this module or validating its output evaluates no such module.
"""
from __future__ import annotations
import hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
from copy import deepcopy
from . import n25_full_join_sources as s,n25_count_evidence as e

same=e.same

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec)
 sys.modules[name]=module;spec.loader.exec_module(module);return module

def equivalent(actual,reference,*,root=False):
 """Full mathematical equality; only explicitly named transport slots differ."""
 if type(actual)is not type(reference):return False
 if type(reference)is dict:
  if actual.keys()!=reference.keys():return False
  for k,want in reference.items():
   if root and k in('source_sha256','imported_workspace_modules'):
    if type(actual[k])is not dict:return False
   elif not equivalent(actual[k],want):return False
  return True
 if type(reference)is list:return len(actual)==len(reference)and all(equivalent(a,b)for a,b in zip(actual,reference))
 return actual==reference

def check_sources(request):
 workspace=Path(request['workspace']).resolve();s.need(sys.platform=='linux'and not sys.flags.optimize and sys.flags.dont_write_bytecode,
  'Fresh ordinary Linux Python -B primitive worker')
 s.need(type(request['sources'])is dict and request['sources'],'Complete current primitive source inventory')
 for name,pin in request['sources'].items():
  p=Path(name);s.need(p.is_absolute()and p.is_relative_to(workspace)and s.digest(p)==pin,'Exact current original primitive input')
 return workspace

def module_origins(request,allowed,*,extra=()):
 root=Path(request['workspace']).resolve();allowed={Path(p).resolve()for p in allowed};extra={Path(p).resolve()for p in extra};out={}
 for name,module in tuple(sys.modules.items()):
  filename=getattr(module,'__file__',None)
  if filename:
   p=Path(filename).resolve()
   if p.is_relative_to(root):
    s.need((p.parent in allowed or p in extra)and str(p)in request['sources']
     and s.digest(p)==request['sources'][str(p)],'Every actual original module comes from its exact selected native/helper source')
    out[name]=dict(path=str(p),sha256=s.digest(p))
 return out

def claim(request,entry,out):
 """One isolated exact primitive chain, with no historical source-gate fiction."""
 root=check_sources(request);T=root/'work/cutoff25_20261013';index=entry['statement']['panel']
 D=root/f'work/cutoff25_20261011/new_root/global_local_contact_b5_p{index}_v14'
 H=T/'archive_audit/normalized_defect_frontier_v1';G=H.parent/'support_coupled_frontier_v1'
 P=H.parent/'joint_contact_preflight_v1';W=H.parent/'affine_contact_cell_v1';N=H.parent/'normalized_defect_rho_v1'
 sys.path.insert(0,str(H));protocol=load('protocol',H/'protocol.py')
 sys.path.insert(0,str(D));native=load('count_protocol',D/'count_protocol.py')
 cfg,bound=native.load();s.need(same(cfg,entry['statement']['original_cfg']),'Same entire current original V14 conditional cfg')
 old=s.read(entry['reference_result']);target=old['target'];s.need(target['id']==entry['statement']['source_target_id']
  and target['k']==entry['statement']['k']and same(target['box'],entry['statement']['box']),
  'Exact original same-count closed saved rectangle, not a different discovery box')
 for p in(G,P,W):sys.path.insert(0,str(p))
 chain=load('feedback',G/'feedback.py');args=protocol.arguments(target['box'],target['k'])
 ratio=T/'low/tighter_ratio_rho_v1/ratio.py'
 before_origins=module_origins(request,(D,H,G,P,W),extra=(ratio,))
 fresh=chain.feedback(cfg,**args);candidate=protocol.validate_chain(fresh,cfg,args)
 chain_origins=module_origins(request,(D,H,G,P,W),extra=(ratio,))
 s.need(equivalent(fresh,old['chain']),'Entire original coupled moment/Gaussian/contact chain freshly reproduced')
 prefix=None;point=None;status='CHAIN_EMPTY'
 if fresh['status']=='COUPLED_CONTINUE':
  # As in original prefix_worker.py, this scalar projection is run in a fresh
  # process and never inherits feedback's module namespace.
  input_path=Path(out).with_suffix('.prefix-input.json')
  packet=dict(request=request,entry=entry,chain=fresh,candidate=candidate)
  input_path.write_text(json.dumps(packet)+'\n',encoding='utf-8')
  cmd=[sys.executable,'-B','-S','-m','be_replay.n25_mixed_primitives','--prefix',str(input_path)]
  run=subprocess.run(cmd,cwd=s.ROOT,capture_output=True)
  Path(out).with_suffix('.prefix.stdout.txt').write_bytes(run.stdout);Path(out).with_suffix('.prefix.stderr.txt').write_bytes(run.stderr)
  s.need(type(run.returncode)is int and run.returncode==0 and run.stderr==b'','Actual isolated full original scalar prefix stopped successfully')
  prefix=json.loads(run.stdout,object_pairs_hook=s.base.unique)
  s.need(equivalent(prefix,old['prefix_result'],root=True),'Entire fresh prefix/Gaussian/normalized result equals the selected saved proof')
  status=prefix['status']
  if entry['statement']['selected_method']=='POINTWISE_EMPTY':
   # The original pointwise interface derives every argument from this fresh
   # chain/prefix, rather than treating a stored rho or total as an acquisition.
   packet=dict(request=request,entry=entry,row=dict(old,chain=fresh,prefix_result=prefix))
   p=Path(out).with_suffix('.pointwise-input.json');p.write_text(json.dumps(packet)+'\n',encoding='utf-8')
   command=[sys.executable,'-B','-S','-m','be_replay.n25_mixed_primitives','--pointwise',str(p)]
   child=subprocess.run(command,cwd=s.ROOT,capture_output=True)
   Path(out).with_suffix('.pointwise.stdout.txt').write_bytes(child.stdout);Path(out).with_suffix('.pointwise.stderr.txt').write_bytes(child.stderr)
   s.need(type(child.returncode)is int and child.returncode==0 and child.stderr==b'','Actual isolated original pointwise primitive completed')
   result=json.loads(child.stdout,object_pairs_hook=s.base.unique);status=result['status'];point=result['result']
   old_point=s.read(entry['reference_pointwise']);matches=[r for r in old_point['rows']if r['index']==index and r['target']['id']==target['id']]
   s.need(len(matches)==1 and same(point,matches[0]['result']),'Entire selected strict pointwise result freshly recomputed')
 s.need(status==entry['statement']['selected_method'],'The exact selected D exclusion, never an unresolved prefix')
 check_sources(request)
 result=dict(schema='FULL_FRESH_SAME_CFG_D_SCALAR_CLAIM_V1',claim_id=entry['statement']['claim_id'],panel=index,
  k=target['k'],box=target['box'],original_cfg=cfg,selected_method=status,chain=fresh,prefix=prefix,pointwise=point,
  native_count_calls=0,full_feedback_recomputed=True,full_prefix_recomputed=prefix is not None,
  full_pointwise_recomputed=point is not None,sources_sha256=request['sources'],
  chain_imports_before=before_origins,chain_imports_after=chain_origins)
 Path(out).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');return result

def pointwise_worker(packet):
 request=packet['request'];root=check_sources(request);T=root/'work/cutoff25_20261013'
 H=T/'archive_audit/pointwise_finished_prefix_v1';P=T/'low/pointwise_inward_defect_v2'
 sys.path.insert(0,str(H));inter=load('_n25_D_pointwise_interface',H/'interface.py')
 kw,O0,V0u,V1u=inter.arguments(packet['row']);sys.path.insert(0,str(P))
 pointwise=load('pointwise_inward_v2',P/'pointwise_inward_v2.py')
 pointwise.validate(kw,O0,V0u,V1u);value=pointwise.upper(kw,O0,V0u,V1u)
 status=inter.validate_result(value,kw);origins=module_origins(request,(H,P));check_sources(request)
 return dict(status=status,result=inter.enc(value),imported_original_modules=origins)

def prefix_worker(packet):
 request,entry=packet['request'],packet['entry'];root=check_sources(request);T=root/'work/cutoff25_20261013'
 index=entry['statement']['panel'];D=root/f'work/cutoff25_20261011/new_root/global_local_contact_b5_p{index}_v14'
 H=T/'archive_audit/normalized_defect_frontier_v1';N=H.parent/'normalized_defect_rho_v1'
 for p in(D,H):sys.path.insert(0,str(p))
 protocol=load('protocol',H/'protocol.py');c=load('exact35_core',D/'exact35_core.py')
 original=s.read(D/'contract.json')['rows'][0];s.need(same(original,entry['statement']['original_cfg']),'Entire unchanged original physical cfg')
 old=s.read(entry['reference_result']);target=old['target'];args=protocol.arguments(target['box'],target['k'])
 cfg=protocol.validate_chain(packet['chain'],original,args);s.need(same(cfg,packet['candidate']),'Fresh preceding same-law contact contraction')
 known=protocol.verify_port(D);project=load('prefix_project',H/'prefix_project.py').project
 sys.path.insert(0,str(N));normalized=load('normalized',N/'normalized.py')
 z=project(cfg,**args)
 def encode(x):
  if isinstance(x,c.I):return[str(x.l),str(x.h)]
  if type(x)is protocol.F:return str(x)
  if type(x)is dict:return{k:encode(v)for k,v in x.items()}
  if type(x)in(list,tuple):return[encode(v)for v in x]
  return x
 z=encode(z);empty=protocol.validate_prefix(z,known)
 row=dict(index=index,target=target,original_cfg=original,input_cfg=cfg,prefix=z,
  actual_scalar_prefix_calls=1,actual_native24_calls=0,actual_native25_calls=0)
 if empty:row.update(status='PREFIX_EMPTY',reason=z['status'])
 else:
  kw=protocol.normalized_arguments(z,cfg,target['box'],target['k']);value=normalized.upper(**kw)
  s.need(value['status']in protocol.NORMAL_EMPTY|{'VALID_NORMALIZED_DEFECT_RHO_UPPER'},'Original normalized cap status')
  row.update(status='NORMALIZED_EMPTY'if value['status']in protocol.NORMAL_EMPTY else'NORMALIZED_CONTINUE',
   reason=value['status'],normalized_arguments=protocol.enc(kw),normalized_result=protocol.enc(value))
 origins={}
 for name,module in tuple(sys.modules.items()):
  filename=getattr(module,'__file__',None)
  if filename:
   p=Path(filename).resolve()
   if p.is_relative_to(root):
    s.need(str(p)in request['sources']and s.digest(p)==request['sources'][str(p)],'Every actually imported original primitive helper is sealed')
    origins[name]=dict(path=str(p),sha256=s.digest(p))
 row['source_sha256']=request['sources'];row['imported_workspace_modules']=origins;check_sources(request);return row

def run(request_file,out):
 request=s.read(request_file);check_sources(request);entries=request['claims']
 s.need(len(entries)==92 and len({r['statement']['claim_id']for r in entries})==92,'Every92 independently selected D statement')
 out=Path(out);folder=out.with_suffix('');folder.mkdir(exist_ok=False);rows=[]
 for i,entry in enumerate(entries):
  one=folder/(str(i).zfill(3)+'-input.json');result=folder/(str(i).zfill(3)+'-result.json')
  one.write_text(json.dumps(dict(request=request,entry=entry))+'\n',encoding='utf-8')
  command=[sys.executable,'-B','-S','-m','be_replay.n25_mixed_primitives','--claim',str(one),str(result)]
  child=subprocess.run(command,cwd=s.ROOT,capture_output=True)
  stdout=folder/(str(i).zfill(3)+'.stdout.txt');stderr=folder/(str(i).zfill(3)+'.stderr.txt')
  stdout.write_bytes(child.stdout);stderr.write_bytes(child.stderr)
  s.need(type(child.returncode)is int and child.returncode==0 and child.stderr==b'','Each original selected primitive chain actually stopped successfully')
  checked=s.read(result);rows.append(dict(claim_id=entry['statement']['claim_id'],result=str(result),sha256=s.digest(result),
   command=command,returncode=child.returncode,input_sha256=s.digest(one),stdout_sha256=s.digest(stdout),stderr_sha256=s.digest(stderr)))
  print('D_FULL_PRIMITIVE',i+1,92,entry['statement']['claim_id'],flush=True)
 packet=dict(schema='FULL92_FRESH_ORIGINAL_D_PRIMITIVES_V1',claims=rows,claim_count=92,
  request_sha256=s.digest(request_file),source_sha256=request['sources'],native_count_calls=0,
  all_feedback_prefix_normalized_and_selected_pointwise_recomputed=True,full66_complete=False)
 out.write_text(json.dumps(packet,indent=2)+'\n',encoding='utf-8');print('FULL92_D_PRIMITIVES_COMPLETE',s.digest(out),flush=True)
 return packet

if __name__=='__main__':
 if sys.argv[1]=='--prefix':print(json.dumps(prefix_worker(s.read(sys.argv[2]))),flush=True)
 elif sys.argv[1]=='--pointwise':print(json.dumps(pointwise_worker(s.read(sys.argv[2]))),flush=True)
 elif sys.argv[1]=='--claim':
  p=s.read(sys.argv[2]);claim(p['request'],p['entry'],sys.argv[3]);print('D_CLAIM_COMPLETE',flush=True)
 else:run(sys.argv[1],sys.argv[2])
