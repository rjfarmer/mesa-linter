import sys
import os
import re
    
def search(filename,checks):
    with open(str(filename),'r') as f:
        for ldx,line in enumerate(f):
            if line.startswith('!') or line.startswith('c '):
                # Skip comment lines
                continue
            for c in checks:
                x = c(line)
                if x is not None:
                    print(line.strip())
                    print(str(filename),"Line:",str(ldx),x)
                    print()
    
def check_float(line):
    if 'float(' in line:
        return "Don't use float() use dble()"
    return None
    
def check_crlibm(line):
    # Match the function with the bracket as crlibm puts a _cr at the end of each function
    checks = ['log(','exp(','cos(','sin(','log10(','exp10(','tan(']
    found = []
    for c in checks:
        if c in line:
            found.append(c.replace('(',''))
    if len(found):
        return "Not using crlibm function",found
    return None
    
def check_pow(line):
    # Look for 3**5
    if re.search("[0-9]\*\*[0-9]", line):
        return "Maybe found ** use, use powX() instead"
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
    if re.search("[0-9]e[+?][-?][0-9]", line):
        return "Found use of exponent E, use D instead"
    return None
    
def check_real_d(line):
    # Look for 1.5 but not 1.5d0
    if re.search("([0-9]\.[0-9]+)(?!d)", line):
        return "Missing D on float"
    return None

allchecks = [check_float,check_crlibm,check_pow,check_real_op,check_real_exp,check_real_d] 

if __name__ == "__main__":
    for f in sys.argv[1:]:
        search(f,allchecks)
