"""Explicit41st actual20 action: original conditional coupled scalar lemma.

The original mathematical functions and all controls are unchanged. Only the
historical PREPARED/492-edge transport in main is replaced by five exact
externally pinned conditional contracts. No old resource/capture is acquired.
The native generated program is run only by the stopped-action supervisor.
"""
from pathlib import Path
import ast,hashlib,json
from . import finite2024_remaining_sources as s
from .finite1039_count_evidence import same

B='work/cutoff20_20261016/'
DIRECTORY=B+'root/coupled_noise_v1'
SCRIPT=DIRECTORY+'/check.py'
HELPER=B+'finite/coupled_noise_all_v1/helper.py'
DRIVER=DIRECTORY+'/CURRENT_PARENT.py'
REQUEST=DIRECTORY+'/CURRENT_PARENT_REQUEST.json'
RESULT=DIRECTORY+'/CHECKED.json'
SOURCE_SHA='f58735273e2a8cbc87409e3785ed221c78d7c3d8d99e10c45627ea35ca8d3c74'
CASES=(('B0',37),('B0',42),('B0',50),('BN',37),('BN',42))
CONTROLS=dict(actual_laws=144,rare_distant_cases=48,negative_f_cases=52,
              excluded_unsupported_collision_domain=1,malformed_domains=5)


def contract_path(band,index):
 base='finite/sharp20_b0_counts_all_v1'if band=='B0'else'fourier/narrow_count_v1'
 return B+base+f'/capsule{index}/contract.json'


def source_files(task):
 from .finite2024_actual20_full import original_files
 return original_files(task)


def original(task,name):
 row=source_files(task)[name];path=Path(task)/row['location']/name;raw=path.read_bytes()
 s.need(len(raw)==row['bytes']and hashlib.sha256(raw).hexdigest()==row['sha256'],'Exact original coupled-parent source/reference')
 return raw


def request(task):
 task=Path(task);rows=source_files(task);entries=[]
 for band,index in CASES:
  name=contract_path(band,index);row=rows[name];path=task/'capsule'/name
  s.need(path.is_file()and path.stat().st_size==row['bytes']and s.digest(path)==row['sha256'],
         'Every whole original conditional scalar contract remains unchanged')
  entries.append(dict(band=band,index=index,path=name,bytes=row['bytes'],sha256=row['sha256']))
 old=json.loads(original(task,RESULT));s.need(len(old['files_sha256'])==492,'Full historical graph retained only as source provenance')
 return dict(schema='CURRENT_CONDITIONAL_COUPLED_SCALAR_PARENT_INPUTS_V1',contracts=entries,
  original_check_sha256=SOURCE_SHA,original_parent_reference_sha256=rows[RESULT]['sha256'],
  original_parent_graph_sha256=hashlib.sha256(json.dumps(old['files_sha256'],sort_keys=True,separators=(',',':')).encode()).hexdigest(),
  historical_graph_edges=492,historical_graph_acquired=False,historical_resource_or_capture_replayed=False,
  scope='Five exact conditional scalar contracts and unchanged coupled contractor/control program; no count/resource/global acquisition')


