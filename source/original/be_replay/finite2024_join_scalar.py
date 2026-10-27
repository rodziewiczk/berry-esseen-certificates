"""Exact original native CE lower target; no rounded substitute."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import ast,hashlib
ORIGINAL_SHA256='363fc0071bbc324449c9bc0490a861c20eb0e0ee2af684cbef52509266b6cd7f'

def exact_native_target():
    scale = 10**30
    def root_low(x):
        return F(isqrt(x.numerator * scale * scale // x.denominator), scale)
    def atan(q, m):
        lo = sum((F((-1)**k, (2*k+1)*q**(2*k+1)) for k in range(2*m)), F(0))
        return lo, lo + F(1, (4*m+1)*q**(4*m+1))
    _, a5hi = atan(5, 24)
    a239lo, _ = atan(239, 8)
    pi_hi = 16*a5hi - 4*a239lo
    return (3+root_low(F(10))) * root_low(1/(2*pi_hi)) / 6


def verify_projection():
 root=Path(__file__).resolve().parents[1];p=root/'proof/provenance/58H/geometry_audit_v2.py'
 if hashlib.sha256(p.read_bytes()).hexdigest()!=ORIGINAL_SHA256:raise ValueError('Original complete native geometry source pin')
 old=next(n for n in ast.parse(p.read_bytes()).body if isinstance(n,ast.FunctionDef)and n.name=='exact_native_target')
 own=next(n for n in ast.parse(Path(__file__).read_bytes()).body if isinstance(n,ast.FunctionDef)and n.name=='exact_native_target')
 if ast.dump(old,include_attributes=False)!=ast.dump(own,include_attributes=False):raise ValueError('Entire original exact-target arithmetic projection')
 return ORIGINAL_SHA256
