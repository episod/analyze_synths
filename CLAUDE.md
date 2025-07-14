# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a comprehensive Python audio analysis toolkit designed specifically for composers and synthesizer music creators. It processes audio files to extract creative musical features, detect phases/sections, analyze mood and character, and provide intelligent song sequencing recommendations. The system focuses on creative descriptors rather than academic metrics, using terms like "spacey," "organic," "crystalline," and "oozy" that resonate with electronic music producers.

## New Modular Architecture (v2.0)

The project has been completely refactored from a monolithic structure into a professional Python package with extensive inline documentation explaining analytical approaches and their creative relevance.

### Package Structure
```
audio_analysis/
├── __init__.py                 # Main package interface
├── core/                       # Core analysis algorithms
│   ├── feature_extraction.py   # 80+ audio features with detailed comments
│   ├── phase_detection.py      # Musical structure detection
│   ├── clustering.py           # K-means clustering for track grouping
│   └── sequencing.py           # Intelligent song ordering
├── analysis/                   # Creative interpretation modules
│   ├── mood_analyzer.py        # 17 creative mood descriptors
│   ├── character_analyzer.py   # Synthesis type identification
│   └── descriptors.py          # Descriptor definitions and thresholds
├── utils/                      # Support utilities
│   ├── audio_io.py            # File loading and validation
│   ├── data_processing.py     # Data cleaning and standardization
│   └── visualization.py       # Publication-quality plots
├── exporters/                  # Output format handlers
│   ├── csv_exporter.py        # CSV export for spreadsheets
│   ├── json_exporter.py       # JSON for programmatic access
│   └── markdown_exporter.py   # Human-readable reports
├── api/                        # Main interfaces
│   ├── analyzer.py            # Primary AudioAnalyzer class
│   └── mcp_server.py          # FastMCP server integration
└── cli/                        # Command-line interface
    └── main.py                # Enhanced CLI with extensive options
```

## Environment Setup
- **Python Version**: 3.8+ (developed and tested on 3.13.5)
- **Virtual Environment**: Active venv located in project root
- **Dependencies**: Install with `pip install -r requirements.txt`
- **Key Libraries**: librosa (audio analysis), scikit-learn (clustering), matplotlib/seaborn (visualization), pydub (audio processing), fastmcp (server integration)

## Running the Application

### Local Directory Mode (Multiple Options)

**Option 1: Wrapper Script (Recommended)**
```bash
# Activate virtual environment (if not already active)
source bin/activate  # or `source .venv/bin/activate` if using .venv

# Run analysis using the wrapper script
python analyze_library.py <path_to_audio_directory>
python analyze_library.py --mode local <path_to_audio_directory>

# All CLI options work with the wrapper script
python analyze_library.py <path_to_audio_directory> --clusters 3 --export-format markdown --verbose

# Get processing time estimate
python analyze_library.py <path_to_audio_directory> --estimate

# Show supported formats and capabilities
python analyze_library.py --info

# Show detailed help
python analyze_library.py --help
```

**Option 2: Direct Module Access**
```bash
# Run analysis using direct module invocation
python -m audio_analysis.cli.main <path_to_audio_directory>
python -m audio_analysis.cli.main --mode local <path_to_audio_directory>

# All CLI options work the same way
python -m audio_analysis.cli.main <path_to_audio_directory> --clusters 3 --export-format markdown --verbose

# Get processing time estimate
python -m audio_analysis.cli.main <path_to_audio_directory> --estimate

# Show supported formats and capabilities
python -m audio_analysis.cli.main --info

# Show detailed help
python -m audio_analysis.cli.main --help
```

### MCP Server Mode (Multiple Options)

**Option 1: Dedicated MCP Server Script (Recommended for FastMCP)**
```bash
# Start FastMCP server using dedicated wrapper
python mcp_server.py

# For use with FastMCP command
fastmcp run mcp_server.py
```

**Option 2: Via analyze_library.py Wrapper**
```bash
# Start FastMCP server using main wrapper
python analyze_library.py --mode mcp
python analyze_library.py --mode mcp --host 0.0.0.0 --port 8080
```

