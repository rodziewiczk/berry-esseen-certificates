"""Standalone stdlib bootstrap embedded verbatim in delivered notebooks.

The whole runtime ZIP is pinned before any extraction or local import. The
manifest also checks every member, exact inventory, paths, types and sizes.
"""
from pathlib import Path
import hashlib,json,os,shutil,stat,sys,tempfile,uuid,zipfile

def _require(ok,message):
 if not ok:raise ValueError(message)

def _sha_file(path):
 h=hashlib.sha256()
 with Path(path).open('rb')as f:
  for block in iter(lambda:f.read(1024**2),b''):h.update(block)
 return h.hexdigest()

def _json_unique(pairs):
 result={}
 for k,v in pairs:_require(k not in result,'Duplicate manifest JSON key');result[k]=v
 return result

def install_runtime(archive,expected_sha256,destination):
 archive=Path(archive);destination=Path(destination)
 for p in(archive,destination,*archive.parents,*destination.parents):_require(not p.is_symlink(),'No linked runtime ancestry')
 _require(archive.is_file()and archive.stat().st_size<=1024**3 and _sha_file(archive)==expected_sha256,'Exact delivered runtime ZIP SHA256 required')
 with zipfile.ZipFile(archive)as z:
  entries=z.infolist();_require(0<len(entries)<=20000,'Bounded runtime file census');names=set();folded=set();total=0
  for entry in entries:
   name=entry.filename;parts=name.split('/');mode=stat.S_IFMT(entry.external_attr>>16)
   _require(name and not any(c in name for c in ('\\',':','\0'))and all(p and p not in('.','..')and p==p.rstrip(' .')for p in parts)
    and name not in names and name.casefold()not in folded and not entry.is_dir()and not entry.flag_bits&1
    and mode in(0,stat.S_IFREG)and 0<=entry.file_size<=256*1024**2,'Ordinary unique contained runtime member')
   names.add(name);folded.add(name.casefold());total+=entry.file_size
  _require(total<=2*1024**3 and 'RUNTIME_MANIFEST.json'in names,'Bounded complete runtime and manifest')
  manifest=json.loads(z.read('RUNTIME_MANIFEST.json'),object_pairs_hook=_json_unique)
  _require(manifest['schema']=='BE_LOCAL_RUNTIME_SHA256_V1'and set(manifest['files'])==names-{'RUNTIME_MANIFEST.json'},'Exact runtime manifest inventory')
  for name,row in manifest['files'].items():
   entry=z.getinfo(name);_require(type(row['bytes'])is int and entry.file_size==row['bytes'],'Every original runtime byte length')
   h=hashlib.sha256()
   with z.open(entry)as source:
    for block in iter(lambda:source.read(1024**2),b''):h.update(block)
   _require(h.hexdigest()==row['sha256'],'Every original runtime SHA256: '+name)
  if destination.exists():
   tree=list(destination.rglob('*'))
   for p in tree:_require(not p.is_symlink()and (p.is_file()or p.is_dir()),'Existing runtime has only ordinary files/directories')
   expected_dirs={str(Path(name).parent).replace('\\','/')for name in names}
   expected_dirs|={'/'.join(name.split('/')[:i])for name in names for i in range(1,len(name.split('/')))}
   expected_dirs.discard('.')
   _require({p.relative_to(destination).as_posix()for p in tree if p.is_dir()}==expected_dirs,'Existing runtime has an exact directory inventory')
   actual={p.relative_to(destination).as_posix()for p in destination.rglob('*')if p.is_file()}
   _require(actual==names,'Existing runtime has an exact inventory; use a fresh hash-specific path')
   for name,row in manifest['files'].items():_require(_sha_file(destination/name)==row['sha256'],'Existing runtime source changed')
   _require((destination/'RUNTIME_MANIFEST.json').read_bytes()==z.read('RUNTIME_MANIFEST.json'),'Existing exact manifest')
  else:
   destination.parent.mkdir(parents=True,exist_ok=True);temporary=destination.with_name(destination.name+'.pending-'+uuid.uuid4().hex[:8]);temporary.mkdir()
   try:
    for entry in entries:
     target=temporary.joinpath(*entry.filename.split('/'));target.parent.mkdir(parents=True,exist_ok=True)
     with z.open(entry)as source,target.open('xb')as output:shutil.copyfileobj(source,output,1024**2)
    temporary.replace(destination)
   except BaseException:
    shutil.rmtree(temporary,ignore_errors=True);raise
 # A notebook kernel can otherwise retain modules loaded by a previous pin.
 for name in tuple(sys.modules):
  if name=='be_replay'or name.startswith('be_replay.'):del sys.modules[name]
 sys.dont_write_bytecode=True;sys.path.insert(0,str(destination.resolve()))
 return destination.resolve()

def synchronize_and_release(*,drive=None,runtime=None,sync=None,managed=None):
 """A synchronization exception prevents the release call, including errors."""
 if managed is None:managed=bool(os.environ.get('TBE_RUNTIME_ADDR'))
 if not managed:
  print('Outside Colab; saved artifacts remain available.');return False
 if drive is None or runtime is None:
  from google.colab import drive,runtime
 sys.stdout.flush();sys.stderr.flush();(sync or os.sync)()
 drive.flush_and_unmount(timeout_ms=300_000)
 runtime.unassign()
 return True

def save_notebook_exit(local_directory,durable_directory,task,*,error=None,result=None):
 """Always create an inspectable final ZIP; Drive copy failure is propagated."""
 local=Path(local_directory);local.mkdir(parents=True,exist_ok=True);durable=Path(durable_directory)
 state='INCOMPLETE'if error else'FINISHED'
 if not error and isinstance(result,dict)and isinstance(result.get('status'),dict):state=result['status'].get('state',state)
 packet=dict(schema='BE_NOTEBOOK_FINALIZATION_V1',task=task,state=state,
  error=error,result=result,all_index_conclusion_verified=False)
 (local/'NOTEBOOK_RESULT.json').write_text(json.dumps(packet,indent=2,default=str)+'\n',encoding='utf-8')
 output=local.parent/(local.name+'-notebook-results.zip');pending=output.with_suffix('.pending')
 with zipfile.ZipFile(pending,'w',zipfile.ZIP_DEFLATED)as z:
  for p in sorted(local.rglob('*')):
   _require(not p.is_symlink(),'Ordinary notebook log artifact')
   if p.is_file():z.write(p,local.name+'/'+p.relative_to(local).as_posix())
 pending.replace(output);pin=_sha_file(output);output.with_suffix('.zip.sha256').write_text(pin+'  '+output.name+'\n',encoding='ascii')
 # These writes deliberately propagate: shutdown is blocked unless durable
 # bytes and their sidecar have actually been saved and compared.
 durable.mkdir(parents=True,exist_ok=True);target=durable/output.name;tmp=target.with_name(target.name+'.pending')
 shutil.copyfile(output,tmp);_require(_sha_file(tmp)==pin,'Whole final ZIP copied to Drive');tmp.replace(target)
 target.with_suffix('.zip.sha256').write_text(pin+'  '+target.name+'\n',encoding='ascii')
 print('Final notebook ZIP:',target,flush=True);return str(target)
