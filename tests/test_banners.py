#!/usr/bin/env python3
"""Display all available banner styles for preview."""

from src.banner import (
    BANNER, BANNER_COMPACT, BANNER_MINIMAL,
    BANNER_ALT1, BANNER_ALT2, BANNER_RETRO,
    __version__, show_banner
)


def display_all_banners():
    """Show all banner style options."""

    print("=" * 60)
    print("STACK MACHINE BANNER OPTIONS")
    print("=" * 60)
    print()

    print("OPTION 1: FULL (Default Large)")
    print("-" * 60)
    print(BANNER.format(version=__version__))
    print()

    print("OPTION 2: COMPACT (Recommended Default)")
    print("-" * 60)
    print(BANNER_COMPACT.format(version=__version__))
    print()

    print("OPTION 3: MINIMAL")
    print("-" * 60)
    print(BANNER_MINIMAL.format(version=__version__))
    print()

    print("OPTION 4: ALTERNATIVE 1 (Block Letters)")
    print("-" * 60)
    print(BANNER_ALT1.format(version=__version__))
    print()

    print("OPTION 5: ALTERNATIVE 2 (Compact with Stack)")
    print("-" * 60)
    print(BANNER_ALT2.format(version=__version__))
    print()

    print("OPTION 6: RETRO (ASCII Blocks)")
    print("-" * 60)
    print(BANNER_RETRO.format(version=__version__))
    print()

    print("=" * 60)
    print("USAGE EXAMPLES")
    print("=" * 60)
    print()
    print("Show banner (default):")
    print("  python stackr.py program.stkm")
    print()
    print("Suppress banner:")
    print("  python stackr.py program.stkm --no-banner")
    print()
    print("Choose style:")
    print("  python stackr.py program.stkm --banner-style full")
    print("  python stackr.py program.stkm --banner-style compact")
    print("  python stackr.py program.stkm --banner-style minimal")
    print()
    print("Environment variable:")
    print("  export STACKMAC_NO_BANNER=1")
    print("  python stackr.py program.stkm  # No banner")
    print()

    print("=" * 60)
    print("USING show_banner() FUNCTION")
    print("=" * 60)
    print()
    print("Example with tool name:")
    show_banner(style="compact", tool_name="Runtime (stackr)")


if __name__ == '__main__':
    display_all_banners()
