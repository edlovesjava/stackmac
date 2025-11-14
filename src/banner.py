"""Stack Machine ASCII Banner Utility"""

import sys
import os

__version__ = "1.0.0"

# ASCII art banner for Stack Machine (Compact style - default)
BANNER_COMPACT = r"""
  ┌──────────────────────────────────┐
  │  STACK MAC  v{version:<19}│
  │  ┌───┐                           │
  │  │ █ │  Stack-Based VM           │
  │  ├───┤  12 Base Opcodes          │
  │  │ █ │  Extension Support        │
  │  └───┘                           │
  │  stackc | stackr | stackp        │
  └──────────────────────────────────┘
"""

# Alias for default banner
BANNER = BANNER_COMPACT

# Minimal banner for constrained environments
BANNER_MINIMAL = r"""
  STACK MAC v{version}
  stackc | stackr | stackp
"""


def show_banner(tool_name=None, file=None):
    """Display the Stack Machine banner.

    Args:
        tool_name: Optional tool name to display (e.g., "Compiler", "Runtime")
        file: Output file (default: sys.stdout)
    """
    if file is None:
        file = sys.stdout

    # Format with version
    output = BANNER_COMPACT.format(version=__version__)
    print(output, file=file)

    # Optionally show tool name
    if tool_name:
        print(f" Running: {tool_name}", file=file)
        print(file=file)


def should_show_banner(no_banner_flag):
    """Determine if banner should be shown.

    Args:
        no_banner_flag: Value of --no-banner command line flag

    Returns:
        True if banner should be shown, False otherwise
    """
    # Explicit flag takes precedence
    if no_banner_flag:
        return False

    # Check environment variable
    if os.environ.get('STACKMAC_NO_BANNER', '').lower() in ('1', 'true', 'yes'):
        return False

    # Check if output is being piped (not a TTY)
    if not sys.stdout.isatty():
        return False

    return True


# Alternative compact designs for different preferences:

BANNER_ALT1 = r"""
╭──────────────────────────────────────╮
│  ████████  ███████  █████   █████   │
│  ██           ██    ██   ██ ██   ██ │
│  ██████       ██    ███████ ██      │
│      ██       ██    ██   ██ ██   ██ │
│  ████████     ██    ██   ██  █████  │
│                                      │
│  Stack Machine  •  v{version:<16}│
│  stackc | stackr | stackp            │
╰──────────────────────────────────────╯
"""

BANNER_ALT2 = r"""
 ╔═══════════════════════════════╗
 ║  ┌───┐ STACK MAC v{version:<11}║
 ║  │ █ │ Stack-Based VM         ║
 ║  ├───┤ 12 Opcodes + Extensions║
 ║  │ █ │ Full Toolchain         ║
 ║  └───┘                        ║
 ╚═══════════════════════════════╝
"""

BANNER_RETRO = r"""
┌────────────────────────────────────┐
│ ▓▓▓▓▓▓  ▓▓▓▓▓▓▓  ▓▓▓    ▓▓▓  ▓▓▓  │
│ ▓▓         ▓▓    ▓▓▓▓  ▓▓▓▓  ▓▓   │
│ ▓▓▓▓▓▓     ▓▓    ▓▓ ▓▓▓▓ ▓▓  ▓▓▓▓ │
│     ▓▓     ▓▓    ▓▓  ▓▓  ▓▓    ▓▓ │
│ ▓▓▓▓▓▓     ▓▓    ▓▓      ▓▓  ▓▓▓▓ │
│                                    │
│ Stack Machine  v{version:<18}│
│ [ Compiler • Runtime • Disasm ]    │
└────────────────────────────────────┘
"""
