"""Private ordinary-count section of full66, with lossless saved search work.

This is not the full66 entry point. It has no standalone notebook and cannot
declare n25 or full66 complete. Only supervised children call original math.
"""
from __future__ import annotations
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time
import uuid
import zipfile
from . import count_task as common,n25_full_count_sources as sources
from . import n25_full_discovery_sources as discovery,n25_full_counts_evidence as evidence
from . import n25_full_transport as transport
from .colab_batch import atomic_json,event

MIB=1024**2
CPU=WALL=82800
MEMORY=2048*MIB
need=common.need


def prepare(task,target,source_capsule=None,*,recovery_archive=None):
    # Supplying the original recovery archive selects a distinct pinned epoch.
    # No legacy source capsule: prefer the recovered original, never discovery.
    if recovery_archive is not None or source_capsule is None:
        need(source_capsule is None, "Choose recovered originals OR an explicit legacy source capsule")
        from . import n25_recovered_counts as recovered
        from . import n25_recovery_sources as recovered_sources
        return recovered.prepare(task,target,archive=(recovery_archive if recovery_archive is not None
                                                     else recovered_sources.DEFAULT_ARCHIVE))
    task=Path(task).absolute()
    sources.base._no_link_ancestors(task)
    need(not task.exists(),"New isolated ordinary-count task")
    task.mkdir(parents=True,exist_ok=False)
    sources.prepare(target,source_capsule,task/"capsule")
    discovery.prepare(task/"discovery")
    record=dict(schema="N25_FULL66_ORDINARY_COUNT_TASK_V1",target=target,
        source_plan_sha256=sources.PLAN_SHA256,discovery_plan_sha256=discovery.PLAN_SHA256,
        implementation=evidence.implementation(),arithmetic_accepted=False,
        parent_acquisitions_verified=False,full66_complete=False)
    atomic_json(task/"TASK.json",record)
    return record


def check_task(task,target):
    task=transport.ordinary(task,directory=True).resolve()
    row=common.read(task/"TASK.json",4*MIB)
    need(type(row) is dict and set(row)=={"schema","target","source_plan_sha256","discovery_plan_sha256",
        "implementation","arithmetic_accepted","parent_acquisitions_verified","full66_complete"}
        and row["schema"]=="N25_FULL66_ORDINARY_COUNT_TASK_V1" and row["target"]==target
        and row["source_plan_sha256"]==sources.PLAN_SHA256 and row["discovery_plan_sha256"]==discovery.PLAN_SHA256
        and all(row[k] is False for k in ("arithmetic_accepted","parent_acquisitions_verified","full66_complete")),
        "Exact current unaccepted ordinary task")
    evidence._implementation(row["implementation"])
    sources.verify(target,task/"capsule");discovery.verify(task/"discovery")
    return row


def initial_checkpoint(task,target):
    check_task(task,target)
    return dict(schema="UNTRUSTED_COUNT_SEARCH_CHECKPOINT_V1",arithmetic_accepted=False,
        binding=dict(design_sha256=sources.profile(target)["design_sha256"],
            native_header=sources.native_header(target,Path(task)/"capsule"),**discovery.binding(Path(task)/"discovery")),
        roots=[dict(k=k,tree=dict(kind="pending")) for k in range(26)])


def check_checkpoint(task,target,packet):
    expected=initial_checkpoint(task,target)["binding"]
    need(type(packet) is dict and sources.base._same(packet.get("binding"),expected),"Exact current native and PREFIX2 checkpoint binding")
    return sources.geometry(target,Path(task)/"capsule",packet,checkpoint=True)


def extends(before,after):
    """Only pending nodes may be replaced; all earlier work is immutable."""
    if type(before) is not list or type(after) is not list or len(before)!=len(after):return False
    stack=[]
    for a,b in zip(before,after):
        if type(a) is not dict or type(b) is not dict or a.get("k")!=b.get("k"):return False
        stack.append((a.get("tree"),b.get("tree")))
    while stack:
        a,b=stack.pop()
        if type(a) is not dict or type(b) is not dict:return False
        if a.get("kind")=="pending":continue
        if a.get("kind")!=b.get("kind"):return False
        if a.get("kind")=="leaf":
            if not sources.base._same(a,b):return False
        elif a.get("kind")=="split":
            if a.get("axis")!=b.get("axis") or a.get("cut")!=b.get("cut"):return False
            stack.extend(((a.get("left"),b.get("left")),(a.get("right"),b.get("right"))))
        else:return False
    return True


