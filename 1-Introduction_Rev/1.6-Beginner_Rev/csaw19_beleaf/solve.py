from pwn import *

beleaf = ELF('./beleaf')
password_length = 0x21
# for some reason the values in ghidra start 0x100000 ahead 
# (this must have a reasonable explanation but I just don't know enough)
char_lookup_address = 0x301020 - 0x100000
order_lookup_address = 0x3014e0 - 0x100000

char_list = []
char_order_list = []

for i in range(password_length):
    char_order_list += beleaf.read(order_lookup_address + i * 8, 1)

for i in range(max(char_order_list) + 1):
    char_list += beleaf.read(char_lookup_address + i * 4, 1)

print(''.join(chr(char_list[x]) for x in char_order_list))