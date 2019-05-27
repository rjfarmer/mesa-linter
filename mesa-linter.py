from __future__ import print_function

import sys
import os
import re
    
def search(filename,checks):
    with open(str(filename),'r') as f:
        for ldx,line in enumerate(f):
            if any(line.startswith(i) for i in ['!','c ','C ','* ']):
                # Skip comment lines
                continue
            for c in checks:
                if '!' in line:
                    l = line[:line.index('!')]
                else:
                    l = line
                x = c(l)
                if x is not None:
                    print(line.strip())
                    print(str(filename),":",str(ldx+1),":",x)
                    print()
    
def check_float(line):
    if 'float(' in line:
        return "Don't use float() use dble()"
    return None
    
def check_crlibm(line):
    # Match the function with the bracket as crlibm puts a _cr at the end of each function
    checks = ['log(','exp(','cos(','sin(','log10(','exp10(','tan(','dlog(']
    found = []
    for c in checks:
        if c in line and not '_'+c in line:
            found.append(c.replace('(',''))
    if len(found):
        return "Not using crlibm function",found
    return None
    
def check_pow(line):
    # Look for 3**5
    if re.search("[a-zA-Z0-9\)]\*\*[a-zA-Z0-9]", line):
        return "Found ** use, use powX() instead"
    return None
    
def check_real_op(line):
    # Lots of code has 1.+2. 
    checks = ['[0-9]\.\*','[0-9]\.\+','[0-9]\.\-','[0-9]\.\/']
    found = []
    for c in checks:
        if re.search(c, line):
            found.append(c)
    if len(found):
        return "Single precision number found "
    return None    
    
def check_real_exp(line):
    # Look for 1e+1, 1e-1, 1e1
    if re.search("[0-9][eE][+]?[-]?[0-9]", line):
        return "Found use of exponent E, use D instead"
    return None
    
# Abit broken at the moment
def check_real_d(line):
    return None
    # # Look for 1.5 but not 1.5d0
    # if re.search("([0-9]\.[0-9]*)(?!(d|D|_)\b)", line):
        # return "Missing D on float"
    # return None
    
def check_real(line):
    # Look for declaring things real and not real(dp)
    if 'real ' in line or 'real,' in line:
        return "Declared real use real(dp) instead"
    return None
    
def check_stop(line):
    if 'stop ' in line:
        return "stop detected maybe use: call mesa_error(__FILE__,__LINE__) instead?"
    return None

allchecks = [check_float,check_crlibm,check_pow,check_real_op,check_real_exp,check_real_d,check_stop] 

if __name__ == "__main__":
    for f in sys.argv[1:]:
        search(f,allchecks)
