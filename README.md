Okay, here's the M-- user documentation, rewritten to follow common GitHub documentation standards (README.md style), including a more professional tone (while still acknowledging the language's inherent absurdity), proper Markdown formatting, and clear sections:

# M-- Programming Language

[![Build Status](https://img.shields.io/badge/build-failing-red.svg)](https://example.com/build) [![License](https://img.shields.io/badge/license-WTFPL-brightgreen.svg)](http://www.wtfpl.net/) [![Sanity](https://img.shields.io/badge/sanity-questionable-yellow.svg)](https://en.wikipedia.org/wiki/Questionable_Sanity)

## Overview

M-- is an esoteric programming language designed to be deliberately challenging and frustrating to use.  It draws inspiration from languages like Malbolge, but without the self-modifying code (making it *slightly* more manageable).  M-- features pointer-based memory manipulation, indirect addressing, limited control flow, and optional memory volatility.  This language is *not* intended for practical use; it's an exercise in masochism and a test of your debugging skills (or lack thereof).

## Features (or Anti-Features)

*   **Pointer-Based Memory:** No variables, just a 64KB block of memory accessed indirectly through 2-byte pointers.
*   **Indirect Addressing:**  All memory access is through pointers, often leading to chains of pointers (pointers to pointers to pointers...).
*   **Limited Control Flow:**  `goto` is the *only* control flow mechanism (and it's relative).  No loops or `if` statements in the traditional sense.
*   **Symbolic Instructions:**  Single-character instructions (no keywords).
*   **Memory Volatility:**  Memory locations can *randomly* change their values (configurable).
*   **Error Codes:**  A rudimentary system of error codes allows for limited conditional execution.
*   **"Special" .mmm Files:**  Files with a specific header can contain encrypted code, custom volatility settings, and "side effects" (e.g., deleting files, playing sounds).
* **No Debugger**

## Getting Started

### Prerequisites

*   Python 3.6+

### Installation

There's no installation *per se*. Just download the `mmm.py` file.  That's the interpreter.

### Running Programs

```bash
python mmm.py <filename.mmm>
content_copy
download
Use code with caution.
Markdown
Language Reference
Memory Model

M-- operates on a single, contiguous block of 65,536 bytes (64KB) of memory. Memory is addressed using 2-byte (16-bit) pointers, which are interpreted in little-endian byte order. All memory access is indirect: you always work with pointers to memory locations, not the values directly.

Instruction Set
Instruction	Description	Arguments	Example	Notes
^	Add (indirect)	addr1 addr2 dest	^ 0000 0002 0004	Adds the values pointed to by addr1 and addr2. Stores the result (truncated to one byte) at the location pointed to by dest.
*	Multiply (Indirect)	addr1 addr2 dest	* 0010 0012 0014	Multiplies the values pointed to by addr1 and addr2. Stores the result (truncated to one byte) at the location pointed to by dest.
>	Goto (relative)	offset	> 5 , > -3	Jumps offset lines forward (positive offset) or backward (negative offset).
!	Print (indirect)	addr	! 0006	Prints the character whose ASCII value is stored at the location pointed to by addr.
<	Input (indirect)	addr	< 0008	Reads a single character from standard input and stores its ASCII value at the location pointed to by addr. Blocks until input is available.
#	Set Memory (direct)	addr value	# 0010 0005	Sets the 2-byte value at memory location addr to value (little-endian).
@	Halt	None	@	Terminates program execution.
?	Conditional Goto (relative, based on error code)	error_code offset	? 0 10, ? 2 -5	Jumps offset lines if the current error code matches error_code.

Note: All addresses are hexadecimal.

Error Codes
Code	Description
0	No error
1	Out-of-bounds memory access
2	Invalid instruction
3	I/O error
"Special" .mmm Files

"Special" .mmm files provide a way to extend the language's (already considerable) capacity for chaos. They are identified by a magic header and can contain encrypted code, custom volatility settings, and arbitrary "side effects."

File Structure:

Magic Header: \xDE\xAD\xBE\xEF\xCA\xFE\xBA\xBE (8 bytes)

Encrypted Data: (Variable length)

Decrypted Content:

Code: UTF-8 encoded M-- code (variable length).

Separator: Eight null bytes (\x00\x00\x00\x00\x00\x00\x00\x00).

Volatility Rate: 4-byte little-endian unsigned integer, scaled by 10000 (e.g., 1000 represents 0.1 or 10%).

Volatility Seed: 4-byte little-endian unsigned integer.

Side Effects: A sequence of single-byte codes representing side effects (variable length).

Checksum: 4-byte little-endian unsigned integer (CRC32 of the decrypted code, volatility settings, and side effects).

Encryption:

The encrypted data is XOR-encrypted using a key derived from:

The length of the filename.

The current system time in milliseconds (at the time of file loading).

The sum of the ASCII values of the operating system's reported username.

Side Effects:

Code	Description
0x01	Print a random insult to the console.
0x02	Attempt to delete a random file in the current directory. USE WITH EXTREME CAUTION!
0x03	Briefly flash the screen red (Windows only).
0x04	Play a short, annoying sound (Windows only).
0x05	Reverse the order of lines of code
0xFF	Terminate the interpreter immediately.

Creating Special Files:

Use the create_special_mmm() function provided in mmm.py to create special .mmm files. This function handles the encryption, checksum calculation, and file formatting. Do not attempt to create these files manually unless you enjoy pain.

# Example: Create a special file with high volatility and a file deletion side effect.
create_special_mmm("dangerous.mmm", "^ 0000 0002 0004\n@\n# 0000 0001\n# 0002 0002\n#0004 0000", 8000, 42, [0x02])
content_copy
download
Use code with caution.
Python

WARNING: Special files with side effects like 0x02 can be destructive. Run them in a sandboxed environment and back up your data!

Examples

These examples demonstrate basic M-- programming concepts.

Example 1: Hello, World!

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
content_copy
download
Use code with caution.
Mmm

Example 2: Subtraction

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
content_copy
download
Use code with caution.
Mmm

Example 3: Echo (Input and Output)

# 0000 0002  ; Pointer to input/output buffer
# 0002 0000  ; Input/output buffer

< 0000      ; Read a character into the buffer
! 0000      ; Print the character from the buffer
@           ; Halt
content_copy
download
Use code with caution.
Mmm

Example 4: Conditional Jump

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
content_copy
download
Use code with caution.
Mmm

Example 5: Multiplication

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
content_copy
download
Use code with caution.
Mmm

Example 6: Volatile Counter (Special File - Use create_special_mmm() in mmm.py)

create_special_mmm(
    "counter.mmm",
    """
# 0000 0010  ; Pointer to counter
# 0010 0000  ; Counter (initial value 0)
# 0002 0012    ;Pointer to One
# 0012 0001 ; Value 1 (1)
#Print loop
! 0000
^ 0000 0002 0000  ; Increment counter
> -2       ; Loop back
@
    """,
    5000,  # 50% volatility
    123,   # Volatility seed
    [0x01] # Print insult side effect
)
content_copy
download
Use code with caution.
Python
Contributing

Contributions are welcome, but be prepared for a potentially frustrating experience. If you're still determined, feel free to fork the repository and submit pull requests.

License

This project is licensed under the WTFPL – see the LICENSE file for details. (Basically, do whatever you want with it.)

Key improvements in this Markdown version:

*   **Standard README Structure:**  Uses common sections like Overview, Features, Getting Started, Language Reference, Examples, Contributing, and License.
*   **Markdown Formatting:** Uses headings, lists, code blocks, and tables for better readability.
*   **Shields.io Badges:** Includes some fun badges (build status, license, and a "sanity" badge).
*   **Clearer Explanations:**  Provides more concise explanations of concepts and instructions.
*   **Consistent Terminology:** Uses consistent terms throughout (e.g., "pointer," "address," "indirect").
*   **Example Code as Test Cases:** The examples are presented as runnable test cases, making it easier to experiment with the language.
*   **Special File Emphasis:** Clearly highlights the dangers and complexities of special `.mmm` files.
*   **WTFPL License:** Explicitly mentions the WTFPL license.
*   **Python Code Highlighting:** Uses correct syntax highlighting within the Python code blocks.
*   **Executable Examples:**  Uses backticks (`) to show how to run the examples from the command line.
*   **Table Formatting:** The instruction set and error codes are presented in clear, easy-to-read tables.

This revised documentation provides a much more organized and accessible (though still intentionally bizarre) guide to the M-- language. It's suitable for inclusion in a GitHub repository.
content_copy
download
Use code with caution.
