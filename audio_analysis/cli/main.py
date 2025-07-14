"""
Command-Line Interface for Audio Analysis Toolkit

This module provides a comprehensive command-line interface for the audio
analysis toolkit, supporting both local directory analysis and MCP server
modes with extensive configuration options.

The CLI is designed to be user-friendly while providing access to all
advanced features of the toolkit. It includes progress reporting, error
handling, and flexible output options.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional

# Add the parent directory to the path to import our modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from audio_analysis.api.analyzer import AudioAnalyzer
from audio_analysis.utils.audio_io import get_supported_formats, estimate_processing_time


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments with comprehensive options.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Synthesizer Music Analysis Toolkit - Comprehensive audio analysis for electronic music",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a directory of audio files
  python -m audio_analysis.cli.main /path/to/audio/files
  
  # Run with clustering and sequence analysis
  python -m audio_analysis.cli.main /path/to/audio --clusters 5 --sequence
  
  # Export results in multiple formats
  python -m audio_analysis.cli.main /path/to/audio --export-format all
  
  # Start MCP server
  python -m audio_analysis.cli.main --mode mcp
  
  # Get format information
  python -m audio_analysis.cli.main --info

Supported formats: WAV, AIFF, MP3
        """
    )
    
    # Main operation mode
    parser.add_argument(
        "--mode", 
        choices=["local", "mcp"], 
        default="local",
        help="Operating mode: local directory analysis or MCP server"
    )
    
    # Input directory (required for local mode)
    parser.add_argument(
        "directory", 
        nargs="?",
        help="Path to directory containing audio files (required for local mode)"
    )
    
    # Analysis options
    parser.add_argument(
        "--clusters", 
        type=int, 
        metavar="N",
        help="Number of clusters for grouping analysis (auto-determined if not specified)"
    )
    
    parser.add_argument(
        "--sequence", 
        action="store_true",
        help="Generate optimal listening sequence recommendations"
    )
    
    parser.add_argument(
        "--sample-rate", 
        type=int, 
        metavar="RATE",
        help="Target sample rate for analysis (default: keep original)"
    )
    
    # Export options
    parser.add_argument(
        "--export-format", 
        choices=["csv", "json", "markdown", "all"], 
        default="all",
        help="Export format for results (default: all)"
    )
    
    parser.add_argument(
        "--export-dir", 
        type=Path, 
        metavar="PATH",
        defualt="./reports"
        help="Directory for exported results (default: auto-generated timestamped directory)"
    )
    
    parser.add_argument(
        "--no-plots", 
        action="store_true",
        help="Skip generating visualization plots"
    )
    
    # Output options
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true",
        help="Enable verbose output with detailed progress information"
    )
    
    parser.add_argument(
        "--quiet", "-q", 
        action="store_true",
        help="Suppress non-essential output"
    )
    
    # Information options
    parser.add_argument(
        "--info", 
        action="store_true",
        help="Show supported formats and analysis capabilities"
    )
    
    parser.add_argument(
        "--estimate", 
        action="store_true",
        help="Estimate processing time for directory (no analysis performed)"
    )
    
    # MCP server options
    parser.add_argument(
        "--host", 
        default="localhost",
        help="Host for MCP server (default: localhost)"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000,
        help="Port for MCP server (default: 8000)"
    )
    
    return parser.parse_args()


def print_format_info():
    """Print information about supported formats and capabilities."""
    format_info = get_supported_formats()
    
    print("=" * 60)
    print("AUDIO ANALYSIS TOOLKIT - FORMAT INFORMATION")
    print("=" * 60)
    
    print("\nSupported Audio Formats:")
    for fmt in format_info['formats']:
        description = format_info['descriptions'][fmt]
        print(f"  {fmt:6} - {description}")
    
    print(f"\nRecommended Formats:")
    print(f"  Best Quality: {', '.join(format_info['recommendations']['best_quality'])}")
    print(f"  Most Compatible: {', '.join(format_info['recommendations']['most_compatible'])}")
    print(f"  Recommended: {', '.join(format_info['recommendations']['recommended'])}")
    
    print(f"\nFile Constraints:")
    print(f"  Maximum file size: {format_info['limitations']['max_file_size_mb']} MB")
    print(f"  Minimum duration: {format_info['limitations']['min_duration_seconds']} seconds")
    print(f"  Maximum duration: {format_info['limitations']['max_duration_minutes']} minutes")
    
    print(f"\nAnalysis Capabilities:")
    print(f"  - 80+ audio features per track")
    print(f"  - 17 creative mood descriptors")
    print(f"  - 9 character/synthesis type tags")
    print(f"  - Musical phase detection and analysis")
    print(f"  - K-means clustering for track grouping")
    print(f"  - Intelligent sequence recommendations")
    print(f"  - Multiple export formats (CSV, JSON, Markdown)")
    print(f"  - Publication-quality visualizations")