def _sidecar(path):
    marker=transport.ordinary(path.with_suffix(path.suffix+".sha256"),limit=1024)
    need(marker.read_text("ascii")==common.digest(path)+"  "+path.name+"\n","Actual saved artifact hash sidecar")


def save_checkpoint(task,target,packet,directory):
    census=check_checkpoint(task,target,packet)
    raw=sources.encoded(packet);need(len(raw)<=128*MIB,"Bounded128MiB saved count checkpoint")
    directory=Path(directory);sources.base._no_link_ancestors(directory);directory.mkdir(parents=True,exist_ok=True)
    pin=sources.sha(raw);path=directory/(pin+".json")
    if path.exists():
        transport.ordinary(path,limit=128*MIB);need(path.read_bytes()==raw,"Append-only checkpoint bytes")
        marker=path.with_suffix(".json.sha256")
        if not marker.exists():
            # A power loss can occur between the immutable file and marker.
            # Recreate only its exact digest after full source/geometry checks.
            with marker.open("x",encoding="ascii") as stream:stream.write(pin+"  "+path.name+"\n")
        _sidecar(path)
    else:
        pending=directory/(path.name+".pending-"+uuid.uuid4().hex[:8])
        with pending.open("xb") as stream:stream.write(raw)
        pending.replace(path)
        marker=path.with_suffix(".json.sha256")
        with marker.open("x",encoding="ascii") as stream:stream.write(pin+"  "+path.name+"\n")
    return dict(path=str(path),sha256=pin,census=census,arithmetic_accepted=False)


def restore_checkpoint(task,target,directory,*,log_root=None):
    """Unique maximal compatible lineage, never arbitrary newest/largest work."""
    candidates=[];directory=Path(directory)
    if directory.exists():
        transport.ordinary(directory,directory=True)
        for path in sorted(directory.glob("*.json")):
            try:
                transport.ordinary(path,limit=128*MIB);_sidecar(path)
                packet=common.read(path);census=check_checkpoint(task,target,packet)
                if not any(sources.base._same(packet,x[1]) for x in candidates):candidates.append((path,packet,census))
            except Exception as error:
                if log_root:event(log_root,"full66_checkpoint_rejected",target=target,path=str(path),error=type(error).__name__+": "+str(error))
    if not candidates:return initial_checkpoint(task,target),None
    maxima=[row for row in candidates if not any(
        extends(row[1]["roots"],other[1]["roots"]) and not extends(other[1]["roots"],row[1]["roots"])
        for other in candidates)]
    need(len(maxima)==1,"Ambiguous incomparable valid saved count lineages; preserve all work and select no guessed latest")
    row=maxima[0]
    if log_root:event(log_root,"full66_count_checkpoint_restored",target=target,path=str(row[0]),**row[2])
    return row[1],row[0]


