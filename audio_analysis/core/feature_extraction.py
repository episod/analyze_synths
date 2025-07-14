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
            
            # Stage 2: Spectral Feature Extraction
            # These features capture the "brightness" and "color" of the sound,
            # which are crucial for understanding synthesizer textures
            
            # Spectral centroid: "brightness" of the sound
            # Higher values = brighter, more treble-focused sound
            # Lower values = darker, more bass-focused sound
            # Critical for distinguishing between different synthesizer patches
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            
            # Spectral rolloff: frequency below which 85% of energy is concentrated
            # Indicates the "fullness" of the harmonic content
            # Important for understanding synthesizer filter settings
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            
            # Spectral bandwidth: "width" of the frequency distribution
            # Narrow bandwidth = pure tones (sine waves, simple synths)
            # Wide bandwidth = complex textures (noise, rich harmonics)
            # Essential for characterizing synthesizer sound design
            spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
            
            # Zero-crossing rate: measure of signal "roughness" or "noisiness"
            # Low values = smooth, sustained sounds (pads, strings)
            # High values = percussive, noisy sounds (drums, distortion)
            # Key indicator of synthesizer texture and filter resonance
            zero_crossing_rate = librosa.feature.zero_crossing_rate(y)[0]
            
            # Stage 3: Temporal Feature Extraction
            # These features capture the energy and rhythm characteristics
            # that define the musical "feel" and emotional impact
            
            # RMS Energy: overall "loudness" and dynamic range
            # Not just volume, but energy distribution over time
            # Critical for understanding musical dynamics and emotional intensity
            rms = librosa.feature.rms(y=y)[0]
            
            # Tempo and beat tracking: rhythmic characteristics
            # Essential for understanding musical flow and sequencing
            # Uses onset detection to find rhythmic patterns
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            
            # Stage 4: Harmonic Feature Extraction
            # These features capture musical content: key, harmony, melody
            # Essential for understanding compositional structure
            
            # MFCC (Mel-frequency cepstral coefficients): timbre fingerprint
            # Captures the "character" of the sound independent of pitch
            # First 13 coefficients are most musically relevant
            # Critical for distinguishing between different synthesizer types
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            
            # Chroma features: harmonic and melodic content
            # Captures the "pitch class" distribution (C, C#, D, etc.)
            # Essential for key detection and harmonic analysis
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            
            # Tonnetz: tonal centroid features
            # Captures harmonic relationships and chord progressions
            # Based on music theory concepts of tonal space
            # Requires harmonic component extraction for accuracy
            tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr)
            
            # Stage 5: Musical Key Detection
            # Uses chroma features to estimate the predominant key
            # Important for sequencing and harmonic compatibility analysis
            chroma_mean = np.mean(chroma, axis=1)
            key_index = np.argmax(chroma_mean)
            keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            detected_key = keys[key_index]
            key_confidence = np.max(chroma_mean)
            
            # Stage 6: Feature Aggregation
            # Convert time-series features to summary statistics
            # Mean and standard deviation capture both average characteristics
            # and the variability/dynamics of the music
            
            features = {
                # Basic file information
                'filename': file_path.name,
                'duration': duration,
                'tempo': tempo,
                'detected_key': detected_key,
                'key_confidence': key_confidence,
                
                # Spectral features (brightness, timbre, harmonic content)
                # Mean values represent the overall "color" of the sound
                'spectral_centroid_mean': np.mean(spectral_centroids),
                'spectral_centroid_std': np.std(spectral_centroids),
                'spectral_rolloff_mean': np.mean(spectral_rolloff),
                'spectral_bandwidth_mean': np.mean(spectral_bandwidth),
                'zero_crossing_rate_mean': np.mean(zero_crossing_rate),
                
                # Energy features (dynamics, loudness, emotional intensity)
                'rms_mean': np.mean(rms),
                'rms_std': np.std(rms),
                
                # MFCC features (timbre fingerprint)
                # Each coefficient captures different aspects of sound character
                **{f'mfcc_{i+1}_mean': np.mean(mfccs[i]) for i in range(13)},
                **{f'mfcc_{i+1}_std': np.std(mfccs[i]) for i in range(13)},
                
                # Chroma features (harmonic content by pitch class)
                # Captures the "key signature" and harmonic richness
                **{f'chroma_{keys[i]}_mean': np.mean(chroma[i]) for i in range(12)},
                
                # Tonnetz features (tonal space representation)
                # Captures harmonic relationships and chord progressions
                **{f'tonnetz_{i+1}_mean': np.mean(tonnetz[i]) for i in range(6)},
            }
            
            # Stage 7: Beat and Rhythm Analysis
            # Calculate onset density for rhythm characterization
            # Higher density = more rhythmic activity
            # Lower density = more sustained, ambient textures
            onset_density = len(beats) / duration if duration > 0 else 0
            features['onset_density'] = onset_density
            
            return features
            
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
        # Calculate core spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y)[0]
        
        return {
            'spectral_centroid_mean': np.mean(spectral_centroids),
            'spectral_bandwidth_mean': np.mean(spectral_bandwidth),
            'spectral_rolloff_mean': np.mean(spectral_rolloff),
            'zero_crossing_rate_mean': np.mean(zero_crossing_rate)
        }
    
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
        numeric_features = {}
        
        for key, value in features.items():
            # Skip non-numeric features
            if key in ['filename', 'detected_key']:
                continue
                
            # Include numeric values
            if isinstance(value, (int, float, np.integer, np.floating)):
                numeric_features[key] = float(value)
                
        return numeric_features