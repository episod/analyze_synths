#!/usr/bin/env python3
"""
Hugging Face Spaces Gradio Interface for Audio Analysis Toolkit
Provides web-based access to comprehensive audio analysis for synthesizer music.
"""

import gradio as gr
import tempfile
import os
import sys
import json
import pandas as pd
from pathlib import Path
from typing import Tuple, Dict, Any, Optional
import shutil
import time

# Add parent directory to path to import audio_analysis package
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import our audio analysis toolkit
from audio_analysis import AudioAnalyzer
from audio_analysis.utils.audio_io import AudioLoader


def analyze_single_audio_file(
    audio_file,
    analysis_type: str = "comprehensive",
    export_format: str = "markdown"
):
    """
    Analyze a single audio file and return results in specified format.
    Uses generator approach for progress updates.
    
    Args:
        audio_file: Uploaded audio file from Gradio
        analysis_type: Type of analysis to perform
        export_format: Format for results export
        
    Yields:
        Progress updates and final results
    """
    if audio_file is None:
        yield "Please upload an audio file to analyze.", None, None
        return
    
    try:
        # Yield progress updates
        yield "🔄 Preparing analysis...", None, None
        
        # Create temporary directory for analysis that persists for download
        temp_dir = tempfile.mkdtemp(prefix="gradio_audio_analysis_")
        temp_dir_path = Path(temp_dir)
        
        yield "📁 Processing uploaded file...", None, None
        
        # Copy uploaded file to temp directory
        audio_path = temp_dir_path / Path(audio_file).name
        
        # Handle different input types from Gradio
        if isinstance(audio_file, str):
            # File path
            shutil.copy2(audio_file, audio_path)
        else:
            # File-like object
            with open(audio_path, 'wb') as f:
                f.write(audio_file.read())
        
        yield "🔧 Initializing audio analyzer...", None, None
        
        # Initialize analyzer
        analyzer = AudioAnalyzer(str(temp_dir_path))
        
        # Perform analysis based on type
        if analysis_type == "mood_only":
            progress(0.3, desc="Extracting audio features...")
            time.sleep(0.1)  # Allow UI to update
            
            # Quick mood analysis
            from audio_analysis.analysis.mood_analyzer import MoodAnalyzer
            from audio_analysis.core.feature_extraction import FeatureExtractor
            
            progress(0.4, desc="Loading analysis modules...")
            time.sleep(0.1)
            
            extractor = FeatureExtractor()
            progress(0.5, desc="Processing audio file...")
            time.sleep(0.1)
            
            features = extractor.extract_features(str(audio_path))
            
            progress(0.7, desc="Analyzing mood and character...")
            time.sleep(0.1)
            
            mood_analyzer = MoodAnalyzer()
            mood_data = mood_analyzer.analyze_track_mood(features, str(audio_path.name))
            
            progress(0.9, desc="Formatting results...")
            time.sleep(0.1)
            
            result_text = f"# Mood Analysis for {audio_path.name}\n\n"
            result_text += f"**Primary Moods:** {', '.join(mood_data['primary_moods'])}\n"
            result_text += f"**Secondary Moods:** {', '.join(mood_data['secondary_moods'])}\n"
            result_text += f"**Confidence Score:** {mood_data['confidence']:.2f}\n\n"
            result_text += f"**Character Tags:** {', '.join(mood_data['character_tags'])}\n"
            
            progress(1.0, desc="Analysis complete!")
            return result_text, None, None
            
        elif analysis_type == "phases":
            progress(0.3, desc="Running phase detection analysis...")
            time.sleep(0.1)
            
            # Phase detection analysis
            progress(0.4, desc="Analyzing audio structure...")
            time.sleep(0.1)
            
            df = analyzer.analyze_directory()
            
            progress(0.7, desc="Processing phase data...")
            time.sleep(0.1)
            
            # Get phase data for the file
            phases_data = []
            for _, row in df.iterrows():
                if 'phases' in row and row['phases']:
                    phases_data = row['phases']
                    break
            
            progress(0.9, desc="Formatting phase results...")
            time.sleep(0.1)
            
            result_text = f"# Phase Analysis for {audio_path.name}\n\n"
            if phases_data:
                result_text += f"**Number of Phases:** {len(phases_data)}\n\n"
                for i, phase in enumerate(phases_data, 1):
                    result_text += f"## Phase {i}: {phase['type'].title()}\n"
                    result_text += f"- **Duration:** {phase['start']:.1f}s - {phase['end']:.1f}s ({phase['duration']:.1f}s)\n"
                    result_text += f"- **Energy:** {phase['characteristics'].get('energy', 'N/A')}\n"
                    result_text += f"- **Brightness:** {phase['characteristics'].get('brightness', 'N/A')}\n"
                    result_text += f"- **Mood:** {', '.join(phase['characteristics'].get('moods', []))}\n\n"
            else:
                result_text += "No distinct phases detected in this audio file.\n"
            
            progress(1.0, desc="Phase analysis complete!")
            return result_text, None, None
            
        else:
            progress(0.3, desc="Running comprehensive analysis...")
            time.sleep(0.1)
            
            # Comprehensive analysis
            progress(0.4, desc="Processing audio features...")
            time.sleep(0.1)
            
            df = analyzer.analyze_directory()
            
            progress(0.7, desc="Generating export files...")
            time.sleep(0.1)
            
            # Generate comprehensive report - export to temp directory directly
            progress(0.8, desc="Creating analysis reports...")
            time.sleep(0.1)
            
            export_info = analyzer.export_comprehensive_analysis(
                export_dir=temp_dir_path,
                export_format=export_format,
                base_name="hf_analysis"
            )
            
            progress(0.9, desc="Reading generated reports...")
            time.sleep(0.1)
            
            # Debug: List the actual export directory contents
            export_dir = Path(export_info['export_directory'])
            
            # Read the generated report
            if export_format == "markdown":
                # Check report_exports in export_info for actual path
                if 'report_exports' in export_info and 'comprehensive_report' in export_info['report_exports']:
                    report_path = Path(export_info['report_exports']['comprehensive_report'])
                    if report_path.exists():
                        with open(report_path, 'r', encoding='utf-8') as f:
                            result_text = f.read()
                        
                        # Create downloadable file
                        download_path = str(report_path)
                        progress(1.0, desc="Analysis complete!")
                        return result_text, download_path, None
                    else:
                        result_text = f"Report file not found at: {report_path}"
                        return result_text, None, None
                else:
                    result_text = "No markdown report generated."
                    return result_text, None, None
                    
            elif export_format == "json":
                # Check report_exports in export_info for actual path
                if 'report_exports' in export_info and 'json_data' in export_info['report_exports']:
                    json_path = Path(export_info['report_exports']['json_data'])
                    if json_path.exists():
                        with open(json_path, 'r', encoding='utf-8') as f:
                            json_data = json.load(f)
                        
                        result_text = "# Comprehensive Audio Analysis (JSON)\n\n"
                        result_text += f"**File:** {audio_path.name}\n\n"
                        result_text += "```json\n"
                        result_text += json.dumps(json_data, indent=2)[:2000] + "..."
                        result_text += "\n```\n\n"
                        result_text += "*Full JSON data available in download file.*"
                        
                        progress(1.0, desc="Analysis complete!")
                        return result_text, str(json_path), None
                    else:
                        result_text = f"JSON file not found at: {json_path}"
                        return result_text, None, None
                else:
                    result_text = "No JSON data generated."
                    return result_text, None, None
                    
            else:  # CSV format
                # Check data_exports in export_info for actual path
                if 'data_exports' in export_info and 'features' in export_info['data_exports']:
                    csv_path = Path(export_info['data_exports']['features'])
                    if csv_path.exists():
                        df_features = pd.read_csv(csv_path)
                        
                        result_text = "# Comprehensive Audio Analysis (CSV)\n\n"
                        result_text += f"**File:** {audio_path.name}\n\n"
                        result_text += "## Feature Summary\n"
                        result_text += df_features.describe().to_string()
                        result_text += "\n\n*Full feature data available in download file.*"
                        
                        progress(1.0, desc="Analysis complete!")
                        return result_text, str(csv_path), None
                    else:
                        result_text = f"CSV file not found at: {csv_path}"
                        return result_text, None, None
                else:
                    result_text = "No CSV data generated."
                    return result_text, None, None
    
    except Exception as e:
        error_msg = f"Error during analysis: {str(e)}\n\n"
        error_msg += "Please ensure the uploaded file is a valid audio file (WAV, MP3, AIFF)."
        return error_msg, None, None


