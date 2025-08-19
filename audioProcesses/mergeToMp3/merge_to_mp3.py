#!/usr/bin/env python3
"""
🎵 Audio Merger Script
=====================

This script merges all audio files from rawAudioGood into a single MP3 file.
Useful for creating a combined audio file from multiple microphone channels.

Usage:
    py merge_to_mp3.py

Output:
    cleanAudio/merged_audio.mp3
"""

import os
import sys
from pathlib import Path
import librosa
import soundfile as sf
import numpy as np
from typing import List, Tuple
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_audio_files(input_dir: str) -> List[Path]:
    """Get all supported audio files from the input directory."""
    supported_formats = {'.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg'}
    input_path = Path(input_dir)
    
    if not input_path.exists():
        logger.error(f"Input directory '{input_dir}' does not exist!")
        return []
    
    audio_files = []
    for file_path in input_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_formats:
            audio_files.append(file_path)
    
    # Sort files for consistent ordering
    audio_files.sort()
    
    logger.info(f"Found {len(audio_files)} audio files in {input_dir}")
    return audio_files

def load_and_resample_audio(file_path: Path, target_sr: int = 44100) -> Tuple[np.ndarray, int]:
    """Load audio file and resample to target sample rate."""
    try:
        logger.info(f"Loading: {file_path.name}")
        audio, sr = librosa.load(file_path, sr=target_sr, mono=True)
        logger.info(f"  - Duration: {len(audio)/sr:.2f}s, Sample Rate: {sr}Hz")
        return audio, sr
    except Exception as e:
        logger.error(f"Error loading {file_path.name}: {e}")
        return np.array([]), target_sr

def merge_audio_files(audio_files: List[Path], output_path: Path, target_sr: int = 44100) -> bool:
    """Merge multiple audio files into a single file."""
    if not audio_files:
        logger.error("No audio files to merge!")
        return False
    
    logger.info(f"Starting merge of {len(audio_files)} files...")
    
    # Load all audio files
    loaded_audio = []
    for file_path in audio_files:
        audio, sr = load_and_resample_audio(file_path, target_sr)
        if len(audio) > 0:
            loaded_audio.append(audio)
    
    if not loaded_audio:
        logger.error("No valid audio files loaded!")
        return False
    
    # Find the longest audio length
    max_length = max(len(audio) for audio in loaded_audio)
    logger.info(f"Longest audio duration: {max_length/target_sr:.2f}s")
    
    # Pad shorter audio files with zeros to match the longest
    padded_audio = []
    for i, audio in enumerate(loaded_audio):
        if len(audio) < max_length:
            padding = max_length - len(audio)
            padded = np.pad(audio, (0, padding), mode='constant')
            logger.info(f"  - Padded {audio_files[i].name} with {padding/target_sr:.2f}s of silence")
            padded_audio.append(padded)
        else:
            padded_audio.append(audio)
    
    # Mix all audio files together
    logger.info("Mixing audio files...")
    mixed_audio = np.sum(padded_audio, axis=0)
    
    # Normalize to prevent clipping
    max_amplitude = np.max(np.abs(mixed_audio))
    if max_amplitude > 1.0:
        normalization_factor = 1.0 / max_amplitude
        mixed_audio = mixed_audio * normalization_factor
        logger.info(f"Normalized audio (factor: {normalization_factor:.3f})")
    
    # Save the merged audio
    try:
        logger.info(f"Saving merged audio to: {output_path}")
        
        # Try to save as MP3 first
        try:
            sf.write(output_path, mixed_audio, target_sr, format='MP3')
            logger.info(f"Successfully created merged audio file!")
            logger.info(f"  - Output: {output_path}")
            logger.info(f"  - Duration: {len(mixed_audio)/target_sr:.2f}s")
            logger.info(f"  - Sample Rate: {target_sr}Hz")
            logger.info(f"  - File Size: {output_path.stat().st_size / (1024*1024):.1f}MB")
            return True
        except Exception as mp3_error:
            logger.warning(f"MP3 save failed: {mp3_error}")
            logger.info("Falling back to WAV format...")
            
            # Fallback to WAV format
            wav_path = output_path.with_suffix('.wav')
            sf.write(wav_path, mixed_audio, target_sr, format='WAV')
            logger.info(f"Successfully created merged audio file!")
            logger.info(f"  - Output: {wav_path}")
            logger.info(f"  - Duration: {len(mixed_audio)/target_sr:.2f}s")
            logger.info(f"  - Sample Rate: {target_sr}Hz")
            logger.info(f"  - File Size: {wav_path.stat().st_size / (1024*1024):.1f}MB")
            logger.info(f"  - Note: Saved as WAV instead of MP3 due to format limitations")
            return True
            
    except Exception as e:
        logger.error(f"Error saving merged audio: {e}")
        return False

def main():
    """Main function to merge audio files."""
    print("Audio Merger Script")
    print("=" * 50)
    
    # Configuration
    input_directory = "../../audioFiles/sourceAudio"  # Updated to use correct sourceAudio folder
    output_directory = "../../audioFiles/mergedAudio"   # Updated to use correct mergedAudio folder
    output_filename = "merged_audio.mp3"
    target_sample_rate = 44100  # 44.1 kHz
    
    # Create output directory if it doesn't exist
    output_path = Path(output_directory)
    output_path.mkdir(exist_ok=True)
    
    # Get audio files
    audio_files = get_audio_files(input_directory)
    if not audio_files:
        logger.error("No audio files found!")
        return False
    
    # Display files to be merged
    print("\nFiles to merge:")
    for i, file_path in enumerate(audio_files, 1):
        print(f"  {i}. {file_path.name}")
    
    # Merge audio files
    output_file = output_path / output_filename
    success = merge_audio_files(audio_files, output_file, target_sample_rate)
    
    if success:
        print(f"\nSuccess! Merged audio saved to: {output_file}")
        print(f"Total files merged: {len(audio_files)}")
    else:
        print(f"\nFailed to merge audio files!")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
