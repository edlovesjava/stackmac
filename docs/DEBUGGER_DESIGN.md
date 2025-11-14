# stackd - Stack Machine Debugger Design

## Overview

`stackd` is an interactive debugger for the stack machine emulator, providing step-by-step execution, breakpoints, stack inspection, and program state visualization.

## Command-Line Interface

```bash
python stackd.py program.stkm              # Start debugger
python stackd.py program.stkm -s source.txt # Load with source mapping
```

## Core Features

### 1. Interactive REPL

The debugger runs in an interactive loop accepting commands:

```
stackd> help
stackd> break 5
stackd> run
stackd> step
stackd> stack
```

### 2. Execution Control

| Command | Alias | Description |
|---------|-------|-------------|
| `run` | `r` | Start/continue execution until breakpoint or halt |
| `step` | `s` | Execute one instruction and stop |
| `next` | `n` | Execute one instruction (step over) |
| `continue` | `c` | Continue execution from current position |
| `restart` | | Reset program to beginning |
| `quit` | `q` | Exit debugger |

### 3. Breakpoints

| Command | Description | Example |
|---------|-------------|---------|
| `break <addr>` | Set breakpoint at address | `break 10` |
| `break <addr> if <cond>` | Conditional breakpoint | `break 5 if stack[0] > 10` |
| `delete <num>` | Delete breakpoint | `delete 1` |
| `disable <num>` | Disable breakpoint | `disable 1` |
| `enable <num>` | Enable breakpoint | `enable 1` |
| `info breakpoints` | List all breakpoints | `info breakpoints` |

**Breakpoint display:**
```
Breakpoint 1 at address 5
Breakpoint 2 at address 10 (condition: stack[0] > 5)
```

### 4. Stack Inspection

| Command | Alias | Description |
|---------|-------|-------------|
| `stack` | `st` | Display entire stack |
| `stack <n>` | | Show top N items |
| `peek <index>` | `p` | View item at index (0=top) |
| `watch <index>` | `w` | Watch stack position, break on change |

**Stack display format:**
```
Stack (5 items):
  [0] 42    <- Top
  [1] 10
  [2] 5
  [3] 3
  [4] 1     <- Bottom
```

### 5. Program State Display

| Command | Alias | Description |
|---------|-------|-------------|
| `info` | `i` | Show program counter and stack summary |
| `list` | `l` | Show instructions around current PC |
| `list <addr>` | | Show instructions around address |
| `disasm` | `d` | Disassemble current instruction |
| `where` | | Show current position in source (if available) |

**Info display:**
```
Program Counter: 5
Stack Size: 3
Next Instruction: PUSH 10

Breakpoints: 2
Status: Stopped at breakpoint 1
```

**List display:**
```
    3: PUSH 3
    4: ADD
 => 5: PUSH 2        <- PC (Breakpoint 1)
    6: MUL
    7: PRINT
```

### 6. Source-Level Debugging

If source file is provided (`-s source.txt`):

```
stackd> where
File: example.txt, Line 6
  4 | PUSH 3
  5 | ADD
> 6 | PUSH 2    <- Current
  7 | MUL
  8 | PRINT
```

**Implementation:** Maintain mapping of bytecode addresses to source line numbers during compilation.

### 7. Execution Tracing

| Command | Description |
|---------|-------------|
| `trace on` | Enable instruction trace |
| `trace off` | Disable instruction trace |
| `trace stack` | Trace stack changes |

**Trace output:**
```
[0] PUSH 5        stack: [5]
[1] PUSH 3        stack: [5, 3]
[2] ADD           stack: [8]
[3] PUSH 2        stack: [8, 2]
[4] MUL           stack: [16]
```

### 8. Watchpoints

Monitor stack values and break when they change:

```
stackd> watch 0              # Watch top of stack
Watchpoint 1: stack[0]

stackd> run
Watchpoint 1: stack[0] changed from 5 to 8
  Old value: 5
  New value: 8
  At address 2 (ADD)
```

### 9. History and Reverse Execution (Advanced)

| Command | Description |
|---------|-------------|
| `history` | Show execution history |
| `back` | Step backward one instruction |
| `reverse <n>` | Step back N instructions |

**Implementation:** Record execution history (PC, stack state, instruction) to enable reverse debugging.

## Architecture

### Class Structure

```python
class Debugger:
    def __init__(self, bytecode_file, source_file=None):
        self.machine = StackMachine()
        self.breakpoints = {}
        self.watchpoints = {}
        self.execution_history = []
        self.source_map = None
        self.trace_enabled = False

    def run_repl(self):
        """Main REPL loop"""

    def execute_command(self, command):
        """Parse and execute debugger command"""

    def step_instruction(self):
        """Execute one instruction"""

    def check_breakpoints(self):
        """Check if breakpoint hit"""

    def check_watchpoints(self):
        """Check if watched value changed"""

    def display_stack(self):
        """Pretty-print stack"""

    def display_context(self, lines=5):
        """Show instructions around PC"""
```

### Modified StackMachine

Add debugging hooks to the VM:

```python
class StackMachine:
    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
        self.debug_callback = None

    def execute_instruction(self, instruction):
        if self.debug_callback:
            self.debug_callback(self.pc, instruction, self.stack)
        # ... execute instruction
```

### Source Mapping

Extend compiler to generate debug information:

```python
# In stackc.py
def compile_with_debug_info(source_file):
    """Compile and generate .stkm.dbg file with line mappings"""
    debug_info = {
        'source_file': source_file,
        'address_to_line': {0: 1, 1: 2, ...},
        'line_to_address': {1: 0, 2: 1, ...}
    }
    # Save as JSON alongside .stkm file
```

