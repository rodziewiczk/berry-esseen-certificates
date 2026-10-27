"""Unchanged full trusted-native evidence predicates bound to the new one-job provider.

The factory creates private function-global namespaces. It does not mutate the
published extra-count modules, their 17-job selection, source pins or caches.
Every reused function retains its original code object and complete guard checks.
"""
from pathlib import Path
import sys
from types import FunctionType

from . import count_task as common, retained_n25_extra_evidence as template
from . import n25_b3_p34_sources as sources

SCHEMA = 'FULL66_B3P34_NATIVE_EXECUTION_V1'
SCOPE = 'FRESH_FULL66_B3P34_CONDITIONAL_COUNT_ONLY'


def implementation():
    root = Path(__file__).resolve().parent
    names = ('n25_b3_p34.py', 'n25_b3_p34_sources.py', 'n25_b3_p34_evidence.py',
             'retained_n25_extra.py', 'retained_n25_extra_sources.py',
             'retained_n25_extra_evidence.py', 'retained_n25_sources.py',
             'n25_full_join_sources.py', 'count_task.py', 'linux_supervisor.py',
             'count_recovery_evidence.py', 'n25_count_evidence.py')
    return dict(files_sha256={n: common.digest(root / n) for n in names},
                catalog_sha256=sources.CATALOG_SHA256, python=sys.version,
                template_function_code_unchanged=True,
                existing_module_globals_mutated=False)


def bound_namespace():
    """Bind every local validator together; imported guard helpers stay original."""
    namespace = dict(vars(template))
    namespace.update(sources=sources, SCHEMA=SCHEMA, SCOPE=SCOPE,
                     implementation=implementation, __file__=__file__)
    for name, value in vars(template).items():
        if (isinstance(value, FunctionType) and value.__module__ == template.__name__
                and name != 'implementation'):
            function = FunctionType(value.__code__, namespace, value.__name__,
                                    value.__defaults__, value.__closure__)
            function.__kwdefaults__ = value.__kwdefaults__
            namespace[name] = function
    return namespace


_BOUND = bound_namespace()
validate_run = _BOUND['validate_run']
validate_stage = _BOUND['validate_stage']
premises = _BOUND['premises']
MEMORY = template.MEMORY
