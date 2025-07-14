#!/usr/bin/env python3
"""
Wrapper script for the Audio Analysis Toolkit

This script provides a simple command-line interface that calls the
modular audio analysis toolkit. It's designed to be a drop-in
replacement for the original monolithic script.

Usage:
    python analyze_library.py /path/to/audio/directory
    python analyze_library.py --mode mcp
"""

import sys
from pathlib import Path

# Add the current directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

try:
    from audio_analysis.cli.main import main
    
    if __name__ == "__main__":
        # Simply call the main CLI function
        sys.exit(main())
        
except ImportError as e:
    print(f"Error: Failed to import audio analysis modules: {e}")
    print("Make sure you have installed the required dependencies:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)