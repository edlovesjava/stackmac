# Stack Machine Extensions

This directory contains extension opcodes that can be dynamically loaded by the stack machine.

## How to Create an Extension

Each extension is a Python file that defines:

```python
# Required attributes
OPCODE_NAME = "MYOP"      # Name of the opcode (uppercase)
OPCODE_VALUE = 0x20       # Hex value (0x10-0xFE, avoid base opcodes)
HAS_OPERAND = False       # True if opcode takes an operand

# Required function
def execute(machine, operand):
    """Execute the opcode.

    Args:
        machine: The StackMachine instance
        operand: The operand value (or None if HAS_OPERAND is False)
    """
    # Your implementation here
    # Access the stack: machine.stack.push(), machine.stack.pop(), etc.
    pass
```

## Reserved Opcode Values

Base opcodes (do not use these values):
- 0x01-0x0B: Base arithmetic and stack operations
- 0xFF: HALT

Available for extensions:
- 0x10-0xFE (excluding 0xFF)

## Available Extensions

### MOD (0x10)
Modulo (remainder) operation.
```
PUSH 10
PUSH 3
MOD      # Result: 1
```

### NEG (0x11)
Negate the top stack value.
```
PUSH 5
NEG      # Result: -5
```

## Example Extension

Create `extensions/inc.py`:

```python
"""INC Extension - Increment top value by 1"""

OPCODE_NAME = "INC"
OPCODE_VALUE = 0x12
HAS_OPERAND = False

def execute(machine, operand):
    """Increment the top stack value by 1."""
    value = machine.stack.pop()
    machine.stack.push(value + 1)
```

Then use it in your programs:
```
PUSH 5
INC
PRINT    # Output: 6
```

## Loading Extensions

Extensions are automatically loaded when the stack machine tools start:
- **stackc** - Recognizes extension opcodes during compilation
- **stackr** - Executes extension opcodes at runtime
- **stackp** - Shows extension opcode names during disassembly

You'll see messages like:
```
Loaded extension: MOD (0x10)
Loaded extension: NEG (0x11)
```

## Error Handling

If an extension has errors, you'll see warning messages:
- Missing required attributes
- Conflicting opcode names or values
- Invalid opcode value ranges

Invalid extensions are skipped and won't break the system.
