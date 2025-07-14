#!/usr/bin/env python3
"""
Example client for the Synthesizer Music Analysis MCP server
Shows how to use the MCP tools to analyze audio files
"""

import base64
import json
from pathlib import Path
from typing import List, Dict, Any

def encode_audio_file(file_path: Path) -> Dict[str, Any]:
    """Encode an audio file to base64 for MCP transmission"""
    with open(file_path, 'rb') as f:
        content = base64.b64encode(f.read()).decode('utf-8')
    
    return {
        "filename": file_path.name,
        "content": content
    }

def prepare_audio_files(directory: Path) -> List[Dict[str, Any]]:
    """Prepare audio files from a directory for MCP analysis"""
    audio_files = []
    supported_extensions = ['.wav', '.aiff', '.aif', '.mp3']
    
    for file_path in directory.iterdir():
        if file_path.suffix.lower() in supported_extensions:
            audio_files.append(encode_audio_file(file_path))
    
    return audio_files

def example_mood_analysis():
    """Example of using the mood analysis tool"""
    print("=== Mood Analysis Example ===")
    
    # This would typically be called through an MCP client
    # For demonstration, here's what the call would look like:
    
    example_call = {
        "tool": "analyze_audio_mood",
        "arguments": {
            "audio_files": [
                {
                    "filename": "spacey_track.wav",
                    "content": "base64_encoded_audio_content_here"
                },
                {
                    "filename": "organic_flow.aiff", 
                    "content": "base64_encoded_audio_content_here"
                }
            ]
        }
    }
    
    print("MCP Tool Call:")
    print(json.dumps(example_call, indent=2))
    
    # Expected response format:
    example_response = {
        "success": True,
        "tracks": [
            {
                "filename": "spacey_track.wav",
                "primary_mood": "spacey",
                "mood_descriptors": "spacey, ethereal, atmospheric",
                "primary_character": "analog_synth",
                "character_tags": "analog_synth, warm_harmonics",
                "duration": 245.5,
                "tempo": 72.0,
                "key": "C",
                "energy": 0.025,
                "brightness": 2150.0
            }
        ]
    }
    
    print("\nExpected Response:")
    print(json.dumps(example_response, indent=2))

def example_comprehensive_analysis():
    """Example of using the comprehensive analysis tool"""
    print("\n=== Comprehensive Analysis Example ===")
    
    example_call = {
        "tool": "comprehensive_audio_analysis",
        "arguments": {
            "audio_files": [
                {
                    "filename": "track1.wav",
                    "content": "base64_encoded_content"
                },
                {
                    "filename": "track2.aiff",
                    "content": "base64_encoded_content"
                }
            ],
            "export_format": "all"
        }
    }
    
    print("MCP Tool Call:")
    print(json.dumps(example_call, indent=2))
    
    # Expected response would include:
    # - Complete analysis summary
    # - Cluster analysis
    # - Song sequence recommendations
    # - Exported data in requested formats

def example_sequence_recommendation():
    """Example of using the song sequence recommendation tool"""
    print("\n=== Song Sequence Recommendation Example ===")
    
    example_call = {
        "tool": "recommend_song_sequence",
        "arguments": {
            "audio_files": [
                {"filename": "ambient_intro.wav", "content": "..."},
                {"filename": "driving_main.wav", "content": "..."},
                {"filename": "climax_peak.wav", "content": "..."},
                {"filename": "outro_fade.wav", "content": "..."}
            ]
        }
    }
    
    print("MCP Tool Call:")
    print(json.dumps(example_call, indent=2))
    
    example_response = {
        "success": True,
        "sequence": [
            {
                "position": 1,
                "filename": "ambient_intro.wav",
                "mood": "atmospheric",
                "character": "analog_synth",
                "duration": 180.0,
                "tempo": 65.0,
                "key": "C",
                "reasoning": "Opening track - sets the mood with atmospheric atmosphere"
            },
            {
                "position": 2,
                "filename": "driving_main.wav",
                "mood": "driving",
                "character": "digital_synth",
                "duration": 240.0,
                "tempo": 120.0,
                "key": "G",
                "reasoning": "Core development - showcases driving at 120 BPM"
            }
        ],
        "total_tracks": 4
    }
    
    print("\nExpected Response:")
    print(json.dumps(example_response, indent=2))

if __name__ == "__main__":
    print("Synthesizer Music Analysis MCP Client Examples")
    print("=" * 50)
    
    example_mood_analysis()
    example_comprehensive_analysis()
    example_sequence_recommendation()
    
    print("\n" + "=" * 50)
    print("To use these tools:")
    print("1. Start the MCP server: python analyze_library.py --mode mcp")
    print("2. Connect your MCP client to the server")
    print("3. Use the tools with properly encoded audio files")
    print("4. Audio files must be base64 encoded for transmission")
    print("5. Supported formats: WAV, AIFF, MP3")
    print("\nAvailable MCP Tools:")
    print("- analyze_audio_mood")
    print("- analyze_audio_phases") 
    print("- recommend_song_sequence")
    print("- analyze_audio_clusters")
    print("- comprehensive_audio_analysis")
    print("- get_supported_formats")