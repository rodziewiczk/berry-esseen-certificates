"""Internal coarse actual20 transaction for the grouped58H runner.

There is deliberately no standalone Run-all entrypoint or partial58H claim.
Original numerical execution is restricted to an actual Linux supervisor.
"""
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import platform
import shutil
import stat
import sys
import threading
import time
import uuid
import zipfile
from . import finite20_coarse_sources as src,finite20_coarse_evidence as ev,linux_supervisor
from .colab_batch import atomic_json,event

CACHE_BYTES=512*src.MIB


class Follow:
    def __init__(self,root,task,action):
        self.root,self.task,self.action=Path(root),Path(task),action
        self.stop=threading.Event();self.thread=threading.Thread(target=self.loop,daemon=True)
    def loop(self):
        position=0;partial=b'';started=time.monotonic();last=-20;draining=False
        while True:
            try:
                with(self.task/'executions'/self.action/'stdout.txt').open('rb')as stream:stream.seek(position);data=stream.read(src.MIB)
                position+=len(data);lines=(partial+data).split(b'\n');partial=lines.pop()
                for line in lines:event(self.root,'finite20_coarse_original_stdout',action=self.action,line=line.decode('utf-8',errors='replace')[:4096])
            except FileNotFoundError:pass
            elapsed=time.monotonic()-started
            if elapsed-last>=20:
                event(self.root,'finite20_coarse_heartbeat',action=self.action,elapsed_seconds=elapsed,stdout_bytes=position,
                      conditional_coarse_initial_arithmetic_completed=False,full_notebook58H_completed=False);last=elapsed
            if self.stop.wait(.2):
                if draining:break
                draining=True
    def __enter__(self):self.thread.start();return self
    def __exit__(self,*unused):
        self.stop.set();self.thread.join(timeout=5);src.need(not self.thread.is_alive(),'Stopped bounded original progress observer')


def write_capture(task,request,band,observed,report):
    """A truthful capture of the actual stopped outer process, never a fake child."""
    task=Path(task);meta=ev.capture_metadata(task,request,band,observed,report)
    directory=task/'capsule'/src.capture_directory(band);src.need(not directory.exists(),'Exclusive genuine current constructor capture')
    directory.mkdir(parents=True)
    for kind in('stdout','stderr'):shutil.copyfile(task/'executions'/(band.lower()+'_construct')/(kind+'.txt'),directory/(kind+'.txt'))
    (directory/'metadata.json').write_bytes(src.dump(meta))
    (directory/'CAPTURE_BRIDGE.json').write_bytes(src.dump(ev.bridge_record(task,request,band,observed,report)))
    ev.verify_capture(task,request,band,observed,report)


def execute(task,cache, *,root):
    src.need(sys.platform=='linux','Actual Linux BASIC process-group supervision required')
    task=Path(task).resolve();request=src.prepare(cache,task)
    report=dict(schema=ev.OBSERVED,scope=ev.SCOPE,original_task_root=request['original_task_root'],implementation=ev.implementation(),
        python_executable=sys.executable,python_version=sys.version,platform=platform.platform(),actions=[],
        conditional_coarse_initial_arithmetic_completed=False,**{f:False for f in ev.FLAGS})
    for action in src.ACTIONS:
        src.verify_job(task);paths=src.output_paths(action)
        src.need(all(not(task/'capsule'/p).exists()for p in paths),'Exclusive new outputs for the original action')
        event(root,'finite20_coarse_original_action_started',action=action,cpu_seconds=ev.CPU_SECONDS,
              wall_seconds=ev.WALL_SECONDS,memory_bytes=ev.MEMORY_BYTES,full_notebook58H_completed=False)
        with Follow(root,task,action):
            observed=linux_supervisor.run(ev.command(action,sys.executable),cwd=task/'capsule'/ev.action_cwd(action),
                output_dir=task/'executions'/action,mode='untrusted_search',cpu_seconds=ev.CPU_SECONDS,
                wall_seconds=ev.WALL_SECONDS,memory_bytes=ev.MEMORY_BYTES,disk_bytes=512*src.MIB,
                log_bytes=16*src.MIB,heartbeat_seconds=20,checkpoint_paths=[task/'capsule'/p for p in paths])
        report['actions'].append(dict(action=action,observed=observed));atomic_json(task/'ACTIONS_PARTIAL.json',report)
        try:stdout=ev.transport(task,request,action,observed,report)
        except Exception as error:
            path=task/'executions'/action/'stderr.txt';tail=''
            if path.is_file()and not path.is_symlink()and path.stat().st_size<=16*src.MIB:
                with path.open('rb')as stream:stream.seek(max(0,path.stat().st_size-4096));tail=stream.read(4096).decode('utf-8',errors='replace')
            event(root,'finite20_coarse_action_incomplete',action=action,error=str(error),stderr_tail=tail,full_notebook58H_completed=False)
            raise ValueError('Original coarse action '+action+' incomplete: '+str(error)+'; stderr tail: '+tail)from error
        if action.endswith('_construct'):write_capture(task,request,action[:2].upper(),observed,report)
        if action=='prepare':
            packet=src.read(task/'capsule'/src.AUDIT/'PREPARED.json')
            src.need(ev.same(packet,ev.expected_prepared(task))and ev.same(ev.terminal(stdout),{k:v for k,v in packet.items()if k!='files_sha256'}),
                     'Original preparation completed its whole genuine current source/candidate/capture graph')
        src.verify_job(task)
        event(root,'finite20_coarse_original_action_stopped_successfully',action=action,completed_actions=len(report['actions']),total_actions=5,
              conditional_coarse_initial_arithmetic_completed=False,full_notebook58H_completed=False)
    atomic_json(task/'STAGE_OBSERVED.json',report);summary=ev.validate_run(task,report)
    complete=dict(schema=ev.COMPLETED,scope=ev.SCOPE,implementation=ev.implementation(),
        observed_sha256=src.digest(task/'STAGE_OBSERVED.json'),summary=summary,artifacts=ev.inventory(task),
        conditional_coarse_initial_arithmetic_completed=True,**{f:False for f in ev.FLAGS})
    atomic_json(task/'STAGE_COMPLETED.json',complete);return ev.validate_completed(task)


