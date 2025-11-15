#!/usr/bin/env python3
"""
A simple stack machine emulator.

This stack machine supports:
- Arithmetic operations: ADD, SUB, MUL, DIV
- Stack operations: PUSH, POP, DUP, SWAP
- Control flow: JUMP, JZ (jump if zero)
- I/O: PRINT
- Control: HALT
- Extension opcodes: Loaded dynamically from extensions/ directory
"""

from typing import List, Tuple, Optional, Dict

try:
    from .opcodes_ext import get_registry
except ImportError:
    from opcodes_ext import get_registry


class Stack:
    """A simple stack data structure for the stack machine."""

    def __init__(self) -> None:
        self.items: List[int] = []

    def push(self, item: int) -> None:
        """Push an item onto the stack."""
        self.items.append(item)

    def pop(self) -> int:
        """Pop an item from the stack."""
        if self.is_empty():
            raise IndexError("Stack underflow: cannot pop from empty stack")
        return self.items.pop()

    def peek(self) -> int:
        """Look at the top item without removing it."""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]

    def is_empty(self) -> bool:
        """Check if the stack is empty."""
        return len(self.items) == 0

    def size(self) -> int:
        """Return the number of items in the stack."""
        return len(self.items)

    def __repr__(self) -> str:
        return f"Stack({self.items})"


