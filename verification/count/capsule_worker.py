"""Fresh, key-free execution of explicitly supported mathematical checkers.

This is a numerical replay component of the full public proof driver. It does
not deserialize private accepted objects, read historical authority keys, or
promote a numerical witness into a global theorem. Further native families
must have their own reviewed source adapters before they can be dispatched.
"""
from dataclasses import dataclass,field
from hashlib import sha256
from pathlib import Path
import argparse,importlib.util,json,os,platform,subprocess,sys,time

HERE=Path(__file__).resolve().parent
FAMILIES={
 'N1-dual':dict(source='n1_dual_certificate.py',
  source_sha256='e3e20e8364942adeb5eab4466a407a348be0e72c8b3bed1f6a5fd1a63ef6d096',
  source_bytes=6309,candidate_max_bytes=256*1024,
  mathematical_scope='Complete rational dual-polynomial certificate for the general-law C1 <= 2/5 reduction',
  expected_status='EXACT_DUAL_POLYNOMIAL_CERTIFICATE_VERIFIED')}

def need(ok,message):
 if not ok:raise ValueError(message)

def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')
def digest(raw):return sha256(raw).hexdigest()

def parsed(raw):
 def unique(pairs):
  out={}
  for key,value in pairs:need(key not in out,'Duplicate checker-output field');out[key]=value
  return out
 return json.loads(raw,object_pairs_hook=unique,parse_constant=lambda _:(_ for _ in()).throw(ValueError('Nonfinite checker output')))

def ordinary(path,*,limit):
 path=Path(path).absolute()
 for part in(path,*path.parents):need(not part.is_symlink()and not part.is_junction(),'Ordinary unlinked whole input/source paths')
 need(path.is_file()and 0<path.stat().st_size<=limit,'Bounded whole existing input/source')
 return path.read_bytes()

def source_bytes(directory,family):
 need(family in FAMILIES,'This mathematical family requires an implemented reviewed native adapter')
 root=Path(directory).absolute();spec=FAMILIES[family]
 need(root.is_dir()and not root.is_symlink()and not root.is_junction(),'Ordinary checker capsule directory')
 need({p.name for p in root.iterdir()}=={spec['source']}and all(p.is_file()for p in root.iterdir()),
  'Closed mathematical source capsule; no shadow helpers or operational files')
 raw=ordinary(root/spec['source'],limit=1024*1024)
 need(len(raw)==spec['source_bytes']and digest(raw)==spec['source_sha256'],'Exact reviewed original mathematical checker body')
 return raw

def runtime_projection():
 # A NEW honest runtime namespace. It deliberately makes no claim to inherit
 # historical runtime425, its old kernel, machine paths, or prior signatures.
 return dict(schema='be.public-numerical-replay-runtime/1',implementation=platform.python_implementation(),
  python_version=platform.python_version(),python_build=list(platform.python_build()),
  system=platform.system(),machine=platform.machine(),bytecode_disabled=sys.dont_write_bytecode,
  optimized=bool(sys.flags.optimize),isolated=bool(sys.flags.isolated),
  historical_runtime_identity_reused=False)

def _child(family,source,candidate):
 need(sys.dont_write_bytecode and not sys.flags.optimize and __debug__,'Unoptimized no-bytecode mathematical checking')
 spec=FAMILIES[family];before=source_bytes(source,family)
 candidate_raw=ordinary(candidate,limit=spec['candidate_max_bytes'])
 namespace='public_math_'+family.replace('-','_')
 loaded=importlib.util.spec_from_file_location(namespace,Path(source)/spec['source'])
 module=importlib.util.module_from_spec(loaded);sys.modules[namespace]=module;loaded.loader.exec_module(module)
 if family=='N1-dual':
  value=module.load_certificate(candidate_raw)
  checked=module.verify(value)
  need(checked['status']==spec['expected_status']and checked['arbitrary_standardized_laws_bound']=='2/5'
   and type(checked['cells'])is int and checked['cells']>0
   and type(checked['bernstein_intervals'])is int and checked['bernstein_intervals']>=checked['cells'],
   'The complete actual original dual checker result, including all cells and tails')
 else:raise ValueError('No mathematical adapter for this family')
 need(source_bytes(source,family)==before and ordinary(candidate,limit=spec['candidate_max_bytes'])==candidate_raw,
  'Every complete source and witness byte unchanged across the actual arithmetic checker')
 result=dict(schema='be.public-fresh-numerical-witness-result/1',family=family,
  source_sha256=digest(before),candidate_sha256=digest(candidate_raw),candidate_bytes=len(candidate_raw),
  mathematical_scope=spec['mathematical_scope'],whole_original_checker_result=checked,
  fresh_arithmetic_checker_executed=True,runtime=runtime_projection(),
  historical_authority_key_or_receipt_used=False,all_index_full_pass=False)
 print(encoded(result).decode('ascii'),flush=True)

