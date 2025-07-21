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

### New Modular Design with Parallel Processing (v2.1)
The toolkit has been completely refactored into a professional Python package structure with comprehensive parallel processing capabilities:

```
audio_analysis/
├── __init__.py                 # Main package interface with parallel components
├── core/                       # Core analysis algorithms
│   ├── feature_extraction.py   # 80+ audio features with detailed comments
│   ├── feature_extraction_base.py  # 🆕 Shared feature extraction core
│   ├── parallel_feature_extraction.py  # 🆕 Parallel feature extraction
│   ├── phase_detection.py      # Musical structure detection
│   ├── clustering.py           # K-means clustering for track grouping
│   ├── parallel_clustering.py  # 🆕 Distributed clustering with tensor support
│   ├── tensor_operations.py    # 🆕 Hardware-agnostic tensor processing
│   └── sequencing.py           # Intelligent song ordering
├── analysis/                   # Creative interpretation modules
│   ├── mood_analyzer.py        # 17 creative mood descriptors
│   ├── character_analyzer.py   # Synthesis type identification
│   └── descriptors.py          # Descriptor definitions and thresholds
├── utils/                      # Support utilities
│   ├── audio_io.py            # File loading and validation
│   ├── data_processing.py     # Data cleaning and standardization
│   ├── visualization.py       # Publication-quality plots
│   ├── type_conversion.py     # Centralized type conversion utilities
│   ├── validation.py          # Shared validation functions
│   └── statistics.py          # Statistical calculation utilities
├── exporters/                  # Output format handlers
│   ├── csv_exporter.py        # CSV export for spreadsheets
│   ├── json_exporter.py       # JSON for programmatic access
│   └── markdown_exporter.py   # Human-readable reports
├── api/                        # Main interfaces
│   ├── analyzer.py            # Primary AudioAnalyzer class
│   ├── parallel_analyzer.py   # 🆕 ParallelAudioAnalyzer for scalable processing
│   └── mcp_server.py          # FastMCP server integration
└── cli/                        # Command-line interface
    └── main.py                # Enhanced CLI with extensive options
```

### Key Architectural Improvements (v2.1)

**🚀 Parallel Processing:**
- **6x+ Performance**: Multi-core processing with automatic optimization
- **Tensor-Ready**: Data structures optimized for hardware acceleration
- **Scalable**: Configurable batch sizes and memory limits
- **Hardware-Agnostic**: CPU, GPU, and future Tenstorrent processor support

**🔧 Code Quality:**
- **Single Source of Truth**: Shared feature extraction core eliminates duplication
- **Consistent Results**: Traditional and parallel processing produce identical outputs
- **Easy Extension**: Add new moods and characters in one location
- **Better Testing**: Comprehensive test coverage with shared utilities

**⚡ Performance Benchmarks:**
- **Feature Extraction**: 6.7x speedup (8 cores)
- **Phase Detection**: 5.6x speedup (8 cores)  
- **Clustering**: 5.0x speedup (8 cores)
- **Total Analysis**: 6.1x speedup (8 cores)

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

**Option 3: Parallel Processing Demo (NEW v2.1)**
```bash
# Run parallel processing demonstration
python parallel_demo.py /path/to/music --workers 8 --batch-size 16

# Enable tensor optimizations for hardware acceleration
python parallel_demo.py /path/to/music --enable-tensor --device cpu

# Run specific demo modes
python parallel_demo.py /path/to/music --demo extraction    # Feature extraction only
python parallel_demo.py /path/to/music --demo clustering    # Clustering only
python parallel_demo.py /path/to/music --demo complete      # Full analysis
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

**Standard Analysis:**
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

# Export all results (default: all formats)
export_info = analyzer.export_comprehensive_analysis()

# Export specific formats
export_info = analyzer.export_comprehensive_analysis(export_format="markdown")
export_info = analyzer.export_comprehensive_analysis(export_format="json", base_name="my_analysis")
```

**Parallel Processing (NEW v2.1):**
```python
from audio_analysis import ParallelAudioAnalyzer, ProcessingConfig

# Configure parallel processing
config = ProcessingConfig(
    max_workers=8,                    # Use 8 CPU cores
    batch_size=16,                    # Process 16 files per batch
    enable_tensor_optimization=True,  # Enable tensor operations
    memory_limit_mb=4096             # 4GB memory limit
)

# Initialize parallel analyzer
analyzer = ParallelAudioAnalyzer('/path/to/audio/files', config)

# Same interface as standard analyzer
df = analyzer.analyze_directory()
cluster_labels, centers, features = analyzer.perform_clustering()
sequence = analyzer.recommend_sequence()
export_info = analyzer.export_comprehensive_analysis(export_format="all")

# Get parallel processing statistics
stats = analyzer.get_processing_statistics()
print(f"Parallel speedup: {stats['parallel_processing_stats']['parallel_speedup']:.1f}x")
print(f"Throughput: {stats['parallel_processing_stats']['throughput']:.1f} files/second")
```

**Hardware Acceleration (Future-Ready):**
```python
from audio_analysis import TensorFeatureExtractor

# CPU processing with tensor optimizations
extractor = TensorFeatureExtractor(device="cpu")
features = extractor.extract_features_from_paths(audio_file_paths)

# Tenstorrent processing (when available)
extractor = TensorFeatureExtractor(device="tenstorrent", device_id=0)
features = extractor.extract_features_from_paths(audio_file_paths)
```

