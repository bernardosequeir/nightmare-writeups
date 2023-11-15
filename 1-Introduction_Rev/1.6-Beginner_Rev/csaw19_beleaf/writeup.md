This challenge was quite a step-up from the last ones, at least for me :P

Opening this up in Ghidra we can see that the binary was stripped (`file` could have told us that, but I jumped the gun on that). So looking through the functions we can find one that looks more interesting and meaty than the others (The output below has been tidied up a bit).  

```
undefined8 main(void)
{
  size_t passwordLen;
  long transformedChar;
  long in_FS_OFFSET;
  ulong i;
  char input [136];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  printf("Enter the flag\n>>> ");
  __isoc99_scanf(&DAT_00100a78,input);
  passwordLen = strlen(input);
  if (passwordLen < 0x21) {
    puts("Incorrect!");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  for (i = 0; i < passwordLen; i = i + 1) {
    transformedChar = transformChar(input[i]);
    if (transformedChar != *(long *)(&passwordLookup + i * 8)) {
      puts("Incorrect!");
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
  }
  puts("Correct!");
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

It takes our input and first of all checks it for it's length (`0x21`), so we know that must be the size of our flag. After that it loops over our input char by char and sends it to a function that transforms our character into a value that it checks in the next line.

If we look into the values in passwordLookup we can find integers separated by 8 bytes, as the logic in the if statement suggest, so if we iterate over the memory address for passwordLookup in steps of 8 bytes we can get all the values that it wants to compare our input to.

```
long transformChar(char input)
{
  long value;
  
  value = 0;
  while ((value != -1 && ((int)input != *(int *)(&charLookup + value * 4)))) {
    if ((int)input < *(int *)(&charLookup + value * 4)) {
      value = value * 2 + 1;
    }
    else if (*(int *)(&charLookup + value * 4) < (int)input) {
      value = (value + 1) * 2;
    }
  }
  return value;
}
```

Looking into the transformChar function, we can see a similar logic, just a binary tree search of a lookup table that apparently has values every 4 bytes, and we're searching to find our char's position on the lookup. So if our passwordLookup value is 1 for a given char, we need to find the char that maps to the value 1 in our transformChar function. As this is a pretty morose task to do by hand, and because I had never written a script that interacts with a binary this way using `pwntools`, I decided to write a script to solve this by itself :)

```
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
```
