"""Exact dynamic original source supplement; data preparation, no math imports."""
from pathlib import Path
import shutil,zipfile
from . import finite2024_remaining_sources as s
PIN='1e6cdd0da482729ce18279ffdad59ae8ba3fe72cae1d36caba236b5de5614db4'
def plan():
 p=s.ROOT/'proof/actual20_semantic_inputs.json';s.need(s.digest(p)==PIN,'Whole sealed original dynamic scalar/source inventory')
 r=s.read(p);s.need(r['original_source_plan_sha256']==s.PLAN_SHA256 and r['current_execution_acquired']is False and r['global_proof_accepted']is False,'Reference sources, never fresh acceptance')
 return r['files']
def prepare(assets,target):
 target=s.ordinary(target);target.mkdir(parents=True,exist_ok=True);opened={}
 try:
  for name,r in plan().items():
   path=target/name
   if not path.exists():
    key=r['archive_key']
    if key not in opened:
     asset=s.plan()['assets'][key];p=Path(assets[key]);s.need(s.digest(p)==asset['sha256'],'Whole original dynamic source transport');opened[key]=zipfile.ZipFile(p)
    raw=opened[key].read(r['member']);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
   s.need(path.stat().st_size==r['bytes']and s.digest(path)==r['sha256'],'Every whole dynamic scalar/proof source')
 finally:
  for z in opened.values():z.close()
 verify(target);return target

def verify(target):
 expected={n:r['sha256']for n,r in plan().items()};actual={p.relative_to(target).as_posix():s.digest(p)for p in Path(target).rglob('*')if s.ordinary(p).is_file()}
 s.need(actual==expected,'Exact whole dynamic supplement, no unbound helper/bytecode');return expected
