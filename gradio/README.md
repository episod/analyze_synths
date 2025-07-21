---
title: Audio Analysis Toolkit for Synthesizer Music
emoji: 🎵
colorFrom: purple
colorTo: pink
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
tags:
- audio-analysis
- music-analysis
- synthesizer
- electronic-music
- mood-detection
- feature-extraction
- phase-detection
- music-information-retrieval
---

# 🎵 Audio Analysis Toolkit for Synthesizer Music

A comprehensive audio analysis toolkit designed specifically for composers and synthesizer music creators. This Hugging Face Space provides web-based access to advanced audio analysis features that extract creative musical characteristics, detect structural phases, and analyze mood and character using terms that resonate with electronic music producers.

## ✨ Features

### 🎯 Specialized for Electronic Music
- **17 Mood Descriptors**: Creative terms like "spacey," "organic," "crystalline," "oozy" calibrated for synthesizer music
- **9 Character Tags**: Synthesis type identification (analog_synth, digital_synth, mellotron) and texture analysis
- **Phase Detection**: Automatic musical structure detection (intro, verse, chorus, breakdown, climax, outro)
- **80+ Audio Features**: Comprehensive spectral, temporal, and harmonic analysis

### 🔍 Analysis Types
- **Comprehensive Analysis**: Complete feature extraction, mood analysis, phase detection, and structured reporting
- **Mood Analysis Only**: Quick analysis focusing on emotional and character descriptors
- **Phase Detection Only**: Musical structure analysis with timing and characteristics

### 📊 Export Formats (Enhanced v2.2)
- **Markdown Reports**: Human-readable analysis with insights and recommendations
- **JSON Data**: Structured data for programmatic access and integration
- **CSV Features**: Complete feature matrix for spreadsheet analysis

The web interface uses the enhanced export system with customizable formats and optimized file naming for better integration with downstream workflows.

## 🎼 Optimized for Synthesizer Music

This toolkit is specifically calibrated for electronic and synthesizer music, providing:

- **Creative Descriptors**: Technical analysis translated into musical terms that composers understand
- **Synthesis Recognition**: Identify analog synths, digital synths, mellotrons, and acoustic instruments
- **Texture Analysis**: Rich texture, pure tone, bright harmonics, and warm harmonic identification
- **Energy Progression**: Track how energy and mood evolve throughout compositions

## 🎵 Supported Audio Formats

- **WAV** (Recommended - highest quality)
- **AIFF** (High quality, equivalent to WAV)  
- **MP3** (Supported, slight quality reduction)

**File Specifications:**
- File Size: Up to 100MB per file
- Duration: 1 second minimum, 30 minutes maximum recommended
- Sample Rate: Any (automatically handled)
- Channels: Mono and stereo supported

## 🚀 How to Use

1. **Upload Audio**: Select an audio file (WAV, AIFF, or MP3)
2. **Choose Analysis Type**: 
   - Comprehensive for complete analysis
   - Mood Only for quick emotional profiling
   - Phases Only for structural analysis
3. **Select Export Format**: Choose between Markdown, JSON, or CSV output
4. **Analyze**: Click the analyze button and get detailed results
5. **Download**: Get complete analysis files for further use

## 🎯 Creative Mood Descriptors

### Core Descriptors (9)
- **spacey**: Low energy, high brightness, minimal rhythm
- **organic**: Moderate energy, high roughness, rich harmonics  
- **synthetic**: Low roughness, narrow bandwidth, precise characteristics
- **oozy**: Very low energy, low brightness, sustained character
- **pensive**: Balanced characteristics, contemplative mood
- **tense**: High energy, sharp spectral content, driving rhythm
- **exuberant**: Very high energy, bright, rhythmically active
- **glitchy**: High roughness, complex rhythms, wide bandwidth
- **chaos**: Extreme energy, unpredictable spectrum, very high rhythm

### Extended Descriptors (8)
- **ethereal**: Very low energy, very bright, sparse rhythm
- **atmospheric**: Minimal rhythm, wide spectrum, sustained
- **crystalline**: High brightness, low roughness, precise
- **warm**: Mid-range brightness, rich harmonics
- **melodic**: Balanced characteristics with moderate complexity
- **driving**: Consistent energy, regular rhythm patterns
- **percussive**: High rhythm density, focused energy bursts
- **droning**: Very low rhythm, sustained energy, long duration

## 🔧 Technical Approach

- **Built with**: librosa (audio analysis), scikit-learn (clustering), matplotlib/seaborn (visualization)
- **Empirically Calibrated**: Thresholds optimized specifically for synthesizer music characteristics
- **Professional Architecture**: Modular Python design with comprehensive documentation
- **Creative Focus**: Technical features translated into musical understanding

## 🎨 Use Cases

- **Composition Analysis**: Understand the emotional and structural characteristics of your tracks
- **Sound Design**: Identify synthesis types and textural qualities
- **Music Production**: Analyze phase structures and energy progression  
- **Creative Insights**: Get suggestions for track development and arrangement
- **Educational**: Learn how technical audio features relate to musical perception

## 📚 About the Full Toolkit

This Hugging Face Space provides access to a subset of the full Audio Analysis Toolkit capabilities. The complete Python package includes:

- **Batch Processing**: Analyze entire music libraries simultaneously
- **Clustering Analysis**: Group similar tracks for playlist creation
- **Sequence Recommendations**: Optimal track ordering based on musical flow
- **Visualization Suite**: Publication-quality plots and charts
- **MCP Server**: Integration with AI assistants and development tools
- **Parallel Processing**: Scalable analysis for large collections

## 🤝 Contributing

The full toolkit is open source and designed for extensibility. Contributions welcome for:
- Additional mood descriptors for specific electronic subgenres
- Enhanced visualization options
- Integration with popular DAWs and music software
- Machine learning improvements for descriptor accuracy

## 📄 License

MIT License - Feel free to use, modify, and distribute.

---

**Note**: This toolkit focuses on creative descriptors rather than academic metrics, providing insights that directly support composition and music production workflows. Results are optimized for synthesizer and electronic music - other genres may require threshold adjustments.