**Option 3: Direct Module Access**
```bash
# Start server using direct module invocation
python -m audio_analysis.cli.main --mode mcp
python -m audio_analysis.cli.main --mode mcp --host 0.0.0.0 --port 8080
```

### Python API Usage
```python
from audio_analysis import AudioAnalyzer

# Initialize and run analysis
analyzer = AudioAnalyzer('/path/to/audio/files')
df = analyzer.analyze_directory()

# Perform clustering and sequencing
cluster_labels, centers, features = analyzer.perform_clustering()
sequence = analyzer.recommend_sequence()

# Export comprehensive results
export_info = analyzer.export_comprehensive_analysis()
```

## Wrapper Scripts (v2.0)

The refactored toolkit includes convenient wrapper scripts that provide easy access to the modular architecture:

### analyze_library.py
- **Purpose**: Main wrapper script for command-line analysis
- **Backward Compatibility**: Drop-in replacement for the original monolithic script
- **Usage**: `python analyze_library.py /path/to/audio/directory`
- **Features**: Full CLI interface, MCP server mode, all options supported
- **Implementation**: Imports and calls `audio_analysis.cli.main.main()`

### mcp_server.py
- **Purpose**: Dedicated MCP server wrapper script
- **FastMCP Compatible**: Works with `fastmcp run mcp_server.py`
- **Usage**: `python mcp_server.py` or `fastmcp run mcp_server.py`
- **Features**: Starts MCP server with 6 analysis tools exposed
- **Implementation**: Imports and runs `audio_analysis.api.mcp_server.mcp.run()`

## Core Analysis Components

### FeatureExtractor (core/feature_extraction.py)
- **Purpose**: Extract 80+ comprehensive audio features per track
- **Key Methods**: 
  - `extract_features()`: Main extraction pipeline with detailed comments explaining each feature's creative relevance
  - `extract_basic_spectral_features()`: Lightweight extraction for phase analysis
- **Features**: Spectral (brightness, bandwidth), temporal (energy, rhythm), harmonic (key, chroma), structural (phases)
- **Comments Focus**: Why each feature matters for creative music analysis

### PhaseDetector (core/phase_detection.py)
- **Purpose**: Detect musical phases/sections using signal processing + music theory
- **Key Methods**:
  - `detect_phases()`: Core algorithm using energy and spectral change detection
  - `classify_phase()`: Assign musical meaning (intro, climax, breakdown, etc.)
- **Approach**: 2-second smoothing windows, gradient analysis, heuristic classification
- **Comments Focus**: How signal processing translates to musical understanding

### AudioClusterer (core/clustering.py)
- **Purpose**: Group similar tracks using K-means clustering
- **Key Methods**:
  - `perform_clustering()`: Complete clustering pipeline with optimization
  - `analyze_clusters()`: Interpret cluster characteristics musically
- **Features**: Automatic cluster count, standardization, musical coherence assessment
- **Comments Focus**: Translating technical clusters into musical groupings

### SequenceRecommender (core/sequencing.py)
- **Purpose**: Generate optimal listening sequences using musical flow principles
- **Key Methods**:
  - `recommend_sequence()`: Complete sequencing with transition scoring
  - `_calculate_transition_score()`: Multi-factor compatibility assessment
- **Approach**: Key relationships, tempo progression, energy arcs, mood compatibility
- **Comments Focus**: Music theory principles behind algorithmic sequencing

### MoodAnalyzer (analysis/mood_analyzer.py)
- **Purpose**: Creative mood classification using 17 descriptors
- **Key Methods**:
  - `analyze_mood()`: Threshold-based classification optimized for synthesizer music
  - `analyze_track_mood()`: Complete track-level mood analysis
- **Descriptors**: Core (spacey, organic, synthetic, oozy, pensive, tense, exuberant, glitchy, chaos) + Extended (ethereal, atmospheric, crystalline, warm, melodic, driving, percussive, droning)
- **Comments Focus**: Why each threshold captures specific creative characteristics

### CharacterAnalyzer (analysis/character_analyzer.py)
- **Purpose**: Identify synthesis types and sound characteristics
- **Key Methods**:
  - `analyze_character()`: Spectral analysis + MFCC timbre fingerprinting
  - `analyze_track_character()`: Complete character profiling
