# Banner Integration Examples

This document shows how to integrate the ASCII banner into each Stack Machine tool.

## Integration Pattern

### For stackr.py (Runtime)

```python
#!/usr/bin/env python3
import sys
import argparse
from stack_machine import StackMachine
from banner import show_banner

def main():
    parser = argparse.ArgumentParser(
        description='Stack Machine Runtime - Execute bytecode files',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('bytecode_file', help='Compiled bytecode file (.stkm)')
    parser.add_argument('--no-banner', action='store_true', help='Suppress startup banner')
    parser.add_argument('--banner-style', choices=['full', 'compact', 'minimal'],
                        default='compact', help='Banner style (default: compact)')

    args = parser.parse_args()

    # Show banner unless suppressed
    if not args.no_banner:
        show_banner(style=args.banner_style, tool_name="Runtime (stackr)")

    # Continue with normal execution...
    runtime = Runtime()
    try:
        runtime.run(args.bytecode_file)
    except FileNotFoundError:
        print(f"Error: File '{args.bytecode_file}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Runtime error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

### For stackc.py (Compiler)

```python
#!/usr/bin/env python3
import sys
import argparse
from banner import show_banner

def main():
    parser = argparse.ArgumentParser(
        description='Stack Machine Compiler - Compile source to bytecode',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('source_file', help='Source file (.txt)')
    parser.add_argument('-o', '--output', help='Output bytecode file (.stkm)')
    parser.add_argument('--no-banner', action='store_true', help='Suppress startup banner')
    parser.add_argument('--banner-style', choices=['full', 'compact', 'minimal'],
                        default='compact', help='Banner style')

    args = parser.parse_args()

    # Show banner unless suppressed
    if not args.no_banner:
        show_banner(style=args.banner_style, tool_name="Compiler (stackc)")

    # Continue with compilation...
    compiler = Compiler()
    # ... rest of code
```

### For stackp.py (Disassembler)

```python
#!/usr/bin/env python3
import sys
import argparse
from banner import show_banner

def main():
    parser = argparse.ArgumentParser(
        description='Stack Machine Disassembler - Disassemble bytecode files',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('bytecode_file', help='Bytecode file (.stkm)')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-a', '--addresses', action='store_true', help='Show addresses')
    parser.add_argument('--no-banner', action='store_true', help='Suppress startup banner')
    parser.add_argument('--banner-style', choices=['full', 'compact', 'minimal'],
                        default='compact', help='Banner style')

    args = parser.parse_args()

    # Show banner unless suppressed (but not if output to stdout without -o)
    if not args.no_banner and (args.output or args.verbose or args.addresses):
        show_banner(style=args.banner_style, tool_name="Disassembler (stackp)")

    # Continue with disassembly...
```

## Usage Examples

### With Banner (Default)
```bash
python stackr.py program.stkm
```
Output:
```
  ┌──────────────────────────────────┐
  │  STACK MAC  v1.0.0               │
  │  ┌───┐                           │
  │  │ █ │  Stack-Based VM           │
  │  ├───┤  12 Base Opcodes          │
  │  │ █ │  Extension Support        │
  │  └───┘                           │
  │  stackc | stackr | stackp        │
  └──────────────────────────────────┘
 Running: Runtime (stackr)

Output: 42
Program halted.
```

### Suppressing Banner
```bash
python stackr.py program.stkm --no-banner
```
Output:
```
Output: 42
Program halted.
```

### Different Banner Styles
```bash
python stackr.py program.stkm --banner-style full      # Large banner
python stackr.py program.stkm --banner-style compact   # Medium (default)
python stackr.py program.stkm --banner-style minimal   # Tiny banner
```

### In Scripts (No Banner)
```bash
#!/bin/bash
# Compile and run without banner clutter
python stackc.py source.txt --no-banner
python stackr.py source.stkm --no-banner
```

## Environment Variable Support (Optional Enhancement)

You can add environment variable support:

```python
import os

def should_show_banner(args):
    """Check if banner should be shown based on args and environment."""
    # Explicit flag takes precedence
    if args.no_banner:
        return False

    # Check environment variable
    if os.environ.get('STACKMAC_NO_BANNER', '').lower() in ('1', 'true', 'yes'):
        return False

    # Check if output is being piped (not a TTY)
    if not sys.stdout.isatty():
        return False

    return True

# Usage:
if should_show_banner(args):
    show_banner(style=args.banner_style, tool_name="Runtime")
```

Then users can set:
```bash
export STACKMAC_NO_BANNER=1
python stackr.py program.stkm  # No banner shown
```

## Testing Integration

When adding banner support, update tests to suppress it:

```python
# In tests, always suppress banner
def test_runtime_execution():
    """Test runtime with banner suppressed."""
    result = subprocess.run(
        ['python', 'stackr.py', 'test.stkm', '--no-banner'],
        capture_output=True,
        text=True
    )
    assert "Output: 42" in result.stdout
    assert "STACK MAC" not in result.stdout  # Banner not shown
```

## Recommended Default Settings

- **Interactive use**: Show compact banner by default
- **Piped output**: Auto-suppress (check `sys.stdout.isatty()`)
- **CI/CD**: Use `--no-banner` or `STACKMAC_NO_BANNER=1`
- **Disassembler**: Only show banner if not writing to stdout (unless verbose mode)
