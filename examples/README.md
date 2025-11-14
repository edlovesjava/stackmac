# Stack Machine Examples

This directory contains example programs demonstrating various features of the Stack Machine.

## Running Examples

```bash
# Compile an example
python3 ../stackc.py example1_arithmetic.txt

# Run the compiled bytecode
python3 ../stackr.py example1_arithmetic.stkm

# Disassemble to view the bytecode
python3 ../stackp.py example1_arithmetic.stkm -v

# Or run in one command
python3 ../stackc.py example1_arithmetic.txt && python3 ../stackr.py example1_arithmetic.stkm
```

## Example Programs

### Example 1: Arithmetic Operations (`example1_arithmetic.txt`)

**Demonstrates:** Basic arithmetic, stack operations

**Program:** Calculate `(5 + 3) * 2 = 16`

```assembly
# Example 1: Calculate (5 + 3) * 2
PUSH 5
PUSH 3
ADD
PUSH 2
MUL
PRINT
HALT
```

**Expected Output:**
```
Output: 16
Program halted.
```

**Run:**
```bash
python3 ../stackr.py example1_arithmetic.stkm
```

---

### Example 2: Countdown Loop (`example2_countdown.txt`)

**Demonstrates:** Loops, conditional jumps, control flow

**Program:** Count down from 5 to 1 using `JZ` and `JUMP`

```assembly
# Example 2: Countdown from 5 to 1
PUSH 5          # Initialize counter

# Loop start (address 1)
DUP             # Duplicate for printing
PRINT
PUSH 1
SUB             # Decrement
DUP             # Duplicate for testing
JZ 8            # Exit if zero
JUMP 1          # Loop back

# End (address 8)
POP
HALT
```

**Expected Output:**
```
Output: 5
Output: 4
Output: 3
Output: 2
Output: 1
Program halted.
```

**Run:**
```bash
python3 ../stackr.py example2_countdown.stkm
```

---

### Example 3: SWAP Operation (`example3_swap.txt`)

**Demonstrates:** Stack manipulation with `SWAP`

**Program:** Demonstrate swapping top two stack values

```assembly
# Example 3: Demonstrate SWAP operation
PUSH 10
PUSH 20
PRINT      # Prints 20
SWAP
PRINT      # Prints 10
HALT
```

**Expected Output:**
```
Output: 20
Output: 10
Program halted.
```

**Run:**
```bash
python3 ../stackr.py example3_swap.stkm
```

---

### Example 4: Extension Opcodes (`example4_extensions.txt`)

**Demonstrates:** Extension system with `MOD` and `NEG` opcodes

**Program:** Use custom extension opcodes

```assembly
# Example 4: Extension Opcodes Demo
# Demonstrates MOD and NEG extension opcodes

# Test MOD (modulo)
PUSH 10
PUSH 3
MOD          # 10 % 3 = 1
PRINT

# Test NEG (negate)
PUSH 42
NEG          # -42
PRINT

HALT
```

**Expected Output:**
```
Output: 1
Output: -42
Program halted.
```

**Run:**
```bash
python3 ../stackr.py example4_extensions.stkm
```

---

## Disassembled Files

The `*_dis.txt` files are disassembled versions of the bytecode, showing what the disassembler produces:

- `example3_swap_dis.txt` - Standard disassembly
- `example3_swap_dis2.txt` - Disassembly with verbose mode

**Generate disassembly:**
```bash
python3 ../stackp.py example1_arithmetic.stkm -o example1_dis.txt
python3 ../stackp.py example1_arithmetic.stkm -v -o example1_dis_verbose.txt
```

## Writing Your Own Programs

Create a new `.txt` file with stack machine instructions:

```assembly
# my_program.txt
PUSH 100
PUSH 50
SUB
PRINT
HALT
```

Then compile and run:
```bash
python3 ../stackc.py my_program.txt
python3 ../stackr.py my_program.stkm
```

## Available Opcodes

### Base Opcodes (Always Available)
- `PUSH value` - Push value onto stack
- `POP` - Pop and discard top value
- `ADD` - Add top two values
- `SUB` - Subtract (a - b)
- `MUL` - Multiply top two values
- `DIV` - Integer division (a / b)
- `DUP` - Duplicate top value
- `SWAP` - Swap top two values
- `PRINT` - Print and pop the top value
- `JUMP addr` - Jump to instruction address
- `JZ addr` - Pop value, jump if zero
- `HALT` - Stop execution

### Extension Opcodes (From `../extensions/`)
- `MOD` - Modulo (remainder): a % b
- `NEG` - Negate: -value

## Tips

1. **Comments:** Lines starting with `#` are comments
2. **Case-insensitive:** `PUSH`, `push`, `Push` all work
3. **Addresses:** Jump addresses are instruction indices (0-based)
4. **Stack order:** Operations pop in reverse order (top item is second operand)

## Learning Path

1. Start with **Example 1** - Basic arithmetic
2. Try **Example 3** - Stack manipulation
3. Learn **Example 2** - Loops and jumps
4. Explore **Example 4** - Extensions

Happy coding! 🚀
