"""
Utility modules for audio analysis support functions.

This package contains helper functions and classes that support the main
analysis pipeline. These utilities handle common tasks like file I/O,
data processing, visualization, type conversion, validation, and statistics.

Modules:
- audio_io: Audio file loading, validation, and format support
- data_processing: Data transformation, standardization, and cleaning
- visualization: Plotting and visual analysis functions
- type_conversion: Centralized type conversion utilities
- validation: Data validation and range checking utilities
- statistics: Statistical calculation utilities and data aggregation
"""

from .audio_io import AudioLoader, validate_audio_file, get_supported_formats
from .data_processing import DataProcessor, standardize_features, clean_dataframe
from .visualization import Visualizer, create_phase_timeline, create_cluster_plot
from .type_conversion import (
    safe_float_convert, 
    convert_dict_values_to_float,
    convert_phase_data_types,
    convert_spectral_features_types,
    convert_mood_analysis_input,
    ensure_python_types
)
from .validation import (
    validate_range,
    validate_feature_ranges, 
    validate_phase_data,
    validate_spectral_features,
    validate_audio_files_list
)
from .statistics import (
    calculate_phase_statistics,
    calculate_collection_summary,
    calculate_cluster_statistics,
    calculate_feature_statistics,
    format_time_duration,
    format_time_position,
    calculate_progression_trend,
    safe_divide,
    calculate_normalized_score
)

__all__ = [
    'AudioLoader',
    'validate_audio_file',
    'get_supported_formats',
    'DataProcessor',
    'standardize_features',
    'clean_dataframe',
    'Visualizer',
    'create_phase_timeline',
    'create_cluster_plot',
    'safe_float_convert',
    'convert_dict_values_to_float', 
    'convert_phase_data_types',
    'convert_spectral_features_types',
    'convert_mood_analysis_input',
    'ensure_python_types',
    'validate_range',
    'validate_feature_ranges',
    'validate_phase_data', 
    'validate_spectral_features',
    'validate_audio_files_list',
    'calculate_phase_statistics',
    'calculate_collection_summary',
    'calculate_cluster_statistics',
    'calculate_feature_statistics',
    'format_time_duration',
    'format_time_position',
    'calculate_progression_trend',
    'safe_divide',
    'calculate_normalized_score'
]