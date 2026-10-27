"""Recreate a recorded private runtime namespace from the verified active code.

Native captures retain their actual old absolute cwd/entry paths. Restoring
that namespace changes no historical receipt/hash. Only the dedicated managed
runtime tree may be created; unrelated existing directories are never replaced.
"""
from pathlib import Path
import json,shutil,uuid
from . import delivery_transport as tx
MAX_BYTES=2*1024**3

def _read(p):
 def unique(items):
  d={}
  for k,v in items:tx.need(k not in d,'No duplicate runtime manifest key');d[k]=v
  return d
 return json.loads(Path(p).read_bytes(),object_pairs_hook=unique)
def manifest(root):
 root=tx.ordinary(root);p=root/'RUNTIME_MANIFEST.json';tx.need(p.is_file()and p.stat().st_size<=16*1024**2,'Actual installed local-runtime manifest')
 r=_read(p);tx.need(r['schema']=='BE_LOCAL_RUNTIME_SHA256_V1'and type(r['files'])is dict and 0<len(r['files'])<=100000,'Complete bounded active runtime source inventory')
 total=0;folded=set()
 for n,row in r['files'].items():
  tx.parts(n);tx.need(n.casefold()not in folded and type(row['bytes'])is int and 0<=row['bytes']<=256*1024**2,'Unique ordinary bounded runtime source')
  folded.add(n.casefold());total+=row['bytes'];q=tx.ordinary(root/n)
  tx.need(q.is_file()and q.stat().st_size==row['bytes']and tx.digest(q)==row['sha256'],'Every active runtime byte still equals its bootstrap manifest')
 tx.need(total<=MAX_BYTES,'Whole bounded runtime expansion');return r

def ensure_recorded_runtime(context,*,active_root,managed_root='/content/berry-esseen-runtime'):
 active=tx.ordinary(active_root);origin=tx.ordinary(context['runtime_root'])
 pins={'be_replay/finite2024_actual20_full.py':context['full_bridge_sha256'],
       'be_replay/finite2024_actual20_math.py':context['math_worker_sha256']}
 for n,pin in pins.items():tx.need(tx.digest(active/n)==pin,'Current full producer code exactly matches the cached native prefix profile')
 if origin==active:return dict(runtime_root=str(origin),recreated=False,active_runtime=True,mathematical_acceptance=False)
 base=tx.ordinary(managed_root)
 tx.need(origin.is_relative_to(base)and len(origin.relative_to(base).parts)==2,'Only the recorded two-level private local-runtime namespace may be restored')
 current=manifest(active);preserved=None
 if origin.exists():
  tx.need((origin/'RUNTIME_MANIFEST.json').is_file()and all((origin/n).is_file()and tx.digest(origin/n)==pin for n,pin in pins.items()),
   'Never replace an unrelated directory occupying a recorded runtime namespace')
  try:
   previous=manifest(origin)
   if previous==current:return dict(runtime_root=str(origin),recreated=False,active_runtime=False,mathematical_acceptance=False)
  except (ValueError,OSError):pass
  preserved=origin.with_name(origin.name+'-preserved-'+uuid.uuid4().hex[:12]);origin.rename(preserved)
 origin.parent.mkdir(parents=True,exist_ok=True);pending=origin.with_name(origin.name+'-pending-'+uuid.uuid4().hex[:12]);pending.mkdir()
 for n in current['files']:
  target=pending/n;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(active/n,target)
 shutil.copyfile(active/'RUNTIME_MANIFEST.json',pending/'RUNTIME_MANIFEST.json');tx.need(manifest(pending)==current,'Entire recreated runtime independently revalidated')
 pending.rename(origin);tx.need(manifest(origin)==current,'Exact original absolute module-origin namespace restored')
 return dict(runtime_root=str(origin),recreated=True,preserved=str(preserved)if preserved else None,files=len(current['files']),mathematical_acceptance=False)
