"""
API modules for the audio analysis system.

This package contains the main interfaces and integration points for the
audio analysis toolkit, including the primary analyzer class and MCP
server integration.

Modules:
- analyzer: Main AudioAnalyzer class that orchestrates the complete analysis
- mcp_server: FastMCP server integration for remote analysis capabilities
"""

from .analyzer import AudioAnalyzer
from .mcp_server import MCPAudioAnalyzer

__all__ = [
    'AudioAnalyzer',
    'MCPAudioAnalyzer'
]