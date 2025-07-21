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
- Parallel processing for scalable analysis across multiple CPU cores
- Tensor-optimized operations for hardware acceleration (Tenstorrent, GPU)
- Streaming processing for large audio files and datasets

Usage:
    # Standard analysis
    from audio_analysis import AudioAnalyzer
    
    analyzer = AudioAnalyzer('/path/to/audio/files')
    results = analyzer.analyze_directory()
    analyzer.export_comprehensive_analysis(export_format="all")
    
    # Parallel processing for better performance
    from audio_analysis import ParallelAudioAnalyzer
    
    analyzer = ParallelAudioAnalyzer('/path/to/audio/files')
    results = analyzer.analyze_directory()
    analyzer.export_comprehensive_analysis(export_format="markdown", base_name="my_analysis")
"""

from .api.analyzer import AudioAnalyzer
from .api.parallel_analyzer import ParallelAudioAnalyzer
from .api.mcp_server import MCPAudioAnalyzer
from .analysis.descriptors import MoodDescriptors, CharacterTags

# Parallel processing components
from .core.parallel_feature_extraction import ParallelFeatureExtractor, ProcessingConfig
from .core.parallel_clustering import ParallelKMeansClusterer, ClusteringConfig
from .core.tensor_operations import TensorFeatureExtractor, TensorBatch

__version__ = "2.0.0"
__author__ = "Audio Analysis Toolkit Team"
__email__ = "support@audioanalysis.com"

__all__ = [
    'AudioAnalyzer',
    'ParallelAudioAnalyzer',
    'MCPAudioAnalyzer', 
    'MoodDescriptors',
    'CharacterTags',
    'ParallelFeatureExtractor',
    'ProcessingConfig',
    'ParallelKMeansClusterer',
    'ClusteringConfig',
    'TensorFeatureExtractor',
    'TensorBatch'
]