def get_supported_formats() -> str:
    """Return information about supported audio formats and capabilities."""
    info_text = """
# Audio Analysis Toolkit - Supported Formats & Capabilities

## Supported Audio Formats
- **WAV** (Recommended - highest quality)
- **AIFF** (High quality, equivalent to WAV)
- **MP3** (Supported, slight quality reduction)

## File Specifications
- **File Size**: Up to 100MB per file
- **Duration**: 1 second minimum, 30 minutes maximum recommended
- **Sample Rate**: Any (automatically handled)
- **Channels**: Mono and stereo supported

## Analysis Capabilities

### Mood Detection (17 Descriptors)
**Core Moods**: spacey, organic, synthetic, oozy, pensive, tense, exuberant, glitchy, chaos
**Extended Moods**: ethereal, atmospheric, crystalline, warm, melodic, driving, percussive, droning

### Character Analysis (9 Tags)
**Synthesis Types**: analog_synth, digital_synth, mellotron, percussive_instrument, acoustic_instrument
**Texture Types**: rich_texture, pure_tone, bright_harmonics, warm_harmonics

### Phase Detection
- Automatic detection of musical sections (intro, verse, chorus, breakdown, climax, outro)
- Timing and characteristics for each phase
- Energy and spectral progression analysis

### Feature Extraction (80+ Features)
- Spectral features (brightness, bandwidth, rolloff)
- Temporal features (energy, rhythm, duration)
- Harmonic features (key detection, chroma)
- Structural features (phases, transitions)

## Optimized For
This toolkit is specifically calibrated for **synthesizer and electronic music analysis**, 
providing creative descriptors that resonate with electronic music producers and composers.
"""
    return info_text