- **Categories**: Synthesis types (analog_synth, digital_synth, mellotron, percussive_instrument, acoustic_instrument), Texture types (rich_texture, pure_tone, bright_harmonics, warm_harmonics)
- **Comments Focus**: How technical features map to synthesis identification

## Key Architecture Improvements

### Extensive Inline Documentation
Every analytical approach includes detailed comments explaining:
- **Why this approach**: Creative relevance and musical justification
- **Technical rationale**: How algorithms relate to musical understanding  
- **Parameter choices**: Empirical basis for thresholds and settings
- **Creative context**: Connection to composition and music theory

### Professional Python Patterns
- **Type hints**: Full type annotations for better IDE support and clarity
- **Dataclasses**: Structured data with validation (e.g., SequenceTrack, MoodDescriptor)
- **Error handling**: Comprehensive exception handling with meaningful messages
- **Modular design**: Single responsibility principle, easy testing and maintenance
- **Documentation**: Detailed docstrings explaining purpose and usage

### Robust Data Processing
- **Validation**: Comprehensive file format and content checking
- **Cleaning**: Intelligent handling of missing values and outliers
- **Standardization**: Proper scaling for machine learning algorithms
- **Export optimization**: Multiple formats optimized for different use cases

## Export System

### CSV Exports (exporters/csv_exporter.py)
- `audio_features.csv`: Complete feature matrix (80+ features per track)
- `cluster_analysis.csv`: Cluster characteristics and membership
- `phase_analysis.csv`: Flattened phase data with timing and mood
- `sequence_recommendations.csv`: Optimal ordering with reasoning
- `summary_statistics.csv`: High-level collection metrics

### JSON Exports (exporters/json_exporter.py)
- `analysis_data.json`: Complete structured data for programmatic access
- Proper type conversion from numpy/pandas to JSON-serializable formats
- Hierarchical structure preservation for complex relationships

### Markdown Reports (exporters/markdown_exporter.py)
- `comprehensive_analysis_report.md`: Human-readable report with:
  - Executive summary with key insights
  - Recommended listening sequence with reasoning
  - Track-by-track analysis with mood and character
  - Phase-by-phase structural breakdown
  - Cluster analysis for playlist creation
  - Creative insights and compositional recommendations

## Visualization System (utils/visualization.py)

### Phase Timeline Plots
- Visual representation of musical structure over time
- Color-coded phase types with detailed legends
- Timeline markers for easy navigation
- Multiple tracks displayed in organized layout

### Cluster Analysis Plots
- PCA projection showing track relationships in 2D space
- Feature comparison plots (tempo vs energy, brightness vs bandwidth)
- Cluster size and characteristics visualization
- Key distribution analysis across clusters

### Mood and Sequence Plots
- Mood distribution across collection
- Energy and tempo progression through recommended sequence
- Timeline view of optimal track ordering

## MCP Server Integration (api/mcp_server.py)

### Available Tools
1. **analyze_audio_mood**: Mood and character analysis with confidence scores
2. **analyze_audio_phases**: Musical structure detection with timing and characteristics
3. **recommend_song_sequence**: Optimal listening sequence generation
4. **analyze_audio_clusters**: K-means clustering for similarity grouping
5. **comprehensive_audio_analysis**: Complete analysis pipeline
6. **get_supported_formats**: Capability and format information

### Implementation Features
- Base64 audio file encoding/decoding
- Temporary session management with isolation
- Comprehensive input validation and error handling
- Structured JSON responses optimized for programmatic access
- Helper functions for categorization and insight generation

## Creative Descriptors System

### Mood Descriptors (17 total)
Empirically calibrated thresholds based on energy, spectral, and temporal characteristics:

