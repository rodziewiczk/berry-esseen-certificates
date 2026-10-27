"""Auditable source-only transport ports for the original mixed acquisitions.

Original native contracts/kernels are immutable. The only program ports replace
obsolete historical parent-execution/source-provenance transport by the actual
fully revalidated B5 export. Scalar, containment, same-cfg and replay functions
outside those explicitly identified blocks remain identical ASTs.
"""
from __future__ import annotations
import ast,hashlib,json
from pathlib import Path
from . import n25_full_join_sources as s,reference_graph_epoch as refs

BRIDGE='CURRENT_B5_PARENT_BINDING.json'
ACQUIRERS={
 'cutoff25_20261013/root/sparse_local_acquisition_v1/acquire.py',
 'cutoff25_20261013/root/pointwise_local_acquisition_v1/acquire.py',
 'cutoff25_20261013/archive_audit/saved_scalar_rectangle_acquisition_v1/acquire.py',
 'cutoff25_20261013/b5/p24_pointwise_acquisition_v1/acquire.py',
 'cutoff25_20261013/archive_audit/p25_grid_pointwise_acquisition_v1/acquire.py'}
AB_BINDINGS={f'cutoff25_20261013/archive_audit/{family}/bindings.py'for family in('b5_sparse_halfline_review_v1','b5_sparse_next_pending_review_v1')}
HELPERS='''
import json as _current_json
from hashlib import sha256 as _current_sha
def _current_parent_binding(root):
    path=root/'CURRENT_B5_PARENT_BINDING.json'
    obj=_current_json.loads(path.read_text())
    assert obj['schema']=='CURRENT_COMPLETE_ORIGINAL_B5_PARENT_AND_CONTACT_BINDING_V1'
    assert obj['global_predecessor_license_acquired'] is False
    assert obj['initial_covers']==13 and obj['probability_panels']==100
    assert obj['contact_allowance']=='5/16' and obj['historical_capture_relabelled'] is False
    for name,pin in obj['files_sha256'].items():
        source=root/name
        assert source.is_file() and _current_sha(source.read_bytes()).hexdigest()==pin
    return obj
def _current_contact_extension(root,index):
    obj=_current_parent_binding(root)
    result=obj['contact_extensions'][str(index)]
    assert result['contact_allowance']=='5/16'
    assert result['finite_feedback_rounds']==3 and result['rho_upper_rounding_denominator']==10**9
    assert result['premise']==dict(schema='ATTAINED_POSITIVE_CLOSED_CONTACT_V1',sample_size=25,same_unrestricted_attained_witness=True,positive_closed_threshold=True,score_at_least_CE=True)
    return result
'''

D_HELPERS='''
def _current_d92_packet(root,bind_fn):
    path=root/'CURRENT_FULL_D92_BINDING.json'
    packet=_current_json.loads(path.read_text())
    assert packet['schema']=='CURRENT_FULL92_GENUINE_PRIMITIVE_TRANSPORT_BRIDGE_V1'
    assert packet['complete_original_D92_primitive_readback'] is True
    assert packet['historical_capture_relabelled'] is False
    assert type(packet['claims']) is list and len(packet['claims'])==92
    assert len({x['claim_id'] for x in packet['claims']})==92
    bind_fn(path)
    return packet
def _current_D92_sources(root,bind_fn):
    packet=_current_d92_packet(root,bind_fn)
    for name,pin in packet['files_sha256'].items():
        bind_fn(root/name,pin)
    for name,pin in packet['unchanged_original_module_aliases'].items():
        bind_fn(root/name,pin)
    return packet
def _current_D92_panel(root,index,summary,bind_fn):
    packet=_current_d92_packet(root,bind_fn)
    rows=[x for x in packet['claims'] if x['panel']==index]
    assert type(index) is int and len(rows)=={24:17,25:45,26:30}[index]
    assert summary['index']==index
    return rows
def _current_D92_compatible(root,index,target,row,cfg,bind_fn):
    packet=_current_d92_packet(root,bind_fn)
    hits=[x for x in packet['claims'] if x['panel']==index and x['source_target_id']==target['id']]
    assert len(hits)==1
    observed=hits[0]
    assert observed['original_cfg']==cfg and observed['k']==target['k'] and observed['box']==target['box']
    assert observed['chain']==row['chain']
    # This is an explicitly DERIVED mathematical compatibility view. The
    # original genuine worker streams/input/commands stay unchanged in the
    # bound D92 export; no metadata.json or stdout is invented or rewritten.
    view={k:v for k,v in row['prefix_result'].items() if k not in ('source_sha256','imported_workspace_modules')}
    assert view==observed['full_fresh_prefix_mathematical_view']
    for name,pin in observed['actual_prefix_original_module_aliases'].items():bind_fn(root/name,pin)
    inp=dict(index=index,target=target,chain=row['chain'],original_cfg=cfg)
    return inp,row['prefix_result']
def _current_D92_origins(root,index,target_id,bind_fn):
    packet=_current_d92_packet(root,bind_fn)
    hits=[x for x in packet['claims'] if x['panel']==index and x['source_target_id']==target_id]
    assert len(hits)==1 and hits[0]['actual_prefix_original_module_aliases']
    for name,pin in hits[0]['actual_prefix_original_module_aliases'].items():bind_fn(root/name,pin)
'''

