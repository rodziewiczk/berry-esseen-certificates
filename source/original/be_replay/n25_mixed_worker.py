"""One literal original mixed child inside the separately guarded capsule.

The outer supervisor owns process-group limits and whole streams. This small
stdlib-only relay records the REAL child cwd/argv/return code. It is needed
because the original p24/p25 writers publish beside their native cwd. Neither
their programs nor their mathematics are changed to suit checkpoint transport.
"""
from __future__ import annotations
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys,time
from pathlib import Path

def need(ok,text):
 if not ok:raise ValueError(text)
def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb')as stream:
  for block in iter(lambda:stream.read(1024**2),b''):h.update(block)
 return h.hexdigest()
def unique(rows):
 result={}
 for key,value in rows:need(key not in result,'No duplicate original-child request key');result[key]=value
 return result
def run(request_path):
 need(sys.platform=='linux'and sys.flags.dont_write_bytecode and not sys.flags.optimize,
  'Real Linux exact -B supervisor child')
 path=Path(request_path).resolve();r=json.loads(path.read_bytes(),object_pairs_hook=unique)
 need(r['schema']=='LITERAL_ORIGINAL_FULL66_MIXED_CHILD_REQUEST_V1','Exact current original-child request')
 root=Path(r['capsule']).resolve();cwd=Path(r['cwd']).resolve();out=Path(r['inner_capture']).resolve()
 need(Path.cwd().resolve()==root and path.is_relative_to(root)and cwd.is_relative_to(root)
  and out.is_relative_to(root)and not out.exists(),'One contained source/output capsule and exclusive real capture')
 need(type(r['command'])is list and r['command']and r['command'][0]==sys.executable
  and all(type(x)is str and x and '\x00'not in x for x in r['command']),
  'Exact actual interpreter and literal original argv')
 for name,pin in r['input_sha256'].items():
  source=root.joinpath(*name.split('/'));need(source.is_relative_to(root)and source.is_file()and sha(source)==pin,
   'All whole immutable original input bytes before real launch')
 started=datetime.now(timezone.utc).isoformat();begin=time.monotonic()
 # Keep the supervisor's actual file descriptors: every byte in its whole
 # stdout/stderr is produced by this genuine original subprocess.
 child=subprocess.Popen(r['command'],cwd=cwd,stdin=subprocess.DEVNULL,stdout=sys.stdout,stderr=sys.stderr)
 code=child.wait();sys.stdout.flush();sys.stderr.flush()
 for name,pin in r['input_sha256'].items():need(sha(root.joinpath(*name.split('/')))==pin,'No original input changed during the actual child')
 record=dict(schema='GENUINE_FULL66_ORIGINAL_INNER_CHILD_CAPTURE_V1',command=r['command'],cwd=str(cwd),
  returncode=code,python=sys.version,python_executable=sys.executable,started_utc=started,
  finished_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-begin,
  request_sha256=sha(path),input_sha256=r['input_sha256'],
  stdout_sha256=sha(r['stdout_file']),stderr_sha256=sha(r['stderr_file']),
  historical_execution_relabelled=False,proof_accepted=False)
 out.parent.mkdir(parents=True,exist_ok=True)
 with out.open('x',encoding='utf-8')as stream:json.dump(record,stream,indent=2);stream.write('\n')
 return code

if __name__=='__main__':
 need(len(sys.argv)==2,'One whole original-child request');raise SystemExit(run(sys.argv[1]))
