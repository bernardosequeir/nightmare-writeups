This challenge is a bit more challenging than the last one, in this one we're presented with a binary that asks us for some input and seems to reject us if we don't provide it the flag.

![[20231115085956.png]]

Opening this up in Ghidra we can format the main function to look something like this:

```
bool main(void)

{
  int isValidPassword;
  void *input;
  
  input = calloc(0x32,1);
  puts(&DAT_00102008);
  __isoc99_scanf(&DAT_0010203b,input);
  isValidPassword = validate(input);
  if (isValidPassword == 0) {
    puts(&DAT_00102050);
  }
  else {
    puts("Right this way...");
  }
  return isValidPassword == 0;
}
```

Inspecting the function we've called validate, we can see that it has a bunch of variables that are being assigned to values that map to the ASCII values of letters.

![[20231115090543.png]]

Copying the values into a python script we can quickly obtain the flag :)

```
password_bytes = [0x66,0x6c,0x61,0x67,0x7b,0x48,0x75,0x43,0x66,0x5f,0x6c,0x41,0x62,0x7d]

print("".join(map(lambda c: chr(c), password_bytes)))
```