def D_review_port(raw):
 """Keep all original92 math/geometry/control statements; replace old traces.

 Exact originating D92 commands and full streams are verified by the outer
 complete reader. The supplied in-memory view transports only the original
 mathematical prefix/input equality; it never impersonates a native capture.
 """
 text=raw.decode();tree=ast.parse(text);lines=text.splitlines(keepends=True)
 spans=[
  (34,34,"_current_D92_sources(ROOT,bind)\n"),
  (35,35,"_current=_current_parent_binding(ROOT)\nbind(ROOT/'CURRENT_B5_PARENT_BINDING.json')\nfor _name,_pin in _current['files_sha256'].items():bind(ROOT/_name,_pin)\n"),
  (71,71," additions=read(D/'LOCAL_CONTACT_V14_ADDITIONS.json')\n assert additions['source_directory']=='/'+'Users/bkolodziejek/Downloads/BE_Codex_Handoff/work/cutoff25_20261013/b5/local_contact_v14_combined'\n central=ROOT/'work/cutoff25_20261013/b5/local_contact_v14_combined'\n"),
  (78,84," _current_D92_panel(ROOT,index,summary,bind)\n"),
  (93,96,"  inp,stdout=_current_D92_compatible(ROOT,index,target,row,cfg,bind)\n"),
  (98,102,"  _current_D92_origins(ROOT,index,target['id'],bind)\n")]
 # Pin exact original source and every transport span. The reviewed fixed
 # offsets cannot silently absorb a changed mathematical statement.
 s.need(hashlib.sha256(raw).hexdigest()=='b8e1b596cd1b4698ef62c602f62ef47080824d14cb6f5e7b195d533030097bfa',
  'Exactly the independently pinned original full D checker')
 current=text;changes=[]
 for first,last,replacement in reversed(spans):
  old=''.join(lines[first-1:last]);s.need(old and current.count(old)==1,'One exact D historical-transport span')
  current=current.replace(old,replacement,1);changes.append(dict(first=first,last=last,old=old,current=replacement,
   old_sha256=hashlib.sha256(old.encode()).hexdigest()))
 reverse=current
 for change in reversed(changes):
  s.need(reverse.count(change['current'])==1,'Unambiguous inverse D transport projection')
  reverse=reverse.replace(change['current'],change['old'],1)
 s.need(ast.dump(ast.parse(reverse),include_attributes=False)==ast.dump(tree,include_attributes=False),
  'Every original mathematical, physical, geometry and negative-control statement is unchanged')
 return(HELPERS+D_HELPERS+current).encode(),dict(schema='EXPLICIT_FULL92_CURRENT_CAPTURE_TRANSPORT_PORT_V1',
  spans=changes,original_92_math_geometry_and_controls_preserved=True,
  original_current_D_acquisition_capture_checks_preserved=True,
  compatibility_view_is_explicitly_derived_not_a_native_capture=True,historical_execution_relabelled=False)

def replace_span(text,node,replacement):
 lines=text.splitlines(keepends=True);old=''.join(lines[node.lineno-1:node.end_lineno])
 current=''.join(lines[:node.lineno-1])+replacement+''.join(lines[node.end_lineno:])
 return current,old

