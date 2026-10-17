import os,re
files=['/proc/timer_list','/proc/sched_debug','/proc/zoneinfo','/proc/slabinfo','/proc/self/stack','/proc/self/wchan',
       '/proc/sys/kernel/randomize_va_space','/sys/kernel/debug/tracing/available_filter_functions',
       '/proc/self/maps','/proc/self/smaps','/proc/1/smaps','/proc/vmallocinfo','/proc/interrupts','/proc/keys']
pat=re.compile(rb'(ffffffff[0-9a-f]{6,}|ffff[0-9a-f]{12,})')
for f in files:
    try:
        d=open(f,'rb').read(20000)
        hits=sorted(set(m.group(0).decode() for m in pat.finditer(d)))
        print(f, '->', ('LEAK '+str(hits[:5])) if hits else ('readable %d bytes, no kernel addr'%len(d)))
    except Exception as e:
        print(f,'->',type(e).__name__,str(e)[:50])
print('--- vdso/vvar in self maps ---')
for ln in open('/proc/self/maps'):
    if 'vdso' in ln or 'vvar' in ln or 'vsyscall' in ln: print(' ',ln.strip())
# kernel stack via /proc/self/stat field 29 (kstkesp) / field 30 (kstkeip)
try:
    s=open('/proc/self/stat').read().split()
    print('kstkesp(29)=',s[28],'kstkeip(30)=',s[29])
except Exception as e: print('stat',e)
