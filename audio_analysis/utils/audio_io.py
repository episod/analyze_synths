"""
Audio I/O Utilities for File Loading and Validation

This module provides utilities for loading audio files, validating formats,
and handling different audio file types. It serves as a centralized interface
for all audio file operations in the analysis pipeline.

The module supports:
- WAV files (uncompressed, high quality)
- AIFF files (uncompressed, high quality)
- MP3 files (compressed, widely supported)
- Format validation and error handling
- Metadata extraction and file information
"""

import librosa
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
import warnings


class AudioLoader:
    """
    Centralized audio file loader with format validation and error handling.
    
    This class provides a robust interface for loading audio files using
    librosa, with comprehensive error handling and format validation.
    It handles the common issues that arise when processing diverse audio
    collections.
    """
    
    def __init__(self, target_sample_rate: Optional[int] = None):
        """
        Initialize the audio loader.
        
        Args:
            target_sample_rate: Target sample rate for resampling (None = keep original)
        """
        self.target_sample_rate = target_sample_rate
        self.supported_extensions = ['.wav', '.aiff', '.aif', '.mp3']
        
        # Suppress librosa warnings for cleaner output
        warnings.filterwarnings('ignore', category=UserWarning, module='librosa')
    
    def load_audio(self, file_path: Path) -> Optional[Tuple[np.ndarray, int]]:
        """
        Load an audio file and return the audio data and sample rate.
        
        This method handles the complete audio loading process:
        1. Validates file format and existence
        2. Loads audio using librosa with error handling
        3. Performs optional resampling to target sample rate
        4. Validates the loaded audio data
        5. Returns standardized audio data and sample rate
        
        The loading process is designed to be robust against common issues:
        - Corrupted or incomplete files
        - Unsupported formats or codecs
        - Files with unusual characteristics
        - Memory constraints with large files
        
        Args:
            file_path: Path to the audio file to load
            
        Returns:
            Tuple of (audio_data, sample_rate) or None if loading fails
        """
        try:
            # Stage 1: File Validation
            if not self._validate_file(file_path):
                return None
            
            # Stage 2: Audio Loading
            # Use librosa.load which handles multiple formats and provides
            # consistent preprocessing (mono conversion, normalization)
            audio_data, sample_rate = librosa.load(
                file_path, 
                sr=self.target_sample_rate,
                mono=True,  # Convert to mono for consistent analysis
                dtype=np.float32  # Use float32 for memory efficiency
            )
            
            # Stage 3: Audio Validation
            if not self._validate_audio_data(audio_data, sample_rate):
                return None
            
            # Stage 4: Post-processing
            # Ensure audio is properly normalized and contains no artifacts
            audio_data = self._clean_audio_data(audio_data)
            
            return audio_data, sample_rate
            
        except Exception as e:
            print(f"Error loading audio file {file_path}: {str(e)}")
            return None
    
    def _validate_file(self, file_path: Path) -> bool:
        """
        Validate that the file exists and has a supported format.
        
        This method performs basic file validation before attempting
        to load the audio data. It checks for existence, format support,
        and basic file integrity.
        
        Args:
            file_path: Path to validate
            
        Returns:
            True if file is valid, False otherwise
        """
        # Check file existence
        if not file_path.exists():
            print(f"File not found: {file_path}")
            return False
        
        # Check if file is not empty
        if file_path.stat().st_size == 0:
            print(f"Empty file: {file_path}")
            return False
        
        # Check file extension
        if not any(str(file_path).lower().endswith(ext) for ext in self.supported_extensions):
            print(f"Unsupported file format: {file_path}")
            return False
        
        return True
    
    def _validate_audio_data(self, audio_data: np.ndarray, sample_rate: int) -> bool:
        """
        Validate the loaded audio data.
        
        This method checks the loaded audio data for common issues
        that could cause problems in downstream analysis.
        
        Args:
            audio_data: Audio time series
            sample_rate: Sample rate
            
        Returns:
            True if audio data is valid, False otherwise
        """
        # Check for empty audio
        if len(audio_data) == 0:
            print("Audio data is empty")
            return False
        
        # Check for extremely short audio (less than 1 second)
        if len(audio_data) < sample_rate:
            print(f"Audio too short: {len(audio_data) / sample_rate:.2f} seconds")
            return False
        
        # Check for invalid sample rate
        if sample_rate <= 0:
            print(f"Invalid sample rate: {sample_rate}")
            return False
        
        # Check for NaN or infinite values
        if np.any(np.isnan(audio_data)) or np.any(np.isinf(audio_data)):
            print("Audio contains NaN or infinite values")
            return False
        
        # Check for completely silent audio
        if np.max(np.abs(audio_data)) < 1e-6:
            print("Audio appears to be silent")
            return False
        
        return True
    
    def _clean_audio_data(self, audio_data: np.ndarray) -> np.ndarray:
        """
        Clean and normalize audio data.
        
        This method applies basic cleaning operations to ensure
        the audio data is suitable for analysis.
        
        Args:
            audio_data: Raw audio data
            
        Returns:
            Cleaned audio data
        """
        # Remove DC offset (center around zero)
        audio_data = audio_data - np.mean(audio_data)
        
        # Normalize to prevent clipping (but preserve dynamic range)
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            # Normalize to 90% of maximum to prevent clipping
            audio_data = audio_data * (0.9 / max_val)
        
        return audio_data
    
    def get_audio_info(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Get basic information about an audio file without loading it.
        
        This method provides file metadata and basic characteristics
        without loading the entire file into memory.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary with file information or None if unavailable
        """
        try:
            # Get file size
            file_size = file_path.stat().st_size
            
            # Get duration using librosa without loading full file
            duration = librosa.get_duration(path=file_path)
            
            # Get sample rate
            sample_rate = librosa.get_samplerate(path=file_path)
            
            return {
                'filename': file_path.name,
                'file_size_bytes': file_size,
                'file_size_mb': file_size / (1024 * 1024),
                'duration_seconds': duration,
                'duration_minutes': duration / 60,
                'sample_rate': sample_rate,
                'format': file_path.suffix.lower()
            }
            
        except Exception as e:
            print(f"Error getting audio info for {file_path}: {str(e)}")
            return None
    
    def batch_load_directory(self, directory_path: Path) -> List[Tuple[Path, np.ndarray, int]]:
        """
        Load all supported audio files from a directory.
        
        This method processes an entire directory of audio files,
        handling errors gracefully and providing progress feedback.
        
        Args:
            directory_path: Path to directory containing audio files
            
        Returns:
            List of tuples (file_path, audio_data, sample_rate)
        """
        if not directory_path.exists() or not directory_path.is_dir():
            print(f"Directory not found: {directory_path}")
            return []
        
        # Find all supported audio files
        audio_files = []
        for ext in self.supported_extensions:
            audio_files.extend(directory_path.glob(f'*{ext}'))
            audio_files.extend(directory_path.glob(f'*{ext.upper()}'))
        
        if not audio_files:
            print(f"No supported audio files found in {directory_path}")
            return []
        
        print(f"Found {len(audio_files)} audio files. Loading...")
        
        # Load each file
        loaded_files = []
        for i, file_path in enumerate(audio_files):
            print(f"Loading {i+1}/{len(audio_files)}: {file_path.name}")
            
            result = self.load_audio(file_path)
            if result is not None:
                audio_data, sample_rate = result
                loaded_files.append((file_path, audio_data, sample_rate))
            else:
                print(f"Failed to load: {file_path.name}")
        
        print(f"Successfully loaded {len(loaded_files)}/{len(audio_files)} files")
        return loaded_files


def validate_audio_file(file_path: Path) -> bool:
    """
    Validate that a file is a supported audio format.
    
    This is a standalone function for quick format validation
    without creating an AudioLoader instance.
    
    Args:
        file_path: Path to validate
        
    Returns:
        True if file is valid, False otherwise
    """
    supported_extensions = ['.wav', '.aiff', '.aif', '.mp3']
    
    if not file_path.exists():
        return False
    
    if file_path.stat().st_size == 0:
        return False
    
    return any(str(file_path).lower().endswith(ext) for ext in supported_extensions)


def get_supported_formats() -> Dict[str, Any]:
    """
    Get information about supported audio formats.
    
    Returns:
        Dictionary with format information
    """
    return {
        'formats': ['.wav', '.aiff', '.aif', '.mp3'],
        'descriptions': {
            '.wav': 'Uncompressed PCM audio (recommended for quality)',
            '.aiff': 'Uncompressed PCM audio (Apple format)',
            '.aif': 'Uncompressed PCM audio (Apple format, short extension)',
            '.mp3': 'Compressed audio (widely supported)'
        },
        'recommendations': {
            'best_quality': ['.wav', '.aiff'],
            'most_compatible': ['.mp3'],
            'recommended': ['.wav']
        },
        'limitations': {
            'max_file_size_mb': 500,
            'min_duration_seconds': 1,
            'max_duration_minutes': 30
        }
    }


def get_directory_audio_files(directory_path: Path) -> List[Path]:
    """
    Get all supported audio files from a directory.
    
    This function scans a directory for audio files without loading them,
    useful for quick directory analysis.
    
    Args:
        directory_path: Path to directory
        
    Returns:
        List of paths to audio files
    """
    if not directory_path.exists() or not directory_path.is_dir():
        return []
    
    supported_extensions = ['.wav', '.aiff', '.aif', '.mp3']
    audio_files = []
    
    for ext in supported_extensions:
        audio_files.extend(directory_path.glob(f'*{ext}'))
        audio_files.extend(directory_path.glob(f'*{ext.upper()}'))
    
    return sorted(audio_files)


def estimate_processing_time(directory_path: Path) -> Dict[str, Any]:
    """
    Estimate processing time for a directory of audio files.
    
    This function provides time estimates for processing a directory,
    helping users plan their analysis sessions.
    
    Args:
        directory_path: Path to directory
        
    Returns:
        Dictionary with time estimates
    """
    audio_files = get_directory_audio_files(directory_path)
    
    if not audio_files:
        return {'error': 'No audio files found'}
    
    # Estimate processing time based on file count and typical durations
    # These are rough estimates based on typical synthesizer track lengths
    avg_duration_per_file = 180  # 3 minutes average
    processing_time_per_minute = 2  # 2 seconds processing per minute of audio
    
    total_files = len(audio_files)
    estimated_audio_minutes = total_files * avg_duration_per_file / 60
    estimated_processing_seconds = estimated_audio_minutes * processing_time_per_minute
    
    return {
        'total_files': total_files,
        'estimated_audio_duration_minutes': estimated_audio_minutes,
        'estimated_processing_time_seconds': estimated_processing_seconds,
        'estimated_processing_time_minutes': estimated_processing_seconds / 60,
        'recommendation': 'Consider processing in batches if over 50 files' if total_files > 50 else 'Should process quickly'
    }