# Magnolia-Minus-Minus-M---
M-- User Documentation (v0.666 - Unstable)

Abandon All Hope, Ye Who Enter Here! You have chosen to program in M--, a language specifically designed to be as frustrating and counter-intuitive as possible. This documentation might help, but don't count on it.

Disclaimer: The creators of M-- are not responsible for anything that happens as a result of using this language. This includes, but is not limited to: loss of sanity, hair loss, existential crises, spontaneous combustion, and the heat death of the universe.
1. Introduction (A Journey into the Absurd)

M-- is a language that throws out all modern programming paradigms. Forget variables, data types, and structured programming. Embrace pointers, indirect memory access, and the ever-present threat of random memory corruption.
2. Core Concepts (Things You Might Want to Know)

    Memory: A single, 64KB block of bytes. That's it. No variables, just addresses.

    Pointers: 2-byte values that point to memory locations. Everything is indirect. Expect to deal with pointers to pointers to pointers...

    Volatility: Memory locations can randomly change their values. This is a "feature," not a bug. The frequency of this chaos is controlled by the volatility_rate.

    Instructions: Single-character symbols. No keywords. Consistent meanings (thankfully).

    Control Flow: goto and only goto. Relative jumps. No loops, no if statements (well, not directly).

    Error Codes: Your only (fragile) hope for conditional execution.

3. Instruction Set (The Tools of Your Torment)
Symbol	Description	Arguments	Example	Notes
^	Add (indirect)	addr1 addr2 dest	^ 0000 0002 0004	Adds values pointed to by addr1 and addr2, stores result at location pointed to by dest.
*	Multiply (indirect)	addr1 addr2 dest	* 0010 0012 0014	Multiply values pointed to by addr1 and addr2, stores result at location pointed to by dest.
>	Goto (relative)	offset	> 5 , > -3	Jumps offset lines forward (positive) or backward (negative).
!	Print (indirect)	addr	! 0006	Prints the character whose ASCII value is at the location pointed to by addr.
<	Input (indirect)	addr	< 0008	Reads a character, stores its ASCII value at the location pointed to by addr.
#	Set Memory (direct)	addr value	# 0010 0005	Sets the 2-byte value at addr to value (little-endian).
@	Halt	None	@	Stops the program.
?	Conditional Goto (relative, based on error code)	error_code offset	? 0 10, ? 2 -5	Jumps offset lines if the current error code is error_code.

All addresses are in hexadecimal.
4. Error Codes (Your Fragile Friends)
Code	Description
0	No error (ironically)
1	Out-of-bounds memory access
2	Invalid instruction
3	I/O Error
5. Running M-- Programs