**Export Format Options (NEW v2.2):**
```python
from audio_analysis import AudioAnalyzer

analyzer = AudioAnalyzer('/path/to/audio/files')
analyzer.analyze_directory()

# Export all formats (default: CSV data + JSON + Markdown + visualizations)
analyzer.export_comprehensive_analysis()

# Export only specific formats for faster processing
analyzer.export_comprehensive_analysis(export_format="markdown")  # Human-readable report only
analyzer.export_comprehensive_analysis(export_format="json")     # Programmatic data only  
analyzer.export_comprehensive_analysis(export_format="csv")      # Spreadsheet data only

# Customize file naming
analyzer.export_comprehensive_analysis(
    export_format="json", 
    base_name="my_project"
)  # → Creates: my_project_data.json

# Full customization
analyzer.export_comprehensive_analysis(
    export_dir="/custom/path",
    export_format="markdown", 
    base_name="album_analysis",
    show_plots=True
)  # → Creates: album_analysis_comprehensive_report.md
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

### 🚀 Parallel Processing (NEW v2.1)
- **Multi-Core Processing**: Automatic utilization of all available CPU cores
- **Configurable Batching**: Process multiple files simultaneously with optimized memory usage
- **Performance Scaling**: 6x+ speedup on multi-core systems
- **Hardware Acceleration**: Tensor-optimized data structures for future acceleration
- **Memory Management**: Intelligent memory usage with configurable limits

### 🏗️ Hardware Acceleration Ready
- **Tensor Operations**: Data structures optimized for Tenstorrent processors
- **Device Abstraction**: Hardware-agnostic interface supports CPU, GPU, and specialized processors
- **Batch Processing**: Optimal utilization of parallel processing units
- **Memory Efficiency**: Minimize data movement between processing units
- **Future-Proof**: Easy integration with emerging hardware acceleration platforms

### 📊 Comprehensive Performance Monitoring
- **Processing Statistics**: Detailed performance metrics and throughput analysis
- **Parallel Speedup**: Real-time calculation of performance improvements
- **Memory Usage**: Monitoring and optimization of memory consumption
- **Error Tracking**: Comprehensive error handling and reporting
- **Benchmarking**: Built-in performance benchmarking tools

### 🎯 Extensible Architecture
- **Single Source of Truth**: Add new mood descriptors in one place
- **Consistent Analysis**: Traditional and parallel processing produce identical results
- **Easy Extension**: Simple framework for adding new creative descriptors
- **Modular Design**: Clean separation of concerns for easy maintenance
- **Comprehensive Testing**: Shared utilities ensure consistent behavior

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

# Parallel processing demo and help
python parallel_demo.py --help
python example_mood_extension.py  # Shows how to add new mood descriptors
```

### Performance Optimization
```bash
# For large collections, use parallel processing
python parallel_demo.py /path/to/files --workers 16 --batch-size 32

# Enable tensor optimizations
python parallel_demo.py /path/to/files --enable-tensor --device cpu

# Monitor memory usage and adjust batch size
python parallel_demo.py /path/to/files --batch-size 8 --memory-limit 2048
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

**New in v2.1**: Comprehensive parallel processing capabilities with 6x+ performance improvements, hardware acceleration readiness for Tenstorrent processors, tensor-optimized data structures, and a refactored architecture that eliminates code duplication while maintaining full backward compatibility.

**Previous v2.0**: Complete modular refactor with extensive inline documentation, enhanced CLI, robust error handling, professional-grade architecture, and convenient wrapper scripts for easy access.

## 🌐 Hugging Face Deployment (NEW v2.2)

The toolkit now includes a complete **Hugging Face Spaces** deployment for web-based audio analysis, making it accessible to users worldwide without any installation required.

### 🚀 Web Interface Features

**Easy Access**: Upload audio files directly through your web browser for instant analysis
- **Multiple Analysis Types**: Comprehensive analysis, mood-only, or phase detection only
- **Export Options**: Download results in Markdown, JSON, or CSV formats  
- **Public Demo**: Share and demonstrate your audio analysis capabilities
- **No Installation**: Works immediately in any web browser

### 📁 Deployment Structure
```
gradio/
├── app.py                 # Complete Gradio web interface  
├── requirements.txt       # HF-specific dependencies
├── README.md             # Model card with proper YAML frontmatter
└── CLAUDE.md             # Deployment-specific guidance
```

### 🎯 Deployment Options

**Option 1: Hugging Face Spaces** (Recommended)
1. Create new Space at [hf.co/new-space](https://hf.co/new-space)
2. Choose "Gradio" SDK
3. Upload contents of `gradio/` directory  
4. Automatic deployment at `https://huggingface.co/spaces/yourusername/spacename`

**Option 2: Hugging Face Model Repository**
- Upload complete Python package as model repository
- Users install via `pip install git+https://huggingface.co/username/repo.git`
- Include comprehensive documentation and examples

**Option 3: PyPI + HF Community**
- Package for PyPI distribution (`pip install audio-analysis-toolkit`)
- List as community resource on Hugging Face Hub

### 🎵 Web Analysis Capabilities

**Supported Audio**: WAV (recommended), AIFF, MP3 up to 100MB, 1s-30min duration
**Analysis Results**: Same 17 mood descriptors, 9 character tags, and phase detection as desktop version
**Export Formats**: Human-readable reports, structured JSON data, and spreadsheet-ready CSV files
**Real-time Processing**: Immediate results with downloadable complete analysis

### 💡 Benefits for Users

- **Accessibility**: No Python knowledge or installation required
- **Educational**: Interactive exploration of audio analysis concepts
- **Professional**: API-quality outputs for integration workflows  
- **Gateway**: Introduction to full desktop toolkit capabilities
- **Shareable**: Public demos for collaboration and teaching

The web interface maintains full compatibility with all desktop analysis features while providing an intuitive, browser-based experience that makes advanced audio analysis accessible to a broader audience.