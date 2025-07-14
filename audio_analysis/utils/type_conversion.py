"""
Type Conversion Utilities for Audio Analysis

This module provides centralized type conversion functions to ensure
consistent data type handling throughout the audio analysis toolkit.
It eliminates the need for scattered float() conversions and provides
robust type handling with proper error management.
"""

from typing import Dict, Any, Union, List, Optional, Tuple
import numpy as np


def safe_float_convert(value: Any, default: float = 0.0) -> float:
    """
    Safely convert a value to float with fallback handling.
    
    This function handles numpy scalars, strings, None values, and other
    edge cases that can cause type issues in numerical operations.
    
    Args:
        value: Value to convert to float
        default: Default value if conversion fails
        
    Returns:
        Float value or default if conversion fails
    """
    if value is None:
        return default
    
    try:
        # Handle numpy scalars and arrays
        if isinstance(value, (np.integer, np.floating)):
            return float(value)
        
        # Handle string representations
        if isinstance(value, str):
            if value.lower() in ['nan', 'none', '', 'null']:
                return default
            return float(value)
        
        # Handle regular numbers
        return float(value)
        
    except (ValueError, TypeError):
        return default


def convert_dict_values_to_float(data_dict: Dict[str, Any], 
                                keys_to_convert: Optional[List[str]] = None,
                                default: float = 0.0) -> Dict[str, Any]:
    """
    Convert specified dictionary values to float type.
    
    Args:
        data_dict: Dictionary containing values to convert
        keys_to_convert: List of keys to convert. If None, converts all numeric-convertible values
        default: Default value for failed conversions
        
    Returns:
        Dictionary with converted values
    """
    converted_dict = data_dict.copy()
    
    if keys_to_convert is None:
        # Try to convert all values that look numeric
        for key, value in converted_dict.items():
            if isinstance(value, (int, float, np.number, str)):
                try:
                    converted_dict[key] = safe_float_convert(value, default)
                except:
                    # Keep original value if conversion fails
                    pass
    else:
        # Convert only specified keys
        for key in keys_to_convert:
            if key in converted_dict:
                converted_dict[key] = safe_float_convert(converted_dict[key], default)
    
    return converted_dict


def convert_phase_data_types(phase_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert phase data dictionary to ensure all numeric values are Python floats.
    
    This function specifically handles the phase data structure used throughout
    the analysis pipeline, ensuring consistent type handling.
    
    Args:
        phase_dict: Phase data dictionary
        
    Returns:
        Phase dictionary with converted numeric values
    """
    # Define keys that should be converted to float
    numeric_keys = [
        'avg_energy', 'avg_brightness', 'avg_roughness', 'onset_density',
        'duration', 'start_time', 'end_time', 'phase_number'
    ]
    
    return convert_dict_values_to_float(phase_dict, numeric_keys)


def convert_spectral_features_types(spectral_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert spectral features dictionary to ensure all values are Python floats.
    
    Args:
        spectral_dict: Spectral features dictionary
        
    Returns:
        Dictionary with converted numeric values
    """
    # Define keys that should be converted to float
    numeric_keys = [
        'spectral_centroid_mean', 'spectral_bandwidth_mean', 
        'spectral_rolloff_mean', 'zero_crossing_rate_mean'
    ]
    
    return convert_dict_values_to_float(spectral_dict, numeric_keys)


def convert_mood_analysis_input(phase_data: Dict[str, Any], 
                              spectral_features: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Convert mood analysis input data to ensure proper numeric types.
    
    This is a convenience function that handles the common pattern of
    converting both phase data and spectral features for mood analysis.
    
    Args:
        phase_data: Phase-level audio characteristics
        spectral_features: Spectral analysis results
        
    Returns:
        Tuple of (converted_phase_data, converted_spectral_features)
    """
    converted_phase = convert_phase_data_types(phase_data)
    converted_spectral = convert_spectral_features_types(spectral_features)
    
    return converted_phase, converted_spectral


def safe_int_convert(value: Any, default: int = 0) -> int:
    """
    Safely convert a value to integer with fallback handling.
    
    Args:
        value: Value to convert to int
        default: Default value if conversion fails
        
    Returns:
        Integer value or default if conversion fails
    """
    if value is None:
        return default
    
    try:
        # Handle numpy scalars
        if isinstance(value, (np.integer, np.floating)):
            return int(value)
        
        # Handle string representations
        if isinstance(value, str):
            if value.lower() in ['nan', 'none', '', 'null']:
                return default
            return int(float(value))  # Convert through float to handle "1.0" strings
        
        # Handle regular numbers
        return int(value)
        
    except (ValueError, TypeError):
        return default


def ensure_python_types(data: Union[Dict, List, Any]) -> Union[Dict, List, Any]:
    """
    Recursively convert numpy types to Python native types.
    
    This function handles nested dictionaries and lists, converting
    all numpy scalars to Python equivalents to prevent type issues.
    
    Args:
        data: Data structure to convert
        
    Returns:
        Data structure with Python native types
    """
    if isinstance(data, dict):
        return {key: ensure_python_types(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [ensure_python_types(item) for item in data]
    elif isinstance(data, (np.integer, np.floating)):
        return float(data) if isinstance(data, np.floating) else int(data)
    elif isinstance(data, np.ndarray):
        return data.tolist()
    else:
        return data


def convert_confidence_scores(confidence_dict: Dict[str, Any]) -> Dict[str, float]:
    """
    Convert confidence score dictionary to ensure all values are floats.
    
    Args:
        confidence_dict: Dictionary of confidence scores
        
    Returns:
        Dictionary with float confidence values
    """
    return {key: safe_float_convert(value, 0.0) for key, value in confidence_dict.items()}