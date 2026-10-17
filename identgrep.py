import os,glob,re
out=[]
# every mount + readable file that might carry an app-platform identity
for root in ['/','/alloc','/local','/secrets','/run','/var/run','/etc','/tmp','/app','/opt']:
    try:
        for dp,dn,fn in os.walk(root):
            if any(x in dp for x in ('site-packages','node_modules','/proc','/sys','/usr/lib','/usr/share')): 
                dn[:]=[]; continue
            if dp.count('/')>6: dn[:]=[]
            for f in fn:
                p=os.path.join(dp,f)
                try:
                    if os.path.getsize(p)>100000: continue
                    d=open(p,'rb').read()
                    if re.search(rb'(?i)(jwt|bearer|token|aiven\.app|userapi|authorization|ca\.crt|client\.crt|service\.key)',d):
                        out.append(p)
                except Exception: pass
    except Exception: pass
print("CANDIDATE FILES:",out[:40])
# specifically: any cert/key material
import subprocess
print("PEM/cert files:")
for pat in ['/**/*.pem','/**/*.crt','/**/*.key','/run/**/*','/etc/**/*']:
    for f in glob.glob(pat,recursive=True)[:50]:
        if '/proc' in f or '/sys' in f: continue
        if os.path.isfile(f):
            try:
                d=open(f,'rb').read(200)
                if b'BEGIN' in d: print("  ",f, d[:40])
            except Exception: pass
