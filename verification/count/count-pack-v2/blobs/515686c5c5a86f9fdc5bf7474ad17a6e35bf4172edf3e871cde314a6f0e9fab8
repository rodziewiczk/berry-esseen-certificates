"""Exact independent mean/noise geometry; original affine budget is untouched."""
from fractions import Fraction as F
def need(x,m):
 if not x:raise ValueError(m)
def bounds(n,pl,pu,ml,Lambda):
 need(type(n)is int and n>=2 and all(type(x)is F for x in(pl,pu,ml,Lambda)),'exact mean/noise arguments')
 need(0<pl<=pu<1 and 0<ml<=F(1,2) and Lambda>0,'positive mean/noise domain')
 vl=min(pl*(1-pl),pu*(1-pu));vh=F(1,4)if pl<=F(1,2)<=pu else max(pl*(1-pl),pu*(1-pu))
 cap=min(Lambda,n*max(F(0),vl*vl/(ml*ml)-vl,vh*vh/(ml*ml)-vh))
 return dict(lambda_upper=cap,scale_upper=vh/ml,variance_lower=vl,variance_upper=vh)
def margins(n,pl,pu,hm,hp,scale):
 need(type(n)is int and n>=2 and all(type(x)is F for x in(pl,pu,hm,hp,scale)),'exact nearest-root arguments')
 need(0<pl<=pu<1 and hm>0 and hp>0 and scale>0,'positive nearest-root domain')
 return(n*pl-hm*scale+F(1,2),F(n)+F(1,2)-n*pu-hp*scale)
