#!/usr/bin/env python3
"""
Audio Normalization Script
==========================

Standalone script for audio normalization that accepts config parameters.
Can be run independently or as part of a processing pipeline.

Usage:
    python 01_normalize.py --input input.wav --output output.wav --target-db -24.0
    python 01_normalize.py --config config.py --input-dir input/ --output-dir output/
"""

import argparse
import logging
import time
from pathlib import Path
from typing import Tuple, Optional
import numpy as np
import librosa
import soundfile as sf
from tqdm import tqdm

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AudioNormalizer:
    """Standalone audio normalization processor."""
    
    def __init__(self, target_db: float = -24.0, max_amplitude: float = 1.0):
        """Initialize normalizer with parameters."""
        self.target_db = target_db
        self.max_amplitude = max_amplitude
        logger.info(f"Normalizer initialized: target={target_db}dB, max_amp={max_amplitude}")
    
    def load_audio(self, file_path: Path) -> Tuple[np.ndarray, int]:
        """Load audio file using librosa."""
        try:
            logger.debug(f"Loading: {file_path.name}")
            audio, sample_rate = librosa.load(str(file_path), sr=None)
            return audio, sample_rate
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            raise
    
    def normalize_audio(self, audio: np.ndarray) -> np.ndarray:
        """Normalize audio volume to target level."""
        try:
            # Calculate RMS
            rms = np.sqrt(np.mean(audio ** 2))
            
            if rms > 0:
                # Convert target dB to amplitude
                target_amplitude = 10 ** (self.target_db / 20)
                
                # Calculate scaling factor
                scale_factor = target_amplitude / rms
                
                # Prevent clipping
                max_amplitude = np.max(np.abs(audio))
                if max_amplitude * scale_factor > self.max_amplitude:
                    scale_factor = self.max_amplitude / max_amplitude
                
                # Apply normalization
                normalized_audio = audio * scale_factor
                
                # Clip to prevent overflow
                normalized_audio = np.clip(normalized_audio, -self.max_amplitude, self.max_amplitude)
                
                logger.debug(f"Normalized audio (scale: {scale_factor:.3f})")
                return normalized_audio
            else:
                logger.warning("Audio has zero RMS, skipping normalization")
                return audio
                
        except Exception as e:
            logger.error(f"Error normalizing audio: {e}")
            return audio
    
    def save_audio(self, audio: np.ndarray, sample_rate: int, output_path: Path) -> None:
        """Save audio to file."""
        try:
            sf.write(str(output_path), audio, sample_rate)
            logger.debug(f"Saved: {output_path.name}")
        except Exception as e:
            logger.error(f"Error saving {output_path}: {e}")
            raise
    
    def process_file(self, input_file: Path, output_file: Path) -> bool:
        """Process single file: Load → Normalize → Save."""
        start_time = time.time()
        
        try:
            logger.info(f"Normalizing: {input_file.name}")
            
            # Load audio
            audio, sample_rate = self.load_audio(input_file)
            
            # Normalize
            normalized_audio = self.normalize_audio(audio)
            
            # Save
            self.save_audio(normalized_audio, sample_rate, output_file)
            
            processing_time = time.time() - start_time
            logger.info(f"Completed: {output_file.name} ({processing_time:.2f}s)")
            
            return True
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Error processing {input_file.name}: {str(e)}")
            return False

def get_audio_files(directory: Path) -> list:
    """Get all audio files from directory."""
    supported_formats = {'.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg'}
    audio_files = []
    
    for file_path in directory.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_formats:
            audio_files.append(file_path)
    
    return sorted(audio_files)

def load_config(config_path: Optional[Path] = None) -> dict:
    """Load configuration from file or return defaults."""
    if config_path and config_path.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", config_path)
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)
        return config_module.get_config()
    else:
        # Default settings
        return {
            "NORMALIZATION_TARGET_DB": -24.0,
            "MAX_AUDIO_AMPLITUDE": 1.0,
            "INPUT_DIRECTORY": "input",
            "OUTPUT_DIRECTORY": "output",
            "OUTPUT_FILE_PREFIX": "normalized_"
        }

def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(description="Audio Normalization Script")
    parser.add_argument("--config", type=Path, help="Path to config file")
    parser.add_argument("--input", type=Path, help="Input audio file")
    parser.add_argument("--output", type=Path, help="Output audio file")
    parser.add_argument("--input-dir", type=Path, help="Input directory")
    parser.add_argument("--output-dir", type=Path, help="Output directory")
    parser.add_argument("--target-db", type=float, help="Target loudness in dB")
    parser.add_argument("--max-amplitude", type=float, default=1.0, help="Maximum amplitude")
    
    args = parser.parse_args()
    
    # Load config
    config = load_config(args.config)
    
    # Override config with command line arguments
    if args.target_db is not None:
        config["NORMALIZATION_TARGET_DB"] = args.target_db
    if args.max_amplitude is not None:
        config["MAX_AUDIO_AMPLITUDE"] = args.max_amplitude
    
    # Initialize normalizer
    normalizer = AudioNormalizer(
        target_db=config["NORMALIZATION_TARGET_DB"],
        max_amplitude=config["MAX_AUDIO_AMPLITUDE"]
    )
    
    # Single file processing
    if args.input and args.output:
        success = normalizer.process_file(args.input, args.output)
        exit(0 if success else 1)
    
    # Batch processing
    input_dir = args.input_dir or Path(config["INPUT_DIRECTORY"])
    output_dir = args.output_dir or Path(config["OUTPUT_DIRECTORY"])
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Get audio files
    audio_files = get_audio_files(input_dir)
    
    if not audio_files:
        logger.warning(f"No audio files found in {input_dir}")
        return
    
    logger.info(f"Found {len(audio_files)} audio files to normalize")
    logger.info(f"Input: {input_dir}")
    logger.info(f"Output: {output_dir}")
    logger.info(f"Target: {config['NORMALIZATION_TARGET_DB']}dB")
    
    # Process all files
    successful = 0
    total = len(audio_files)
    
    for audio_file in tqdm(audio_files, desc="Normalizing files"):
        # Create output filename
        output_filename = f"{config.get('OUTPUT_FILE_PREFIX', 'normalized_')}{audio_file.name}"
        output_file = output_dir / output_filename
        
        if normalizer.process_file(audio_file, output_file):
            successful += 1
    
    # Summary
    logger.info(f"Normalization complete: {successful}/{total} files successful")
    if successful < total:
        logger.warning(f"{total - successful} files failed to process")

if __name__ == "__main__":
    main()