_REPLAYED=[]

@dataclass(frozen=True,repr=False)
class FreshNumericalReplay:
 canonical_bytes:bytes=field(repr=False)
 def metadata(self):
  # An observation value, not an accepted all-law/13-role/global proof type.
  need(any(self is value for value in _REPLAYED),'Actual live result of fresh mathematical replay; no JSON or field-replaced reconstruction')
  result=parsed(self.canonical_bytes)
  need(encoded(result)==self.canonical_bytes and result['all_index_full_pass']is False,'Canonical numerical replay observation only')
  return result

def replay(family,source,candidate,*,timeout=120):
 need(sys.dont_write_bytecode and not sys.flags.optimize and __debug__,'Use unoptimized Python -B')
 need(family in FAMILIES and type(timeout)is int and 1<=timeout<=600,'Known reviewed family and finite local wall limit')
 before=source_bytes(source,family);spec=FAMILIES[family]
 witness=ordinary(candidate,limit=spec['candidate_max_bytes'])
 own=ordinary(__file__,limit=1024*1024);started=time.monotonic()
 command=[sys.executable,'-I','-B','-S',str(Path(__file__).resolve()),'_check',family,
  '--source',str(Path(source).resolve()),'--candidate',str(Path(candidate).resolve())]
 completed=subprocess.run(command,stdin=subprocess.DEVNULL,capture_output=True,timeout=timeout,check=False)
 need(completed.returncode==0,'Fresh numerical replay rejected or failed: '+completed.stderr.decode('utf-8','replace')[-4000:])
 need(0<len(completed.stdout)<=256*1024 and len(completed.stderr)<=64*1024,'Bounded complete actual checker output')
 result=parsed(completed.stdout)
 need(result['schema']=='be.public-fresh-numerical-witness-result/1'and result['family']==family
  and result['source_sha256']==digest(before)and result['candidate_sha256']==digest(witness)
  and result['candidate_bytes']==len(witness)and result['fresh_arithmetic_checker_executed']is True
  and result['historical_authority_key_or_receipt_used']is False and result['all_index_full_pass']is False,
  'Whole actual mathematical result bound to this exact source/witness, not a saved success label')
 need(source_bytes(source,family)==before and ordinary(candidate,limit=spec['candidate_max_bytes'])==witness
  and ordinary(__file__,limit=1024*1024)==own,'Entire replay adapter, checker and candidate unchanged')
 result['actual_execution']=dict(returncode=completed.returncode,stdout_sha256=digest(completed.stdout),
  stderr_sha256=digest(completed.stderr),seconds=time.monotonic()-started,
  adapter_sha256=digest(own),new_process=True,cache_or_old_receipt_reused=False)
 answer=FreshNumericalReplay(encoded(result));_REPLAYED.append(answer);answer.metadata();return answer

def main():
 p=argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
 p.add_argument('action',choices=('_check','replay'));p.add_argument('family',choices=tuple(FAMILIES))
 p.add_argument('--source',type=Path,required=True);p.add_argument('--candidate',type=Path,required=True)
 p.add_argument('--output',type=Path);p.add_argument('--timeout',type=int,default=120)
 args=p.parse_args()
 if args.action=='_check':_child(args.family,args.source,args.candidate);return
 need(args.output is not None and not args.output.exists(),'Fresh numerical observation path; never overwrite accepted proof files')
 for part in(args.output,*args.output.parents):need(not part.is_symlink()and not part.is_junction(),'Ordinary new observation output path')
 value=replay(args.family,args.source,args.candidate,timeout=args.timeout)
 args.output.parent.mkdir(parents=True,exist_ok=True)
 with args.output.open('xb')as stream:stream.write(value.canonical_bytes)
 print(encoded(dict(numerical_family=args.family,fresh_numeric_replay=True,output_sha256=digest(value.canonical_bytes),
  historical_authority_used=False,all_index_full_pass=False)).decode('ascii'))

if __name__=='__main__':main()
