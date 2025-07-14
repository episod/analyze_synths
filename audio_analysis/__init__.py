"""
Synthesizer Music Analysis Toolkit

A comprehensive Python package for analyzing synthesizer music with creative descriptors.
Designed specifically for composers and electronic music creators to understand their work
through mood analysis, phase detection, clustering, and intelligent sequencing.

Key Features:
- Creative mood classification using 17 descriptors (spacey, organic, synthetic, etc.)
- Musical phase detection for song structure analysis
- K-means clustering for track grouping and playlist creation
- Intelligent song sequencing based on musical flow principles
- Export to multiple formats (CSV, JSON, Markdown) optimized for LLM consumption
- FastMCP server integration for remote analysis capabilities

Usage:
    from audio_analysis import AudioAnalyzer
    
    analyzer = AudioAnalyzer('/path/to/audio/files')
    results = analyzer.analyze_directory()
    analyzer.export_comprehensive_analysis()
"""

from .api.analyzer import AudioAnalyzer
from .api.mcp_server import MCPAudioAnalyzer
from .analysis.descriptors import MoodDescriptors, CharacterTags

__version__ = "1.0.0"
__author__ = "Audio Analysis Toolkit Team"
__email__ = "support@audioanalysis.com"

__all__ = [
    'AudioAnalyzer',
    'MCPAudioAnalyzer', 
    'MoodDescriptors',
    'CharacterTags'
]