"""
Main Audio Analyzer Class

This module contains the primary AudioAnalyzer class that orchestrates the
complete audio analysis pipeline. It integrates all the specialized analysis
components into a cohesive system for synthesizer music analysis.

The AudioAnalyzer serves as the main entry point for the toolkit, providing:
- Comprehensive audio analysis with creative descriptors
- Musical phase detection and structural analysis
- Clustering for track grouping and similarity analysis
- Intelligent song sequencing recommendations
- Multiple export formats (CSV, JSON, Markdown)
- Visualization generation for analysis results

The class is designed to be the primary interface that users interact with,
hiding the complexity of the underlying analysis modules while providing
extensive customization options for advanced users.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import json

# Import core analysis modules
from ..core.feature_extraction import FeatureExtractor
from ..core.phase_detection import PhaseDetector
from ..core.clustering import AudioClusterer
from ..core.sequencing import SequenceRecommender

# Import analysis modules
from ..analysis.mood_analyzer import MoodAnalyzer
from ..analysis.character_analyzer import CharacterAnalyzer

# Import utility modules
from ..utils.audio_io import AudioLoader
from ..utils.data_processing import DataProcessor
from ..utils.visualization import Visualizer

# Import exporters
from ..exporters.csv_exporter import CSVExporter
from ..exporters.json_exporter import JSONExporter
from ..exporters.markdown_exporter import MarkdownExporter

# Import export utilities
from ..utils.export_utils import create_export_directory, create_export_subdirectories


class AudioAnalyzer:
    """
    Main audio analysis orchestrator for synthesizer music.
    
    This class provides a comprehensive analysis system that combines multiple
    specialized analysis modules into a cohesive toolkit. It handles the entire
    analysis pipeline from audio loading to final export and visualization.
    
    The analysis process follows these stages:
    1. Audio loading and validation
    2. Feature extraction (spectral, temporal, harmonic)
    3. Phase detection and structural analysis
    4. Creative mood and character analysis
    5. Clustering for similarity grouping
    6. Sequence recommendation for optimal ordering
    7. Export and visualization generation
    
    Key Features:
    - Processes WAV, AIFF, and MP3 files
    - Extracts 80+ audio features per track
    - Detects musical phases with mood analysis
    - Provides 17 creative mood descriptors
    - Identifies synthesis types and characteristics
    - Groups tracks using intelligent clustering
    - Recommends optimal listening sequences
    - Exports results in multiple formats
    - Generates publication-quality visualizations
    """
    
    def __init__(self, directory_path: Path, sample_rate: Optional[int] = None):
        """
        Initialize the AudioAnalyzer with a directory of audio files.
        
        This constructor sets up all the analysis components and prepares
        the system for processing audio files. It validates the directory
        and initializes the various analysis modules with appropriate settings.
        
        Args:
            directory_path: Path to directory containing audio files
            sample_rate: Target sample rate for analysis (None = keep original)
        """
        # Validate and store directory path
        self.directory_path = Path(directory_path)
        if not self.directory_path.exists():
            raise ValueError(f"Directory does not exist: {directory_path}")
        if not self.directory_path.is_dir():
            raise ValueError(f"Path is not a directory: {directory_path}")
        
        # Initialize core analysis components
        # These components handle the fundamental audio analysis tasks
        self.feature_extractor = FeatureExtractor(sample_rate)
        self.phase_detector = PhaseDetector()
        self.clusterer = AudioClusterer()
        self.sequencer = SequenceRecommender()
        
        # Initialize analysis components
        # These components provide creative interpretation of technical features
        self.mood_analyzer = MoodAnalyzer()
        self.character_analyzer = CharacterAnalyzer()
        
        # Initialize utility components
        # These components handle file I/O, data processing, and visualization
        self.audio_loader = AudioLoader(sample_rate)
        self.data_processor = DataProcessor()
        self.visualizer = Visualizer()
        
        # Initialize exporters
        # These components handle different output formats
        self.csv_exporter = CSVExporter()
        self.json_exporter = JSONExporter()
        self.markdown_exporter = MarkdownExporter()
        
        # Initialize data storage
        # These attributes store the analysis results
        self.audio_features = []  # List of feature dictionaries
        self.phase_data = []      # List of phase analysis results
        self.df = None           # Main DataFrame with all results
        self.cluster_labels = None  # Cluster assignments
        self.cluster_analysis = None  # Cluster analysis results
        self.sequence_recommendations = None  # Sequence recommendations
        
        # Analysis statistics
        self.analysis_stats = {
            'files_found': 0,
            'files_processed': 0,
            'processing_errors': 0,
            'start_time': None,
            'end_time': None
        }
    
    def analyze_directory(self) -> Optional[pd.DataFrame]:
        """
        Analyze all audio files in the directory.
        
        This method orchestrates the complete analysis pipeline:
        1. Discovers and validates audio files in the directory
        2. Loads each audio file using robust error handling
        3. Extracts comprehensive features from each file
        4. Performs phase detection for structural analysis
        5. Analyzes mood and character for creative insights
        6. Combines all results into a structured DataFrame
        
        The method is designed to be robust against various issues:
        - Corrupted or unsupported audio files
        - Feature extraction failures
        - Memory constraints with large collections
        - Inconsistent file formats and characteristics
        
        Returns:
            DataFrame with comprehensive analysis results or None if failed
        """
        # Record analysis start time
        self.analysis_stats['start_time'] = datetime.now()
        
        # Stage 1: Audio File Discovery
        # Find all supported audio files in the directory
        print(f"Analyzing audio files in: {self.directory_path}")
        
        # Get list of audio files from the directory
        audio_files = self._discover_audio_files()
        if not audio_files:
            print("No supported audio files found")
            return None
        
        self.analysis_stats['files_found'] = len(audio_files)
        print(f"Found {len(audio_files)} audio files. Processing...")
        
        # Stage 2: Audio Analysis Pipeline
        # Process each audio file through the complete analysis pipeline
        for i, file_path in enumerate(audio_files):
            print(f"Processing {i+1}/{len(audio_files)}: {file_path.name}")
            
            try:
                # Load and validate audio file
                audio_result = self.audio_loader.load_audio(file_path)
                if audio_result is None:
                    print(f"Failed to load: {file_path.name}")
                    self.analysis_stats['processing_errors'] += 1
                    continue
                
                audio_data, sample_rate = audio_result
                
                # Extract comprehensive features
                features = self._extract_comprehensive_features(file_path, audio_data, sample_rate)
                if features is None:
                    print(f"Failed to extract features: {file_path.name}")
                    self.analysis_stats['processing_errors'] += 1
                    continue
                
                # Store results
                self.audio_features.append(features)
                self.analysis_stats['files_processed'] += 1
                
            except Exception as e:
                print(f"Error processing {file_path.name}: {str(e)}")
                self.analysis_stats['processing_errors'] += 1
                continue
        
        # Stage 3: Results Compilation
        # Convert results to DataFrame and perform final processing
        if not self.audio_features:
            print("No files were successfully processed")
            return None
        
        # Create DataFrame from features
        self.df = pd.DataFrame(self.audio_features)
        
        # Clean and validate the DataFrame
        self.df = self.data_processor.clean_dataframe(self.df)
        
        # Record analysis end time
        self.analysis_stats['end_time'] = datetime.now()
        
        # Print summary
        self._print_analysis_summary()
        
        return self.df
    
    def _discover_audio_files(self) -> List[Path]:
        """
        Discover all supported audio files in the directory.
        
        This method scans the directory for audio files with supported
        extensions and validates their basic properties.
        
        Returns:
            List of paths to valid audio files
        """
        # Supported audio file extensions
        supported_extensions = ['*.wav', '*.WAV', '*.aiff', '*.AIFF', '*.aif', '*.AIF', '*.mp3', '*.MP3']
        
        # Find all audio files
        audio_files = []
        for extension in supported_extensions:
            audio_files.extend(list(self.directory_path.glob(extension)))
        
        # Validate and filter files
        valid_files = []
        for file_path in audio_files:
            if file_path.is_file() and file_path.stat().st_size > 0:
                valid_files.append(file_path)
        
        return sorted(valid_files)
    
    def _extract_comprehensive_features(self, file_path: Path, audio_data: np.ndarray, 
                                      sample_rate: int) -> Optional[Dict[str, Any]]:
        """
        Extract comprehensive features from an audio file.
        
        This method orchestrates the complete feature extraction pipeline,
        combining technical audio features with creative analysis.
        
        Args:
            file_path: Path to the audio file
            audio_data: Audio time series data
            sample_rate: Sample rate of the audio
            
        Returns:
            Dictionary with comprehensive features or None if failed
        """
        try:
            # Stage 1: Basic Feature Extraction
            # Extract fundamental audio characteristics
            features = self.feature_extractor.extract_features(file_path)
            if features is None:
                return None
            
            # Stage 2: Phase Detection and Analysis
            # Detect musical phases and analyze their characteristics
            phases, times, rms_smooth, spectral_smooth, change_signal = self.phase_detector.detect_phases(
                audio_data, sample_rate
            )
            
            # Store phase data for later use
            phase_info = {
                'filename': file_path.name,
                'total_duration': features['duration'],
                'num_phases': len(phases),
                'phases': phases
            }
            self.phase_data.append(phase_info)
            
            # Stage 3: Creative Mood Analysis
            # Analyze the overall mood using creative descriptors
            mood_descriptors, primary_mood, mood_confidence = self.mood_analyzer.analyze_track_mood(features)
            
            # Stage 4: Character Analysis
            # Identify synthesis type and character
            character_tags, primary_character, character_confidence = self.character_analyzer.analyze_track_character(features)
            
            # Stage 5: Phase-Level Mood Analysis
            # Analyze mood for each detected phase
            for phase in phases:
                phase_mood, phase_confidence = self.mood_analyzer.analyze_mood(
                    phase['phase_data'], phase['basic_spectral']
                )
                phase['mood_descriptors'] = phase_mood
                phase['mood_confidence'] = phase_confidence
            
            # Stage 6: Structural Analysis
            # Calculate structural characteristics from phases
            structural_features = self._calculate_structural_features(phases)
            
            # Stage 7: Combine All Features
            # Merge all analysis results into a comprehensive feature set
            comprehensive_features = {
                **features,  # Basic audio features
                **structural_features,  # Structural characteristics
                'mood_descriptors': ', '.join(mood_descriptors),
                'primary_mood': primary_mood,
                'mood_confidence': mood_confidence.get(primary_mood, 0),
                'character_tags': ', '.join(character_tags),
                'primary_character': primary_character,
                'character_confidence': character_confidence.get(primary_character, 0),
                'num_phases': len(phases),
                'phase_analysis_available': True
            }
            
            # Ensure all values are proper Python types
            from ..utils.type_conversion import ensure_python_types
            return ensure_python_types(comprehensive_features)
            
        except Exception as e:
            print(f"Error in comprehensive feature extraction for {file_path.name}: {str(e)}")
            return None
    
    def _calculate_structural_features(self, phases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate structural features from phase analysis.
        
        This method derives higher-level structural characteristics from
        the detected phases, providing insights into the compositional
        structure of the music.
        
        Args:
            phases: List of detected phases
            
        Returns:
            Dictionary with structural features
        """
        if not phases:
            return {}
        
        # Calculate energy and brightness ranges across phases
        from ..utils.type_conversion import safe_float_convert
        energies = [safe_float_convert(phase['avg_energy']) for phase in phases]
        brightnesses = [safe_float_convert(phase['avg_brightness']) for phase in phases]
        
        # Structural characteristics
        structural_features = {
            'energy_range': max(energies) - min(energies),
            'brightness_range': max(brightnesses) - min(brightnesses),
            'avg_phase_duration': np.mean([safe_float_convert(phase['duration']) for phase in phases]),
            'phase_duration_std': np.std([safe_float_convert(phase['duration']) for phase in phases]),
            'has_climax': any('Climax' in phase['phase_type'] for phase in phases),
            'has_breakdown': any('Breakdown' in phase['phase_type'] or 'Quiet' in phase['phase_type'] for phase in phases),
            'has_build_up': any('Build-up' in phase['phase_type'] for phase in phases),
            'structural_complexity': len(set(phase['phase_type'] for phase in phases)),
            'energy_progression': self._calculate_energy_progression(phases),
            'brightness_progression': self._calculate_brightness_progression(phases)
        }
        
        return structural_features
    
    def _calculate_energy_progression(self, phases: List[Dict[str, Any]]) -> str:
        """
        Calculate the energy progression pattern across phases.
        
        Args:
            phases: List of detected phases
            
        Returns:
            String describing energy progression
        """
        if len(phases) < 2:
            return 'static'
        
        from ..utils.statistics import calculate_progression_trend
        from ..utils.type_conversion import safe_float_convert
        
        energies = [safe_float_convert(phase['avg_energy']) for phase in phases]
        
        # Use shared utility for trend calculation
        trend = calculate_progression_trend(energies)
        
        # Map to energy-specific terms
        if trend == 'increasing':
            return 'building'
        elif trend == 'decreasing':
            return 'declining'
        else:
            return 'stable'
    
    def _calculate_brightness_progression(self, phases: List[Dict[str, Any]]) -> str:
        """
        Calculate the brightness progression pattern across phases.
        
        Args:
            phases: List of detected phases
            
        Returns:
            String describing brightness progression
        """
        if len(phases) < 2:
            return 'static'
        
        from ..utils.statistics import calculate_progression_trend
        from ..utils.type_conversion import safe_float_convert
        
        brightnesses = [safe_float_convert(phase['avg_brightness']) for phase in phases]
        
        # Use shared utility for trend calculation
        trend = calculate_progression_trend(brightnesses)
        
        # Map to brightness-specific terms
        if trend == 'increasing':
            return 'brightening'
        elif trend == 'decreasing':
            return 'darkening'
        else:
            return 'stable'
    
    def perform_clustering(self, n_clusters: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        Perform clustering analysis on the processed tracks.
        
        This method groups tracks with similar characteristics using
        K-means clustering. It automatically determines the optimal
        number of clusters if not specified.
        
        Args:
            n_clusters: Number of clusters (None = auto-determine)
            
        Returns:
            Tuple containing cluster labels, cluster centers, and feature names
        """
        if self.df is None or self.df.empty:
            raise ValueError("No data available for clustering. Run analyze_directory() first.")
        
        # Perform clustering using the clusterer
        cluster_labels, cluster_centers, feature_names = self.clusterer.perform_clustering(
            self.df, n_clusters
        )
        
        # Store results
        self.cluster_labels = cluster_labels
        
        # Analyze cluster characteristics
        self.cluster_analysis = self.clusterer.analyze_clusters(self.df, cluster_labels)
        
        return cluster_labels, cluster_centers, feature_names
    
    def recommend_sequence(self) -> List[Dict[str, Any]]:
        """
        Generate optimal sequence recommendations for the analyzed tracks.
        
        This method uses the sequence recommender to create an optimal
        listening order based on musical flow principles.
        
        Returns:
            List of sequence recommendations
        """
        if self.df is None or self.df.empty:
            raise ValueError("No data available for sequencing. Run analyze_directory() first.")
        
        # Generate sequence recommendations
        self.sequence_recommendations = self.sequencer.recommend_sequence(self.df)
        
        return self.sequence_recommendations
    
    def export_comprehensive_analysis(self, export_dir: Optional[Path] = None,
                                    show_plots: bool = False) -> Dict[str, Any]:
        """
        Export comprehensive analysis results in all formats.
        
        This method creates a complete export package with all analysis
        results, visualizations, and reports in an organized directory structure.
        
        Args:
            export_dir: Directory for export (None = create timestamped directory)
            show_plots: Whether to display plots during generation
            
        Returns:
            Dictionary with export information
        """
        if self.df is None or self.df.empty:
            raise ValueError("No data available for export. Run analyze_directory() first.")
        
        # Create export directory using shared utility
        export_dir = create_export_directory(export_dir, prefix="audio_analysis")
        
        # Create subdirectories using shared utility
        create_export_subdirectories(export_dir)
        
        print(f"Exporting comprehensive analysis to: {export_dir}")
        
        # Export data files
        data_exports = self._export_data_files(export_dir)
        print("✓ Data files exported")
        
        # Generate visualizations
        visualization_exports = self._generate_visualizations(export_dir, show_plots)
        print("✓ Visualizations generated")
        
        # Generate reports
        report_exports = self._generate_reports(export_dir)
        print("✓ Reports generated")
        
        # Create export summary
        export_summary = {
            'export_directory': str(export_dir),
            'export_timestamp': datetime.now().isoformat(),
            'files_analyzed': len(self.df),
            'data_exports': data_exports,
            'visualization_exports': visualization_exports,
            'report_exports': report_exports,
            'analysis_stats': self.analysis_stats
        }
        
        # Save export summary
        with open(export_dir / "export_summary.json", 'w') as f:
            json.dump(export_summary, f, indent=2, default=str)
        
        return export_summary
    
    def _export_data_files(self, export_dir: Path) -> Dict[str, str]:
        """
        Export data files in various formats.
        
        Args:
            export_dir: Export directory
            
        Returns:
            Dictionary with exported file paths
        """
        data_dir = export_dir / "data"
        
        # Export main features as CSV
        features_path = data_dir / "audio_features.csv"
        self.csv_exporter.export_features(self.df, features_path)
        
        # Export phase data as CSV
        phase_path = data_dir / "phase_analysis.csv"
        self.csv_exporter.export_phases(self.phase_data, phase_path)
        
        # Export cluster analysis if available
        cluster_path = None
        if self.cluster_analysis:
            cluster_path = data_dir / "cluster_analysis.csv"
            self.csv_exporter.export_clusters(self.cluster_analysis, cluster_path)
        
        # Export sequence recommendations if available
        sequence_path = None
        if self.sequence_recommendations:
            sequence_path = data_dir / "sequence_recommendations.csv"
            self.csv_exporter.export_sequence(self.sequence_recommendations, sequence_path)
        
        # Export summary statistics
        summary_path = data_dir / "summary_statistics.csv"
        self.csv_exporter.export_summary_stats(self.df, self.phase_data, summary_path)
        
        return {
            'features': str(features_path),
            'phases': str(phase_path),
            'clusters': str(cluster_path) if cluster_path else None,
            'sequence': str(sequence_path) if sequence_path else None,
            'summary': str(summary_path)
        }
    
    def _generate_visualizations(self, export_dir: Path, show_plots: bool) -> Dict[str, str]:
        """
        Generate visualization files.
        
        Args:
            export_dir: Export directory
            show_plots: Whether to display plots
            
        Returns:
            Dictionary with visualization file paths
        """
        images_dir = export_dir / "images"
        visualization_paths = {}
        
        # Phase timeline visualization
        if self.phase_data:
            phase_timeline_path = images_dir / "phase_timeline.png"
            self.visualizer.create_phase_timeline(self.phase_data, phase_timeline_path, show_plots)
            visualization_paths['phase_timeline'] = str(phase_timeline_path)
        
        # Cluster visualization
        if self.cluster_labels is not None:
            cluster_path = images_dir / "cluster_analysis.png"
            features_scaled = self.data_processor.prepare_clustering_features(self.df)
            standardized_features, _ = self.data_processor.standardize_features(features_scaled)
            
            self.visualizer.create_cluster_visualization(
                self.df, self.cluster_labels, 
                standardized_features.values, list(standardized_features.columns),
                cluster_path, show_plots
            )
            visualization_paths['cluster_analysis'] = str(cluster_path)
        
        # Mood distribution visualization
        if 'primary_mood' in self.df.columns:
            mood_path = images_dir / "mood_distribution.png"
            mood_data = self.mood_analyzer.analyze_mood_distribution(self.df['primary_mood'].tolist())
            self.visualizer.create_mood_distribution_plot(mood_data, mood_path, show_plots)
            visualization_paths['mood_distribution'] = str(mood_path)
        
        # Sequence visualization
        if self.sequence_recommendations:
            sequence_path = images_dir / "sequence_recommendations.png"
            self.visualizer.create_sequence_visualization(
                self.sequence_recommendations, sequence_path, show_plots
            )
            visualization_paths['sequence_recommendations'] = str(sequence_path)
        
        return visualization_paths
    
    def _generate_reports(self, export_dir: Path) -> Dict[str, str]:
        """
        Generate analysis reports.
        
        Args:
            export_dir: Export directory
            
        Returns:
            Dictionary with report file paths
        """
        reports_dir = export_dir / "reports"
        report_paths = {}
        
        # Generate comprehensive markdown report
        markdown_path = reports_dir / "comprehensive_analysis_report.md"
        self.markdown_exporter.generate_comprehensive_report(
            self.df, self.phase_data, self.cluster_analysis, 
            self.sequence_recommendations, markdown_path
        )
        report_paths['comprehensive_report'] = str(markdown_path)
        
        # Generate JSON export for programmatic access
        json_path = reports_dir / "analysis_data.json"
        self.json_exporter.export_comprehensive_data(
            self.df, self.phase_data, self.cluster_analysis,
            self.sequence_recommendations, json_path
        )
        report_paths['json_data'] = str(json_path)
        
        return report_paths
    
    def _print_analysis_summary(self):
        """Print a summary of the analysis results."""
        processing_time = (self.analysis_stats['end_time'] - self.analysis_stats['start_time']).total_seconds()
        
        print("\n" + "="*60)
        print("ANALYSIS SUMMARY")
        print("="*60)
        print(f"Files found: {self.analysis_stats['files_found']}")
        print(f"Files processed: {self.analysis_stats['files_processed']}")
        print(f"Processing errors: {self.analysis_stats['processing_errors']}")
        print(f"Processing time: {processing_time:.1f} seconds")
        print(f"Success rate: {(self.analysis_stats['files_processed'] / self.analysis_stats['files_found']) * 100:.1f}%")
        
        if self.df is not None:
            print(f"Features extracted: {len(self.df.columns)}")
            print(f"Total phases detected: {sum(len(f['phases']) for f in self.phase_data)}")
            print(f"Average phases per track: {np.mean([len(f['phases']) for f in self.phase_data]):.1f}")
    
    def get_analysis_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the analysis.
        
        Returns:
            Dictionary with analysis statistics
        """
        if self.df is None:
            return {'error': 'No analysis data available'}
        
        stats = {
            'processing_stats': self.analysis_stats,
            'data_stats': {
                'total_tracks': len(self.df),
                'total_features': len(self.df.columns),
                'total_phases': sum(len(f['phases']) for f in self.phase_data),
                'avg_track_duration': self.df['duration'].mean(),
                'total_collection_duration': self.df['duration'].sum()
            }
        }
        
        # Add clustering stats if available
        if self.cluster_labels is not None:
            stats['clustering_stats'] = {
                'num_clusters': len(np.unique(self.cluster_labels)),
                'cluster_distribution': {f'cluster_{i}': int(np.sum(self.cluster_labels == i)) 
                                       for i in np.unique(self.cluster_labels)}
            }
        
        # Add mood stats if available
        if 'primary_mood' in self.df.columns:
            mood_counts = self.df['primary_mood'].value_counts()
            stats['mood_stats'] = {
                'unique_moods': len(mood_counts),
                'dominant_mood': mood_counts.index[0] if len(mood_counts) > 0 else 'Unknown',
                'mood_distribution': mood_counts.to_dict()
            }
        
        return stats