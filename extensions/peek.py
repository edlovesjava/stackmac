"""PEEK Opcode Extension.
Implements the PEEK opcode for the stack machine.

Peeks at the top item of the stack without removing it.

"""

OPCODE_NAME = "PEEK"
OPCODE_VALUE = 0x1B
HAS_OPERAND = False


def execute(machine, operand):
    """Peek at the top item: [a b c] -> [a b c]."""

    if machine.stack.size() < 1:
        raise IndexError("PEEK requires at least 1 item on stack")

    top_item = machine.stack.peek()
    print(f"PEEK: Top item is {top_item}")
