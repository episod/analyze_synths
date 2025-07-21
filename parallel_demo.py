#!/usr/bin/env python3
"""
Parallel Audio Analysis Demo

This script demonstrates the new parallel processing capabilities designed
for scalable audio analysis and future hardware acceleration including
Tenstorrent processors.

Key Features Demonstrated:
1. Parallel feature extraction with configurable batch sizes
2. Tensor-optimized data structures for hardware acceleration
3. Streaming processing for large audio files
4. Distributed clustering with performance metrics
5. Comprehensive analysis with parallel processing statistics

Usage:
    python parallel_demo.py <audio_directory> [options]

Examples:
    # Basic parallel processing
    python parallel_demo.py /path/to/audio/files
    
    # With custom configuration
    python parallel_demo.py /path/to/audio/files --workers 8 --batch-size 16
    
    # Enable tensor optimizations
    python parallel_demo.py /path/to/audio/files --enable-tensor --device cpu
    
    # Streaming mode for large files
    python parallel_demo.py /path/to/audio/files --enable-streaming
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Optional

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from audio_analysis.core.parallel_feature_extraction import ProcessingConfig, ParallelFeatureExtractor
from audio_analysis.core.parallel_clustering import ClusteringConfig, ParallelKMeansClusterer
from audio_analysis.core.tensor_operations import TensorFeatureExtractor
from audio_analysis.api.parallel_analyzer import ParallelAudioAnalyzer


def create_processing_config(args) -> ProcessingConfig:
    """Create processing configuration from command line arguments."""
    return ProcessingConfig(
        max_workers=args.workers,
        batch_size=args.batch_size,
        use_multiprocessing=args.multiprocessing,
        enable_tensor_optimization=args.enable_tensor,
        memory_limit_mb=args.memory_limit,
        sample_rate=args.sample_rate
    )


def create_clustering_config(args) -> ClusteringConfig:
    """Create clustering configuration from command line arguments."""
    return ClusteringConfig(
        max_workers=args.workers,
        batch_size=args.batch_size * 100,  # Larger batch size for clustering
        use_mini_batch=args.enable_tensor,
        device=args.device,
        enable_tensor_optimization=args.enable_tensor,
        memory_limit_mb=args.memory_limit
    )


def demo_parallel_feature_extraction(directory: Path, config: ProcessingConfig):
    """Demonstrate parallel feature extraction capabilities."""
    print("\n" + "="*60)
    print("PARALLEL FEATURE EXTRACTION DEMO")
    print("="*60)
    
    # Initialize parallel feature extractor
    extractor = ParallelFeatureExtractor(config)
    
    # Discover audio files
    audio_files = []
    for ext in ['*.wav', '*.mp3', '*.aiff']:
        audio_files.extend(list(directory.glob(ext)))
    
    if not audio_files:
        print("No audio files found in directory")
        return None
    
    print(f"Found {len(audio_files)} audio files")
    
    # Get processing time estimate
    estimate = extractor.estimate_processing_time(audio_files)
    print(f"Estimated processing time: {estimate['estimated_time']:.1f}s")
    print(f"Parallel speedup: {estimate['parallel_speedup']:.1f}x")
    
    # Extract features in parallel
    start_time = time.time()
    features = extractor.extract_features_batch(audio_files)
    processing_time = time.time() - start_time
    
    print(f"Processed {len(features)} files in {processing_time:.2f}s")
    print(f"Throughput: {len(features) / processing_time:.1f} files/second")
    
    # Show processing statistics
    stats = extractor.get_processing_stats()
    print(f"Configuration: {stats['config']}")
    
    return features


def demo_tensor_operations(directory: Path, device: str = "cpu"):
    """Demonstrate tensor-optimized operations."""
    print("\n" + "="*60)
    print("TENSOR OPERATIONS DEMO")
    print("="*60)
    
    # Initialize tensor feature extractor
    extractor = TensorFeatureExtractor(device=device)
    
    # Discover audio files
    audio_files = []
    for ext in ['*.wav', '*.mp3', '*.aiff']:
        audio_files.extend(list(directory.glob(ext)))
    
    if not audio_files:
        print("No audio files found")
        return None
    
    print(f"Processing {len(audio_files)} files with tensor operations")
    print(f"Device: {device}")
    
    # Extract features using tensor operations
    start_time = time.time()
    features = extractor.extract_features_from_paths(audio_files[:10])  # Limit for demo
    processing_time = time.time() - start_time
    
    print(f"Tensor processing completed in {processing_time:.2f}s")
    print(f"Device info: {extractor.get_device_info()}")
    
    return features


def demo_parallel_clustering(features_data, config: ClusteringConfig):
    """Demonstrate parallel clustering capabilities."""
    print("\n" + "="*60)
    print("PARALLEL CLUSTERING DEMO")
    print("="*60)
    
    if not features_data:
        print("No features available for clustering")
        return None
    
    # Convert features to DataFrame
    import pandas as pd
    df = pd.DataFrame(features_data)
    
    print(f"Clustering {len(df)} tracks with {len(df.columns)} features")
    
    # Initialize parallel clusterer
    clusterer = ParallelKMeansClusterer(config)
    
    # Perform clustering
    start_time = time.time()
    result = clusterer.fit_predict(df)
    clustering_time = time.time() - start_time
    
    print(f"Clustering completed in {clustering_time:.2f}s")
    print(f"Found {result.n_clusters} clusters")
    print(f"Silhouette score: {result.silhouette_score:.3f}")
    print(f"Calinski-Harabasz score: {result.calinski_harabasz_score:.1f}")
    
    # Analyze clusters
    cluster_analysis = clusterer.analyze_clusters(df, result)
    
    print("\nCluster Summary:")
    for cluster_name, analysis in cluster_analysis.items():
        print(f"  {cluster_name}: {analysis['size']} tracks ({analysis['percentage']:.1f}%)")
    
    return result, cluster_analysis


def demo_complete_parallel_analysis(directory: Path, config: ProcessingConfig):
    """Demonstrate complete parallel analysis pipeline."""
    print("\n" + "="*60)
    print("COMPLETE PARALLEL ANALYSIS DEMO")
    print("="*60)
    
    # Initialize parallel analyzer
    analyzer = ParallelAudioAnalyzer(directory, config)
    
    # Perform complete analysis
    start_time = time.time()
    df = analyzer.analyze_directory(show_progress=True)
    analysis_time = time.time() - start_time
    
    if df is None:
        print("Analysis failed")
        return
    
    print(f"Complete analysis finished in {analysis_time:.2f}s")
    
    # Perform clustering
    cluster_labels, cluster_centers, feature_names = analyzer.perform_clustering()
    
    # Generate sequence recommendations
    sequence = analyzer.recommend_sequence()
    
    # Show comprehensive statistics
    stats = analyzer.get_processing_statistics()
    print("\nProcessing Statistics:")
    print(f"  Parallel speedup: {stats['parallel_processing_stats']['parallel_speedup']:.1f}x")
    print(f"  Throughput: {stats['parallel_processing_stats']['throughput']:.1f} files/second")
    print(f"  Success rate: {stats['parallel_processing_stats']['success_rate']:.1f}%")
    
    # Export results
    export_dir = Path(f"parallel_analysis_demo_{int(time.time())}")
    export_info = analyzer.export_comprehensive_analysis(export_dir, export_format="all")
    
    print(f"\nResults exported to: {export_dir}")
    print(f"Export files: {len(export_info['data_exports'])} data files, {len(export_info['visualization_exports'])} visualizations")


def main():
    """Main demo function."""
    parser = argparse.ArgumentParser(description='Parallel Audio Analysis Demo')
    parser.add_argument('directory', type=Path, help='Directory containing audio files')
    parser.add_argument('--workers', type=int, default=4, help='Number of parallel workers')
    parser.add_argument('--batch-size', type=int, default=8, help='Batch size for processing')
    parser.add_argument('--multiprocessing', action='store_true', help='Use multiprocessing')
    parser.add_argument('--enable-tensor', action='store_true', help='Enable tensor optimizations')
    parser.add_argument('--enable-streaming', action='store_true', help='Enable streaming processing')
    parser.add_argument('--device', choices=['cpu', 'tenstorrent'], default='cpu', help='Processing device')
    parser.add_argument('--memory-limit', type=int, default=2048, help='Memory limit in MB')
    parser.add_argument('--sample-rate', type=int, help='Target sample rate')
    parser.add_argument('--demo', choices=['extraction', 'tensor', 'clustering', 'complete'], 
                       default='complete', help='Demo to run')
    
    args = parser.parse_args()
    
    # Validate directory
    if not args.directory.exists():
        print(f"Error: Directory does not exist: {args.directory}")
        sys.exit(1)
    
    if not args.directory.is_dir():
        print(f"Error: Path is not a directory: {args.directory}")
        sys.exit(1)
    
    # Create configurations
    processing_config = create_processing_config(args)
    clustering_config = create_clustering_config(args)
    
    print("Parallel Audio Analysis Demo")
    print(f"Directory: {args.directory}")
    print(f"Workers: {args.workers}")
    print(f"Batch size: {args.batch_size}")
    print(f"Device: {args.device}")
    print(f"Tensor optimization: {args.enable_tensor}")
    
    # Run selected demo
    if args.demo == 'extraction':
        demo_parallel_feature_extraction(args.directory, processing_config)
    
    elif args.demo == 'tensor':
        demo_tensor_operations(args.directory, args.device)
    
    elif args.demo == 'clustering':
        # First extract features
        features = demo_parallel_feature_extraction(args.directory, processing_config)
        if features:
            demo_parallel_clustering(features, clustering_config)
    
    elif args.demo == 'complete':
        demo_complete_parallel_analysis(args.directory, processing_config)
    
    print("\nDemo completed!")


if __name__ == '__main__':
    main()