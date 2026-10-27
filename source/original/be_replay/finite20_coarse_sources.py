"""Source sealing for the internal five-call coarse actual20 component of58H.

This module never imports the original numerical programs. It is not a
standalone notebook or a completed actual20 acquisition.
"""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import time
import urllib.request
import zipfile
from . import finite1039_sources as base

ROOT,MIB=base.ROOT,base.MIB
need,digest,read,ordinary,parts=base.need,base.digest,base.read,base.ordinary,base.parts
PLAN=ROOT/'proof/finite20_coarse_source_plan.json'
PLAN_SHA256='934af5d6ca26b0a0552bfe19ee26b80cd9abb57c9ce74cae26a71b8ac77ce9d8'
NATIVE='work/cutoff20_20261016/finite/sharp20_banded_initial_v1'
AUDIT='work/cutoff20_20261016/analytic/sharp20_initial_replay_v1'
RUNS='runs/cutoff20_20261016/finite'
ACTIONS=('b0_construct','b1_construct','prepare','b0_replay','b1_replay')
SCHEMA='SEALED_FINITE20_COARSE_INITIAL_CURRENT_CAPTURE_V1'


def dump(obj):return(json.dumps(obj,sort_keys=True,indent=2)+'\n').encode('utf-8')


def plan():
    need(digest(PLAN)==PLAN_SHA256,'Externally pinned coarse actual20 source plan');d=read(PLAN)
    need(d['schema']=='FINITE20_COARSE_INITIAL_SOURCE_PLAN_V1'and d['native']==NATIVE and d['audit']==AUDIT
         and len(d['source_files'])==29 and len(d['source_graph'])==26 and set(d['cases'])=={'B0','B1'}
         and d['actions']==list(ACTIONS)and all(d[k]is False for k in('arithmetic_computed',
             'full_notebook58H_completed','actual20_sharp_verified','all_index_conclusion_verified')),
         'Complete unchanged29-input source closure, without a full58H claim')
    return d


def obtain_assets(directory, *,progress=lambda *a,**k:None):
    directory=ordinary(directory);directory.mkdir(parents=True,exist_ok=True);out={}
    for row in plan()['assets']:
        name=row['name'];need(tuple(parts(name))==(name,),'Pinned archive basename');p=ordinary(directory/name)
        if not p.exists():
            pending=ordinary(p.with_suffix('.zip.pending'));size=0;last=time.monotonic();at=0
            progress('finite20_coarse_download_started',archive=name,total_bytes=row['bytes'])
            with urllib.request.urlopen(row['url'])as source,pending.open('wb')as target:
                while block:=source.read(MIB):
                    size+=len(block);need(size<=row['bytes'],'Bounded full archive download');target.write(block)
                    if size-at>=16*MIB or time.monotonic()-last>=5:
                        progress('finite20_coarse_download',archive=name,bytes=size,total_bytes=row['bytes']);last=time.monotonic();at=size
            need(size==row['bytes']and digest(pending)==row['sha256'],'Full original archive identity');pending.replace(p)
        need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Exact immutable source transport')
        out[name]=p.resolve()
    return out


def prepare_cache(assets,output, *,progress=lambda *a,**k:None):
    d=plan();output=ordinary(output);output.mkdir(parents=True,exist_ok=True);opened={}
    try:
        for row in d['assets']:
            p=ordinary(assets[row['name']]);need(p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Full source archive pin')
            z=zipfile.ZipFile(p);base.zip_index(z);opened[row['name']]=z
        for i,(name,row)in enumerate(d['source_files'].items()):
            p=ordinary(output.joinpath(*parts(name)))
            if not p.exists():
                z=opened[row['archive']];info=z.getinfo(row['member']);need(info.file_size==row['bytes'],'Original selected source length')
                p.parent.mkdir(parents=True,exist_ok=True)
                with z.open(info)as source,p.open('xb')as target:shutil.copyfileobj(source,target,MIB)
            need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Every unchanged original source byte')
            if i%10==0:progress('finite20_coarse_source_cache',files=i,total=29,arithmetic_computed=False)
        base.verify_cache(output,d['source_files'])
    finally:
        for z in opened.values():z.close()
    return output.resolve()


def capture_directory(band):
    need(band in('B0','B1'),'Literal original band');return RUNS+'/sharp20_'+band.lower()+'_initial01'


def capture_paths(band):
    return [capture_directory(band)+'/'+n for n in('metadata.json','stdout.txt','stderr.txt','CAPTURE_BRIDGE.json')]


def output_paths(action):
    need(action in ACTIONS,'One original coarse action')
    if action.endswith('_construct'):return [NATIVE+'/'+action[:2].upper()+'_RESULT.json']
    if action=='prepare':return [AUDIT+'/PREPARED.json']+[AUDIT+'/engine/'+n for n in plan()['copied_modules']]
    return [AUDIT+'/'+action[:2].upper()+'_REPLAY_CHECKED.json']


def allowed_outputs():
    return {p for a in ACTIONS for p in output_paths(a)}|{p for b in('B0','B1')for p in capture_paths(b)}


def prepare(cache,task):
    d=plan();task=ordinary(task);need(not task.exists(),'Exclusive fresh coarse component');task.mkdir(parents=True)
    for name,row in d['source_files'].items():
        p=ordinary(Path(cache)/name);need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Pinned original source')
        out=task/'capsule'/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,out)
    packet=dict(schema=SCHEMA,source_plan_sha256=PLAN_SHA256,source_adapter_sha256=digest(__file__),
        original_task_root=str(task.resolve()),sources={n:r['sha256']for n,r in d['source_files'].items()},
        arithmetic_computed=False,full_notebook58H_completed=False,actual20_sharp_verified=False,all_index_conclusion_verified=False)
    (task/'SOURCES.json').write_bytes(dump(packet));verify_job(task);return packet


def verify_job(task):
    task=ordinary(task);d=plan();packet=read(task/'SOURCES.json');c=task/'capsule'
    need(packet['schema']==SCHEMA and packet['source_plan_sha256']==PLAN_SHA256
         and packet['source_adapter_sha256']==digest(__file__)
         and packet['sources']=={n:r['sha256']for n,r in d['source_files'].items()}
         and all(packet[k]is False for k in('arithmetic_computed','full_notebook58H_completed',
             'actual20_sharp_verified','all_index_conclusion_verified')),'Exact source epoch and explicitly conditional scope')
    found=set()
    for p in c.rglob('*'):
        ordinary(p)
        if p.is_file():found.add(p.relative_to(c).as_posix())
    need(set(packet['sources'])<=found<=set(packet['sources'])|allowed_outputs(),'Sealed static sources and only declared current outputs')
    for name,pin in packet['sources'].items():need(digest(c/name)==pin,'No changed mathematical/source byte')
    for name in d['copied_modules']:
        p=c/AUDIT/'engine'/name
        if p.exists():need(digest(p)==d['source_graph'][NATIVE+'/'+name],'Original preparation copied byte-identical math helper')
    return packet