## User Interface

### Command Prompt

```
stackd> _
```

With status indicator:
```
[RUNNING] stackd> _
[STOPPED] stackd> _
[BREAKPOINT] stackd> _
```

### Display Layout (Optional TUI Mode)

```
┌─ Source ────────────────────┬─ Disassembly ────────────┐
│ 4 | PUSH 3                  │    3: PUSH 3              │
│ 5 | ADD                     │    4: ADD                 │
│>6 | PUSH 2                  │ => 5: PUSH 2              │
│ 7 | MUL                     │    6: MUL                 │
│ 8 | PRINT                   │    7: PRINT               │
├─ Stack ─────────────────────┴───────────────────────────┤
│ [0] 8    <- Top                                         │
│ [1] 2                                                   │
├─ Breakpoints ───────────────────────────────────────────┤
│ 1: address 5 (enabled)                                  │
│ 2: address 10 if stack[0] > 5 (enabled)                │
├─ Command ───────────────────────────────────────────────┤
│ stackd> _                                               │
└─────────────────────────────────────────────────────────┘
```

## Example Session

```bash
$ python stackd.py example1_arithmetic.stkm -s example1_arithmetic.txt
Stack Machine Debugger v1.0
Loaded: example1_arithmetic.stkm (7 instructions)
Source: example1_arithmetic.txt
Type 'help' for commands

stackd> break 2
Breakpoint 1 at address 2 (ADD)

stackd> break 5 if stack[0] > 15
Breakpoint 2 at address 5 (PRINT) if stack[0] > 15

stackd> run
Breakpoint 1 hit at address 2

Stack (2 items):
  [0] 3    <- Top
  [1] 5

Next: ADD

stackd> stack
Stack (2 items):
  [0] 3    <- Top
  [1] 5

stackd> step
Executed: ADD

Stack (1 item):
  [0] 8    <- Top

stackd> list
    0: PUSH 5
    1: PUSH 3
    2: ADD
 => 3: PUSH 2    <- PC
    4: MUL
    5: PRINT
    6: HALT

stackd> continue
Breakpoint 2 hit at address 5
Condition met: stack[0] > 15 (value: 16)

stackd> peek 0
stack[0] = 16

stackd> continue
Output: 16
Program halted.

stackd> quit
```

## Implementation Phases

### Phase 1: Basic Debugger
- [x] Load bytecode files
- [ ] Interactive REPL
- [ ] Basic commands: run, step, quit
- [ ] Stack display
- [ ] Program counter display

### Phase 2: Breakpoints
- [ ] Set/delete breakpoints
- [ ] Hit detection
- [ ] List breakpoints
- [ ] Enable/disable breakpoints

### Phase 3: Enhanced Display
- [ ] List disassembly with context
- [ ] Info command
- [ ] Stack inspection commands
- [ ] Instruction trace

### Phase 4: Advanced Features
- [ ] Conditional breakpoints
- [ ] Watchpoints
- [ ] Source-level debugging
- [ ] Debug info generation in compiler

### Phase 5: Polish
- [ ] Command history (readline)
- [ ] Tab completion
- [ ] Help system
- [ ] Error handling
- [ ] TUI mode (optional, using curses)

## File Formats

### Debug Information File (.stkm.dbg)

JSON format with source mapping:

```json
{
  "version": 1,
  "source_file": "example1_arithmetic.txt",
  "address_to_line": {
    "0": 2,
    "1": 3,
    "2": 4,
    "3": 5,
    "4": 6,
    "5": 7,
    "6": 8
  },
  "line_to_address": {
    "2": 0,
    "3": 1,
    "4": 2,
    "5": 3,
    "6": 4,
    "7": 5,
    "8": 6
  },
  "source_lines": [
    "# Example 1: Calculate (5 + 3) * 2",
    "PUSH 5",
    "PUSH 3",
    "ADD",
    "PUSH 2",
    "MUL",
    "PRINT",
    "HALT"
  ]
}
```

## Error Handling

The debugger should handle:
- Invalid commands gracefully
- Out-of-bounds addresses
- Stack underflow/overflow during stepping
- Invalid breakpoint conditions
- File not found errors

## Testing Strategy

1. **Unit tests** for each command
2. **Integration tests** for command sequences
3. **Example programs** with expected debug sessions
4. **Edge cases**: empty programs, invalid breakpoints, etc.

## Future Enhancements

- **Remote debugging**: Debug over network
- **Multi-threaded debugging**: If VM supports concurrency
- **Performance profiling**: Instruction counts, hotspots
- **Memory debugging**: If memory is added to VM
- **Scripting**: Automate debug sessions with scripts
- **GUI**: Graphical debugger interface

## Command Reference Quick Card

```
EXECUTION          BREAKPOINTS        INSPECTION
---------          -----------        ----------
run, r             break <addr>       stack, st
step, s            delete <n>         peek <idx>
continue, c        info breakpoints   list, l
restart            disable/enable     info, i
quit, q                               where

ADVANCED
--------
watch <idx>        trace on/off       history
```

## Integration with Toolchain

```bash
# Typical debugging workflow
python stackc.py myprogram.txt          # Compile with debug info
python stackd.py myprogram.stkm         # Debug the program

# Or with source mapping
python stackd.py myprogram.stkm -s myprogram.txt
```

The compiler should automatically generate `.stkm.dbg` files when compiling.