def acquire_port(raw):
 text=raw.decode();tree=ast.parse(text);function=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='acquire')
 body=function.body
 start=next(i for i,n in enumerate(body)if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='retained'for t in n.targets))
 end=next(i for i,n in enumerate(body[start:],start)if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)
  and any(isinstance(x,ast.Constant)and x.value=='initial_covers'for x in ast.walk(n)))
 first,last=body[start],body[end];lines=text.splitlines(keepends=True);old=''.join(lines[first.lineno-1:last.end_lineno])
 replacement=""" current=_current_parent_binding(ROOT)
 c.configure(5)
 c.bind(ROOT/'CURRENT_B5_PARENT_BINDING.json')
 for name,value in current['files_sha256'].items():c.bind(ROOT/name,value)
 b,i,out=5,32,dict(initial_covers=13,local_covers=0)
"""
 current=''.join(lines[:first.lineno-1])+replacement+''.join(lines[last.end_lineno:])
 # These original calls validate source-constructor history as well as the
 # actual entire V12+two-fields contract extension. The replacement is the
 # separately reconstructed current exact extension, bound to original bytes.
 changed=ast.parse(current);calls=[]
 for n in ast.walk(changed):
  if (isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and isinstance(n.func.value,ast.Name)
   and n.func.value.id=='v8'and n.func.attr=='selected_extension'):calls.append(n)
 edits=[];current_lines=current.splitlines(keepends=True)
 for call in calls:
  s.need(call.lineno==call.end_lineno and len(call.args)==3 and
   ((isinstance(call.args[1],ast.Constant)and type(call.args[1].value)is int)
    or(isinstance(call.args[1],ast.Name)and call.args[1].id=='index')),'One literal original selected contact index or original fixed-PANELS loop')
  line=current_lines[call.lineno-1];old_call=line[call.col_offset:call.end_col_offset]
  index=repr(call.args[1].value)if isinstance(call.args[1],ast.Constant)else'index'
  new_call='_current_contact_extension(ROOT,'+index+')';edits.append((old_call,new_call))
 for old_call,new_call in edits:
  s.need(current.count(old_call)==1,'One explicit contact constructor-history call');current=current.replace(old_call,new_call)
 reverse=current
 for a,b in reversed(edits):reverse=reverse.replace(b,a)
 reverse=reverse.replace(replacement,old)
 s.need(ast.dump(ast.parse(reverse),include_attributes=False)==ast.dump(tree,include_attributes=False),
  'All original mathematical acquisition statements outside the named transport blocks are unchanged')
 return(HELPERS+current).encode(),dict(parent_block_original=old,parent_block_current=replacement,
  contact_constructor_calls=edits,original_mathematical_statement_projection_unchanged=True,
  historical_acquisition_promoted=False)

def bindings_port(raw):
 text=raw.decode();tree=ast.parse(text);function=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='initialize')
 tests=[n for n in ast.walk(function)if isinstance(n,ast.If)and isinstance(n.test,ast.Compare)
  and any(isinstance(x,ast.Constant)and x.value=='source_inputs_sha256'for x in ast.walk(n.test))]
 s.need(len(tests)==1,'One original historical contract-provenance graph gate')
 replacement="""  current=_current_parent_binding(ROOT)
  bind(ROOT/'CURRENT_B5_PARENT_BINDING.json')
  for name,value in current['files_sha256'].items():bind(ROOT/name,value)
"""
 current,old=replace_span(text,tests[0],replacement)
 s.need(ast.dump(ast.parse(current.replace(replacement,old)),include_attributes=False)==ast.dump(tree,include_attributes=False),
  'Only historical source-provenance transport changes; native cfg and all scalar/moment/COUNT predicates remain exact')
 return(HELPERS+current).encode(),dict(old_source_provenance_gate=old,current_parent_transport=replacement,
  mathematical_functions_unchanged=True,historical_source_inputs_are_fresh=False)

