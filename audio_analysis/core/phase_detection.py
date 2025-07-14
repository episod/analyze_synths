"""
Musical Phase Detection Module

This module implements advanced algorithms for detecting musical phases/sections
in long-form synthesizer compositions. The approach is based on the observation
that electronic music often follows structural patterns that can be detected
through changes in energy, spectral content, and rhythmic activity.

The analytical approach combines:
1. Signal processing techniques for change detection
2. Music theory principles for structural understanding
3. Creative intuition about electronic music composition patterns

Key Concepts:
- Phase: A coherent musical section with consistent characteristics
- Transition: A detected change point between different musical sections
- Classification: Assignment of musical meaning to detected phases

The algorithm is particularly effective for:
- Ambient/atmospheric synthesizer music with gradual changes
- Progressive electronic music with distinct sections
- Long-form compositions with clear structural evolution
"""

import numpy as np
import librosa
from scipy import signal
from scipy.ndimage import uniform_filter1d
from typing import List, Dict, Any, Tuple
from pathlib import Path


class PhaseDetector:
    """
    Advanced musical phase detection for synthesizer music analysis.
    
    This class implements a sophisticated algorithm for detecting musical phases
    in electronic music compositions. The approach combines signal processing
    techniques with musical understanding to identify coherent sections.
    
    The detection process works by:
    1. Analyzing energy and spectral changes over time
    2. Detecting significant transition points
    3. Classifying the resulting phases based on musical characteristics
    4. Providing mood analysis for each detected phase
    """
    
    def __init__(self, hop_length: int = 512, frame_length: int = 2048):
        """
        Initialize the phase detector with analysis parameters.
        
        Args:
            hop_length: Number of samples between successive frames
            frame_length: Length of each analysis frame in samples
        """
        self.hop_length = hop_length
        self.frame_length = frame_length
        
    def detect_phases(self, y: np.ndarray, sr: int) -> Tuple[List[Dict[str, Any]], np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Detect musical phases in an audio signal using advanced change detection.
        
        This method implements a multi-stage process:
        1. Extract time-series features (energy, spectral characteristics)
        2. Smooth features to reduce noise while preserving musical changes
        3. Detect significant change points using gradient analysis
        4. Classify detected phases based on musical characteristics
        5. Analyze mood and character for each phase
        
        The analytical approach is based on the principle that musical phases
        are characterized by relatively stable characteristics separated by
        significant changes. The algorithm uses both energy and spectral
        features to detect these transitions.
        
        Args:
            y: Audio time series
            sr: Sample rate
            
        Returns:
            Tuple containing:
            - List of phase dictionaries with timing and characteristics
            - Time axis for feature visualization
            - Smoothed RMS energy
            - Smoothed spectral centroids
            - Change signal showing detected transitions
        """
        # Stage 1: Time-Series Feature Extraction
        # Extract features with consistent frame size for temporal analysis
        # These features capture the evolving characteristics of the music
        
        # RMS Energy: Measures the overall "loudness" or energy content
        # Critical for detecting dynamic changes in synthesizer music
        # Higher values = more energetic sections, lower = ambient/quiet
        rms = librosa.feature.rms(y=y, frame_length=self.frame_length, hop_length=self.hop_length)[0]
        
        # Spectral Centroid: Measures the "brightness" of the sound
        # Higher values = brighter, more treble-focused content
        # Lower values = darker, more bass-focused content
        # Essential for detecting timbral changes in synthesizer patches
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=self.hop_length)[0]
        
        # Spectral Rolloff: Frequency below which 85% of energy is concentrated
        # Indicates the "fullness" of the harmonic content
        # Important for understanding filter sweeps and synthesis changes
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, hop_length=self.hop_length)[0]
        
        # Zero-Crossing Rate: Measure of signal "roughness" or texture
        # Low values = smooth, sustained sounds (pads, strings)
        # High values = percussive, noisy sounds (drums, distortion)
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y, frame_length=self.frame_length, hop_length=self.hop_length)[0]
        
        # Stage 2: Onset Detection for Rhythmic Analysis
        # Detect rhythmic events that may indicate phase transitions
        # Particularly important for identifying build-ups and breakdowns
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=self.hop_length)
        onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=self.hop_length)
        
        # Create time axis for all features
        times = librosa.frames_to_time(range(len(rms)), sr=sr, hop_length=self.hop_length)
        
        # Stage 3: Feature Smoothing for Noise Reduction
        # Apply temporal smoothing to reduce noise while preserving musical changes
        # The 2-second window is chosen to capture musical phrases while
        # filtering out brief fluctuations that don't represent structural changes
        smooth_window = int(sr / self.hop_length * 2)  # 2-second smoothing window
        rms_smooth = uniform_filter1d(rms, size=smooth_window)
        spectral_centroids_smooth = uniform_filter1d(spectral_centroids, size=smooth_window)
        
        # Stage 4: Change Detection Using Gradient Analysis
        # Calculate derivatives to detect significant changes in musical characteristics
        # This approach is based on the principle that phase boundaries occur
        # where there are significant changes in energy or spectral content
        
        # RMS derivative: detects energy changes (dynamics, build-ups, breakdowns)
        rms_diff = np.gradient(rms_smooth)
        
        # Spectral derivative: detects timbral changes (filter sweeps, patch changes)
        spectral_diff = np.gradient(spectral_centroids_smooth)
        
        # Combine features into a unified "change signal"
        # The spectral component is normalized to balance with energy changes
        # This creates a single signal that represents overall musical change
        change_signal = np.abs(rms_diff) + np.abs(spectral_diff) / 1000
        
        # Stage 5: Peak Detection for Transition Points
        # Find significant peaks in the change signal that represent phase boundaries
        # The threshold is set adaptively based on the signal's characteristics
        change_peaks, _ = signal.find_peaks(
            change_signal, 
            height=np.std(change_signal) * 1.5,  # Adaptive threshold
            distance=int(sr / self.hop_length * 10)  # Minimum 10 seconds between phases
        )
        
        # Convert peak indices to time values
        change_times = times[change_peaks]
        
        # Stage 6: Phase Boundary Construction
        # Create a list of phase boundaries including start and end times
        phase_boundaries = [0.0]  # Always start at the beginning
        
        # Add significant change points, but ignore very early changes
        # This prevents false positives from initial audio artifacts
        for change_time in change_times:
            if change_time > 5.0:  # Ignore changes in the first 5 seconds
                phase_boundaries.append(change_time)
        
        # Always end at the track's end time
        phase_boundaries.append(times[-1])
        
        # Remove duplicates and ensure proper ordering
        phase_boundaries = sorted(list(set(phase_boundaries)))
        
        # Stage 7: Phase Analysis and Classification
        # Analyze each detected phase to determine its musical characteristics
        phases = []
        for i in range(len(phase_boundaries) - 1):
            start_time = phase_boundaries[i]
            end_time = phase_boundaries[i + 1]
            
            # Calculate frame indices for this phase
            start_frame = int(start_time * sr / self.hop_length)
            end_frame = int(end_time * sr / self.hop_length)
            
            # Ensure we have valid frame range
            if end_frame > start_frame:
                # Calculate average characteristics for this phase
                # These values represent the "personality" of this musical section
                phase_rms = np.mean(rms[start_frame:end_frame])
                phase_spectral = np.mean(spectral_centroids[start_frame:end_frame])
                phase_zcr = np.mean(zero_crossing_rate[start_frame:end_frame])
                
                # Count rhythmic events in this phase
                phase_onsets = np.sum((onset_times >= start_time) & (onset_times < end_time))
                onset_density = phase_onsets / (end_time - start_time)
                
                # Classify this phase based on its characteristics
                phase_type = self._classify_phase(phase_rms, phase_spectral, onset_density, i, len(phase_boundaries) - 2)
                
                # Create phase data structure for further analysis
                from ..utils.type_conversion import ensure_python_types
                phase_data = ensure_python_types({
                    'avg_energy': phase_rms,
                    'avg_brightness': phase_spectral,
                    'avg_roughness': phase_zcr,
                    'onset_density': onset_density,
                    'duration': end_time - start_time
                })
                
                # Extract basic spectral features for mood analysis
                basic_spectral = ensure_python_types({
                    'spectral_centroid_mean': phase_spectral,
                    'spectral_bandwidth_mean': phase_spectral * 0.3,  # Approximation
                    'spectral_rolloff_mean': phase_spectral * 1.5,    # Approximation
                    'zero_crossing_rate_mean': phase_zcr
                })
                
                # Analyze mood for this phase (will be implemented by MoodAnalyzer)
                # For now, we'll leave this as a placeholder
                mood_descriptors = []  # Will be populated by MoodAnalyzer
                
                # Create comprehensive phase dictionary
                phases.append(ensure_python_types({
                    'phase_number': i + 1,
                    'start_time': start_time,
                    'end_time': end_time,
                    'duration': end_time - start_time,
                    'avg_energy': phase_rms,
                    'avg_brightness': phase_spectral,
                    'avg_roughness': phase_zcr,
                    'onset_density': onset_density,
                    'phase_type': phase_type,
                    'mood_descriptors': mood_descriptors,
                    'basic_spectral': basic_spectral,
                    'phase_data': phase_data
                }))
        
        return phases, times, rms_smooth, spectral_centroids_smooth, change_signal
    
    def _classify_phase(self, energy: float, brightness: float, onset_density: float, 
                       phase_idx: int, total_phases: int) -> str:
        """
        Classify a musical phase based on its characteristics and position.
        
        This method implements a rule-based classification system that assigns
        musical meaning to detected phases. The classification considers both
        the absolute characteristics of the phase and its position within the
        overall track structure.
        
        The classification approach is based on common patterns in electronic music:
        - Intro/Outro sections tend to be lower energy and positioned at extremes
        - Climax sections have high energy and appear later in the track
        - Build-ups have moderate energy with increasing onset density
        - Breakdowns have low energy but may appear in the middle of tracks
        
        Args:
            energy: Average RMS energy for this phase
            brightness: Average spectral centroid for this phase
            onset_density: Rhythmic event density (onsets per second)
            phase_idx: Index of this phase in the track
            total_phases: Total number of phases in the track
            
        Returns:
            String describing the phase type
        """
        # Calculate normalized position within the track (0.0 to 1.0)
        # This helps distinguish between similar characteristics in different contexts
        position = phase_idx / max(total_phases - 1, 1)
        
        # Classification logic based on energy, brightness, and rhythmic activity
        # The thresholds are empirically determined for synthesizer music
        
        # Low energy, low rhythm: Ambient/quiet sections
        if energy < 0.02 and onset_density < 0.5:
            if position < 0.3:
                return "Intro/Ambient"
            elif position > 0.7:
                return "Outro/Fade"
            else:
                return "Breakdown/Quiet"
        
        # High energy, high rhythm: Energetic sections
        elif energy > 0.1 and onset_density > 2.0:
            if position > 0.5:
                return "Climax/Peak"
            else:
                return "Build-up/Energetic"
        
        # High rhythm, moderate energy: Rhythmic sections
        elif onset_density > 1.0:
            return "Rhythmic/Percussive"
        
        # High brightness: Melodic sections
        elif brightness > 2000:
            return "Bright/Melodic"
        
        # Position-based classification for ambiguous cases
        elif position < 0.3:
            return "Introduction"
        elif position > 0.7:
            return "Conclusion"
        else:
            return "Development"
    
    def analyze_phase_transitions(self, phases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze the transitions between detected phases.
        
        This method examines how phases connect to each other, which is
        important for understanding the musical flow and compositional
        structure. It identifies the type and quality of transitions.
        
        Args:
            phases: List of detected phases
            
        Returns:
            List of transition analyses
        """
        transitions = []
        
        for i in range(len(phases) - 1):
            current_phase = phases[i]
            next_phase = phases[i + 1]
            
            # Calculate transition characteristics
            energy_change = next_phase['avg_energy'] - current_phase['avg_energy']
            brightness_change = next_phase['avg_brightness'] - current_phase['avg_brightness']
            rhythm_change = next_phase['onset_density'] - current_phase['onset_density']
            
            # Classify transition type
            if energy_change > 0.02:
                transition_type = "Energy Build-up"
            elif energy_change < -0.02:
                transition_type = "Energy Drop"
            elif brightness_change > 500:
                transition_type = "Brightness Increase"
            elif brightness_change < -500:
                transition_type = "Brightness Decrease"
            elif rhythm_change > 0.5:
                transition_type = "Rhythmic Intensification"
            elif rhythm_change < -0.5:
                transition_type = "Rhythmic Simplification"
            else:
                transition_type = "Gradual Evolution"
            
            transitions.append({
                'from_phase': current_phase['phase_number'],
                'to_phase': next_phase['phase_number'],
                'transition_time': next_phase['start_time'],
                'transition_type': transition_type,
                'energy_change': energy_change,
                'brightness_change': brightness_change,
                'rhythm_change': rhythm_change
            })
        
        return transitions
    
    def get_phase_statistics(self, phases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate summary statistics for detected phases.
        
        This method provides aggregate information about the phases,
        which is useful for understanding the overall structure and
        characteristics of the composition.
        
        Args:
            phases: List of detected phases
            
        Returns:
            Dictionary with phase statistics
        """
        if not phases:
            return {}
        
        # Calculate basic statistics
        total_duration = sum(phase['duration'] for phase in phases)
        avg_phase_duration = total_duration / len(phases)
        
        # Energy statistics
        energies = [phase['avg_energy'] for phase in phases]
        energy_range = max(energies) - min(energies)
        
        # Brightness statistics
        brightnesses = [phase['avg_brightness'] for phase in phases]
        brightness_range = max(brightnesses) - min(brightnesses)
        
        # Phase type distribution
        phase_types = [phase['phase_type'] for phase in phases]
        type_counts = {}
        for phase_type in phase_types:
            type_counts[phase_type] = type_counts.get(phase_type, 0) + 1
        
        # Structural characteristics
        has_climax = any('Climax' in phase['phase_type'] for phase in phases)
        has_breakdown = any('Breakdown' in phase['phase_type'] or 'Quiet' in phase['phase_type'] for phase in phases)
        
        return {
            'num_phases': len(phases),
            'total_duration': total_duration,
            'avg_phase_duration': avg_phase_duration,
            'energy_range': energy_range,
            'brightness_range': brightness_range,
            'phase_type_distribution': type_counts,
            'has_climax': has_climax,
            'has_breakdown': has_breakdown
        }