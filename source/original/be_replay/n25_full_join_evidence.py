"""Recompute the complete conditional n25 cover from current admitted exports.

Every COUNT is licensed by all simultaneous physical fields, then selected by
an exact finite closed-interval path. Historical regional PASS files are not
inputs to this implication. No original numerical kernel is imported here.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import re
from . import n25_full_join_sources as s, n25_full_join_semantics as m
from . import n25_full_join_graph as g, n25_full_join_runtime as runtime

REGIONS = (
    ('lower-b0', 'parent:b0'), ('lower-b1', 'parent:b1'), ('lower-b2', 'parent:b2'),
    ('lower-b3', 'seven:n25-parents-b3'), ('lower-b4', 'seven:n25-parents-b4'),
    ('lower-b5', 'parent:b5'), ('middle-0', 'family:middle-negative'),
    ('middle-1', 'family:middle-b0'), ('middle-2', 'family:middle-b1'),
    ('middle-3', 'family:middle-b2'), ('middle-4', 'family:middle-b3'),
    ('middle-5', 'middle:b4'), ('middle-6', 'middle:b5'),
    ('high-0', 'family:high-negative'), ('high-1', 'family:high-quarter2'),
    ('high-2', 'family:high-beta0'), ('high-3', 'family:high-beta1'),
    ('high-4', 'family:high-beta2'), ('high-5', 'high:beta3'),
)


def seven_frame(task, key, checked):
    """Logical original interface IDs; new V14 bytes are always the fresh bytes."""
    from . import count_task as c
    index = c.TARGETS[key][1]
    if key.startswith('b4-'):
        directory = 'global_alpha_stoploss2_b4_p29_'+key[3:]+'_v12'
    elif key.endswith('v14-new'):
        directory = 'global_local_contact_b3_p'+str(index)+'_v14'
    else:
        directory = 'global_alpha_stoploss2_b3_p33_v12'
    capsule = s.path(task, checked['accepted_capsule_relative'])
    return dict(job_id=key, member='cutoff25_20261011/new_root/'+directory,
                task=Path(task), capsule=capsule, validated=checked,
                contract=capsule/'contract.json', forest=capsule/f'COUNT{index}_FOREST.json',
                native=s.path(task, checked['native_receipt_relative']))


def proof_record(owner, base, stage):
    s.need(stage.get('receipt') and stage.get('proof'), 'An accepted full original action, not construction alone')
    proof = s.path(base, stage['folder']+'/'+stage['proof'])
    receipt = s.path(base, stage['folder']+'/'+stage['receipt'])
    s.need(proof.is_file() and receipt.is_file(), 'Actual complete current proof and acceptance bytes')
    kind = stage['kind']; index = stage.get('index')
    if kind == 'local' and index is None:
        match = re.fullmatch(r'local-(\d+)-accept', stage.get('id', stage.get('name', '')))
        s.need(match is not None, 'Literal original accepted local probability panel')
        index = int(match.group(1))
    return dict(owner=owner, kind=kind, index=index, path=proof, receipt=receipt,
                proof=s.read(proof), proof_sha256=s.digest(proof),
                evidence_sha256=s.digest(receipt))


def acquired_graph(admitted, *, p34_task):
    """Only explicit outputs of the constituent full readers enter the pool."""
    from . import n25_collect as seven, n25_parents
    from . import n25_full_acquisition_sources as forty
    from . import n25_b3_p34 as p34
    graph = g.ProofGraph(); proofs = []
    for key, entry in admitted.items():
        value = entry['value']
        if key.startswith(('counts:', 'extra:')) or key in ('upper10', 'recovered11'):
            for frame in value:
                graph.add_count(frame)
        elif key.startswith('seven:') and key[6:] in seven.COUNTS:
            graph.add_count(seven_frame(entry['root'], key[6:], value))
        elif key.startswith('seven:n25-parents-'):
            names = n25_parents.names(key[-2:])
            base = s.path(entry['root'], value['resource_capsule_relative'])
            for kind in ('initial', 'resource'):
                stage = dict(kind='initial' if kind == 'initial' else 'global_resource',
                             folder=names[kind+'_dir'], proof=names[kind+'_proof'],
                             receipt=names[kind+'_receipt'])
                proofs.append(proof_record(key, base, stage))
        elif key.startswith(('parent:', 'middle:', 'high:')):
            for row in value['proofs']:
                if row['stage'].get('receipt'):
                    proofs.append(proof_record(key, value['base'], row['stage']))
        elif key == 'acquisitions40':
            for family, packet in value.items():
                for stage in forty.definition(family)['actions']:
                    if stage.get('receipt'):
                        proofs.append(proof_record('family:'+family, packet['base'], stage))
    graph.add_count(p34.frame(p34_task))
    s.need(len(graph.counts) == 219, 'All219 distinct complete ordinary COUNT inputs, including original B3p34')
    return graph, proofs


def interval_path(edges, whole):
    """A deterministic exact DAG path; never clip or merge a native interval."""
    start, end = map(F, whole)
    s.need(start < end, 'A nonempty closed physical interval')
    outgoing = {}
    for edge in edges:
        left, right = map(F, edge['p'])
        s.need(start <= left < right <= end, 'Entire native closed interval lies inside this whole panel')
        outgoing.setdefault(left, []).append((right, edge))
    reached = {start: []}
    for left in sorted(outgoing):
        if left not in reached:
            continue
        for right, edge in sorted(outgoing[left], key=lambda item: (
                item[0], item[1]['source_capsule'], item[1]['native_evidence_sha256'])):
            candidate = reached[left]+[edge]
            if right not in reached or len(candidate) < len(reached[right]):
                reached[right] = candidate
    result = reached.get(end)
    if result is not None:
        m.closed_partition([r['p'] for r in result], whole)
    return result


def count_cover(graph, resource, *, rho, index, invariants, resource_sha256):
    edges = []
    for name, actual in sorted(graph.counts.items()):
        cfg = actual['cfg']
        if cfg['index'] != index or F(cfg['rho_lower']) != F(rho[0]):
            continue
        try:
            edge = m.resource_interface(resource, cfg, rho=rho, index=index, invariants=invariants)
        except ValueError:
            continue
        edge.update(source_capsule=name, native_evidence_sha256=actual['evidence_sha256'],
                    contract_sha256=s.digest(actual['contract']), forest_sha256=s.digest(actual['forest']),
                    current_resource_proof_sha256=resource_sha256,
                    leaves=actual['receipt']['statistics']['leaves'])
        edges.append(edge)
    return interval_path(edges, [str(F(index,100)), str(F(index+1,100))])


def supplemental_resource(proof, *, incoming_initial):
    expected = dict(n=25, K='0', Q='5/16', band=3, index=30,
                    p=['3/10','31/100'], rho=['13/10','7/5'],
                    radius_minus='83/40', radius_plus='121/40', ambient_floor='23/10',
                    retained_iterations=64, supplemental_steps=2)
    s.need(proof['schema'] == 'SUPPLEMENTAL_N25_B3_P30_FIXED_TWO_STEP_V1'
           and m.same(proof['profile'], expected), 'Literal whole supplemental profile, distinct from INITIAL profile')
    inv = incoming_initial['profile']['invariants']
    s.need(F(inv['rho_lo']) == F(13,10) and F(inv['rho']) == F(7,5),
           'Supplemental calculations preserve this exact incoming lower-B3 witness')
    return dict(excluded=False, result=proof['terminal_resource'],
                raw_row=proof['terminal_raw'], initial=proof['initial_row'])


def region(identity, owner, proofs, graph, *, predecessor_allowance, supplement=None, mixed=None):
    if identity.startswith('lower-'):
        ordinal = int(identity[-1]); rho = list(m.LOWER[ordinal:ordinal+2]); beta = None
    elif identity.startswith('middle-'):
        ordinal = int(identity.split('-')[1]); rho = ['33/20','7/4']; beta = list(m.MIDDLE[ordinal:ordinal+2])
    else:
        ordinal = int(identity.split('-')[1]); rho = ['7/4',m.TAIL]; beta = list(m.HIGH[ordinal:ordinal+2])
    owned = [p for p in proofs if p['owner'] == owner]
    initials = [p for p in owned if p['kind'] == 'initial']
    s.need(len(initials) == 1, 'One explicit complete INITIAL acquisition for '+identity)
    initial = initials[0]['proof']
    license = m.initial_license(initial, rho=rho, beta=beta, lower=identity.startswith('lower-'),
                                predecessor_allowance=predecessor_allowance)
    if identity in ('middle-0','middle-1','high-0'):
        return g.empty_initial_region(identity, rho, beta, initial, proof_pin=initials[0]['evidence_sha256'])
    feedback = [p for p in owned if p['kind'] == 'mixed_feedback']
    if feedback:
        s.need(identity == 'high-3' and len(feedback) == 1, 'One original whole high-beta1 feedback theorem')
        return g.full_feedback_region(identity, rho, beta, feedback[0]['proof'],
                                      proof_pin=feedback[0]['evidence_sha256'], incoming_initial=initial)
    resources = [p for p in owned if p['kind'] == 'global_resource']
    s.need(len(resources) == 1, 'One explicit accepted global resource acquisition for '+identity)
    parent = resources[0]
    rows = g.resource_panels(parent['proof'], rho=rho, profile=initial['profile']); outcomes = []
    locals_ = [p for p in owned if p['kind'] in ('local','local_all100')]
    for index, global_row in enumerate(rows):
        out = dict(index=index, p=[str(F(index,100)),str(F(index+1,100))],
                   evidence_sha256=parent['evidence_sha256'])
        if global_row['result']['excluded'] is True:
            out['method'] = 'current_full_resource_exclusion'; outcomes.append(out); continue
        options = [(global_row['result'], initial['profile'], parent)]
        closed = None
        for local in locals_:
            if local['kind'] == 'local' and local['index'] != index:
                continue
            proof = local['proof']
            s.need(m.same(proof['profile'], initial['profile']), 'Whole same-witness INITIAL profile for each local route')
            resource, profile = g.surviving_resource(global_row['result'], proof)
            if resource is None:
                closed = dict(out, method='current_full_local_exclusion', evidence_sha256=local['evidence_sha256'])
                break
            options.append((resource, profile, local))
        if closed is not None:
            outcomes.append(closed); continue
        if identity == 'lower-b3' and index == 30 and supplement is not None:
            resource = supplemental_resource(supplement['proof'], incoming_initial=initial)
            options.append((resource, initial['profile'], supplement))
        if identity == 'lower-b5' and index in (24,25):
            s.need(mixed is not None and str(index) in mixed['mixed_panels'], 'Full actual mixed p24/p25 execution is required')
            packet = mixed['mixed_panels'][str(index)]
            s.need(packet['index'] == index and packet['same_original_cfg_current_resource_interface'] is True,
                   'Every original mixed premise has an actual current same-law interface')
            out.update(method='current_full_mixed_E' if index == 24 else 'current_full_mixed_ABCDF',
                       mixed=packet, evidence_sha256=packet['evidence_sha256'])
            outcomes.append(out); continue
        for resource, profile, origin in options:
            edges = count_cover(graph, resource, rho=rho, index=index,
                                invariants=profile.get('invariants'), resource_sha256=origin['proof_sha256'])
            if edges is not None:
                closed = dict(out, method='current_full_native_counts', count_interfaces=edges,
                              evidence_sha256=origin['evidence_sha256'])
                break
        s.need(closed is not None, 'No full admitted exact COUNT cover for '+identity+' panel '+str(index))
        outcomes.append(closed)
    return dict(id=identity, n=25, K='0', rho=rho, beta=beta, outcomes=outcomes,
                profile_license=license, full_global_proof_sha256=parent['proof_sha256'],
                all_100_p_intervals_closed=True)


def conjunction(root, records, *, p34_task, supplement_task, mixed_task):
    from . import n25_full_join_supplement as supplement, n25_mixed_runner as mixed
    admitted = runtime.readback(root, records)
    predecessor = admitted['predecessor58H']['value']
    s.need(predecessor['conditional_finite_chain_verified'] is True,
           'The complete independently acquired current finite20--24 chain')
    predecessor_edge = dict(n=24, target='CE', derived_q25='0',
                            conditional_finite_chain_verified=True,
                            current_full_session_sha256=predecessor['session_result_sha256'],
                            retained_analytic_premises=predecessor['summary']['analytic_premises'])
    graph, proofs = acquired_graph(admitted, p34_task=p34_task)
    supplement_checked = supplement.validate_completed(supplement_task)
    original_parent = supplement.parent.validate_completed(Path(supplement_task)/'parent', expected_branch='b3')
    s.need(m.same(original_parent, admitted['seven:n25-parents-b3']['value']),
           'Supplement uses this exact complete B3 parent, not another epoch')
    sp = Path(supplement_task)/'capsule'/supplement.DIRECTORY/supplement.OUTPUTS[0]
    supplemental = dict(proof=s.read(sp), proof_sha256=s.digest(sp),
                        evidence_sha256=supplement_checked['output_sha256'])
    mixed_checked = mixed.validate_completed(mixed_task)
    mixed_parent = mixed.parent.validate_completed(Path(mixed_task)/'parent')
    s.need(m.same(mixed_parent, admitted['parent:b5']['value']['validated']),
           'Both full mixed acceptances use this exact complete current B5 parent')
    regions = [region(identity, owner, proofs, graph, predecessor_allowance='0',
                      supplement=supplemental, mixed=mixed_checked) for identity, owner in REGIONS]
    result = m.global_union(regions, predecessor=predecessor_edge)
    return dict(schema='FULL66_CURRENT_COMPLETE_CONDITIONAL_ARITHMETIC_V1',
                union=result, regions=regions, ordinary_forests=219,
                ordinary_leaves=sum(r['receipt']['statistics']['leaves'] for r in graph.counts.values()),
                current_files=graph.inventory(), supplemental=supplement_checked,
                mixed=mixed_checked, physical_pieces=20,
                conditional_n25_chain_completed=True, all_index_conclusion_verified=False,
                global_proof_accepted=False, full_n25_verified=False,
                universal_analytic_inputs_acquired=False)