# Create Gradio interface
def create_interface():
    """Create and configure the Gradio interface."""
    
    with gr.Blocks(
        title="Audio Analysis Toolkit for Synthesizer Music",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .analysis-output {
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 14px;
        }
        """
    ) as interface:
        
        gr.Markdown("""
        # 🎵 Audio Analysis Toolkit for Synthesizer Music
        
        Upload an audio file to analyze its musical characteristics, mood, and structure. 
        This toolkit is specifically designed for synthesizer and electronic music analysis.
        """)
        
        with gr.Tab("Audio Analysis"):
            with gr.Row():
                with gr.Column(scale=1):
                    audio_input = gr.Audio(
                        label="Upload Audio File",
                        type="filepath",
                        format="wav"
                    )
                    
                    analysis_type = gr.Radio(
                        choices=[
                            ("Comprehensive Analysis", "comprehensive"),
                            ("Mood Analysis Only", "mood_only"),
                            ("Phase Detection Only", "phases")
                        ],
                        value="comprehensive",
                        label="Analysis Type"
                    )
                    
                    export_format = gr.Radio(
                        choices=[
                            ("Markdown Report", "markdown"),
                            ("JSON Data", "json"),
                            ("CSV Features", "csv")
                        ],
                        value="markdown",
                        label="Export Format",
                        visible=True
                    )
                    
                    analyze_btn = gr.Button("🔍 Analyze Audio", variant="primary", size="lg")
                    
                with gr.Column(scale=2):
                    analysis_output = gr.Markdown(
                        label="Analysis Results",
                        elem_classes=["analysis-output"]
                    )
                    
                    download_file = gr.File(
                        label="Download Complete Analysis",
                        visible=False
                    )
            
            # Wire up the analysis function
            def update_analysis(audio_file, analysis_type, export_format, progress=gr.Progress()):
                result_text, download_path, viz_path = analyze_single_audio_file(
                    audio_file, analysis_type, export_format, progress
                )
                
                # Show download file if available
                if download_path:
                    return result_text, gr.File(value=download_path, visible=True)
                else:
                    return result_text, gr.File(visible=False)
            
            analyze_btn.click(
                fn=update_analysis,
                inputs=[audio_input, analysis_type, export_format],
                outputs=[analysis_output, download_file],
                show_progress="full"  # Enable full progress tracking
            )
            
            # Show/hide export format based on analysis type
            def toggle_export_format(analysis_type):
                if analysis_type == "comprehensive":
                    return gr.Radio(visible=True)
                else:
                    return gr.Radio(visible=False)
            
            analysis_type.change(
                fn=toggle_export_format,
                inputs=[analysis_type],
                outputs=[export_format]
            )
        
        with gr.Tab("Supported Formats & Capabilities"):
            gr.Markdown(get_supported_formats())
        
        with gr.Tab("About"):
            gr.Markdown("""
            ## About This Toolkit
            
            This comprehensive Python audio analysis toolkit is designed specifically for composers 
            and synthesizer music creators. It processes audio files to extract creative musical 
            features, detect phases/sections, analyze mood and character, and provide intelligent 
            insights using terms that resonate with electronic music producers.
            
            ### Key Features:
            - **80+ Audio Features**: Comprehensive spectral, temporal, and harmonic analysis
            - **17 Mood Descriptors**: Creative terms like "spacey," "organic," "crystalline," "oozy"
            - **9 Character Tags**: Synthesis type identification and texture analysis
            - **Phase Detection**: Automatic musical structure detection (intro, verse, chorus, etc.)
            - **Professional Reports**: Multiple export formats for different use cases
            
            ### Technical Approach:
            - Built with librosa, scikit-learn, and professional audio analysis libraries
            - Empirically calibrated thresholds based on synthesizer music characteristics
            - Modular Python architecture with comprehensive inline documentation
            - Parallel processing capabilities for scalable analysis
            
            ### Created By:
            This toolkit focuses on creative descriptors rather than academic metrics, 
            providing insights that directly support composition and music production workflows.
            
            ---
            
            **Note**: This interface provides access to a subset of the toolkit's capabilities. 
            For batch processing, clustering analysis, and advanced sequencing features, 
            please refer to the full Python package documentation.
            """)
    
    return interface


if __name__ == "__main__":
    # Create and launch the interface
    demo = create_interface()
    
    # Launch with appropriate settings for Hugging Face Spaces
    demo.launch(
        share=False,  # Set to False for HF Spaces
        server_name="0.0.0.0",  # Required for HF Spaces
        server_port=7860,  # Default HF Spaces port
        show_error=True,
        max_threads=10  # Limit concurrent processing
    )