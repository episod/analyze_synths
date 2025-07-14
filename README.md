# 🎹 Synthesizer Music Analysis Toolkit

A comprehensive, modular audio analysis toolkit designed specifically for composers and synthesizer music creators. This toolkit goes beyond academic metrics to provide intuitive, creative insights into your music using descriptors like "spacey," "organic," "crystalline," and "oozy."

## ✨ Features

### 🎵 Creative Mood Analysis
- **17 Creative Descriptors**: spacey, organic, synthetic, oozy, pensive, tense, exuberant, glitchy, chaos, ethereal, atmospheric, crystalline, warm, melodic, driving, percussive, droning
- **Instrument Character Classification**: Identifies analog synths, digital synths, Mellotron, percussive instruments, and acoustic elements
- **Phase-by-Phase Analysis**: Detailed breakdown of each musical section with mood descriptors

### 🎯 Intelligent Song Sequencing
- **Automatic Playlist Generation**: Creates optimal listening sequences based on musical flow principles
- **Key Compatibility**: Uses circle of fifths relationships for smooth transitions
- **Energy Arc Management**: Builds natural progression from atmospheric to climactic sections
- **Tempo Progression**: Ensures gradual tempo changes for better flow

### 📊 Comprehensive Analysis
- **Musical Phase Detection**: Automatically identifies intro, development, climax, and conclusion sections
- **Cluster Analysis**: Groups similar tracks for themed playlists
- **Creative Insights**: Understand your compositional patterns and sound palette
- **Multiple Export Formats**: CSV, JSON, and Markdown reports optimized for further analysis

## 🏗️ Architecture

### New Modular Design
The toolkit has been completely refactored into a professional Python package structure:

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

## 🚀 Quick Start

### Installation
```bash
# Clone or download the project
cd analyze_synths

# Create virtual environment
python -m venv .

# Activate virtual environment
source bin/activate  # On macOS/Linux
# or
.\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Usage Options

#### 🎵 Local Directory Analysis (Multiple Options)

**Option 1: Wrapper Script (Easiest)**
```bash
# Basic analysis - uses wrapper script
python analyze_library.py /path/to/your/music/directory

# With custom clustering
python analyze_library.py /path/to/music --clusters 3

# Export in specific format
python analyze_library.py /path/to/music --export-format markdown

# Get processing time estimate
python analyze_library.py /path/to/music --estimate

# Verbose output for debugging
python analyze_library.py /path/to/music --verbose

# Show supported formats and capabilities
python analyze_library.py --info
```

**Option 2: Direct Module Access**
```bash
# Same functionality, different invocation method
python -m audio_analysis.cli.main /path/to/your/music/directory

# All other options work the same way
python -m audio_analysis.cli.main /path/to/music --clusters 3
python -m audio_analysis.cli.main --info
```

#### 🌐 MCP Server Mode (Multiple Options)

**Option 1: Wrapper Script (Easiest)**
```bash
# Start MCP server - uses wrapper script
python mcp_server.py

# For use with FastMCP directly
fastmcp run mcp_server.py
```

**Option 2: Via analyze_library.py wrapper**
```bash
# Start MCP server with default settings
python analyze_library.py --mode mcp

# Start on custom host/port
python analyze_library.py --mode mcp --host 0.0.0.0 --port 8080
```

**Option 3: Direct Module Access**
```bash
# Direct module invocation
python -m audio_analysis.cli.main --mode mcp

# With custom settings
python -m audio_analysis.cli.main --mode mcp --host 0.0.0.0 --port 8080
```

#### 🐍 Python API Usage
```python
from audio_analysis import AudioAnalyzer

# Initialize analyzer
analyzer = AudioAnalyzer('/path/to/audio/files')

# Run complete analysis
df = analyzer.analyze_directory()

# Perform clustering
cluster_labels, centers, features = analyzer.perform_clustering()

# Generate sequence recommendations  
sequence = analyzer.recommend_sequence()

