This is the first challenge of this guide/course, so as we can expect, it's very handhold-y, which is good, because even though I think I solved this challenge among the years, I can't say no to some extra help when starting something new.

(I'm copying the questions directly from the post because the initial challenge doesn't seem to be up anymore)
### Question 1 - What is the value of dh after line 129 executes?

Line 129 reads as such:

`xor dh, dh  ; <- Question 1`

So, dh after line 129 is 0, as all values when XOR'ed against themselves turn to 0.

### Question 2 - What is the value of gs after line 145 executes?

Line 145 reads:
`mov gs, dx ; to use them to help me clear     <- Question 2`

Further up in the code we can spot

``` 
mov dx, 0xffff  ; Hexadecimal
not dx 
```

The not instruction does a bitwise not on the value so, 0xffff turns into 0x0 and when moved into gs, it stays at 0x0

### Question 3 - What is the value of si after line 151 executes?

Line 151:  `mov si, sp ; Source Index       <- Question 3`

Above it we can see:

```
 mov cx, 0;
 (...)
 mov sp, cx; Stack Pointer
```


As there aren't any changes between the initial `mov cx, 0` and the move to sp, si will be 0 after line 151 executes. 


### Question 4 - What is the value of ax after line 169 executes?

```
  mov al, 't'
  mov ah, 0x0e      ; <- question 4
```

al and ah are both halves of ax, a**h** being the **H**igher bits and a**l** the **L**ower bits.

So ax is 0x0e74

al -> 't' -> 0x07 after consulting an ascii table, if you're confused by this conversion

### Question 5 - What is the value of ax after line 199 executes for the first time?

```
 ; First let's define a string to print, but remember...now we're defining junk data in the middle of code, so we need to jump around it so there's no attempt to decode our text string

  mov ax, .string_to_print

  jmp print_string

  .string_to_print: db "acOS", 0x0a, 0x0d, "  by Elyk", 0x00  ; label: <size-of-elements> <array-of-elements>

  ; db stands for define-bytes, there's db, dw, dd, dq, dt, do, dy, and dz.  I just learned that three of those exist.  It's not really assembly-specific knowledge. It's okay.  https://www.nasm.us/doc/nasmdoc3.html

    ; The array can be in the form of a "string" or comma,separate,values,.

  

; Now let's make a whole 'function' that prints a string

print_string:

  .init:

    mov si, ax  ; We have no syntactic way of passing parameters, so I'm just going to pass the first argument of a function through ax - the string to print.

  

  .print_char_loop:

    cmp byte [si], 0  ; The brackets around an expression is interpreted as "the address of" whatever that expression is.. It's exactly the same as the dereference operator in C-like languages

                        ; So in this case, si is a pointer (which is a copy of the pointer from ax (line 183), which is the first "argument" to this "function", which is the pointer to the string we are trying to print)

                        ; If we are currently pointing at a null-byte, we have the end of the string... Using null-terminated strings (the zero at the end of the string definition at line 178)

    je .end

    mov al, [si]  ; Since this is treated as a dereference of si, we are getting the BYTE AT si... `al = *si`

  

    mov ah, 0x0e  ; <- Question 5!

    int 0x10      ; Actually print the character

    inc si        ; Increment the pointer, get to the next character

    jmp .print_char_loop

    .end:
```

Finally we get something a **bit** more complicated (badum-tss)

Line 99 reads:

`mov ah, 0x0e ; <- Question 5!`

So, it's the same instruction as the last question, just with some different moves beforehand.

Before the function starts  `"acOS"` is moved into `ax` , which is subsequently moved into `si` just after the function starts. After some comparisons to check if the string has ended, we get a `mov al, [si]` , which moves the current character of the string being printed into `al` , so with `0x0e` being moved into `ah` and the value of lower-case a being passed to `al`, we get an `ax` with the value of `0x0e61`