def search(task,target,packet,seconds):
    check_task(task,target);before=check_checkpoint(task,target,packet)
    need(type(seconds) is int and 1<=seconds<=7200,"Bounded original discovery slice")
    task=Path(task).resolve();run=task/("search-"+uuid.uuid4().hex[:12]);run.mkdir()
    atomic_json(run/"INPUT_CHECKPOINT.json",packet)
    command=[sys.executable,"-B","-S",str(task/"discovery/count_discovery.py"),
        "--capsule",str(task/"capsule"),"--design-sha256",sources.profile(target)["design_sha256"],
        "--output",str(run/"candidate"),"--seconds",str(seconds),"--resume",str(run/"INPUT_CHECKPOINT.json"),
        "--strategy","RESTORED_PREFIX2_V1","--alpha-priority","16","--order","depth"]
    observed=common.supervise(command,cwd=run,output_dir=run/"execution",mode="untrusted_search",
        cpu_seconds=seconds+120,wall_seconds=seconds+120,memory_bytes=MEMORY,disk_bytes=256*MIB,log_bytes=16*MIB,
        checkpoint_paths=[run/"candidate/CHECKPOINT.json",run/"candidate/CHECKPOINT.backup.json"])
    # Discovery can be stopped. Only validated saved geometry survives; no
    # prefix observation, exit code or old decision is arithmetic acceptance.
    candidates=[]
    for name in ("CHECKPOINT.json","CHECKPOINT.backup.json"):
        path=run/"candidate"/name
        try:
            candidate=common.read(path);census=check_checkpoint(task,target,candidate)
            need(extends(packet["roots"],candidate["roots"]),"Search cannot replace previously retained nodes")
            if not any(sources.base._same(candidate,x[0]) for x in candidates):candidates.append((candidate,census,path))
        except (ValueError,OSError,KeyError,TypeError):continue
    if candidates:
        maxima=[r for r in candidates if all(extends(o[0]["roots"],r[0]["roots"]) for o in candidates)]
        need(len(maxima)==1,"Stopped primary/backup checkpoints have a unique descendant")
        after,census,path=maxima[0]
    else:after,census,path=packet,before,None
    sources.verify(target,task/"capsule");discovery.verify(task/"discovery")
    report=dict(schema="N25_FULL66_UNTRUSTED_DISCOVERY_V1",target=target,observed=observed,
        before_statistics=before,after_statistics=census,checkpoint=str(path) if path else None,
        arithmetic_accepted=False,full66_complete=False)
    atomic_json(run/"SEARCH_EXECUTION.json",report)
    return after,report


def accept(task,target,packet,*,cpu_seconds=CPU,wall_seconds=WALL):
    check_task(task,target);census=check_checkpoint(task,target,packet)
    need(census["pending"]==0,"No incomplete forest can enter native acceptance")
    need(type(cpu_seconds) is int and 2<=cpu_seconds<=CPU and type(wall_seconds) is int and 1<=wall_seconds<=WALL,
         "Explicit at-most23-hour full native action")
    task=Path(task).resolve();run=task/("accept-"+uuid.uuid4().hex[:12]);capsule=run/"capsule"
    shutil.copytree(task/"capsule",capsule)
    index=sources.profile(target)["index"]
    forest=dict(**sources.native_header(target,capsule),roots=deepcopy(packet["roots"]))
    atomic_json(capsule/f"COUNT{index}_FOREST.json",forest)
    census=sources.geometry(target,capsule,forest)
    observed=common.supervise([sys.executable,"-B","-S",str(capsule/"count_protocol.py"),"accept"],
        cwd=capsule,output_dir=run/"execution",mode="trusted_native",cpu_seconds=cpu_seconds,
        wall_seconds=wall_seconds,memory_bytes=MEMORY,disk_bytes=256*MIB,log_bytes=16*MIB,checkpoint_paths=[])
    report=dict(schema=evidence.SCHEMA,target=target,epoch=str(run),scope=evidence.SCOPE,observed=observed,
        census=census,implementation=evidence.implementation(),arithmetic_accepted=False,
        parent_acquisitions_verified=False,full66_complete=False)
    atomic_json(run/"NATIVE_OBSERVED.json",report)
    evidence.validate_run(task,target,run,observed,census)
    receipt=capsule/f"COUNT{index}_ACCEPTED.json"
    report.update(arithmetic_accepted=True,native_receipt=str(receipt),native_receipt_sha256=common.digest(receipt),
        negative_controls=24,conditional_premises=evidence.premises(target))
    atomic_json(run/"NATIVE_ACCEPTED.json",report)
    return run,evidence.validate_stage(task,target,run)


def _members(archive):
    # The existing first-party ZIP preflight is geometry/transport only. It
    # never imports kernels, promotes receipts or chooses this stage's source.
    from .retained_n25_extra import _cache_members
    return _cache_members(archive)


