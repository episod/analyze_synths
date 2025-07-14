#!/usr/bin/env python3
"""
FastMCP Server wrapper for the Audio Analysis Toolkit

This script provides a FastMCP server interface that uses the
modular audio analysis toolkit. It's designed to be a drop-in
replacement for the original MCP server script.

Usage:
    python mcp_server.py
    # or
    fastmcp run mcp_server.py
"""

import sys
from pathlib import Path

# Add the current directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

try:
    from audio_analysis.api.mcp_server import mcp, MCP_AVAILABLE
    
    if __name__ == "__main__":
        if not MCP_AVAILABLE:
            print("Error: FastMCP not available. Install with: pip install fastmcp")
            sys.exit(1)
        
        print("Starting FastMCP server for Synthesizer Music Analysis...")
        print("Server will be available for MCP client connections.")
        print("\nSupported MCP tools:")
        print("  - analyze_audio_mood: Analyze mood and character of audio files")
        print("  - analyze_audio_phases: Analyze musical phases/sections")
        print("  - recommend_song_sequence: Generate optimal listening sequence")
        print("  - analyze_audio_clusters: Perform clustering analysis")
        print("  - comprehensive_audio_analysis: Full analysis with export options")
        print("  - get_supported_formats: Get format and descriptor information")
        print("\nPress Ctrl+C to stop the server.")
        
        try:
            # Run the MCP server on default host/port
            mcp.run()
        except KeyboardInterrupt:
            print("\nMCP server stopped.")
            sys.exit(0)
        except Exception as e:
            print(f"Error running MCP server: {e}")
            sys.exit(1)
        
except ImportError as e:
    print(f"Error: Failed to import audio analysis modules: {e}")
    print("Make sure you have installed the required dependencies:")
    print("pip install -r requirements.txt")
    print("pip install fastmcp")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)