**Core Descriptors** (9):
- **spacey**: Low energy (0-0.03), high brightness (>2000Hz), minimal rhythm
- **organic**: Moderate energy (0.02-0.08), high roughness (>0.1), rich harmonics
- **synthetic**: Low roughness (<0.05), narrow bandwidth (<1000Hz), precise characteristics
- **oozy**: Very low energy (<0.025), low brightness (<1500Hz), sustained character
- **pensive**: Balanced characteristics (energy 0.03-0.06, rhythm 0.5-1.5)
- **tense**: High energy (>0.08), high rhythm (>2.0), sharp spectral content
- **exuberant**: Very high energy (>0.1), bright, rhythmically active
- **glitchy**: High roughness (>0.15), complex rhythms (>3.0), wide bandwidth
- **chaos**: Extreme energy (>0.15), very high rhythm (>4.0), unpredictable spectrum

**Extended Descriptors** (8):
- **ethereal**: Very low energy (<0.02), very bright (>3000Hz), sparse rhythm
- **atmospheric**: Minimal rhythm (<0.2), wide spectrum (>1800Hz), sustained
- **crystalline**: High brightness (>2800Hz), low roughness (<0.04), precise
- **warm**: Mid-range brightness (800-1800Hz), rich harmonics (>1200Hz bandwidth)
- **melodic**: Balanced characteristics with moderate complexity
- **driving**: Consistent energy (0.05-0.12), regular rhythm (1.0-2.5)
- **percussive**: High rhythm density (>2.5), focused energy bursts
- **droning**: Very low rhythm (<0.1), sustained energy, long duration (>15s)

### Character Tags (9 total)
Based on spectral analysis and harmonic content:

**Synthesis Types** (5):
- **analog_synth**: Narrow bandwidth (<1000Hz), low roughness (<0.1)
- **digital_synth**: Narrow bandwidth (<800Hz), high brightness (>2000Hz)
- **mellotron**: Moderate bandwidth (1200-2000Hz), irregular spectrum
- **percussive_instrument**: High brightness (>2500Hz), high rolloff (>4000Hz)
- **acoustic_instrument**: Wide bandwidth (>1800Hz), high roughness (>0.12)

**Texture Types** (4):
- **rich_texture**: Very wide bandwidth (>2200Hz)
- **pure_tone**: Very narrow bandwidth (<600Hz)
- **bright_harmonics**: High rolloff (>5000Hz)
- **warm_harmonics**: Low rolloff (<2000Hz)

## Common Development Tasks

### Adding New Mood Descriptors
1. Define descriptor in `analysis/descriptors.py` with technical criteria
2. Add detection logic in `analysis/mood_analyzer.py`
3. Update documentation and tests
4. Ensure thresholds are empirically validated

### Extending Character Analysis
1. Add character definition in `analysis/descriptors.py`
2. Implement detection in `analysis/character_analyzer.py`
3. Update MCP server response formatting
4. Test with representative audio samples

### Adding Export Formats
1. Create new exporter in `exporters/` following existing patterns
2. Integrate with `api/analyzer.py` export system
3. Add CLI option in `cli/main.py`
4. Update documentation

### Enhancing Visualizations
1. Add plot method to `utils/visualization.py`
2. Integrate with analyzer export pipeline
3. Ensure publication-quality output
4. Add configuration options for customization

## Testing and Validation

### Audio Test Files
- Use WAV format for best quality and consistency
- Include variety of synthesis types and moods
- Test with different durations and complexities
- Validate descriptor accuracy against human perception

### Performance Testing
- Monitor memory usage with large collections (100+ files)
- Test clustering stability with different random seeds
- Validate export file sizes and formats
- Ensure MCP server handles concurrent requests

### Error Handling
- Test with corrupted/invalid audio files
- Validate graceful degradation with missing features
- Test memory constraints and cleanup
- Verify proper error messages and logging

## Architecture Benefits

### For Developers
- **Familiar structure**: Standard Python package layout following best practices
- **Clear separation**: Each module has single, well-defined responsibility
- **Extensive documentation**: Every analytical choice explained with creative context
- **Type safety**: Full type hints for better development experience
- **Easy testing**: Modular design allows isolated unit testing

### For Users
- **Same functionality**: All existing features preserved and enhanced
- **Better performance**: Optimized algorithms and data structures
- **More formats**: Additional export options (CSV, JSON, Markdown)
- **Enhanced CLI**: Professional command-line interface with extensive options
- **Better visualization**: Publication-quality plots and charts

