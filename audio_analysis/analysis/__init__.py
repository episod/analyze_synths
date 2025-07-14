"""
Analysis modules for creative mood and character classification.

This package contains the specialized analysis algorithms that interpret
technical audio features into creative, musical descriptors that composers
and producers can relate to and use in their work.

The analysis approach is based on:
1. Mapping technical features to creative characteristics
2. Using thresholds derived from synthesizer music analysis
3. Providing interpretable results for artistic decision-making
4. Supporting both individual track and phase-level analysis

Modules:
- mood_analyzer: Creative mood classification using 17 descriptors
- character_analyzer: Instrument/synthesis character detection
- descriptors: Definitions and mappings for creative descriptors
"""

from .mood_analyzer import MoodAnalyzer
from .character_analyzer import CharacterAnalyzer
from .descriptors import MoodDescriptors, CharacterTags

__all__ = [
    'MoodAnalyzer',
    'CharacterAnalyzer',
    'MoodDescriptors',
    'CharacterTags'
]