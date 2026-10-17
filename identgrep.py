import os,glob
print("== /run/.containerenv =="); 
try: print(open('/run/.containerenv').read()[:400])
except Exception as e: print(e)
print("== /run/secrets ==")
for f in glob.glob('/run/secrets/*')+glob.glob('/run/secrets/**/*',recursive=True):
    try: print(" ",f,open(f,'rb').read(120))
    except Exception: pass
print("== /alloc tree (depth3) ==")
for dp,dn,fn in os.walk('/alloc'):
    if dp.count('/')>4: dn[:]=[]
    for f in fn:
        p=os.path.join(dp,f)
        try: print(" ",p,os.path.getsize(p))
        except Exception: pass
print("== /local tree ==")
for dp,dn,fn in os.walk('/local'):
    for f in fn: print("  /local/",dp,f)
print("== env =="); 
for k,v in sorted(os.environ.items()): print("  %s=%s"%(k,v[:60]))
print("== /etc/aiven* /etc/pki ==")
for g in glob.glob('/etc/aiven*')+glob.glob('/etc/pki/*')+glob.glob('/etc/*.json'): print(" ",g)
