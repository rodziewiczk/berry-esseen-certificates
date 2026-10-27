"""Path/newline ABI only, for the original scalar program on Windows.

No original numerical or control source is changed. Linux runs directly.
The standalone scalar has no child process and no legacy launch-capture claim.
"""
from pathlib import Path
import os, runpy, sys

target=Path(sys.argv[1]).resolve()
if os.name == 'nt':
    original_string=Path.__str__
    original_open=Path.open
    def slash_string(path):
        return original_string(path).replace('\\','/')
    def lf_open(path,mode='r',buffering=-1,encoding=None,errors=None,newline=None):
        if 'b' not in mode and any(c in mode for c in 'wax+') and newline is None:
            newline='\n'
        return original_open(path,mode,buffering,encoding,errors,newline)
    Path.__str__=slash_string
    Path.open=lf_open
    sys.executable=sys.executable.replace('\\','/')
sys.argv=[str(target)]
sys.path.insert(0,str(target.parent))
runpy.run_path(str(target),run_name='__main__')
