"""
Creative Descriptors for Synthesizer Music Analysis

This module defines the creative vocabulary used to describe synthesizer music
characteristics. The descriptors are designed to be intuitive for composers
and producers, bridging the gap between technical analysis and artistic understanding.

The descriptor system is based on:
1. Creative language that artists naturally use
2. Empirical analysis of synthesizer music characteristics
3. Psychological research on musical emotion and perception
4. Practical experience from electronic music production

The descriptors are organized into two main categories:
- Mood Descriptors: Emotional and atmospheric characteristics
- Character Tags: Instrument and synthesis characteristics
"""

from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class MoodDescriptor:
    """
    Definition of a mood descriptor with its characteristics and thresholds.
    
    This class encapsulates the rules and thresholds used to detect
    specific moods in synthesizer music. Each descriptor includes
    the technical criteria that must be met for identification.
    """
    name: str
    description: str
    energy_range: tuple
    brightness_range: tuple
    roughness_range: tuple
    onset_density_range: tuple
    duration_threshold: float
    spectral_bandwidth_range: tuple


@dataclass
class CharacterTag:
    """
    Definition of a character tag with its technical characteristics.
    
    This class defines the technical criteria used to identify
    different synthesizer types and sound sources.
    """
    name: str
    description: str
    spectral_centroid_range: tuple
    spectral_bandwidth_range: tuple
    spectral_rolloff_range: tuple
    zero_crossing_rate_range: tuple
    mfcc_characteristics: Dict[str, Any]


