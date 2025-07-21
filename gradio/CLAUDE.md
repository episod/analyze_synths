# CLAUDE.md - Hugging Face Spaces Deployment

This file provides guidance to Claude Code (claude.ai/code) when working with the Hugging Face Spaces deployment of the Audio Analysis Toolkit.

## Project Overview

This is the **Hugging Face Spaces** deployment of a comprehensive Python audio analysis toolkit designed specifically for composers and synthesizer music creators. The Gradio web interface provides browser-based access to the same advanced audio analysis features available in the desktop version, making the toolkit accessible to users worldwide without any installation requirements.

## Deployment Structure

This `gradio/` directory contains a complete Hugging Face Spaces deployment:

```
gradio/
├── app.py                 # Complete Gradio web interface with relative imports
├── requirements.txt       # HF-specific dependencies (gradio + core analysis libs)
├── README.md             # Model card with proper YAML frontmatter for HF Hub
└── CLAUDE.md             # This file - deployment-specific guidance
```

## Key Technical Implementation

### Relative Import System
The deployment uses a relative import system to access the parent audio analysis package:

```python
# Add parent directory to path to import audio_analysis package
sys.path.insert(0, str(Path(__file__).parent.parent))
from audio_analysis import AudioAnalyzer
```

This allows the Gradio app to use the complete audio analysis toolkit without duplicating code or requiring separate packaging.

### Hugging Face Spaces Configuration

**Server Configuration:**
- Host: `0.0.0.0` (required for HF Spaces)
- Port: `7860` (HF Spaces standard)
- Queue: Enabled for better performance under load
- Max threads: 10 (prevents resource exhaustion)

**Model Card (README.md):**
- Proper YAML frontmatter with SDK configuration
- Comprehensive feature documentation
- Usage examples and technical specifications
- Tags for discoverability

## Web Interface Features

### Analysis Types Available
1. **Comprehensive Analysis**: Complete feature extraction, mood analysis, phase detection, and structured reporting
2. **Mood Analysis Only**: Quick analysis focusing on 17 emotional and character descriptors
3. **Phase Detection Only**: Musical structure analysis with timing and characteristics

### Export Formats Supported
1. **Markdown Reports**: Human-readable analysis with insights and recommendations
2. **JSON Data**: Structured data for programmatic access and integration
3. **CSV Features**: Complete feature matrix suitable for spreadsheet analysis

### File Upload Capabilities
- **Supported Formats**: WAV (recommended), AIFF, MP3
- **File Size Limit**: Up to 100MB per file
- **Duration Range**: 1 second minimum, 30 minutes maximum recommended
- **Processing**: Temporary file system with automatic cleanup

## Analysis Capabilities

The web interface provides the same analytical capabilities as the desktop version:

### Mood Detection (17 Descriptors)
**Core Moods**: spacey, organic, synthetic, oozy, pensive, tense, exuberant, glitchy, chaos
**Extended Moods**: ethereal, atmospheric, crystalline, warm, melodic, driving, percussive, droning

### Character Analysis (9 Tags)
**Synthesis Types**: analog_synth, digital_synth, mellotron, percussive_instrument, acoustic_instrument
**Texture Types**: rich_texture, pure_tone, bright_harmonics, warm_harmonics

### Feature Extraction (80+ Features)
- Spectral features (brightness, bandwidth, rolloff)
- Temporal features (energy, rhythm, duration)
- Harmonic features (key detection, chroma)
- Structural features (phases, transitions)

### Phase Detection
- Automatic detection of musical sections (intro, verse, chorus, breakdown, climax, outro)
- Timing and characteristics for each phase
- Energy and spectral progression analysis

## Error Handling and User Experience

### Robust Error Management
- **File Validation**: Comprehensive format and content checking before processing
- **Graceful Degradation**: Meaningful error messages for unsupported files
- **Timeout Protection**: Processing limits to prevent resource exhaustion
- **Memory Management**: Efficient temporary file handling

### User Interface Design
- **Progressive Disclosure**: Options appear based on analysis type selection
- **Clear Feedback**: Processing status and result presentation
- **Download Integration**: Seamless file download for complete analyses
- **Responsive Layout**: Works on desktop and mobile devices

## Deployment Instructions

### For Hugging Face Spaces

