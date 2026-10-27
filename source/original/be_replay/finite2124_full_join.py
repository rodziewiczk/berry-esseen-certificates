"""58H internal full8-band runtime and clean stopped-evidence reader.

These are complete conditional band implications, never a full58H notebook or
an incoming sharp predecessor. Every row, native forest, scalar reference and
genuine current producer is checked again when restoring a completed action.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,shutil
from . import finite2124_full_join_worker as worker,finite2124_core_evidence as core_ev
from . import finite2124_core_sources as core_src,finite1039_sources as counts,finite1039_count_evidence as count_ev
from . import finite2024_remaining_sources as sources,stopped_prefix as prefix,delivery_transport as tx
from .finite1039_count_evidence import same
from .colab_batch import atomic_json

def input_record(root,task,checked,key):
 return dict(job_id=key,task_relative=Path(task).relative_to(root).as_posix(),validated=checked)
def wrapper(context,n,band):
 runtime=context['original_runtime_root'];pin=context['worker_sha256']
 return ('from pathlib import Path\nimport sys,hashlib\n'
  +'sys.path.insert(0,'+repr(runtime)+')\n'
  +'import be_replay.finite2124_full_join_worker as worker\n'
  +'assert Path(worker.__file__).resolve()==Path('+repr(runtime)+')/"be_replay/finite2124_full_join_worker.py"\n'
  +'assert hashlib.sha256(Path(worker.__file__).read_bytes()).hexdigest()=='+repr(pin)+'\n'
  +'root=Path(__file__).resolve().parent.parent\n'
  +'result=worker.run(root,'+str(n)+','+repr(band)+')\n'
  +'out=Path(__file__).resolve().parent/"CURRENT_BAND_RESULT.json"\nassert not out.exists()\n'
  +'out.write_bytes(worker.dump(result))\n'
  +'print("CURRENT_FULL_BAND_COMPLETE",'+str(n)+','+repr(band)+',hashlib.sha256(out.read_bytes()).hexdigest(),flush=True)\n').encode()
def prepare(cache,task,n,band,*,core_task,count_tasks):
 core_src.case(n,band);task=sources.ordinary(task);sources.need(not task.exists(),'Fresh full actual-index band');task.mkdir(parents=True)
 sources.verify_cache(cache);shutil.copytree(cache,task/'originals');sources.verify_cache(task/'originals')
 core=task/'inputs/core';checked=core_ev.validate_completed(core_task);shutil.copytree(core_task,core)
 sources.need(same(core_ev.validate_completed(core),checked),'Whole original/current four-call parent bytes')
 selected={r['job_id']:r for r in counts.jobs('n20_24')if(r['n'],r['band'])==(n,band)}
 sources.need(set(count_tasks)==set(selected),'Only and all selected full native forests for this band')
 records=[]
 for i,key in enumerate(sorted(selected)):
  source=Path(count_tasks[key]);checked_count=count_ev.validate_completed(source);out=task/'inputs/counts'/str(i);shutil.copytree(source,out)
  sources.need(same(count_ev.validate_completed(out),checked_count),'Whole genuine current native acceptance survives export/copy')
  records.append(input_record(task,out,checked_count,key))
 request=dict(schema='CURRENT_FULL21_24_BAND_INPUTS_V1',n=n,band=band,core_task_relative='inputs/core',core_validated=checked,
  count_inputs=records,reference_catalog_sha256=worker.REFERENCE_SHA256,conditional_statement_only=True,
  original_constructor_history_claimed_current=False,global_proof_accepted=False)
 atomic_json(task/'CURRENT_BAND_INPUTS.json',request)
 context=dict(n=n,band=band,original_runtime_root=str(sources.ROOT),worker_sha256=sources.digest(worker.__file__),
  reference_catalog_sha256=worker.REFERENCE_SHA256,full58H_completed=False,global_proof_accepted=False)
 (task/'capsule').mkdir();(task/'capsule/CURRENT_FAMILY_WORKER.py').write_bytes(wrapper(context,n,band))
 return prefix.begin(task,adapter=Adapter(n,band),context=context)

class Adapter:
 def __init__(self,n,band):core_src.case(n,band);self.n,self.band=n,band
 def specs(self):return [dict(id=f'full_band_{self.n}_{self.band}',cwd='',argv=['{python}','-B','-S','CURRENT_FAMILY_WORKER.py'],outputs=['CURRENT_BAND_RESULT.json'])]
 def identity(self):
  return dict(n=self.n,band=self.band,source_plan_sha256=sources.PLAN_SHA256,reference_catalog_sha256=worker.REFERENCE_SHA256,
   files={n:sources.digest(sources.ROOT/'be_replay'/n)for n in('finite2124_full_join.py','finite2124_full_join_worker.py','finite2024_join_scalar.py',
    'finite2124_core_evidence.py','finite1039_count_evidence.py')})
 def _inputs(self,task):
  task=Path(task);request=sources.read(task/'CURRENT_BAND_INPUTS.json')
  sources.need(request['schema']=='CURRENT_FULL21_24_BAND_INPUTS_V1'and type(request['n'])is int and request['n']==self.n
   and request['band']==self.band and request['reference_catalog_sha256']==worker.REFERENCE_SHA256
   and request['conditional_statement_only']is True and request['original_constructor_history_claimed_current']is False
   and request['global_proof_accepted']is False,'Explicit complete conditional native band inputs')
  core=task.joinpath(*sources.parts(request['core_task_relative']));checked=core_ev.validate_completed(core)
  sources.need(same(checked,request['core_validated']),'Whole current core stage, not a declared parent PASS')
  selected={r['job_id']:r for r in counts.jobs('n20_24')if(r['n'],r['band'])==(self.n,self.band)};by_id={r['job_id']:r for r in request['count_inputs']}
  sources.need(len(by_id)==len(request['count_inputs'])and set(by_id)==set(selected),'Exact complete current COUNT domain')
  actual={}
  for key,row in by_id.items():
   path=task.joinpath(*sources.parts(row['task_relative']));checked=count_ev.validate_completed(path)
   sources.need(same(checked,row['validated']),'Every full original fresh native acceptance, all roots/leaves/control/capture/source fields')
   actual[key]=dict(task=path,checked=checked,row=selected[key])
  return request,core,actual
 def validate_initial(self,task,state):
  sources.verify_cache(Path(task)/'originals');self._inputs(task);context=state['context'];worker.verify_projection();worker.references()
  sources.need(context['n']==self.n and context['band']==self.band and context['worker_sha256']==sources.digest(worker.__file__)
   and context['reference_catalog_sha256']==worker.REFERENCE_SHA256 and context['full58H_completed']is False and context['global_proof_accepted']is False,
   'Exact original/current band runtime source identity and limited scope')
  expected=hashlib.sha256(wrapper(context,self.n,self.band)).hexdigest()
  sources.need(state['initial_inventory']=={'CURRENT_FAMILY_WORKER.py':expected},'Independently derived exact actual-entry wrapper')
 def copy_validation_context(self,task,target):
  for folder in('originals','inputs'):shutil.copytree(Path(task)/folder,Path(target)/folder)
  shutil.copyfile(Path(task)/'CURRENT_BAND_INPUTS.json',Path(target)/'CURRENT_BAND_INPUTS.json')
 def validate_live(self,task,state):
  sources.need(state['adapter_identity']==self.identity()and not state['actions'],'Exactly one fresh complete band invocation')
  self.validate_initial(task,state);sources.need(prefix.hashes(Path(task)/'capsule')==state['initial_inventory'],'No partial source/output state may resume')
 def prepare_action(self,task,state,spec):return dict(source_epoch_required=False,original_mathematical_interface_functions_unchanged=True)
 def validate_epoch(self,task,state,spec,item):
  sources.need(item['source_changes']=={}and same(item['source_epoch'],self.prepare_action(task,state,spec)),'No invented source mutation in the full band worker')
 def capture_inputs(self,task,spec):return {'CURRENT_FAMILY_WORKER.py':sources.digest(Path(task)/'capsule/CURRENT_FAMILY_WORKER.py')}
 def validate_output(self,task,state,spec,item,stdout):
  request,core,counts_by_id=self._inputs(task);result=sources.read(Path(task)/'capsule/CURRENT_BAND_RESULT.json')
  fields={'schema','n','band','K','target','exact_native_target','historical_dependency_graph_reproduced','numerical_resource_or_leaf_oracle_calls','rho_interval','p_interval','panels','total_count_leaves','total_count_nodes',
   'maximum_recorded_count_score','typed_contract_controls','current_full_parent_stage_sha256','full_original_interface_source_sha256',
   'historical_constructor_execution_claimed_current','current_full_count_acceptance_revalidated','conditional_band_excluded',
   'predecessor_n','predecessor_global_sharp_required','predecessor_verified','global_bound_proved','cutoff20_proved','all_index_conclusion_verified'}
  sources.need(set(result)==fields and result['schema']=='CURRENT_COMPLETE_ACTUAL21_24_CONDITIONAL_BAND_V1'and type(result['n'])is int and result['n']==self.n
   and result['band']==self.band and result['K']=='0'and result['target']=='CE'and result['exact_native_target']==str(worker.exact_native_target())
   and result['historical_dependency_graph_reproduced']is False and type(result['numerical_resource_or_leaf_oracle_calls'])is int and result['numerical_resource_or_leaf_oracle_calls']==0
   and result['rho_interval']==core_src.BANDS[self.band][0]and result['p_interval']==['0','1']
   and result['conditional_band_excluded']is True and result['predecessor_n']==self.n-1 and result['predecessor_global_sharp_required']is True
   and result['current_full_count_acceptance_revalidated']is True and all(result[k]is False for k in('historical_constructor_execution_claimed_current',
    'predecessor_verified','global_bound_proved','cutoff20_proved','all_index_conclusion_verified')),'Entire original-index conditional band scope, no parent or global promotion')
  ref=sources.read(sources.ROOT/'proof/finite2124_full_interface_references.json');band=ref['bands'][core_src.case(self.n,self.band)];reference=worker.references()
  folder=core/'capsule'/core_src.RESOURCE/core_src.case(self.n,self.band);candidate=core_src.read(folder/'CANDIDATE.json',128*core_src.MIB)
  sources.need(len(result['panels'])==len(band['rows'])==len(candidate['rows'])==100,'Whole100 original probability panels')
  used=set();total_leaves=total_nodes=0;maximum=F(0)
  for i,(row,original,desc)in enumerate(zip(result['panels'],band['rows'],candidate['rows'])):
   sources.need(type(row['index'])is int and row['index']==i and row['p']==original['p']==[str(F(i,100)),str(F(i+1,100))]
    and row['disposition']==original['disposition'],'Every exact original closed probability disposition')
   base_fields={'index','p','resource_row_sha256','disposition'}
   extra=({'scalar_proof'}if row['disposition']=='EXCLUDED_BY_STRICT_SCALAR_MOMENT'else
    {'job_id','contract_sha256','current_count_stage_sha256','scalar_proof_sha256','scalar_proof','statistics','current_parent_binding'}
    if row['disposition']=='EXCLUDED_BY_FRESH_NATIVE_FULL_COUNT'else set())
   sources.need(set(row)==base_fields|extra,'Whole exact original panel schema without an extra success claim')
   physical=folder/desc['path'];packet=core_src.read(physical,128*core_src.MIB)
   sources.need(row['resource_row_sha256']==sources.digest(physical)==desc['sha256']and worker.canonical(packet)==original['reference_row_canonical_sha256'],
    'Entire current parent mathematical row, all original fields unchanged')
   if row['disposition']=='EXCLUDED_BY_FRESH_RESOURCE':sources.need(packet['result']['excluded']is True,'Real whole-panel resource exclusion')
   elif row['disposition']=='EXCLUDED_BY_STRICT_SCALAR_MOMENT':
    sources.need(worker.canonical(row['scalar_proof'])==original['reference_scalar_canonical_sha256']
     and F(original['scalar_rho_floor'])>F(packet['result']['result']['rho_hi']),'Entire independently checked original strict scalar certificate')
   else:
    key=original['job_id'];sources.need(row['job_id']==key and key not in used,'Exactly one full native forest for this retained panel');used.add(key)
    current=counts_by_id[key];r=current['row'];receipt=counts.read(current['task']/current['checked']['summary']['receipt_relative'])
    count_folder=current['task']/'capsule'/r['directory']
    sources.need(sources.digest(count_folder/r['candidate'])==r['candidate_sha256']
     and sources.digest(count_folder/r['contract_name'])==r['contract_sha256'],'Immediate immutable whole forest and contract identities')
    forest=counts.read(count_folder/r['candidate'],limit=128*counts.MIB);contract=counts.read(count_folder/r['contract_name'])
    sources.need(same(row['statistics'],receipt['statistics'])and row['contract_sha256']==r['contract_sha256']==reference[key]['immutable_contract_sha256']
     and row['current_count_stage_sha256']==current['checked']['stage_result_sha256']and worker.canonical(contract['rows'][0])==reference[key]['whole_contract_cfg_canonical_sha256'],
     'Whole current complete native count and immutable simultaneous contract')
    scalar_sha=hashlib.sha256(worker.dump(row['scalar_proof'])).hexdigest()
    sources.need(worker.canonical(row['scalar_proof'])==reference[key]['reference_scalar_canonical_sha256']
     and scalar_sha==row['scalar_proof_sha256'],'Entire scalar certificate independently matches its immutable reference and actual current serialization')
    sources.need(F(row['statistics']['maximum_score'])<F(forest['target'])<=worker.exact_native_target(),
     'Strict original exact native target licensed by the rigorous CE lower enclosure')
    binding=row['current_parent_binding'];sources.need(set(binding)=={'historical_candidate_sha256','historical_acceptance_sha256',
     'current_candidate_sha256','current_acceptance_sha256','current_full_core_stage_sha256','same_complete_physical_row',
     'historical_hashes_rewritten','original_row_sha256','current_row_sha256','original_scalar_sha256','current_scalar_sha256',
     'entire_row_and_scalar_canonical_equality_verified'}and binding['historical_candidate_sha256']==contract['resource_candidate_sha256']
     and binding['historical_acceptance_sha256']==contract['resource_replay_sha256']and binding['historical_hashes_rewritten']is False
     and binding['current_candidate_sha256']==sources.digest(folder/'CANDIDATE.json')and binding['current_acceptance_sha256']==sources.digest(folder/'ACCEPTED.json')
     and binding['current_full_core_stage_sha256']==request['core_validated']['stage_result_sha256']and binding['same_complete_physical_row']is True
     and binding['entire_row_and_scalar_canonical_equality_verified']is True
     and binding['original_row_sha256']==reference[key]['reference_row_sha256']and binding['current_row_sha256']==row['resource_row_sha256']
     and binding['original_scalar_sha256']==reference[key]['whole_scalar_proof_sha256']and binding['current_scalar_sha256']==scalar_sha,
     'Historical identities preserved; actual current whole parent facts separately bound')
    total_leaves+=receipt['statistics']['leaves'];total_nodes+=receipt['statistics']['nodes'];maximum=max(maximum,F(receipt['statistics']['maximum_score']))
  sources.need(used==set(counts_by_id)and result['total_count_leaves']==total_leaves and result['total_count_nodes']==total_nodes
   and F(result['maximum_recorded_count_score'])==maximum and result['typed_contract_controls']==8*len(used),
   'Every selected complete forest, all original typed controls, exact total native census')
  sources.need(result['current_full_parent_stage_sha256']==request['core_validated']['stage_result_sha256'],
   'Whole actual original four-call current parent is the same parent throughout this band')
  expected_sources={name:sources.digest(Path(task)/'originals'/relative)for name,relative in worker.MODULES}
  sources.need(result['full_original_interface_source_sha256']==expected_sources,'Every entire original physical/scalar/coupled reader source')
  sources.need(stdout.splitlines()[-1].split()==['CURRENT_FULL_BAND_COMPLETE',str(self.n),self.band,
   sources.digest(Path(task)/'capsule/CURRENT_BAND_RESULT.json')],'Actual whole stopped current band terminal')
  return dict(n=self.n,band=self.band,panels=100,count_forests=len(used),count_leaves=total_leaves,count_nodes=total_nodes,
   conditional_band_excluded=True,current_whole_count_execution_revalidated=True,global_proof_accepted=False)

def execute_prepared(task,n,band,*,root):
 adapter=Adapter(n,band);prefix.advance(task,adapter=adapter,root=root);return validate_completed(task)
def validate_completed(task):
 state=prefix.read(Path(task)/'PREFIX.json');adapter=Adapter(state['context']['n'],state['context']['band']);checked=prefix.validate(task,adapter=adapter)
 sources.need(checked['all_original_actions_completed']is True,'Complete full100-panel current band action')
 summary=state['actions'][0]['validated_output']
 return dict(schema='REVALIDATED_COMPLETE_CURRENT_ACTUAL21_24_BAND_V1',n=adapter.n,band=adapter.band,
  prefix_sha256=checked['prefix_sha256'],summary=summary,conditional_band_excluded=True,global_proof_accepted=False)
