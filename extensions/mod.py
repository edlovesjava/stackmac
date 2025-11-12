"""
MOD Extension - Modulo (remainder) operation

Pops two values from the stack, computes a % b, and pushes the result.

Example:
    PUSH 10
    PUSH 3
    MOD      # Result: 1 (10 % 3 = 1)
"""

OPCODE_NAME = "MOD"
OPCODE_VALUE = 0x10
HAS_OPERAND = False


def execute(machine, operand):
    """Execute the MOD operation.

    Pops b, then a, computes a % b, and pushes result.
    """
    b = machine.stack.pop()
    a = machine.stack.pop()

    if b == 0:
        raise ZeroDivisionError("Modulo by zero")

    result = a % b
    machine.stack.push(result)
