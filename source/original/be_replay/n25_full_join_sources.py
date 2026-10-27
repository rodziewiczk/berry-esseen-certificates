"""Exact original source/reference closure for the complete n25 delivery.

Preparing these bytes establishes no numerical or mathematical acceptance.
The old absolute capture graphs remain provenance; fresh executions are admitted
only by their dedicated stopped-output readers.
"""
from __future__ import annotations
import ast,hashlib,json,shutil,types,zipfile
from pathlib import Path
from . import count_task as base,delivery_transport as tx

ROOT=Path(__file__).resolve().parents[1]
PLAN=ROOT/'proof/n25_full_join_source_plan.json'
PLAN_SHA256='8ec99ede44824345c48dbc0ebb6db5aed65ecd290cce379a2c4b74449829477e'
MIB=1024**2
need=tx.need
digest=tx.digest
_PARSED=None

def read(path,limit=128*MIB):return base.read(tx.ordinary(path),limit)
def plan():
 global _PARSED
 need(digest(PLAN)==PLAN_SHA256,'Exact complete66 source/reference plan')
 if _PARSED is None:_PARSED=read(PLAN,32*MIB)
 p=_PARSED
 need(p['schema']=='N25_FULL66_ORIGINAL_SOURCE_CLOSURE_V1'and p['original_mathematical_code_executed']is False
      and p['historical_acceptance_is_current']is False and not p['provenance_conflicts'],'Honest source-only complete66 closure')
 return p

def path(root,name):return tx.ordinary(Path(root).joinpath(*tx.parts(name)))
def source(cache,name):
 row=plan()['files'].get(name);p=path(cache,name)
 need(row is not None and p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],
      'Whole independently pinned original source/reference: '+name)
 return p

def obtain(archives,*,progress=None):
 result={k:base.obtain_asset(archives,k,download=True,progress=progress)for k in('old','base13')}
 result['recovery']=ROOT/'assets/BE_cutoff25_missing_files_20261024.zip'
 for key,p in result.items():
  spec=plan()['archives'][key]
  need(p.is_file()and p.stat().st_size==spec['bytes']and digest(p)==spec['sha256'],'Exact original complete66 archive '+key)
 return result

def prepare_cache(archives,cache,*,progress=lambda *a,**k:None):
 cache=tx.ordinary(cache);cache.mkdir(parents=True,exist_ok=True);p=plan();opened={}
 try:
  for key,filename in archives.items():
   spec=p['archives'][key];need(Path(filename).stat().st_size==spec['bytes']and digest(filename)==spec['sha256'],'Exact archive before extraction')
   opened[key]=zipfile.ZipFile(filename)
  for i,(name,row)in enumerate(p['files'].items()):
   out=path(cache,name)
   if not(out.is_file()and out.stat().st_size==row['bytes']and digest(out)==row['sha256']):
    out.parent.mkdir(parents=True,exist_ok=True);temp=out.with_name(out.name+'.pending')
    with opened[row['archive']].open(name)as s,temp.open('wb')as d:shutil.copyfileobj(s,d,MIB)
    need(temp.stat().st_size==row['bytes']and digest(temp)==row['sha256'],'Exact selected archive member after extraction')
    temp.replace(out)
   if i%1000==0:progress('n25_full_source_cache',completed=i,total=len(p['files']),arithmetic_computed=False)
  return cache
 finally:
  for z in opened.values():z.close()

def functions(cache,name,names,*,context=None):
 """Project only named original pure functions, never an executable entry point.

The caller supplies explicit stdlib context. No original imports/top-level
assignments, arbitrary setup or mathematical kernel can execute here.
 """
 p=source(cache,name);tree=ast.parse(p.read_text('utf-8'));selected=[];wanted=set(names)
 for node in tree.body:
  if isinstance(node,ast.FunctionDef)and node.name in wanted:selected.append(node)
 need({n.name for n in selected}==wanted,'Every named original independent pure predicate exists')
 module=types.ModuleType('_n25_full_pure_'+hashlib.sha256(name.encode()).hexdigest()[:12]);module.__file__=str(p)
 if context:module.__dict__.update(context)
 exec(compile(ast.Module(body=selected,type_ignores=[]),str(p),'exec'),module.__dict__)
 return module

def implementation():
 files=sorted({p.name for pattern in('n25_full_join*.py','n25_mixed*.py','n25_b3_p34*.py')for p in Path(__file__).parent.glob(pattern)})
 return {n:digest(Path(__file__).parent/n)for n in files}|dict(source_plan=PLAN_SHA256)
