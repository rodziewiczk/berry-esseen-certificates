"""Download pinned public certificate assets and extract within the data directory."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,shutil,stat,urllib.request,zipfile
root=Path(__file__).resolve().parent.parent
p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--counts',action='store_true');g.add_argument('--all',action='store_true');a=p.parse_args()
m=json.loads((root/'certificates/RELEASE.json').read_bytes());cache=root/'.be/downloads';cache.mkdir(parents=True,exist_ok=True)
for item in m['assets']:
 if a.counts and item['name']!='count-candidates.zip':continue
 target=cache/item['name']
 def valid():
  if not target.is_file()or target.stat().st_size!=item['bytes']:return False
  with target.open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()==item['sha256']
 if not valid():
  if target.exists():raise RuntimeError('Existing asset has wrong size/SHA; preserve it and choose a fresh download directory')
  url='https://github.com/'+m['repository']+'/releases/download/'+m['tag']+'/'+item['name'];print('Downloading',item['name'],flush=True);urllib.request.urlretrieve(url,target)
  if not valid():raise RuntimeError('Complete public asset SHA/size mismatch')
 destination=root/item['extract_to'];destination.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(target)as z:
  for member in z.infolist():
   relative=PurePosixPath(member.filename)
   if relative.is_absolute()or '..'in relative.parts or chr(92)in member.filename or stat.S_ISLNK(member.external_attr>>16):raise RuntimeError('Unsafe archive member')
   output=destination.joinpath(*relative.parts)
   if not output.resolve().is_relative_to(destination.resolve()):raise RuntimeError('Archive path escapes data directory')
   if member.is_dir():output.mkdir(parents=True,exist_ok=True);continue
   output.parent.mkdir(parents=True,exist_ok=True)
   if output.exists():
    with z.open(member)as f:expected=hashlib.file_digest(f,'sha256').hexdigest()
    with output.open('rb')as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
    if actual!=expected:raise RuntimeError('Existing data differs; never overwrite unknown files')
   else:
    with z.open(member)as f,output.open('xb')as out:shutil.copyfileobj(f,out)
 print('Verified and extracted',item['name'],flush=True)