# Export all results
export_info = analyzer.export_comprehensive_analysis()
```

## 📁 What You Get

Each analysis creates a timestamped directory with organized results:

### 📈 Data Files (CSV format)
- `audio_features.csv` - Complete feature matrix (80+ features per track)
- `cluster_analysis.csv` - Musical groupings and characteristics
- `phase_analysis.csv` - Detailed phase breakdown with mood descriptors
- `sequence_recommendations.csv` - Optimal track ordering with reasoning
- `summary_statistics.csv` - High-level collection insights

### 🎨 Visualizations
- `phase_timeline.png` - Visual timeline of musical phases for all tracks
- `cluster_analysis.png` - Multi-panel cluster visualization with PCA
- `mood_distribution.png` - Mood analysis across your collection
- `sequence_recommendations.png` - Visual representation of optimal flow

### 📝 Reports
- `comprehensive_analysis_report.md` - **The main report** with:
  - Executive summary with key insights
  - Recommended listening sequence with detailed reasoning
  - Track-by-track mood and character analysis
  - Phase-by-phase structural breakdown
  - Cluster analysis for playlist creation
  - Creative insights and compositional recommendations
- `analysis_data.json` - Complete analysis data for programmatic access

## 🎼 Understanding Your Music

### Mood Descriptors (17 Total)
**Core Moods:**
- **Spacey**: Low energy, ethereal, expansive atmospheres
- **Organic**: Natural textures, acoustic-like characteristics  
- **Synthetic**: Clean, precise, distinctly electronic
- **Oozy**: Slow, flowing, liquid-like textures
- **Pensive**: Contemplative, moderate energy, thoughtful
- **Tense**: High energy, sharp, angular characteristics
- **Exuberant**: Joyful, high energy, bright
- **Glitchy**: Fragmented, stuttering, digital artifacts
- **Chaos**: Extreme energy, unpredictable, intense

**Extended Moods:**
- **Ethereal**: Delicate, floating, otherworldly
- **Atmospheric**: Environmental, ambient, immersive
- **Crystalline**: Clear, precise, bell-like
- **Warm**: Comfortable, enveloping, intimate
- **Melodic**: Tuneful, songlike, memorable
- **Driving**: Forward-moving, rhythmic, propulsive
- **Percussive**: Rhythmic, transient, beat-focused
- **Droning**: Sustained, minimal, hypnotic

### Character Tags (9 Total)
**Synthesis Types:**
- **Analog Synth**: Warm, vintage synthesizer characteristics
- **Digital Synth**: Clean, precise digital synthesis
- **Mellotron**: Sampled instrument textures, tape-like
- **Percussive Instrument**: Mallet instruments, bells, percussion
- **Acoustic Instrument**: Live recorded instruments

**Texture Types:**
- **Rich Texture**: Complex, layered, harmonically dense
- **Pure Tone**: Simple, clean, focused
- **Bright Harmonics**: High-frequency emphasis, sparkly
- **Warm Harmonics**: Low-frequency emphasis, cozy

## 🎯 Creative Applications

### For Composers
- **Study Your Patterns**: Understand your compositional tendencies through data
- **Album Sequencing**: Use AI-generated optimal listening sequences
- **Sound Palette Analysis**: Identify your dominant musical characteristics
- **Structural Insights**: Learn from phase analysis of your work
- **Mood Development**: Track emotional progression in your compositions

### For Producers
- **Playlist Creation**: Use cluster analysis for themed collections
- **Remix Planning**: Find compatible phases and sections across tracks
- **Energy Management**: Plan DJ sets using detailed energy progression data
- **Mood Matching**: Pair tracks with complementary emotional characteristics
- **Track Selection**: Find similar tracks for consistent album flow

### For Musicians
- **Practice Planning**: Sequence practice sessions using energy flow principles
- **Performance Sets**: Create dynamic live performance sequences
- **Collaboration**: Share detailed analysis with band members and collaborators
- **Inspiration**: Discover hidden patterns in your creative process
- **Learning**: Understand how your music affects listeners emotionally

## 🛠 Technical Requirements

- **Python 3.8+** (Developed and tested on 3.13)
- **Audio Formats**: WAV, AIFF, MP3 (WAV recommended for best quality)
- **Memory**: 4GB+ RAM for large collections (100+ files)
- **Storage**: Analysis exports typically 1-50MB per session
- **Dependencies**: All handled by requirements.txt

## 📊 Sample Output

### Command Line
```bash
$ python analyze_library.py /Users/composer/my_tracks

Initializing audio analyzer for: /Users/composer/my_tracks
Found 12 audio files. Processing...
Processing 1/12: ambient_dawn.wav
Processing 2/12: crystalline_patterns.wav
...

✓ CSV files exported to data/
✓ Plots saved to images/  
✓ Markdown report saved to comprehensive_analysis_report.md
✓ JSON results saved to analysis_data.json

============================================================
ANALYSIS COMPLETE
============================================================
Files processed: 12
Features extracted: 89
Phases detected: 47
Clusters created: 3
Export directory: /Users/composer/my_tracks/audio_analysis_20241213_143022
```

### Sequence Recommendations
```
RECOMMENDED LISTENING SEQUENCE
==============================================================

1. ambient_dawn.wav
   atmospheric • analog_synth • 3:45 • 72 BPM • C
   Opening track - sets the mood with atmospheric atmosphere

2. crystalline_patterns.wav  
   crystalline • digital_synth • 4:20 • 85 BPM • G
   Early exploration - introduces digital_synth textures

3. organic_flow.wav
   organic • mellotron • 5:12 • 92 BPM • G  
   Core development - showcases organic at 92 BPM