def freeze_A_port(raw):
 text=raw.decode();tree=ast.parse(text);loops=[n for n in tree.body if isinstance(n,ast.For)and isinstance(n.target,ast.Tuple)
  and [t.id for t in n.target.elts if isinstance(t,ast.Name)]==['label','script','rc']]
 s.need(len(loops)==1,'One exact A review capture-history loop');node=loops[0]
 old=ast.literal_eval(node.iter);s.need(len(old)==4 and old[1]==('b5_sparse_scalar01','check_scalar.py',1),
  'The excluded record is exactly the historical failed draft, not a mathematical replay/control')
 new=[item for item in old if item[2]==0];s.need(len(new)==3,'Every successful original16/scalar/25 replay remains')
 # Replace precisely the iteration literal, preserving the entire capture
 # validation body. The old failed trial is provenance, never a fake fresh run.
 lines=text.splitlines(keepends=True);n=node.iter;s.need(n.lineno==n.end_lineno,'One source literal')
 line=lines[n.lineno-1];literal=line[n.col_offset:n.end_col_offset];replacement=repr(new)
 current=text.replace(literal,replacement,1)
 s.need(ast.dump(ast.parse(current.replace(replacement,literal,1)),include_attributes=False)==ast.dump(tree,include_attributes=False),
  'All original A arithmetic/control and successful capture statements remain unchanged')
 return current.encode(),dict(historical_failed_trial_preserved_as_provenance_only=True,
  removed_historical_trial=old[1],fresh_successful_actions=new,mathematical_body_changed=False)

def freeze_B_port(raw):
 text=raw.decode();tree=ast.parse(text);loops=[n for n in tree.body if isinstance(n,ast.For)
  and isinstance(n.target,ast.Tuple)and [t.id for t in n.target.elts if isinstance(t,ast.Name)]==['run','rc']]
 s.need(len(loops)==1,'One exact B review capture-history loop');node=loops[0]
 old=ast.literal_eval(node.iter)
 s.need(old==[('b5_sparse_next_24_check01',1),('b5_sparse_next_24_check02',0),
  ('b5_sparse_next_scalar_check01',0),('b5_sparse_next_25_check01',0)],
  'The omitted record is only the original failed no-op seam fixture; every successful full replay remains')
 lines=text.splitlines(keepends=True);n=node.iter
 # The exact literal may span lines; tokenize the source span in its own
 # already parsed node rather than changing the loop's capture checks.
 first=lines[n.lineno-1][:n.col_offset];last=lines[n.end_lineno-1][n.end_col_offset:]
 literal=''.join(lines[n.lineno-1:n.end_lineno]);replacement=repr(old[1:])
 current=''.join(lines[:n.lineno-1])+first+replacement+last+''.join(lines[n.end_lineno:])
 reverse=current.replace(replacement,literal[len(first):len(literal)-len(last)],1)
 s.need(ast.dump(ast.parse(reverse),include_attributes=False)==ast.dump(tree,include_attributes=False),
  'All successful B arithmetic, complete scalar/count joins and corruption controls remain unchanged')
 return current.encode(),dict(historical_failed_trial_preserved_as_provenance_only=True,
  removed_historical_trial=old[0],fresh_successful_actions=old[1:],mathematical_body_changed=False)

def port(name,raw):
 if name in ACQUIRERS:return acquire_port(raw)
 if name in AB_BINDINGS:return bindings_port(raw)
 if name=='cutoff25_20261013/archive_audit/b5_sparse_halfline_review_v1/freeze.py':return freeze_A_port(raw)
 if name=='cutoff25_20261013/archive_audit/b5_sparse_next_pending_review_v1/freeze.py':return freeze_B_port(raw)
 if name=='cutoff25_20261013/b5/saved_scalar_rectangle_acquisition_review_v1/check_v2.py':return D_review_port(raw)
 return raw,dict(no_transport_body_edit=True)

def verify_port(name,original,current):
 expected,report=port(name,original)
 s.need(current==expected,'Exact individually reviewed current mixed source transport port')
 return dict(report,original_sha256=hashlib.sha256(original).hexdigest(),current_sha256=hashlib.sha256(current).hexdigest())

def reference_epoch(originals,registry):
 """Apply only registered path/SHA identities after the named transport ports.

Native contracts/count protocols and numerical kernels are never passed here.
Every current result registered in ``registry`` must already have a complete
stopped-execution readback; candidate metadata carries only a derived role.
 """
 ported={};projections={}
 for name,raw in originals.items():
  ported[name],projections[name]=port(name,raw)
 current,report=refs.derive(ported,registry)
 return current,dict(schema='FULL66_MIXED_EXPLICIT_CURRENT_TRANSPORT_EPOCH_V1',ports=projections,
  registered_reference_graph=report,original_count_contracts_and_math_kernels_changed=False,
  historical_execution_relabelled=False,mathematical_acceptance=False)
