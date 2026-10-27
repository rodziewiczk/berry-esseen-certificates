"""Experimental, stdlib-only exact checker for a general-law C1 <= 2/5 dual.

No existing campaign theorem or accepted external premise is changed by this file.
The producer's floating arithmetic is not used here.
"""
from fractions import Fraction as F
from math import comb, factorial, isqrt
import json

BOUND = F(2, 5)
SCHEMA = 'be.n1-dual-certificate/1'

def rational(value):
    if type(value) is not str or len(value)>128:
        raise ValueError('rational must be a string')
    x = F(value)
    if str(x) != value:
        raise ValueError('noncanonical rational')
    return x

def load_certificate(raw):
    if type(raw) is not bytes or len(raw)>256*1024:
        raise ValueError('certificate byte limit')
    def pairs(items):
        out={}
        for key,value in items:
            if key in out:
                raise ValueError('duplicate JSON key')
            out[key]=value
        return out
    def number(value):
        raise ValueError('JSON numbers not admitted')
    return json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,
                      parse_int=number,parse_float=number,parse_constant=number)

def atan_bounds(inverse, terms):
    """Alternating series, positive inverse argument less than one."""
    x = F(1, inverse)
    even = sum(((-1)**k * x**(2*k+1) / (2*k+1) for k in range(2*terms+1)), F())
    odd = even - x**(4*terms+3) / (4*terms+3)
    return odd, even

def gaussian_multiplier_bounds():
    """Machin identity plus rational square tests; neither float nor libm."""
    aL, aH = atan_bounds(5, 15)
    bL, bH = atan_bounds(239, 5)
    piL, piH = 16*aL-4*bH, 16*aH-4*bL
    assert F(3) < piL < piH < F(22, 7)
    scale = 10**30
    lo_squared = F(scale*scale, 1) / (2*piH)
    hi_squared = F(scale*scale, 1) / (2*piL)
    low = F(isqrt(lo_squared.numerator // lo_squared.denominator), scale)
    high = F(isqrt(hi_squared.numerator // hi_squared.denominator) + 1, scale)
    assert low*low*2*piH <= 1 <= high*high*2*piL
    return low, high

def gaussian_lower(a):
    """Exact lower enclosure of Phi(a), only for |a| <= 2.

    Integral of exp(-s^2/2) is an alternating series whose terms decrease
    already from k=0 on this interval (ratio <= 2/3).
    """
    a = F(a)
    if not -2 <= a <= 2:
        raise ValueError('Gaussian argument outside proved interval')
    z = abs(a)
    integral_upper = sum(((-1)**k*z**(2*k+1)/(2**k*factorial(k)*(2*k+1))
                          for k in range(31)), F())
    integral_lower = integral_upper - z**63/(2**31*factorial(31)*63)
    assert 0 <= integral_lower <= integral_upper
    cL, cH = gaussian_multiplier_bounds()
    return F(1,2) + cL*integral_lower if a >= 0 else F(1,2)-cH*integral_upper

def polynomial_value(coefficients, x):
    result = F()
    for coefficient in reversed(coefficients):
        result = result*x + coefficient
    return result

def interval_bernstein(coefficients, left, right):
    """Power -> Bernstein coefficients of P(left+(right-left)*z)."""
    degree = len(coefficients)-1
    shifted = [sum((coefficients[i]*comb(i,j)*left**(i-j)*(right-left)**j
                    for i in range(j,degree+1)), F()) for j in range(degree+1)]
    return [sum((shifted[j]*F(comb(k,j),comb(degree,j)) for j in range(k+1)), F())
            for k in range(degree+1)]

def check_interval(coefficients, left, right, depth=0):
    if not left < right:
        raise ValueError('empty polynomial interval')
    if all(value >= 0 for value in interval_bernstein(coefficients,left,right)):
        return 1
    if polynomial_value(coefficients,left) < 0 or polynomial_value(coefficients,right) < 0:
        raise ValueError('negative polynomial endpoint')
    if depth >= 16:
        raise ValueError('Bernstein budget unresolved')
    middle = (left+right)/2
    return check_interval(coefficients,left,middle,depth+1)+check_interval(coefficients,middle,right,depth+1)

def check_tail(coefficients, start, direction):
    """All coefficients of P(start+direction*z), z>=0, must be nonnegative."""
    degree = len(coefficients)-1
    shifted = [sum((coefficients[i]*comb(i,j)*start**(i-j)*direction**j
                    for i in range(j,degree+1)), F()) for j in range(degree+1)]
    if not all(value >= 0 for value in shifted):
        raise ValueError('tail coefficient certificate failed')

def check_cell(a,b,u,v):
    phi = gaussian_lower(a)
    cuts = sorted(set([F(-10),F(0),F(10),b]))
    count = 0
    for left,right in zip(cuts,cuts[1:]):
        midpoint = (left+right)/2
        indicator = F(int(midpoint <= b))
        cubic = BOUND if midpoint >= 0 else -BOUND
        p = (phi-v-indicator,u,v,cubic)
        count += check_interval(p,left,right)
    check_tail((phi-v-1,u,v,-BOUND),F(-10),F(-1))
    check_tail((phi-v,u,v,BOUND),F(10),F(1))
    # At b use the left, closed-indicator polynomial; at 0 both cubics agree.
    closed_at_b = (phi-v-1,u,v,BOUND if b>=0 else -BOUND)
    if polynomial_value(closed_at_b,b)<0:
        raise ValueError('closed atom boundary rejected')
    return count

def verify(value):
    if type(value) is not dict or set(value) != {'schema','bound','cells'}:
        raise ValueError('certificate fields')
    if value['schema'] != SCHEMA or value['bound'] != '2/5':
        raise ValueError('certificate scope')
    cells = value['cells']
    if type(cells) is not list or not 1 <= len(cells) <= 1000:
        raise ValueError('cell count')
    last, intervals = F(-2), 0
    for cell in cells:
        if type(cell) is not dict or set(cell) != {'a','b','u','v'}:
            raise ValueError('cell fields')
        a,b,u,v = [rational(cell[key]) for key in ('a','b','u','v')]
        if a != last or not -2 <= a < b <= 1:
            raise ValueError('whole closed grid')
        if abs(u)>10 or abs(v)>10:
            raise ValueError('coefficient size')
        intervals += check_cell(a,b,u,v)
        last = b
    if last != 1:
        raise ValueError('missing right boundary')
    if not gaussian_lower(F(1)) > F(3,5):
        raise ValueError('right exterior')
    return {'status':'EXACT_DUAL_POLYNOMIAL_CERTIFICATE_VERIFIED',
            'cells':len(cells),'bernstein_intervals':intervals,
            'arbitrary_standardized_laws_bound':'2/5',
            'campaign_grant_issued':False,'independent_review_pending':True}
