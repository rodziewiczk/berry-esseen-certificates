"""Bounded real native math, whole-reader and fail-closed regression checks."""
from pathlib import Path
import importlib.util,json,subprocess,sys
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('actual20_count_bridge',HERE/'replay.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
out=HERE/'smoke-final-p58';job='n20.B0.p58.79bbd7ee573f'
subprocess.run([sys.executable,'-I','-B',str(HERE/'replay.py'),'replay','--job',job,'--output',str(out),'--timeout','30'],check=True)
sys.path.insert(0,str(out/'runtime'))
from be_replay import finite1039_sources as src,finite1039_count_evidence as ce
row=r.rows(src)[job];result=r.validate_portable(out,row,src,ce)
assert result['summary']['census']['leaves']==30 and len(result['summary']['native_controls'])==24
checks=['fresh30-leaf24-control-native-acceptor','whole-original-mathematical-reader','complete-fresh-process-and-source-inventory']
for args in ([ 'replay','--job','C20-fabricated','--output',str(HERE/'must-not-exist')],['replay','--job',job,'--timeout','nan','--output',str(HERE/'must-not-exist')]):
 p=subprocess.run([sys.executable,'-I','-B',str(HERE/'replay.py'),*args],capture_output=True,text=True);assert p.returncode==2 and not(HERE/'must-not-exist').exists()
checks+=['unknown-job-rejected-before-output','nonfinite-timeout-rejected-before-output']
try:r.count_files({job:str(out)},src,ce)
except ValueError as error:assert 'All49' in str(error)
else:raise AssertionError('Incomplete bridge accepted')
checks.append('incomplete49-bridge-rejected')
# Corrupt complete receipt, update the advisory public inventory, and ensure
# the unchanged original whole mathematical reader still rejects it.
receipt=out/'task/capsule'/row['directory']/row['output'];original=receipt.read_bytes();original_result=(out/'RESULT.json').read_bytes()
try:
 packet=r.read(receipt);packet['negative_controls'].pop();r.write(receipt,packet)
 r.write(out/'RESULT.json',dict(result,artifacts=r.inventory(out/'task')))
 try:r.validate_portable(out,row,src,ce)
 except ValueError:pass
 else:raise AssertionError('Altered native controls accepted')
finally:receipt.write_bytes(original);(out/'RESULT.json').write_bytes(original_result)
r.validate_portable(out,row,src,ce);checks.append('altered-native-controls-rejected-by-original-whole-reader')
manifest=r.manifest()
assert len(manifest['source_files'])==1366 and len(r.rows(src))==49
r.write(HERE/'SMOKE-RESULT.json',dict(checks=checks,job=job,leaves=30,native_controls=24,all49_sources_verified=True,all49_arithmetic_executed=False,linux_original_stage_executed=False,full_pass=False))
print(json.dumps(checks))