class MoodDescriptors:
    """
    Complete definition of all mood descriptors for synthesizer music.
    
    This class contains the comprehensive set of mood descriptors
    used to characterize the emotional and atmospheric qualities
    of electronic music. Each descriptor is defined with specific
    technical thresholds derived from analysis of synthesizer music.
    """
    
    # Core mood descriptors - the fundamental emotional categories
    CORE_DESCRIPTORS = {
        'spacey': MoodDescriptor(
            name='spacey',
            description='Ethereal, otherworldly atmosphere with sustained tones and minimal rhythm',
            energy_range=(0.0, 0.03),
            brightness_range=(2000, float('inf')),
            roughness_range=(0.0, 0.1),
            onset_density_range=(0.0, 0.5),
            duration_threshold=20.0,
            spectral_bandwidth_range=(0.0, 1500)
        ),
        
        'organic': MoodDescriptor(
            name='organic',
            description='Natural, textured sounds with harmonic richness and moderate energy',
            energy_range=(0.02, 0.08),
            brightness_range=(0.0, float('inf')),
            roughness_range=(0.1, float('inf')),
            onset_density_range=(0.0, float('inf')),
            duration_threshold=0.0,
            spectral_bandwidth_range=(1500, float('inf'))
        ),
        
        'synthetic': MoodDescriptor(
            name='synthetic',
            description='Precise, artificial textures with clean spectral characteristics',
            energy_range=(0.0, float('inf')),
            brightness_range=(1500, float('inf')),
            roughness_range=(0.0, 0.05),
            onset_density_range=(0.0, float('inf')),
            duration_threshold=0.0,
            spectral_bandwidth_range=(0.0, 1000)
        ),
        
        'oozy': MoodDescriptor(
            name='oozy',
            description='Slow, flowing textures with low energy and sustained character',
            energy_range=(0.0, 0.025),
            brightness_range=(0.0, 1500),
            roughness_range=(0.0, float('inf')),
            onset_density_range=(0.0, 0.5),
            duration_threshold=0.0,
            spectral_bandwidth_range=(0.0, float('inf'))
        ),
        
        'pensive': MoodDescriptor(
            name='pensive',
            description='Contemplative, balanced energy with moderate brightness and steady rhythm',
            energy_range=(0.03, 0.06),
            brightness_range=(1200, 2200),
            roughness_range=(0.0, float('inf')),
            onset_density_range=(0.5, 1.5),
            duration_threshold=0.0,
            spectral_bandwidth_range=(0.0, float('inf'))
        ),
        
        'tense': MoodDescriptor(
            name='tense',
            description='High energy with sharp spectral content and active rhythm',
            energy_range=(0.08, float('inf')),
            brightness_range=(2500, float('inf')),
            roughness_range=(0.0, float('inf')),
            onset_density_range=(2.0, float('inf')),
            duration_threshold=0.0,
            spectral_bandwidth_range=(0.0, float('inf'))
        ),
        
        'exuberant': MoodDescriptor(
            name='exuberant',
            description='High energy, bright, and rhythmically active with joyful character',
            energy_range=(0.1, float('inf')),
            brightness_range=(2000, float('inf')),
            roughness_range=(0.0, float('inf')),
            onset_density_range=(1.5, float('inf')),
            duration_threshold=0.0,
            spectral_bandwidth_range=(0.0, float('inf'))
        ),
        
        'glitchy': MoodDescriptor(
            name='glitchy',
            description='Irregular, fragmented textures with high roughness and complex rhythms',
            energy_range=(0.0, float('inf')),
            brightness_range=(0.0, float('inf')),
            roughness_range=(0.15, float('inf')),
            onset_density_range=(3.0, float('inf')),
            duration_threshold=0.0,
            spectral_bandwidth_range=(2000, float('inf'))
        ),
        
        'chaos': MoodDescriptor(
            name='chaos',
            description='Extreme energy and rhythm with unpredictable spectral characteristics',
            energy_range=(0.15, float('inf')),
            brightness_range=(0.0, 800),  # Can be very bright OR very dark
            roughness_range=(0.0, float('inf')),
            onset_density_range=(4.0, float('inf')),
            duration_threshold=0.0,
            spectral_bandwidth_range=(0.0, float('inf'))
        )
    }
    
    # Extended mood descriptors - more nuanced emotional categories
    EXTENDED_DESCRIPTORS = {
        'ethereal': MoodDescriptor(
            name='ethereal',
            description='Delicate, floating textures with very low energy and high brightness',
            energy_range=(0.0, 0.02),
            brightness_range=(3000, float('inf')),
            roughness_range=(0.0, float('inf')),
            onset_density_range=(0.0, 0.3),
            duration_threshold=0.0,
            spectral_bandwidth_range=(0.0, float('inf'))
        ),
        
        'atmospheric': MoodDescriptor(
            name='atmospheric',
            description='Ambient, environmental textures with minimal rhythm and wide spectrum',
            energy_range=(0.0, 0.015),
            brightness_range=(0.0, float('inf')),
            roughness_range=(0.0, float('inf')),
            onset_density_range=(0.0, 0.2),
            duration_threshold=0.0,
            spectral_bandwidth_range=(1800, float('inf'))
        ),
        
        'crystalline': MoodDescriptor(
            name='crystalline',
            description='Clear, precise textures with high brightness and low roughness',
            energy_range=(0.0, float('inf')),
            brightness_range=(2800, float('inf')),
            roughness_range=(0.0, 0.04),
            onset_density_range=(0.5, 1.5),
            duration_threshold=0.0,
            spectral_bandwidth_range=(0.0, float('inf'))
        ),
        
        'warm': MoodDescriptor(
            name='warm',
            description='Comfortable, enveloping textures with moderate brightness and rich harmonics',
            energy_range=(0.03, 0.08),
            brightness_range=(800, 1800),
            roughness_range=(0.0, float('inf')),
            onset_density_range=(0.0, float('inf')),
            duration_threshold=0.0,
            spectral_bandwidth_range=(1200, float('inf'))
        ),
        
        'melodic': MoodDescriptor(
            name='melodic',
            description='Tuneful, balanced textures with moderate characteristics',
            energy_range=(0.04, 0.09),
            brightness_range=(0.0, float('inf')),
            roughness_range=(0.0, float('inf')),
            onset_density_range=(0.3, 1.2),
            duration_threshold=0.0,
            spectral_bandwidth_range=(1000, 1600)
        ),
        
        'driving': MoodDescriptor(
            name='driving',
            description='Consistent, forward-moving energy with regular rhythm',
            energy_range=(0.05, 0.12),
            brightness_range=(0.0, float('inf')),
            roughness_range=(0.0, float('inf')),
            onset_density_range=(1.0, 2.5),
            duration_threshold=0.0,
            spectral_bandwidth_range=(800, 1800)
        ),
        
        'percussive': MoodDescriptor(
            name='percussive',
            description='Rhythmically active with high onset density and focused energy',
            energy_range=(0.06, float('inf')),
            brightness_range=(0.0, float('inf')),
            roughness_range=(0.0, float('inf')),
            onset_density_range=(2.5, float('inf')),
            duration_threshold=0.0,
            spectral_bandwidth_range=(0.0, float('inf'))
        ),
        
        'droning': MoodDescriptor(
            name='droning',
            description='Sustained, minimal rhythm with continuous energy',
            energy_range=(0.01, float('inf')),
            brightness_range=(0.0, float('inf')),
            roughness_range=(0.0, float('inf')),
            onset_density_range=(0.0, 0.1),
            duration_threshold=15.0,
            spectral_bandwidth_range=(0.0, float('inf'))
        )
    }
    
    @classmethod
    def get_all_descriptors(cls) -> Dict[str, MoodDescriptor]:
        """Get all mood descriptors combined."""
        all_descriptors = {}
        all_descriptors.update(cls.CORE_DESCRIPTORS)
        all_descriptors.update(cls.EXTENDED_DESCRIPTORS)
        return all_descriptors
    
    @classmethod
    def get_descriptor_names(cls) -> List[str]:
        """Get list of all descriptor names."""
        return list(cls.get_all_descriptors().keys())
    
    @classmethod
    def get_core_descriptor_names(cls) -> List[str]:
        """Get list of core descriptor names."""
        return list(cls.CORE_DESCRIPTORS.keys())
    
    @classmethod
    def get_extended_descriptor_names(cls) -> List[str]:
        """Get list of extended descriptor names."""
        return list(cls.EXTENDED_DESCRIPTORS.keys())