class StackMachine:
    """A simple stack-based virtual machine."""

    # Constants
    PC_JUMP_OFFSET = 1  # Adjustment for post-increment after jump
    TRACE_STACK_LIMIT = 10  # Max stack items to display in trace

    # Instruction costs (for educational purposes - simulated cycles)
    INSTRUCTION_COSTS: Dict[str, int] = {
        'PUSH': 1, 'POP': 1, 'DUP': 1, 'SWAP': 1,
        'ADD': 1, 'SUB': 1,
        'MUL': 3,  # Multiplication is more expensive
        'DIV': 10,  # Division is most expensive
        'JUMP': 2, 'JZ': 2,  # Control flow has overhead
        'PRINT': 5,  # I/O is expensive
        'HALT': 1,
    }

    # Opcode definitions (loaded from registry to include extensions)
    OPCODES: Optional[Dict[str, int]] = None  # Will be initialized from registry

    @classmethod
    def _init_opcodes(cls) -> None:
        """Initialize opcodes from registry (includes extensions)."""
        if cls.OPCODES is None:
            registry = get_registry()
            cls.OPCODES = registry.get_opcodes()

    def __init__(self) -> None:
        self._init_opcodes()
        self.stack: Stack = Stack()
        self.program: List[Tuple[str, Optional[int]]] = []
        self.pc: int = 0  # Program counter
        self.running: bool = False
        self.registry = get_registry()
        self.instruction_count: int = 0  # Total instructions executed
        self.cycle_count: int = 0  # Total cycles (weighted by cost)

    def load_program(self, program: List[Tuple[str, Optional[int]]]) -> None:
        """Load a program into memory.

        Program format: list of tuples (opcode, operand)
        For opcodes without operands, use (opcode, None)
        """
        self.program = program
        self.pc = 0

    def execute(self, trace: bool = False, step: bool = False) -> None:
        """Execute the loaded program."""
        self.running = True
        self.pc = 0
        self.instruction_count = 0
        self.cycle_count = 0

        while self.running and self.pc < len(self.program):
            instruction = self.program[self.pc]
            opcode, operand = instruction

            # Show trace if requested
            if trace:
                self.trace_state(opcode, operand, step=step)

            # Execute the instruction
            self.execute_instruction(opcode, operand)

            # Move to next instruction (unless a jump occurred)
            if self.running:
                self.pc += 1

    def execute_instruction(self, opcode: str, operand: Optional[int]) -> None:
        """Execute a single instruction."""

        # Track instruction execution
        self.instruction_count += 1
        self.cycle_count += self.get_instruction_cost(opcode)

        if opcode == 'PUSH':
            self.stack.push(operand)

        elif opcode == 'POP':
            self.stack.pop()

        elif opcode == 'ADD':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(a + b)

        elif opcode == 'SUB':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(a - b)

        elif opcode == 'MUL':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(a * b)

        elif opcode == 'DIV':
            b = self.stack.pop()
            a = self.stack.pop()
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            self.stack.push(a // b)  # Integer division

        elif opcode == 'DUP':
            # Duplicate the top item on the stack
            value = self.stack.peek()
            self.stack.push(value)

        elif opcode == 'SWAP':
            # Swap the top two items
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(b)
            self.stack.push(a)

        elif opcode == 'PRINT':
            # Print and pop the top value from the stack
            value = self.stack.pop()
            print(f"Output: {value}")

        elif opcode == 'JUMP':
            # Unconditional jump to address
            self.pc = operand - self.PC_JUMP_OFFSET  # Adjust for post-increment

        elif opcode == 'JZ':
            # Jump if top of stack is zero
            value = self.stack.pop()
            if value == 0:
                self.pc = operand - self.PC_JUMP_OFFSET

        elif opcode == 'HALT':
            self.running = False
            print("Program halted.")

        else:
            # Check if it's an extension opcode
            if self.registry.is_extension(opcode):
                self.registry.execute_extension(opcode, self, operand)
            else:
                # Try to suggest similar opcodes
                suggestions = self._find_similar_opcodes(opcode)
                msg = f"Unknown opcode: {opcode}"
                if suggestions:
                    msg += f" (did you mean {', '.join(suggestions)}?)"
                raise ValueError(msg)

    def debug_state(self) -> None:
        """Print the current state of the machine."""
        print(f"PC: {self.pc}, Stack: {self.stack}")

    def get_instruction_cost(self, opcode: str) -> int:
        """Get the cycle cost of an instruction (for educational purposes).

        Args:
            opcode: The opcode name

        Returns:
            Number of simulated cycles for this instruction
        """
        # Check known costs first
        if opcode in self.INSTRUCTION_COSTS:
            return self.INSTRUCTION_COSTS[opcode]

        # Extension opcodes have default cost of 1
        if self.registry.is_extension(opcode):
            return 1

        # Unknown opcodes default to 1
        return 1

    def get_stats(self) -> Dict[str, int]:
        """Get execution statistics.

        Returns:
            Dictionary with 'instructions' and 'cycles' counts
        """
        return {
            'instructions': self.instruction_count,
            'cycles': self.cycle_count
        }

    def _find_similar_opcodes(self, opcode: str, threshold: float = 0.6) -> List[str]:
        """Find similar opcode names using fuzzy matching.

        Args:
            opcode: The unknown opcode to find matches for
            threshold: Similarity threshold (0.0-1.0)

        Returns:
            List of up to 3 similar opcode names
        """
        import difflib
        if self.OPCODES is None:
            return []
        return difflib.get_close_matches(opcode, self.OPCODES.keys(), n=3, cutoff=threshold)

    def trace_state(self, opcode: str, operand: Optional[int], step: bool = False) -> None:
        """Print a one-line trace of the current execution state."""
        # Format instruction
        if operand is not None:
            instruction = f"{opcode} {operand}"
        else:
            instruction = opcode
        
        # Format stack (top N items, top on right)
        stack_items = self.stack.items
        if self.stack.size() > self.TRACE_STACK_LIMIT:
            stack_display = stack_items[-self.TRACE_STACK_LIMIT:]
        else:
            stack_display = stack_items
        stack_str = str(stack_display)
        
        # Print trace line
        print(f"PC:{self.pc:3d} {instruction:<12} Stack: {stack_str}")
        
        # Pause for keypress if stepping
        if step:
            try:
                input("Press Enter to continue (Ctrl+C to exit)...")
            except KeyboardInterrupt:
                print("\nExecution interrupted by user")
                self.running = False


class ProgramParser:
    """Parser for stack machine programs from text files."""

    @staticmethod
    def parse_file(filename: str) -> List[Tuple[str, Optional[int]]]:
        """Parse a command file and return a program.

        File format:
        - Lines starting with # are comments
        - Other lines are commands in the format: OPCODE [operand]
        - Blank lines are ignored

        Example:
            # This is a comment
            PUSH 5
            PUSH 3
            ADD
            PRINT
            HALT
        """
        program = []

        try:
            with open(filename, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()

                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue

                    # Remove inline comments (anything after #)
                    if '#' in line:
                        line = line[:line.index('#')].strip()

                    # Parse command
                    parts = line.split(None, 1)  # Split on whitespace, max 2 parts
                    if not parts:
                        continue

                    opcode = parts[0].upper()

                    # Validate opcode
                    if opcode not in StackMachine.OPCODES:
                        # Try to suggest similar opcodes
                        import difflib
                        suggestions = difflib.get_close_matches(opcode, StackMachine.OPCODES.keys(), n=3, cutoff=0.6)
                        msg = f"Line {line_num}: Unknown opcode '{opcode}'"
                        if suggestions:
                            msg += f" (did you mean {', '.join(suggestions)}?)"
                        raise ValueError(msg)

                    # Parse operand if present
                    operand = None
                    if len(parts) == 2:
                        try:
                            operand = int(parts[1])
                        except ValueError:
                            raise ValueError(f"Line {line_num}: Invalid operand '{parts[1]}' - must be an integer")

                    program.append((opcode, operand))

        except FileNotFoundError:
            raise FileNotFoundError(f"Command file '{filename}' not found")

        return program


def main():
    """Demonstrate the stack machine with example programs."""
    import sys

    print("=" * 60)
    print("Stack Machine Emulator")
    print("=" * 60)

    # Check if a command file was provided
    if len(sys.argv) > 1:
        # Load program from file
        filename = sys.argv[1]
        print(f"\nLoading program from: {filename}")
        print("-" * 40)

        try:
            parser = ProgramParser()
            program = parser.parse_file(filename)

            machine = StackMachine()
            machine.load_program(program)
            machine.execute()

            print("\n" + "=" * 60)
            return

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    # Otherwise, run hardcoded examples
    print("=" * 60)
    print("Stack Machine Emulator")
    print("=" * 60)

    # Example 1: Simple arithmetic (5 + 3) * 2
    print("\nExample 1: Calculate (5 + 3) * 2")
    print("-" * 40)

    machine = StackMachine()
    program = [
        ('PUSH', 5),      # Push 5
        ('PUSH', 3),      # Push 3
        ('ADD', None),    # 5 + 3 = 8
        ('PUSH', 2),      # Push 2
        ('MUL', None),    # 8 * 2 = 16
        ('PRINT', None),  # Print result
        ('HALT', None),
    ]

    machine.load_program(program)
    machine.execute()

    # Example 2: Countdown from 5 to 1
    print("\nExample 2: Countdown from 5 to 1")
    print("-" * 40)

    machine = StackMachine()
    program = [
        ('PUSH', 5),      # 0: counter = 5
        # Loop start (address 1)
        ('DUP', None),    # 1: duplicate counter for printing
        ('PRINT', None),  # 2: print current value
        ('PUSH', 1),      # 3: push 1
        ('SUB', None),    # 4: counter - 1
        ('DUP', None),    # 5: duplicate to check if zero
        ('JZ', 8),        # 6: if zero, jump to end (address 8)
        ('JUMP', 1),      # 7: jump back to loop start
        # End (address 8)
        ('POP', None),    # 8: clean up the zero
        ('HALT', None),   # 9: halt
    ]

    machine.load_program(program)
    machine.execute()

    # Example 3: Swap demonstration
    print("\nExample 3: Demonstrate SWAP operation")
    print("-" * 40)

    machine = StackMachine()
    program = [
        ('PUSH', 10),     # Push 10
        ('PUSH', 20),     # Push 20
        ('PRINT', None),  # Print 20 (top of stack)
        ('SWAP', None),   # Swap
        ('PRINT', None),  # Print 10 (now on top)
        ('HALT', None),
    ]

    machine.load_program(program)
    machine.execute()

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