### For Composers
- **Creative insights**: Technical analysis translated to musical understanding
- **Educational value**: Learn audio analysis through extensive inline comments
- **Practical tools**: Better integration with music production workflows
- **Artistic context**: Technical features connected to creative decisions
- **Professional reports**: Detailed analysis suitable for sharing and archiving

## Migration from Legacy System

### Backward Compatibility
- Original `analyze_library.py` still functional
- Same output directory structure and file formats
- Identical analysis results and recommendations
- MCP server tools maintain same interface

### New Features Available
- Enhanced CLI with extensive options and help
- Professional Python API for integration
- Additional export formats and visualization options
- Improved error handling and progress reporting
- Modular architecture for custom extensions

### Recommended Migration Path
1. Test new CLI interface with existing audio collections
2. Explore enhanced export formats and visualizations
3. Integrate Python API for custom workflows
4. Utilize MCP server for AI assistant integration
5. Leverage modular architecture for custom extensions

## Important Notes

### Virtual Environment Required
- **Critical**: Always activate virtual environment before running any scripts
- **Command**: `source bin/activate` (or `source .venv/bin/activate` if using .venv)
- **Error**: Import errors will occur if virtual environment is not activated
- **Dependencies**: All required packages are installed in the virtual environment

### Wrapper Scripts vs Direct Module Access
- **Wrapper Scripts**: Easier to use, maintain backward compatibility
  - `python analyze_library.py` - Main analysis interface
  - `python mcp_server.py` - Dedicated MCP server
- **Direct Module**: More explicit, better for development
  - `python -m audio_analysis.cli.main` - Direct CLI access
- **Both methods**: Provide identical functionality and options

### Performance Considerations
- Large collections (100+ files) may require significant RAM
- Phase detection is the most memory-intensive operation
- Consider processing in batches for very large collections
- Export files can be substantial (1-50MB) for large analyses

### Audio Format Recommendations
- **WAV**: Best quality, fastest processing, recommended for analysis
- **AIFF**: Equivalent to WAV, fully supported
- **MP3**: Supported but may have slight quality reduction
- **File size**: Up to 100MB per file supported
- **Duration**: 1 second minimum, 30 minutes maximum recommended

### Creative Accuracy
- Descriptors calibrated specifically for synthesizer music
- Thresholds may need adjustment for other musical genres
- Human validation recommended for critical applications
- Confidence scores help assess reliability of classifications

### Common Issues and Solutions
- **Import Errors**: Ensure virtual environment is activated
- **Module Not Found**: Check that all dependencies are installed in venv
- **MCP Server Issues**: Verify `fastmcp` is installed: `pip install fastmcp`
- **Memory Issues**: Process smaller batches or increase system RAM
- **Pandas/Numpy Errors**: Fixed in v2.0 - update to latest version

## Future Development

### Planned Enhancements
- Additional mood descriptors for specific electronic subgenres
- Real-time analysis capabilities for live performance
- Integration with popular DAWs and music software
- Machine learning improvements for descriptor accuracy
- Extended visualization options and customization

### Extension Points
- Custom descriptor definitions in `analysis/descriptors.py`
- Additional clustering algorithms in `core/clustering.py`
- New export formats in `exporters/`
- Enhanced visualization types in `utils/visualization.py`
- Custom analysis workflows in `api/analyzer.py`

## Code Quality Improvements (v2.1)

### Code Duplication Elimination
The codebase has been systematically analyzed and refactored to eliminate code duplication patterns that emerged during the initial v2.0 modularization. This cleanup ensures better maintainability and consistency.

#### New Shared Utility Modules Added:

**`utils/type_conversion.py`** - Centralized type conversion utilities
- `safe_float_convert()`: Robust float conversion with fallback values
- `convert_dict_values_to_float()`: Batch dictionary value conversion  
- `convert_phase_data_types()`: Specialized phase data type conversion
- `convert_spectral_features_types()`: Spectral feature type conversion
- `convert_mood_analysis_input()`: Mood analysis input standardization
- `ensure_python_types()`: Convert numpy/pandas types to Python types for JSON serialization