class CharacterTags:
    """
    Complete definition of all character tags for synthesizer music.
    
    This class contains the comprehensive set of character tags
    used to identify different synthesizer types and sound sources.
    Each tag is defined with specific technical characteristics.
    """
    
    # Synthesis type tags
    SYNTHESIS_TAGS = {
        'analog_synth': CharacterTag(
            name='analog_synth',
            description='Analog synthesizer with warm, organic characteristics',
            spectral_centroid_range=(0.0, float('inf')),
            spectral_bandwidth_range=(0.0, 1000),
            spectral_rolloff_range=(0.0, float('inf')),
            zero_crossing_rate_range=(0.0, 0.1),
            mfcc_characteristics={'warmth': 'high', 'precision': 'low'}
        ),
        
        'digital_synth': CharacterTag(
            name='digital_synth',
            description='Digital synthesizer with precise, clean characteristics',
            spectral_centroid_range=(2000, float('inf')),
            spectral_bandwidth_range=(0.0, 800),
            spectral_rolloff_range=(0.0, float('inf')),
            zero_crossing_rate_range=(0.0, float('inf')),
            mfcc_characteristics={'precision': 'high', 'warmth': 'low'}
        ),
        
        'mellotron': CharacterTag(
            name='mellotron',
            description='Mellotron/sampled instrument with irregular spectral content',
            spectral_centroid_range=(0.0, float('inf')),
            spectral_bandwidth_range=(1200, 2000),
            spectral_rolloff_range=(0.0, float('inf')),
            zero_crossing_rate_range=(0.05, 0.15),
            mfcc_characteristics={'organic': 'high', 'irregularity': 'high'}
        ),
        
        'percussive_instrument': CharacterTag(
            name='percussive_instrument',
            description='Percussive instrument with bright, transient characteristics',
            spectral_centroid_range=(2500, float('inf')),
            spectral_bandwidth_range=(0.0, float('inf')),
            spectral_rolloff_range=(4000, float('inf')),
            zero_crossing_rate_range=(0.1, float('inf')),
            mfcc_characteristics={'attack': 'sharp', 'sustain': 'low'}
        ),
        
        'acoustic_instrument': CharacterTag(
            name='acoustic_instrument',
            description='Acoustic instrument with rich, complex spectral content',
            spectral_centroid_range=(0.0, float('inf')),
            spectral_bandwidth_range=(1800, float('inf')),
            spectral_rolloff_range=(0.0, float('inf')),
            zero_crossing_rate_range=(0.12, float('inf')),
            mfcc_characteristics={'complexity': 'high', 'naturalness': 'high'}
        )
    }
    
    # Texture tags
    TEXTURE_TAGS = {
        'rich_texture': CharacterTag(
            name='rich_texture',
            description='Complex, layered texture with wide spectral bandwidth',
            spectral_centroid_range=(0.0, float('inf')),
            spectral_bandwidth_range=(2200, float('inf')),
            spectral_rolloff_range=(0.0, float('inf')),
            zero_crossing_rate_range=(0.0, float('inf')),
            mfcc_characteristics={'complexity': 'high', 'richness': 'high'}
        ),
        
        'pure_tone': CharacterTag(
            name='pure_tone',
            description='Simple, clean texture with narrow spectral bandwidth',
            spectral_centroid_range=(0.0, float('inf')),
            spectral_bandwidth_range=(0.0, 600),
            spectral_rolloff_range=(0.0, float('inf')),
            zero_crossing_rate_range=(0.0, float('inf')),
            mfcc_characteristics={'simplicity': 'high', 'purity': 'high'}
        ),
        
        'bright_harmonics': CharacterTag(
            name='bright_harmonics',
            description='Bright harmonic content with high spectral rolloff',
            spectral_centroid_range=(0.0, float('inf')),
            spectral_bandwidth_range=(0.0, float('inf')),
            spectral_rolloff_range=(5000, float('inf')),
            zero_crossing_rate_range=(0.0, float('inf')),
            mfcc_characteristics={'brightness': 'high', 'harmonics': 'upper'}
        ),
        
        'warm_harmonics': CharacterTag(
            name='warm_harmonics',
            description='Warm harmonic content with low spectral rolloff',
            spectral_centroid_range=(0.0, float('inf')),
            spectral_bandwidth_range=(0.0, float('inf')),
            spectral_rolloff_range=(0.0, 2000),
            zero_crossing_rate_range=(0.0, float('inf')),
            mfcc_characteristics={'warmth': 'high', 'harmonics': 'lower'}
        )
    }
    
    @classmethod
    def get_all_tags(cls) -> Dict[str, CharacterTag]:
        """Get all character tags combined."""
        all_tags = {}
        all_tags.update(cls.SYNTHESIS_TAGS)
        all_tags.update(cls.TEXTURE_TAGS)
        return all_tags
    
    @classmethod
    def get_tag_names(cls) -> List[str]:
        """Get list of all tag names."""
        return list(cls.get_all_tags().keys())
    
    @classmethod
    def get_synthesis_tag_names(cls) -> List[str]:
        """Get list of synthesis tag names."""
        return list(cls.SYNTHESIS_TAGS.keys())
    
    @classmethod
    def get_texture_tag_names(cls) -> List[str]:
        """Get list of texture tag names."""
        return list(cls.TEXTURE_TAGS.keys())
    
    @classmethod
    def get_tag_descriptions(cls) -> Dict[str, str]:
        """Get descriptions for all tags."""
        return {name: tag.description for name, tag in cls.get_all_tags().items()}


