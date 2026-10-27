"""Data-only current-reference epochs for the remaining original protocols.

This module neither executes a producer nor accepts a mathematical parent.
Every changed identity must be supplied by a full stopped-execution reader in
the caller. Only paths and registered SHA identities change; all mathematical
values, controls, function bodies and candidate leaf results are preserved.
"""
from __future__ import annotations
import ast,hashlib,io,json,re,tokenize
from copy import deepcopy
from pathlib import PurePosixPath

HEX=re.compile(r'[0-9a-f]{64}\Z')
GRAPH_KEYS=frozenset(('source_sha256','files_sha256','input_sha256','sources_sha256','kernel_sha256','copies_sha256'))

def need(ok,message):
 if not ok:raise ValueError(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(value):return sha(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode())
def dump(value):return(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
def unique(items):
 result={}
 for k,v in items:need(k not in result,'Duplicate reference JSON key');result[k]=v
 return result
def read(raw):
 def invalid(_):raise ValueError('Nonfinite reference JSON')
 return json.loads(raw,object_pairs_hook=unique,parse_constant=invalid)
def same(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b

class References:
 """Explicit identities; this registry never certifies their acquisition."""
 def __init__(self,*,old_root,new_root,context_literals=None):
  for p in(old_root,new_root):need(type(p)is str and p.startswith('/')and str(PurePosixPath(p))==p and'..'not in PurePosixPath(p).parts,'Canonical original/current workspace root')
  need(old_root!=new_root,'Distinct honest workspace epoch')
  self.old_root,self.new_root=old_root,new_root;self.context=dict(context_literals or{});self.hashes={};self.roles={}
  need(all(type(k)is str and type(v)is str and k!=v for k,v in self.context.items()),'Literal actual capture contexts')
 def add(self,old,new,*,role,evidence_sha256=None):
  need(type(old)is str and HEX.fullmatch(old)and type(new)is str and HEX.fullmatch(new),'Exact registered SHA256 identities')
  need(role in('derived_source_metadata','derived_graph_metadata','derived_canonical_identity','validated_current_result','genuine_current_capture'),'Explicit identity role')
  if role in('validated_current_result','genuine_current_capture'):need(type(evidence_sha256)is str and HEX.fullmatch(evidence_sha256),'A genuine parent/capture needs separately revalidated execution evidence')
  need(old not in self.hashes or self.hashes[old]==new,'Ambiguous identity requires a path-specific reviewed epoch')
  changed=self.hashes.get(old)!=new;self.hashes[old]=new;self.roles[old]=dict(current=new,role=role,evidence_sha256=evidence_sha256);return changed
 def string(self,value):
  if value in self.hashes:return self.hashes[value]
  if value in self.context:return self.context[value]
  if value==self.old_root:return self.new_root
  if value.startswith(self.old_root+'/'):
   p=PurePosixPath(value);need(str(p)==value and'..'not in p.parts and'\n'not in value and'\0'not in value,'One canonical absolute reference path')
   return self.new_root+value[len(self.old_root):]
  return value
 def value(self,value):
  if type(value)is str:return self.string(value)
  if type(value)is list:return[self.value(x)for x in value]
  if type(value)is dict:
   result={}
   for k,v in value.items():
    key=self.string(k);need(key not in result,'No path alias collapses two graph edges');result[key]=self.value(v)
   return result
  return value
 def report(self):
  return dict(original_root=self.old_root,current_root=self.new_root,context_literals=self.context,identity_roles=self.roles,
   mathematical_acquisition_established_by_registry=False)

def _metadata_context(node,parents):
 """A SHA substitution must occur in an identity/guard data context."""
 cursor=node
 while cursor in parents:
  child=cursor;cursor=parents[cursor]
  if isinstance(cursor,ast.keyword):return cursor.arg is not None and bool(re.search(r'(sha|hash|pin|source|manifest|freeze|review|capture)',cursor.arg,re.I))
  if isinstance(cursor,ast.Assign):
   names=[n.id for t in cursor.targets for n in ast.walk(t)if isinstance(n,ast.Name)]
   return any(re.search(r'(sha|hash|pin|source|manifest|freeze|review|receipt|capture|fixed|expected)',name,re.I)for name in names)
  if isinstance(cursor,ast.Call):
   name=cursor.func.id if isinstance(cursor.func,ast.Name)else cursor.func.attr if isinstance(cursor.func,ast.Attribute)else''
   return any(bit in name.lower()for bit in('sha','hash','bind','closure','capture','digest','pin','source','freeze'))
  if isinstance(cursor,ast.Compare):
   names=[n.id if isinstance(n,ast.Name)else n.attr for n in ast.walk(cursor)if isinstance(n,(ast.Name,ast.Attribute))]
   strings=[n.value for n in ast.walk(cursor)if isinstance(n,ast.Constant)and type(n.value)is str]
   return any(re.search(r'(sha|hash|pin|digest|bind|source|manifest|freeze|review|capture)',n,re.I)for n in names+strings)
  if isinstance(cursor,(ast.Return,ast.BinOp,ast.UnaryOp,ast.Expr)):return False
 return False

def python_epoch(original,refs):
 need(type(original)is bytes and isinstance(refs,References),'Immutable source and explicit references')
 text=original.decode();tree=ast.parse(text);parents={c:p for p in ast.walk(tree)for c in ast.iter_child_nodes(p)};wanted={}
 for node in ast.walk(tree):
  if not isinstance(node,ast.Constant)or type(node.value)is not str:continue
  new=refs.string(node.value)
  if new==node.value:continue
  if HEX.fullmatch(node.value):need(_metadata_context(node,parents),'SHA change outside a source/reference identity guard')
  wanted[node.lineno,node.col_offset]=(node.value,new)
 lines=text.splitlines(keepends=True);starts=[];size=0
 for line in lines:starts.append(size);size+=len(line)
 edits=[]
 for tok in tokenize.generate_tokens(io.StringIO(text).readline):
  if tok.type!=tokenize.STRING:continue
  at=(tok.start[0],len(lines[tok.start[0]-1][:tok.start[1]].encode()))
  if at not in wanted:continue
  old,new=wanted[at];need(ast.literal_eval(tok.string)==old,'One exact original reference token')
  begin=starts[tok.start[0]-1]+tok.start[1];end=starts[tok.end[0]-1]+tok.end[1]
  edits.append((begin,end,repr(new),old,new))
 need(len(edits)==len(wanted),'No hidden joined/f-string reference rewrite')
 current=text
 for a,b,value,_,_ in reversed(edits):current=current[:a]+value+current[b:]
 expected=deepcopy(tree)
 for node in ast.walk(expected):
  if isinstance(node,ast.Constant)and(node.lineno,node.col_offset)in wanted:node.value=wanted[node.lineno,node.col_offset][1]
 need(ast.dump(ast.parse(current),include_attributes=False)==ast.dump(expected,include_attributes=False),'The entire program changes only in admitted metadata literals')
 raw=current.encode();return raw,dict(original_sha256=sha(original),current_sha256=sha(raw),reference_literals_changed=len(edits),all_numeric_constants_and_controls_preserved=True,mathematical_source_body_changed=False)

def canonical_aliases(original,current,refs,*,this_pass=None):
 """Register identity digests of changed JSON subobjects, never new facts."""
 changed=False
 if type(original)in(dict,list):
  need(type(current)is type(original),'Metadata projection preserves JSON types')
  old,new=canonical(original),canonical(current)
  if old!=new:
   this_pass={}if this_pass is None else this_pass
   need(old not in this_pass or this_pass[old]==new,'One old canonical object cannot split into conflicting current objects')
   this_pass[old]=new
   if old in refs.hashes and refs.hashes[old]!=new:
    need(refs.roles[old]['role']=='derived_canonical_identity','Never overwrite an acquired parent with a derived canonical identity')
    refs.hashes.pop(old);refs.roles.pop(old);changed=True
   changed=refs.add(old,new,role='derived_canonical_identity')or changed
  pairs=zip(original.values(),current.values())if type(original)is dict else zip(original,current)
  for a,b in pairs:changed=canonical_aliases(a,b,refs,this_pass=this_pass)or changed
 return changed

def derive(originals,refs,*,maximum_passes=None):
 """Derive the complete source/data graph, failing on cycles/ambiguity.

 ``originals`` must come from independently pinned archives. Accepted current
 outputs are not passed here as originals: their identities are supplied only
 after the caller's full genuine stopped-execution validation.
 """
 need(type(originals)is dict and originals and isinstance(refs,References),'Complete immutable graph plus explicit current dependencies')
 for name,raw in originals.items():need(type(name)is str and not PurePosixPath(name).is_absolute()and'..'not in PurePosixPath(name).parts and type(raw)is bytes,'Contained immutable graph entries')
 limit=maximum_passes or len(originals)+2;need(type(limit)is int and 1<=limit<=len(originals)+2,'Bounded graph dependency expansion')
 current=dict(originals);reports={};previous=None
 for iteration in range(limit):
  output={};this={};new_aliases=False;canonical_this_pass={}
  for name,raw in originals.items():
   if name.endswith('.py'):data,report=python_epoch(raw,refs);this[name]=report
   elif name.endswith('.json'):
    old=read(raw);value=refs.value(old);data=raw if same(value,old)else dump(value)
    new_aliases=canonical_aliases(old,value,refs,this_pass=canonical_this_pass)or new_aliases
   else:data=raw
   output[name]=data
  for name,data in output.items():
   old,new=sha(originals[name]),sha(data)
   if old!=new:
    role='derived_source_metadata'if name.endswith('.py')else'derived_graph_metadata'
    # A dependent node may have acquired a newer identity this pass. It is
    # replaced only while deriving this exclusive graph, never a parent fact.
    if old in refs.hashes and refs.hashes[old]!=new:
     need(refs.roles[old]['role'].startswith('derived_'),'Never overwrite a validated current parent or genuine capture')
     refs.hashes.pop(old);refs.roles.pop(old)
    refs.add(old,new,role=role)
  state={n:sha(b)for n,b in output.items()}
  if state==previous and not new_aliases:
   return output,dict(schema='CURRENT_REFERENCE_GRAPH_EPOCH_V1',files=state,passes=iteration+1,python_projections=this,references=refs.report(),
    historical_execution_impersonated=False,mathematical_source_body_changed=False,mathematical_acquisition_verified=False)
  previous=state;current=output;reports=this
 raise ValueError('Reference graph did not stabilize: inconsistent/cyclic metadata commitments require an explicit typed stage boundary')
