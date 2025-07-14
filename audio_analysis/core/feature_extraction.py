"""
Audio Feature Extraction Module

This module implements comprehensive audio feature extraction specifically designed
for synthesizer music analysis. The features are chosen to capture the creative
characteristics that composers care about: mood, texture, energy, and harmonic content.

The extraction process follows these principles:
1. Capture both spectral and temporal characteristics
2. Focus on features that correlate with musical creativity
3. Extract enough information to distinguish between different musical moods
4. Maintain compatibility with machine learning clustering algorithms

Key Features Extracted:
- Spectral: Centroid, bandwidth, rolloff (brightness and timbre)
- Temporal: RMS energy, zero-crossing rate (rhythm and texture)
- Harmonic: MFCC, chroma, tonnetz (musical content and key)
- Structural: Tempo, duration, phase analysis (musical form)
- Creative: Mood descriptors, character tags (artistic interpretation)
"""

import librosa
import numpy as np
from typing import Dict, Any, Optional
from pathlib import Path

# Import shared feature extraction core
from .feature_extraction_base import (
    feature_extraction_core,
    extract_features_from_audio,
    extract_basic_spectral_features,
    get_numeric_features
)


class FeatureExtractor:
    """
    Comprehensive audio feature extractor optimized for synthesizer music analysis.
    
    This class extracts ~80 features per audio file, focusing on characteristics
    that are musically meaningful for electronic music composers. The features
    are designed to capture creative intent rather than just technical metrics.
    """
    
    def __init__(self, sample_rate: Optional[int] = None):
        """
        Initialize the feature extractor.
        
        Args:
            sample_rate: Target sample rate for audio loading. If None, uses original rate.
                        Common values: 22050 (librosa default), 44100 (CD quality)
        """
        self.sample_rate = sample_rate
        
        # Use shared feature extraction core
        if sample_rate is not None:
            feature_extraction_core.sample_rate = sample_rate
        
    def extract_features(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Extract comprehensive audio features from a single audio file.
        
        This method implements a multi-stage feature extraction process:
        1. Load audio using librosa (handles WAV, AIFF, MP3)
        2. Extract spectral features (brightness, timbre, harmonic content)
        3. Extract temporal features (rhythm, energy, texture)
        4. Extract harmonic features (key, chord, tonal content)
        5. Perform basic phase detection for structural analysis
        
        The analytical approach is based on the principle that synthesizer music
        can be understood through its spectral characteristics (what frequencies
        are present) and temporal evolution (how it changes over time).
        
        Args:
            file_path: Path to the audio file to analyze
            
        Returns:
            Dictionary containing all extracted features, or None if extraction fails
        """
        try:
            # Stage 1: Audio Loading and Validation
            # Load audio file using librosa, which handles multiple formats
            # and provides consistent preprocessing (normalization, resampling)
            y, sr = librosa.load(file_path, sr=self.sample_rate)
            
            # Basic validation - ensure we have audio data
            if len(y) == 0:
                raise ValueError("Audio file is empty or corrupted")
                
            # Calculate basic duration - important for understanding track length
            # and its impact on listener experience
            duration = librosa.get_duration(y=y, sr=sr)
            
            # Use shared feature extraction core for consistent analysis
            return extract_features_from_audio(y, sr, file_path, duration)
            
        except Exception as e:
            print(f"Error extracting features from {file_path}: {str(e)}")
            return None
    
    def extract_basic_spectral_features(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        """
        Extract basic spectral features for use in phase analysis.
        
        This is a lightweight version of spectral extraction used when
        we need features for individual phases/sections rather than
        entire tracks. Focuses on the most essential characteristics.
        
        Args:
            y: Audio time series
            sr: Sample rate
            
        Returns:
            Dictionary with basic spectral features
        """
        # Use shared feature extraction core for consistency
        return extract_basic_spectral_features(y, sr)
    
    def get_numeric_features(self, features: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract only numeric features suitable for machine learning.
        
        This method filters out string/categorical features and returns
        only the numeric values that can be used for clustering and
        statistical analysis.
        
        Args:
            features: Full feature dictionary
            
        Returns:
            Dictionary containing only numeric features
        """
        # Use shared feature extraction core for consistency
        return get_numeric_features(features)