def cache_members(z):
    rows=z.infolist();src.need(0<len(rows)<=1000,'Bounded complete coarse transaction inventory');names=set();folded=set();total=0
    for r in rows:
        src.parts(r.filename);mode=r.external_attr>>16
        src.need(not r.is_dir()and not r.flag_bits&1 and not stat.S_ISLNK(mode)and stat.S_IFMT(mode)in(0,stat.S_IFREG)
                 and r.filename not in names and r.filename.casefold()not in folded and 0<=r.file_size<=128*src.MIB,
                 'Unique ordinary bounded coarse ZIP member')
        names.add(r.filename);folded.add(r.filename.casefold());total+=r.file_size
    needed={'SOURCES.json','STAGE_OBSERVED.json','STAGE_COMPLETED.json'}
    needed|={'executions/'+a+'/'+n for a in src.ACTIONS for n in('launch.json','supervisor-result.json','stdout.txt','stderr.txt')}
    needed|={'capsule/'+p for p in src.allowed_outputs()}
    src.need(total<=CACHE_BYTES and needed<=names,'All five complete coarse launches/captures/results');return rows


def save_completed(task,cache):
    task=Path(task);checked=ev.validate_completed(task);cache=src.ordinary(cache);cache.mkdir(parents=True,exist_ok=True)
    name=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]+'-complete.zip';p=cache/name;pending=cache/(name+'.pending')
    with zipfile.ZipFile(pending,'x',compression=zipfile.ZIP_DEFLATED,strict_timestamps=False)as z:
        for file in sorted(task.rglob('*')):
            src.ordinary(file)
            if file.is_file():z.write(file,file.relative_to(task).as_posix())
        cache_members(z)
    src.need(pending.stat().st_size<=CACHE_BYTES,'Bounded full coarse export');pin=src.digest(pending);pending.replace(p)
    p.with_suffix('.zip.sha256').write_bytes((pin+'  '+p.name+'\n').encode('ascii'))
    return dict(path=str(p),sha256=pin,stage_result_sha256=checked['stage_result_sha256'])


def restore_completed(cache,destination, *,root):
    cache=src.ordinary(cache);destination=Path(destination)
    if not cache.exists():return None
    src.need(cache.is_dir(),'Ordinary completed coarse cache directory')
    for p in sorted(cache.glob('*-complete.zip'),reverse=True)[:8]:
        try:
            src.ordinary(p);side=src.ordinary(p.with_suffix('.zip.sha256'))
            src.need(p.is_file()and p.stat().st_size<=CACHE_BYTES and side.is_file()and side.stat().st_size<=1024
                     and side.read_text('ascii')==src.digest(p)+'  '+p.name+'\n','Actual complete coarse ZIP SHA sidecar')
            restored=destination/('coarse-restored-'+uuid.uuid4().hex[:8])
            with zipfile.ZipFile(p)as z:
                rows=cache_members(z);restored.mkdir(parents=True,exist_ok=False)
                for row in rows:
                    target=restored.joinpath(*src.parts(row.filename));target.parent.mkdir(parents=True,exist_ok=True)
                    with z.open(row)as source,target.open('xb')as output:shutil.copyfileobj(source,output,src.MIB)
            checked=ev.validate_completed(restored)
            event(root,'finite20_coarse_complete_transaction_revalidated',cache=str(p),sha256=src.digest(p),numerical_replay_skipped=True,full_notebook58H_completed=False)
            return restored,checked,dict(path=str(p),sha256=src.digest(p))
        except Exception as error:event(root,'finite20_coarse_cache_rejected',cache=str(p),error=type(error).__name__+': '+str(error))
    return None
