"""Portable execution of the original complete selected COUNT checkers.

Numerical conclusions remain conditional on the exact same-law contract.
No historical authority key, receipt, cloud observation or saved PASS is used.
These live numerical witnesses are inputs to the forthcoming full proof binder;
an individual COUNT replay is never the all-law or all-index theorem.
"""
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import argparse
import json
import os
import signal
import subprocess
import sys
import time

from capsule_worker import encoded, need, ordinary, parsed, runtime_projection

HERE = Path(__file__).resolve().parent
PACK = HERE / 'count-pack-v2'
MANIFEST_SHA256 = 'f5ddd40aefe85b5ce036b2c23fe540c2032997bf8a51f4999a08573e9a4c34f7'
MIB = 1024 ** 2
_LIVE = []


def digest(raw):
 return sha256(raw).hexdigest()


def manifest():
 raw = ordinary(PACK / 'MANIFEST.json', limit=16 * MIB)
 need(digest(raw) == MANIFEST_SHA256, 'The complete reviewed selected COUNT source registry')
 value = parsed(raw)
 need(value['schema'] == 'be.public-selected-count-sources/2'
      and len(value['jobs']) == 1243 and value['all_index_full_pass'] is False,
      'Exact complete selected numerical task universe')
 return value


def definition(job_id):
 jobs = manifest()['jobs']
 need(job_id in jobs, 'Unknown selected COUNT obligation')
 return jobs[job_id]


def sources(row):
 bodies = {}
 for name, pin in row['source'].items():
  need(Path(name).name == name and not any(c in name for c in ('/', '\\', ':')), 'Closed flat native source member')
  raw = ordinary(PACK / 'blobs' / pin['sha256'], limit=MIB)
  need(len(raw) == pin['bytes'] and digest(raw) == pin['sha256'], 'Entire original native body: ' + name)
  bodies[name] = raw
 return bodies


def install(row, folder):
 need(not folder.exists(), 'A fresh native execution directory is required')
 bodies = sources(row)
 folder.mkdir(parents=True)
 for name, raw in bodies.items():
  with (folder / name).open('xb') as stream:
   stream.write(raw)
 return bodies


def unchanged(folder, bodies):
 for name, expected in bodies.items():
  need(ordinary(folder / name, limit=MIB) == expected, 'Original mathematical source changed during replay: ' + name)


def native(folder, script, arguments, timeout, log_name):
 need(type(timeout) is int and 1 <= timeout <= 54000, 'Finite explicit native wall limit')
 need(script in {p.name for p in folder.iterdir()}, 'Reviewed installed native entry point')
 command = [sys.executable, '-E', '-B', '-S', str((folder / script).resolve()), *arguments]
 started = time.monotonic()
 log = folder / log_name
 need(not log.exists(), 'Native execution logs cannot preexist')
 with log.open('xb') as stream:
  child = subprocess.Popen(command, cwd=folder, stdin=subprocess.DEVNULL,
                           stdout=stream, stderr=subprocess.STDOUT,
                           start_new_session=(os.name == 'posix'))
  try:
   while child.poll() is None:
    need(time.monotonic() - started < timeout, 'Native wall limit exceeded; no acceptance')
    need(log.stat().st_size <= 16 * MIB, 'Native log bound exceeded; no acceptance')
    time.sleep(0.05)
  except BaseException:
   if os.name == 'posix':
    try:
     os.killpg(child.pid, signal.SIGKILL)
    except ProcessLookupError:
     pass
   else:
    child.kill()
   child.wait()
   raise
 raw = ordinary(log, limit=16 * MIB)
 need(child.returncode == 0,
      'Original complete native checker rejected or did not finish: ' + raw[-3000:].decode('utf-8', 'replace'))
 return {'returncode': child.returncode, 'seconds': time.monotonic() - started,
         'log_sha256': digest(raw), 'native_script': script, 'native_arguments': arguments,
         'new_process': True, 'historical_receipt_reused': False}


@dataclass(frozen=True, repr=False)
class FreshCountReplay:
 canonical_bytes: bytes

 def metadata(self):
  need(any(self is item for item in _LIVE), 'A live result of actual full numerical replay is required')
  value = parsed(self.canonical_bytes)
  need(encoded(value) == self.canonical_bytes and value['all_index_full_pass'] is False,
       'Numerical witness only; no reconstructed accepted theorem')
  return value