def save_stage(task,target,epoch,directory):
    evidence.validate_stage(task,target,epoch)
    directory=Path(directory);sources.base._no_link_ancestors(directory);directory.mkdir(parents=True,exist_ok=True)
    output=directory/(Path(epoch).name+"-native.zip")
    need(not output.exists(),"Append-only completed count export")
    temporary=output.with_name(output.name+".pending-"+uuid.uuid4().hex[:8])
    with zipfile.ZipFile(temporary,"x",compression=zipfile.ZIP_DEFLATED,strict_timestamps=False) as zipped:
        for path in sorted(Path(epoch).rglob("*")):
            if path.is_file():
                transport.ordinary(path,limit=128*MIB);zipped.write(path,path.relative_to(task).as_posix())
        _members(zipped)
    need(temporary.stat().st_size<=512*MIB,"Bounded complete count-stage export")
    pin=common.digest(temporary);temporary.replace(output)
    with output.with_suffix(".zip.sha256").open("x",encoding="ascii") as stream:stream.write(pin+"  "+output.name+"\n")
    return output


def restore_stage(task,target,directory,*,log_root=None):
    task=Path(task).resolve();directory=Path(directory)
    if not directory.exists():return None
    transport.ordinary(directory,directory=True)
    for path in sorted(directory.glob("accept-*-native.zip")):
        restored=None
        try:
            transport.ordinary(path,limit=512*MIB);_sidecar(path)
            with zipfile.ZipFile(path) as zipped:
                name,rows=_members(zipped);restored=task/name
                need(not restored.exists(),"No overwrite while restoring completed count evidence")
                restored.mkdir()
                for row in rows:
                    output=task/Path(*row.filename.split("/"));output.parent.mkdir(parents=True,exist_ok=True)
                    with zipped.open(row) as src,output.open("xb") as dst:shutil.copyfileobj(src,dst,MIB)
            result=evidence.validate_stage(task,target,restored)
            if log_root:event(log_root,"full66_completed_count_revalidated",target=target,cache=str(path),leaves=result["census"]["leaves"])
            return restored,result
        except Exception as error:
            if log_root:event(log_root,"full66_completed_count_cache_rejected",target=target,cache=str(path),error=type(error).__name__+": "+str(error))
    return None


def run_target(task,target,durable,*,deadline,log_root=None,slice_seconds=1800):
    """Recovered originals replay directly; explicitly prepared legacy tasks retain search."""
    if (Path(task)/"RECOVERY_INPUTS.json").exists():
        # Never fall back to discovery after a recovered-source validation error.
        need(not (Path(task)/"TASK.json").exists(), "No mixed original/reconstructed task identities")
        from . import n25_recovered_counts as recovered
        return recovered.run_target(task,target,durable,deadline=deadline,log_root=log_root)
    check_task(task,target);durable=Path(durable)
    cache=durable/target/sources.PLAN_SHA256[:16]
    completed=restore_stage(task,target,cache/"completed",log_root=log_root)
    if completed:return dict(state="complete_conditional_arithmetic",result=completed[1],native_rerun=False)
    packet,_=restore_checkpoint(task,target,cache/"checkpoints",log_root=log_root)
    while check_checkpoint(task,target,packet)["pending"]:
        remaining=int(deadline-time.monotonic())
        if remaining<125:
            saved=save_checkpoint(task,target,packet,cache/"checkpoints")
            return dict(state="incomplete_checkpoint_preserved",checkpoint=saved,arithmetic_accepted=False,full66_complete=False)
        seconds=min(slice_seconds,7200,remaining-120)
        previous=deepcopy(packet);packet,report=search(task,target,packet,seconds)
        saved=save_checkpoint(task,target,packet,cache/"checkpoints")
        if log_root:event(log_root,"full66_count_search_slice_stopped",target=target,**saved["census"])
        if sources.base._same(previous,packet):
            return dict(state="incomplete_no_search_progress",checkpoint=saved,execution=report,
                        arithmetic_accepted=False,full66_complete=False)
    remaining=int(deadline-time.monotonic())
    if remaining<2:
        saved=save_checkpoint(task,target,packet,cache/"checkpoints")
        return dict(state="incomplete_native_replay_pending",checkpoint=saved,arithmetic_accepted=False,full66_complete=False)
    run,result=accept(task,target,packet,cpu_seconds=min(CPU,remaining),wall_seconds=min(WALL,remaining))
    output=save_stage(task,target,run,cache/"completed")
    if log_root:event(log_root,"full66_ordinary_count_complete",target=target,leaves=result["census"]["leaves"],cache=str(output))
    return dict(state="complete_conditional_arithmetic",result=result,native_rerun=True)