**`utils/validation.py`** - Shared validation utilities
- `validate_range()`: Check if values fall within specified ranges
- `validate_feature_ranges()`: Comprehensive feature validation
- `validate_phase_data()`: Phase data structure validation
- `validate_spectral_features()`: Spectral feature validation
- `validate_audio_files_list()`: Audio file list validation

**`utils/statistics.py`** - Statistical calculation utilities
- `calculate_phase_statistics()`: Comprehensive phase metrics across all files
- `calculate_collection_summary()`: High-level collection statistics
- `calculate_cluster_statistics()`: Cluster analysis metrics
- `calculate_feature_statistics()`: Feature distribution analysis
- `format_time_duration()`: Human-readable duration formatting (e.g., "3:45", "1:23:45")
- `format_time_position()`: Time position formatting (e.g., "03:45")
- `calculate_progression_trend()`: Trend analysis for value sequences ('increasing', 'decreasing', 'stable')
- `safe_divide()`: Division with zero-denominator protection
- `calculate_normalized_score()`: 0-1 normalized scoring

#### Duplication Patterns Eliminated:

**High Priority (Completed)**:
1. **Scattered `float()` conversions** - Centralized in type conversion utilities
   - 15+ instances across mood_analyzer.py, character_analyzer.py, phase_detection.py
   - Now uses `safe_float_convert()` with proper error handling
   
2. **Duplicate `_in_range()` methods** - Unified validation logic  
   - Previously duplicated in mood_analyzer.py and character_analyzer.py
   - Now uses shared `validate_range()` function
   
3. **Repeated type conversion patterns** - Standardized approach
   - Complex conversion logic for mood and character analysis
   - Now uses specialized conversion functions for different data types
   
4. **Statistical calculations** - Centralized computation
   - Summary statistics duplicated between csv_exporter.py and analyzer.py
   - Phase statistics calculated multiple times across different files
   - Now uses shared statistical utilities
   
5. **Time formatting functions** - Unified formatting
   - Duration and time formatting duplicated in CSV exporter
   - Now uses shared formatting functions with consistent output

#### Files Refactored to Use Shared Utilities:

**`analysis/mood_analyzer.py`**:
- Uses `convert_mood_analysis_input()` for input standardization
- Uses `validate_range()` for threshold checking
- Uses `safe_float_convert()` for fallback mood determination

**`analysis/character_analyzer.py`**:
- Uses `convert_spectral_features_types()` for input processing
- Uses `validate_range()` replacing duplicate `_in_range()` method
- Eliminated duplicate validation code

**`core/phase_detection.py`**:
- Uses `ensure_python_types()` for phase data type conversion
- Consistent type handling for all phase characteristics
- Proper numpy to Python type conversion for JSON serialization

**`api/analyzer.py`**:
- Uses `calculate_progression_trend()` for energy/brightness progression analysis
- Uses `safe_float_convert()` for structural feature calculations
- Unified trend calculation logic replacing custom implementations

**`exporters/csv_exporter.py`**:
- Uses `calculate_collection_summary()` replacing `_calculate_summary_statistics()`
- Uses `format_time_duration()` and `format_time_position()` for time formatting
- Eliminated duplicate time formatting methods

#### Benefits Achieved:

**Consistency**: All type conversions, validations, and statistical calculations now use the same robust implementations across the entire codebase.

**Maintainability**: Changes to validation logic, type conversion, or statistical calculations only need to be made in one place, reducing maintenance burden.

**Reliability**: Shared utilities have centralized error handling and edge case management, improving overall system stability.

**Code Quality**: Eliminated approximately 15+ instances of duplicated code patterns while maintaining backward compatibility.

**Development Efficiency**: Developers can now rely on well-tested utility functions instead of reimplementing common patterns.

#### Updated Package Structure:
```
utils/
├── audio_io.py            # File loading and validation
├── data_processing.py     # Data cleaning and standardization  
├── visualization.py       # Publication-quality plots
├── type_conversion.py     # 🆕 Centralized type conversion utilities
├── validation.py          # 🆕 Shared validation functions
└── statistics.py          # 🆕 Statistical calculation utilities
```

The utils package now provides a comprehensive suite of support functions that eliminate code duplication while maintaining clean, modular architecture. All utility functions are properly imported and available through the package's `__init__.py` interface.