def checked_receipt(row, candidate, raw):
 result = parsed(raw)
 need(type(result) is dict, 'Whole original checker result')
 for key, expected in row['receipt_invariants'].items():
  need(key in result and type(result[key]) is type(expected) and result[key] == expected,
       'Exact original numerical statement: ' + key)
 digest_field = 'forest_sha256' if 'forest_sha256' in result else 'candidate_sha256'
 need(result.get(digest_field) == digest(candidate), 'Original checker actually consumed this whole candidate')
 need(result.get('contract_sha256') == row['source']['contract.json']['sha256'], 'Exact original conditional contract')
 if 'checker_sha256' in result:
  need(result['checker_sha256'] == row['source'][row['script']]['sha256'], 'Exact actual native checker')
 for field in ('kernel_sha256', 'source_sha256'):
  if field in result:
   need(type(result[field]) is dict and result[field], 'Complete actual numerical source binding')
   for name, expected in result[field].items():
    need(name in row['source'] and row['source'][name]['sha256'] == expected,
         'Every native mathematical dependency bound to its unchanged whole body')
 expected = row['expected_negative_controls']
 controls = result.get('negative_controls')
 if expected is None:
  need(type(controls) is list and len(controls) == len(set(controls)) == 24
       and all(type(item) is str for item in controls), 'All 24 original recovered-task controls')
 else:
  need(type(controls) is type(expected) and controls == expected, 'All original native corruption controls')
 if 'statistics' in result:
  stats = result['statistics']
  need(type(stats) is dict and type(stats.get('leaves')) is int and stats['leaves'] > 0
       and type(result.get('fresh_leaf_evaluations')) is int
       and result['fresh_leaf_evaluations'] == stats['leaves'], 'Every complete original leaf freshly evaluated')
  header = parsed(candidate)
  need(Fraction(stats['maximum_score']) < Fraction(header['target']), 'Strict full numerical score bound')
 else:
  need(type(result.get('all_closed_leaves')) is int and result['all_closed_leaves'] > 0
       and result['passed_cells'] + result['empty_cells'] == result['all_closed_leaves'], 'Complete strict COUNT leaf census')
  need(Fraction(result['maximum_score']) < Fraction(result['target_lower']), 'Strict original target')
 return result


def execute(job_id, directory, *, candidate=None, construct=False, timeout=1800):
 need(sys.dont_write_bytecode and not sys.flags.optimize and __debug__, 'Unoptimized Python -B mathematical replay')
 need(type(construct) is bool and (construct != (candidate is not None)), 'Choose a full witness or fresh construction')
 row = definition(job_id)
 directory = Path(directory).absolute()
 for parent in (directory, *directory.parents):
  need(not parent.is_symlink() and not parent.is_junction(), 'Ordinary create-only numerical execution paths')
 own = ordinary(__file__, limit=MIB)
 if construct:
  constructor = row['constructor']['script']
  need(constructor in row['source'], 'This original constructor must be projected before fresh generation')
  arguments = row['constructor']['arguments']
  original = None
 else:
  original = ordinary(candidate, limit=64 * MIB)
 bodies = install(row, directory)
 produced = None
 candidate_file = directory / row['candidate']
 need(not candidate_file.exists() and not (directory / row['receipt']).exists(), 'No historical mathematical outputs staged')
 if construct:
  produced = native(directory, constructor, arguments, timeout, 'fresh-construct.log')
  unchanged(directory, bodies)
  original = ordinary(candidate_file, limit=64 * MIB)
 else:
  with candidate_file.open('xb') as stream:
   stream.write(original)
 actual = native(directory, row['script'], row['arguments'], timeout, 'fresh-verify.log')
 unchanged(directory, bodies)
 receipt_raw = ordinary(directory / row['receipt'], limit=64 * MIB)
 result = checked_receipt(row, original, receipt_raw)
 need(ordinary(candidate_file, limit=64 * MIB) == original and ordinary(__file__, limit=MIB) == own,
      'Whole replay adapter and witness immutable throughout original arithmetic verification')
 if candidate is not None:
  need(ordinary(candidate, limit=64 * MIB) == original, 'Original input witness unchanged')
 value = {'schema': 'be.public-fresh-complete-count-witness/1', 'job_id': job_id, 'role': row['role'],
          'n': row['n'], 'index': row['index'], 'registry_sha256': MANIFEST_SHA256,
          'source': row['source'], 'candidate_sha256': digest(original), 'candidate_bytes': len(original),
          'whole_original_checker_result': result, 'whole_original_receipt_sha256': digest(receipt_raw),
          'actual_construct': produced, 'actual_replay': actual, 'runtime': runtime_projection(),
          'adapter_sha256': digest(own), 'fresh_arithmetic_checker_executed': True,
          'conditional_on_exact_same_law_resource_acquisition': True,
          'historical_authority_key_or_receipt_used': False, 'all_law_theorem_issued': False,
          'all_index_full_pass': False}
 answer = FreshCountReplay(encoded(value))
 _LIVE.append(answer)
 answer.metadata()
 with (directory / 'FRESH-PUBLIC-COUNT-REPLAY.json').open('xb') as stream:
  stream.write(answer.canonical_bytes)
 return answer


def main():
 parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
 parser.add_argument('action', choices=('verify', 'run'))
 parser.add_argument('job_id')
 parser.add_argument('--directory', type=Path, required=True)
 parser.add_argument('--candidate', type=Path)
 parser.add_argument('--timeout', type=int, default=1800)
 args = parser.parse_args()
 value = execute(args.job_id, args.directory, candidate=args.candidate,
                 construct=args.action == 'run', timeout=args.timeout)
 print(encoded({'job_id': args.job_id, 'actual_native_replay': True,
                'observation_sha256': digest(value.canonical_bytes),
                'conditional_numerical_witness_only': True, 'all_index_full_pass': False}).decode('ascii'))


if __name__ == '__main__':
 main()