1. **Create New Space**:
   - Visit [hf.co/new-space](https://hf.co/new-space)
   - Choose "Gradio" SDK
   - Set visibility (public/private)

2. **Upload Files**:
   - Upload entire `gradio/` directory contents
   - Ensure parent `audio_analysis/` package is available
   - Verify `requirements.txt` includes all dependencies

3. **Configuration**:
   - HF automatically detects `app.py` as entry point
   - SDK version specified in README.md YAML frontmatter
   - Dependencies installed from `requirements.txt`

4. **Launch**:
   - Space builds automatically upon file upload
   - Available at `https://huggingface.co/spaces/username/spacename`
   - Build logs available in HF interface

### Dependencies Management

The `requirements.txt` is optimized for Hugging Face Spaces:

```
gradio              # Web interface framework
librosa            # Audio analysis core library
pandas             # Data manipulation and analysis
scikit-learn       # Machine learning algorithms (clustering)
matplotlib         # Visualization (for future plot features)
seaborn            # Statistical visualization
pydub              # Audio file format handling
numpy              # Numerical computing
scipy              # Scientific computing
```

Notable omissions:
- `fastmcp` (not needed for web interface)
- Development dependencies (testing frameworks, etc.)

## Performance Considerations

### Processing Limitations
- **Single File Processing**: Web interface processes one file at a time
- **Memory Management**: Temporary directories with automatic cleanup
- **Processing Time**: 30-60 seconds typical for 3-5 minute audio files
- **Queue System**: Handles multiple concurrent users efficiently

### Optimization Strategies
- **Batch Processing**: Not available in web interface (use desktop version)
- **Parallel Processing**: Not enabled (use desktop ParallelAudioAnalyzer)
- **Caching**: Temporary file system only, no persistent caching
- **Resource Limits**: Configured for HF Spaces hardware constraints

## User Guidance

### Getting Started
1. **Upload Audio File**: Select WAV, AIFF, or MP3 file
2. **Choose Analysis Type**: Start with "Comprehensive Analysis" for full features
3. **Select Export Format**: Markdown for readable reports, JSON for data integration
4. **Analyze**: Click button and wait for processing to complete
5. **Download Results**: Get complete analysis file for further use

### Best Practices
- **File Format**: Use WAV for highest analysis quality
- **File Size**: Smaller files (under 10MB) process faster
- **Duration**: 3-5 minute tracks work best for demonstration
- **Export Choice**: Use JSON format for programmatic integration

### Limitations vs Desktop Version
- **Single File Only**: No batch processing or directory analysis
- **No Clustering**: K-means clustering requires multiple files
- **No Sequencing**: Track sequencing requires collection of files
- **No Visualization**: Static plots not available in current web version

## Integration with Full Toolkit

### From Web to Desktop
Users can progress from web interface to full desktop installation:
1. **Explore**: Use web interface to understand capabilities
2. **Learn**: Download analysis results to see data structure
3. **Install**: Set up desktop version for advanced features
4. **Integrate**: Use JSON outputs in custom workflows

### API Compatibility
Web interface outputs are compatible with desktop toolkit:
- **Same Feature Set**: Identical 80+ audio features extracted
- **Consistent Format**: JSON structure matches desktop exports
- **Mood Descriptors**: Same 17 creative mood classifications
- **Character Tags**: Identical synthesis type identification

## Future Enhancements

### Potential Web Features
- **Multi-File Upload**: Enable clustering and sequencing in web interface
- **Visualization**: Add interactive plots and charts
- **Batch Processing**: Queue multiple files for sequential analysis
- **Real-time Processing**: Stream analysis results as they become available

### Technical Improvements
- **Progressive Web App**: Enable offline functionality
- **WebAssembly**: Client-side processing for enhanced performance
- **Cloud Storage**: Integration with cloud file services
- **API Endpoints**: Direct programmatic access to analysis functions

## Troubleshooting

### Common Issues
- **Import Errors**: Ensure parent `audio_analysis/` directory is accessible
- **File Upload Failures**: Check file format and size limits
- **Processing Timeouts**: Large files may exceed processing limits
- **Download Issues**: Browser may block file downloads - check settings

### Development Testing
```bash
# Test locally before deployment
cd gradio
python app.py

# Access at http://localhost:7860
# Verify all analysis types work correctly
# Test different file formats and sizes
```

### Debugging
- **Error Messages**: Check HF Spaces logs for detailed error information
- **File Paths**: Verify relative import paths are correct
- **Dependencies**: Ensure all required packages are in requirements.txt
- **Memory Usage**: Monitor for out-of-memory errors with large files

## Best Practices for Development

### Code Maintenance
- **DRY Principle**: Uses parent package to avoid code duplication
- **Error Handling**: Comprehensive try-catch blocks with user-friendly messages
- **Type Hints**: Full type annotations for better code clarity
- **Documentation**: Clear docstrings explaining function purposes

### User Experience
- **Progressive Disclosure**: Show/hide options based on user selections
- **Clear Feedback**: Informative messages during processing
- **Accessibility**: Proper labeling and semantic HTML structure
- **Performance**: Efficient temporary file management

### Security Considerations
- **File Validation**: Strict checking of uploaded file types and sizes
- **Temporary Files**: Automatic cleanup prevents disk space issues
- **Resource Limits**: Processing timeouts prevent system overload
- **Input Sanitization**: Safe handling of user-provided file names

---

This Hugging Face Spaces deployment democratizes access to advanced audio analysis while maintaining the full analytical power of the desktop toolkit. It serves as both a standalone tool for individual users and a gateway to the complete audio analysis ecosystem.