# Utility functions for working with descriptors
def get_descriptor_info() -> Dict[str, Any]:
    """
    Get comprehensive information about all available descriptors.
    
    Returns:
        Dictionary with descriptor information for documentation
    """
    return {
        'mood_descriptors': {
            'core': MoodDescriptors.get_core_descriptor_names(),
            'extended': MoodDescriptors.get_extended_descriptor_names(),
            'total_count': len(MoodDescriptors.get_all_descriptors())
        },
        'character_tags': {
            'synthesis': CharacterTags.get_synthesis_tag_names(),
            'texture': CharacterTags.get_texture_tag_names(),
            'total_count': len(CharacterTags.get_all_tags())
        },
        'descriptions': {
            'moods': {name: desc.description for name, desc in MoodDescriptors.get_all_descriptors().items()},
            'characters': CharacterTags.get_tag_descriptions()
        }
    }


def validate_descriptor_thresholds() -> Dict[str, Any]:
    """
    Validate that all descriptor thresholds are properly defined.
    
    Returns:
        Dictionary with validation results
    """
    issues = []
    
    # Check mood descriptors
    for name, desc in MoodDescriptors.get_all_descriptors().items():
        if desc.energy_range[0] > desc.energy_range[1]:
            issues.append(f"Mood {name}: Invalid energy range")
        if desc.brightness_range[0] > desc.brightness_range[1]:
            issues.append(f"Mood {name}: Invalid brightness range")
    
    # Check character tags
    for name, tag in CharacterTags.get_all_tags().items():
        if tag.spectral_centroid_range[0] > tag.spectral_centroid_range[1]:
            issues.append(f"Character {name}: Invalid spectral centroid range")
        if tag.spectral_bandwidth_range[0] > tag.spectral_bandwidth_range[1]:
            issues.append(f"Character {name}: Invalid spectral bandwidth range")
    
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'total_descriptors': len(MoodDescriptors.get_all_descriptors()) + len(CharacterTags.get_all_tags())
    }