def driver(raw):
 s.need(hashlib.sha256(raw).hexdigest()==SOURCE_SHA,'Whole original coupled contractor and controls pinned')
 text=raw.decode('utf-8');start=text.index("        if band=='B0':\n",text.index('def main():'))
 end=text.index("        need(cfg['n']==20",start);before=text[start:end]
 after="""        context=read(HERE/'CURRENT_PARENT_REQUEST.json')
        need(context['schema']=='CURRENT_CONDITIONAL_COUPLED_SCALAR_PARENT_INPUTS_V1' and context['historical_graph_acquired'] is False and context['historical_resource_or_capture_replayed'] is False,'explicit conditional transport without historical acquisition')
        need(context['original_check_sha256']==sha(HERE/'check.py'),'whole original mathematical source identity')
        entries=[r for r in context['contracts']if r['band']==band and type(r['index'])is int and r['index']==i]
        need(len(context['contracts'])==5 and len(entries)==1,'all and only five exact conditional contracts')
        selected=entries[0];path=ROOT/selected['path']
        need(path.is_file() and path.stat().st_size==selected['bytes'] and sha(path)==selected['sha256'],'exact whole original conditional contract')
        obj=read(path);cfg=obj['rows'][0]
        need(len(obj['rows'])==1,'one simultaneous conditional scalar resource tuple')
        graph[str(path.relative_to(ROOT))]=selected['sha256']
"""
 needle="[Path(__file__),HERE/'PROOF.txt',HERE.parent/'inward_quadratic_noise_v1'/'PROOF.txt']"
 replacement="[Path(__file__),HERE/'check.py',HERE/'CURRENT_PARENT_REQUEST.json',HERE/'PROOF.txt',HERE.parent/'inward_quadratic_noise_v1'/'PROOF.txt']"
 s.need(text.count(needle)==1,'One exact source-transport closure loop')
 changed=(text[:start]+after+text[end:]).replace(needle,replacement)
 reverse=changed.replace(after,before).replace(replacement,needle)
 s.need(ast.dump(ast.parse(reverse),include_attributes=False)==ast.dump(ast.parse(text),include_attributes=False),
        'Reverse transport port preserves every mathematical/control/source statement outside the two named transport blocks')
 names={n.name:n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)}
 actual={n.name:n for n in ast.parse(changed).body if isinstance(n,ast.FunctionDef)}
 s.need(set(names)==set(actual)and all(ast.dump(n,include_attributes=False)==ast.dump(actual[k],include_attributes=False)
        for k,n in names.items()if k!='main'),'Entire original coupled/fixed_cap/roots/controls AST preserved')
 return changed.encode('utf-8')


def prepare(task):
 task=Path(task);raw=original(task,SCRIPT)
 s.need(s.digest(task/'capsule'/SCRIPT)==s.digest(task/'capsule'/HELPER)==SOURCE_SHA,
        'Original check.py and mapper helper.py remain byte-identical, without literal rewriting')
 packet=request(task);generated=driver(raw);path=task/'capsule'/REQUEST;path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(packet,indent=2)+'\n',encoding='utf-8',newline='\n');(task/'capsule'/DRIVER).write_bytes(generated)
 return dict(schema='EXPLICIT_CURRENT_CONDITIONAL_COUPLED_PARENT_SOURCE_EPOCH_V1',
  files_sha256={REQUEST:s.digest(path),DRIVER:s.digest(task/'capsule'/DRIVER)},
  mathematical_source_body_changed=False,historical_execution_relabelled=False,original_controls=CONTROLS)


def validate(task,stdout):
 task=Path(task);capsule=task/'capsule';old=json.loads(original(task,RESULT));current=s.read(capsule/RESULT)
 expected_request=(json.dumps(request(task),indent=2)+'\n').encode('utf-8')
 s.need((capsule/DRIVER).read_bytes()==driver(original(task,SCRIPT))and(capsule/REQUEST).read_bytes()==expected_request,
        'Independently reconstructed exact driver/request transport port')
 s.need(s.digest(capsule/SCRIPT)==s.digest(capsule/HELPER)==SOURCE_SHA,'Original byte-identical contractor/helper retained')
 s.need(set(current)==set(old)and same({k:v for k,v in current.items()if k!='files_sha256'},
                                      {k:v for k,v in old.items()if k!='files_sha256'}),
        'All five original scalar derivations and every original control remain unchanged')
 s.need(same(current['controls'],CONTROLS)and all(type(v)is int for v in current['controls'].values())
        and [(r['band'],r['index'])for r in current['rows']]==list(CASES),'Full144/48/52/1/5 controls and exact five scalar scopes')
 names={contract_path(b,i)for b,i in CASES}|{DRIVER,SCRIPT,REQUEST,DIRECTORY+'/PROOF.txt',B+'root/inward_quadratic_noise_v1/PROOF.txt'}
 expected={name:s.digest(capsule/name)for name in names}
 s.need(same(current['files_sha256'],expected),'Exact current conditional source graph; no historical492-edge graph promoted')
 s.need(stdout.splitlines()[0]==current['status']+' '+str(CONTROLS)and len(stdout.splitlines())==6,
        'Whole stopped original scalar terminal and all five displayed cases')
 return dict(action='coupled_scalar_parent',output_sha256=s.digest(capsule/RESULT),conditional_scalar_cases=5,
  controls=CONTROLS,original_math_and_control_AST_preserved=True,whole_conditional_contracts_checked=True,
  historical_graph_edges=492,historical_graph_acquired=False,global_proof_accepted=False)