You need the mmm.py interpreter (written in Python, because we're not completely insane) and your .mmm code file.

Command-line Usage:

      
python mmm.py <filename.mmm>

    

Use code with caution.Bash
6. "Special" .mmm Files (For the Truly Masochistic)

Special .mmm files add another layer of complexity (and potential harm). They are identified by a magic header and contain encrypted code, custom volatility settings, and side effects.

Structure:

    Magic Header: \xDE\xAD\xBE\xEF\xCA\xFE\xBA\xBE

    Encrypted Data:

        Decrypted Content:

            Code: (UTF-8)

            Separator: (8 null bytes)

            Volatility Rate: (4-byte little-endian int, scaled by 10000)

            Volatility Seed: (4-byte little-endian int)

            Side Effects: (Byte array)

            Checksum: (4-byte little-endian int, CRC32)

    Encryption: XOR with a key derived from filename length, system time, and username.

Side Effects (Things That Can Go Wrong):
Code	Description
0x01	Print a random insult.
0x02	Attempt to delete a random file.
0x03	Flash the screen red (Windows only).
0x04	Play an annoying sound (Windows only).
0x05	Reverse the code
0xFF	Terminate immediately.

Creating Special Files: Use the create_special_mmm() function in mmm.py. Be extremely careful!
7. Test Cases (Examples of Suffering)

These examples demonstrate various M-- features (and anti-features). Copy and paste them into .mmm files.

Test Case 1: Hello, World!

      
# 0000 0010  ; Pointer to "H"
# 0002 0011  ; Pointer to "e"
# 0004 0012  ; Pointer to "l"
# 0006 0013  ; Pointer to "l"
# 0008 0014  ; Pointer to "o"
# 000a 0015  ; Pointer to ", "
# 000c 0017  ; Pointer to "W"
# 000e 0018  ; Pointer to "o"
# 0010 0048  ; "H"
# 0011 0065  ; "e"
# 0012 006c  ; "l"
# 0013 006c  ; "l"
# 0014 006f  ; "o"
# 0015 002c  ; ","
# 0016 0020 ; " "
# 0017 0057  ; "W"
# 0018 006f  ; "o"
# 0019 0072 ; "r"
# 001a 006c ; "l"
# 001b 0064 ; "d"
# 001c 0021 ; "!"
# 001d 0000 ; Counter address
# 001e 001d ; Counter pointer

# 0020 000d ; String length

#Print loop
! 0000
^ 001d 0000 001d ;Increment letter pointer, write to counter pointer.
^ 001e 0020 001f; Increment counter, result written to 001f
? 0 -3 ; Check for error 0, go back 3 lines
@

    

Use code with caution.Mmm

Expected Output: Hello, World!

Test Case 2: Subtraction

      
# 0000 0010  ; Pointer to value 1 (5)
# 0002 0012  ; Pointer to value 2 (2)
# 0004 0014  ; Pointer to result (initially 5)
# 0006 0016    ;Pointer to one
# 0010 0005  ; Value 1 (5)
# 0012 0002  ; Value 2 (2)
# 0014 0005  ; Result (initialized to 5)
# 0016 0001 ; Constant One

; Loop to decrement result until value2 is zero
^ 0004 0006 0004  ; Decrement result by one
^ 0002 0006 0002    ;Decrement value 2 by one
? 0 -2 ;Check for error 0, go up 2 lines (loop)

! 0004        ; Print the result
@             ; Halt

    

Use code with caution.Mmm

Expected Output: 3

Test Case 3: Echo (Input and Output)

      
# 0000 0002  ; Pointer to input/output buffer
# 0002 0000  ; Input/output buffer

< 0000      ; Read a character into the buffer
! 0000      ; Print the character from the buffer
@           ; Halt

    

Use code with caution.Mmm

Expected Output: Whatever character you input.

Test Case 4: Conditional Jump

      
# 0000 0010 ; Ptr to value.
# 0002 004e ;Pointer to 'N'
# 0004 0059 ; Pointer to 'Y'

# 0010 0005 ; Value to check (non-zero in this case)
# 004e 004e ; The character 'N'
# 0059 0059 ; The character 'Y'

* 0000 0000 0006 ; Multiply the value with itself. Result at 0x0006. This also serves as error check
? 0 3 ; if result == 0 (and also no error), jump 3 lines (to print 'N').
! 0004 ; print 'Y'
> 2    ; Jump over printing 'N'
! 0002 ; Print 'N'
@      ; Halt

    

Use code with caution.Mmm

If value at 0x0010 is non-zero:
Expected Output: Y
If value at 0x0010 is zero:
Expected Output: N

Test Case 5: Multiplication

      
# 0000 0010  ; Pointer to multiplicand (5)
# 0002 0012  ; Pointer to multiplier (3)
# 0004 0014  ; Pointer to result (initially 0)
# 0006 0016 ; Pointer to temporary value (initially 0)
# 0008 0018 ; Pointer to 1

# 0010 0005  ; Multiplicand (5)
# 0012 0003  ; Multiplier (3)
# 0014 0000  ; Result (0)
# 0016 0000
# 0018 0001

; Outer loop (multiplier times)
^ 0006 0000 0006 ;Copy Multiplicand to temporary

; Inner loop (add multiplicand to result)
^ 0004 0006 0004 ; Add temporary to result
^ 0006 0008 0006 ; Decrement temporary
? 0 -2           ;If no error, loop (inner)

^ 0002 0008 0002; Decrement multiplier.
? 0 -5 ; Check for error 0, go back (outer loop)

! 0004      ;Print result
@

    

Use code with caution.Mmm

If the values on memory pointed by 0000 and 0002 are 5 and 3, respectivly:
Expected Output:  (Vertical tab, or 15)

Test Case 6: Volatile Counter (Special File)

Use the following Python code to generate counter.mmm:

      
create_special_mmm(
    "counter.mmm",
    """
# 0000 0010  ; Pointer to counter
# 0010 0000  ; Counter (initial value 0)
# 0002 0012    ;Pointer to One
# 0012 0001 ; Value 1 (1)
#Print loop
! 0000
^ 0000 0002 0000  ; Increment counter (counter = counter + 1)
> -2       ; Loop back
@
    """,
    5000,  # 50% volatility
    123,   # Volatility seed
    [0x01] # Print insult as side effect
)

    

Use code with caution.Python

Expected Output: A chaotic stream of characters, due to memory volatility. The output will be different each time. Also, an insult will be printed.
8. Debugging (A Waste of Time)

There is no debugger. Print statements (!) are your only friend, and they are unreliable. Embrace the futility.
9. Contributing (Join the Suffering)

If you're crazy enough to want to contribute, fork the repository and submit pull requests. But don't say we didn't warn you.