```

## 🌐 MCP Server Tools

When running in MCP mode, six powerful tools are available for remote analysis:

### 🎭 `analyze_audio_mood`
Comprehensive mood and character analysis with confidence scores
- **Input**: Audio files (base64 encoded)
- **Output**: 17 mood descriptors, character tags, musical metrics

### 🎵 `analyze_audio_phases`
Musical structure detection with mood analysis per section
- **Input**: Audio files (base64 encoded)  
- **Output**: Detailed phase breakdown with timing and characteristics

### 🎼 `recommend_song_sequence`
AI-powered optimal listening sequence generation
- **Input**: Multiple audio files (base64 encoded)
- **Output**: Recommended order with detailed reasoning

### 🎯 `analyze_audio_clusters`
K-means clustering for musical similarity grouping
- **Input**: Audio files and optional cluster count
- **Output**: Cluster analysis with musical groupings and characteristics

### 🎨 `comprehensive_audio_analysis`
Complete analysis pipeline with all features
- **Input**: Audio files and export format preference
- **Output**: Full analysis with mood, phases, clustering, and sequencing

### ℹ️ `get_supported_formats`
System capabilities and format information
- **Input**: None
- **Output**: Supported formats, descriptors, analysis capabilities

## 🔧 Advanced Features

### Extensive Inline Documentation
Every analytical approach is thoroughly documented with:
- **Why this method**: Explanation of creative relevance
- **How it works**: Technical implementation details  
- **Parameter choices**: Justification for thresholds and settings
- **Musical context**: Connection to composition and music theory

### Robust Error Handling
- **File validation**: Comprehensive format and content checking
- **Graceful degradation**: Analysis continues even with problematic files
- **Memory management**: Efficient processing of large collections
- **Progress reporting**: Detailed feedback during long operations

### Professional Export Options
- **CSV**: Optimized for spreadsheet analysis and data science
- **JSON**: Structured data for programmatic access and APIs
- **Markdown**: Human-readable reports with musical insights
- **Visualizations**: Publication-quality plots and charts

## 🔧 Troubleshooting

### Common Issues
- **Out of Memory**: Process files in smaller batches, increase system RAM
- **MP3 Issues**: Install additional codecs, convert to WAV for best results
- **No Files Found**: Verify audio files are in supported formats (WAV, AIFF, MP3)
- **Import Errors**: Ensure all dependencies installed: `pip install -r requirements.txt`
- **MCP Server Issues**: Install FastMCP: `pip install fastmcp`

### Getting Help
```bash
# Show detailed help (any method works)
python analyze_library.py --help
python -m audio_analysis.cli.main --help

# Show format information  
python analyze_library.py --info
python -m audio_analysis.cli.main --info

# Estimate processing time
python analyze_library.py /path/to/files --estimate
python -m audio_analysis.cli.main /path/to/files --estimate

# Run with verbose output for debugging
python analyze_library.py /path/to/files --verbose
python -m audio_analysis.cli.main /path/to/files --verbose
```

## 📚 Next Steps

### For New Users
1. **Start with a small collection** (5-10 tracks) to understand the output
2. **Read the comprehensive report** - Focus on the markdown file first
3. **Try the recommended sequence** - Play tracks in suggested order
4. **Explore the visualizations** - Understand your musical patterns
5. **Experiment with clustering** - Create themed playlists

### For Advanced Users
1. **Use the Python API** - Integrate with your existing workflow
2. **Customize analysis parameters** - Adjust clustering and export options
3. **Run MCP server** - Enable AI assistant integration
4. **Process large collections** - Use batch processing techniques
5. **Contribute improvements** - The modular architecture welcomes enhancements

### Integration Examples

#### With AI Assistants
```python
# Example for Claude/ChatGPT integration
from audio_analysis import AudioAnalyzer

analyzer = AudioAnalyzer('/path/to/music')
results = analyzer.analyze_directory()

# Send results to AI for creative interpretation
mood_analysis = results[['filename', 'primary_mood', 'mood_descriptors']]
# "Please analyze these mood patterns and suggest creative directions..."
```

#### With Music Software
```python
# Export data for DAW integration
analyzer.export_comprehensive_analysis(export_format='json')
# Import JSON into your DAW or music management software
```

#### Batch Processing
```bash
# Process multiple directories (using wrapper script)
for dir in /path/to/albums/*; do
    python analyze_library.py "$dir" --export-format csv
done

# Or using direct module access
for dir in /path/to/albums/*; do
    python -m audio_analysis.cli.main "$dir" --export-format csv
done
```

---

*Transform your music analysis from academic metrics to creative insights. Perfect for composers who want to understand their art through an intuitive, musical lens.* 🎶

**New in v2.0**: Complete modular refactor with extensive inline documentation, enhanced CLI, robust error handling, professional-grade architecture, and convenient wrapper scripts for easy access. The toolkit now provides multiple ways to run analysis while maintaining full backward compatibility.