def run_local_analysis(args: argparse.Namespace) -> int:
    """
    Run local directory analysis.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    if not args.directory:
        print("Error: Directory path required for local mode")
        print("Usage: python -m audio_analysis.cli.main <directory_path>")
        return 1
    
    directory_path = Path(args.directory)
    
    # Validate directory
    if not directory_path.exists():
        print(f"Error: Directory does not exist: {directory_path}")
        return 1
    
    if not directory_path.is_dir():
        print(f"Error: Path is not a directory: {directory_path}")
        return 1
    
    # Show estimation if requested
    if args.estimate:
        estimation = estimate_processing_time(directory_path)
        if 'error' in estimation:
            print(f"Error: {estimation['error']}")
            return 1
        
        print(f"Processing Time Estimation for: {directory_path}")
        print(f"  Files found: {estimation['total_files']}")
        print(f"  Estimated audio duration: {estimation['estimated_audio_duration_minutes']:.1f} minutes")
        print(f"  Estimated processing time: {estimation['estimated_processing_time_minutes']:.1f} minutes")
        print(f"  Recommendation: {estimation['recommendation']}")
        return 0
    
    try:
        # Initialize analyzer
        if not args.quiet:
            print(f"Initializing audio analyzer for: {directory_path}")
        
        analyzer = AudioAnalyzer(directory_path, args.sample_rate)
        
        # Run analysis
        if not args.quiet:
            print("Running comprehensive audio analysis...")
        
        df = analyzer.analyze_directory()
        
        if df is None or df.empty:
            print("Error: No audio files could be processed")
            return 1
        
        # Perform clustering if requested or by default
        n_clusters = args.clusters
        if not args.quiet:
            print("Performing clustering analysis...")
        
        cluster_labels, cluster_centers, feature_names = analyzer.perform_clustering(n_clusters)
        
        # Generate sequence recommendations if requested or by default
        if args.sequence or args.sequence is None:  # Default to True
            if not args.quiet:
                print("Generating sequence recommendations...")
            
            sequence_recommendations = analyzer.recommend_sequence()
        
        # Export results
        if not args.quiet:
            print("Exporting analysis results...")
        
        export_results = analyzer.export_comprehensive_analysis(
            export_dir=args.export_dir,
            show_plots=not args.no_plots
        )
        
        # Print summary
        if not args.quiet:
            print("\n" + "=" * 60)
            print("ANALYSIS COMPLETE")
            print("=" * 60)
            
            stats = analyzer.get_analysis_statistics()
            print(f"Files processed: {stats['data_stats']['total_tracks']}")
            print(f"Features extracted: {stats['data_stats']['total_features']}")
            print(f"Phases detected: {stats['data_stats']['total_phases']}")
            print(f"Clusters created: {stats.get('clustering_stats', {}).get('num_clusters', 'N/A')}")
            print(f"Export directory: {export_results['export_directory']}")
            
            if args.verbose:
                print(f"\nDetailed Statistics:")
                print(f"  Average track duration: {stats['data_stats']['avg_track_duration']:.1f} seconds")
                print(f"  Total collection duration: {stats['data_stats']['total_collection_duration']/60:.1f} minutes")
                print(f"  Average phases per track: {stats['data_stats']['total_phases']/stats['data_stats']['total_tracks']:.1f}")
                
                if 'mood_stats' in stats:
                    print(f"  Dominant mood: {stats['mood_stats']['dominant_mood']}")
                    print(f"  Unique moods: {stats['mood_stats']['unique_moods']}")
        
        return 0
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def run_mcp_server(args: argparse.Namespace) -> int:
    """
    Run MCP server mode.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        from audio_analysis.api.mcp_server import mcp, MCP_AVAILABLE
        
        if not MCP_AVAILABLE:
            print("Error: FastMCP not available. Install with: pip install fastmcp")
            return 1
        
        print("Starting FastMCP server for Synthesizer Music Analysis...")
        print(f"Server will be available at: http://{args.host}:{args.port}")
        print("\nSupported MCP tools:")
        print("  - analyze_audio_mood: Analyze mood and character of audio files")
        print("  - analyze_audio_phases: Analyze musical phases/sections")
        print("  - recommend_song_sequence: Generate optimal listening sequence")
        print("  - analyze_audio_clusters: Perform clustering analysis")
        print("  - comprehensive_audio_analysis: Full analysis with export options")
        print("  - get_supported_formats: Get format and descriptor information")
        print("\nPress Ctrl+C to stop the server.")
        
        # Run the MCP server
        mcp.run(host=args.host, port=args.port)
        
        return 0
        
    except ImportError as e:
        print(f"Error: MCP server dependencies not available: {str(e)}")
        print("Install with: pip install fastmcp")
        return 1
    except KeyboardInterrupt:
        print("\nMCP server stopped.")
        return 0
    except Exception as e:
        print(f"Error running MCP server: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def main() -> int:
    """
    Main entry point for the CLI application.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    args = parse_arguments()
    
    # Handle information requests
    if args.info:
        print_format_info()
        return 0
    
    # Validate argument combinations
    if args.mode == "local" and not args.directory and not args.estimate:
        print("Error: Directory path required for local mode")
        print("Use --help for usage information")
        return 1
    
    if args.quiet and args.verbose:
        print("Error: Cannot use both --quiet and --verbose options")
        return 1
    
    # Route to appropriate function based on mode
    if args.mode == "mcp":
        return run_mcp_server(args)
    else:
        return run_local_analysis(args)


if __name__ == "__main__":
    sys.exit(main())