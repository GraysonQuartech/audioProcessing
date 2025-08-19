#!/usr/bin/env python3
"""
Manual Noise Gate Script
========================

Standalone script for manual noise gating that accepts config parameters.
Can be run independently or as part of a processing pipeline.

Usage:
    python 03_noisegate.py --input input.wav --output output.wav --threshold -25.0
    python 03_noisegate.py --config config.py --input-dir input/ --output-dir output/
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

class NoiseGateProcessor:
    """Standalone noise gate processor."""
    
    def __init__(self, threshold_db: float = -25.0, attack_ms: float = 10.0, 
                 release_ms: float = 500.0, ratio: float = 10.0):
        """Initialize noise gate with parameters."""
        self.threshold_db = threshold_db
        self.attack_ms = attack_ms
        self.release_ms = release_ms
        self.ratio = ratio
        logger.info(f"Noise gate initialized: threshold={threshold_db}dB, attack={attack_ms}ms, release={release_ms}ms")
    
    def load_audio(self, file_path: Path) -> Tuple[np.ndarray, int]:
        """Load audio file using librosa."""
        try:
            logger.debug(f"Loading: {file_path.name}")
            audio, sample_rate = librosa.load(str(file_path), sr=None)
            return audio, sample_rate
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            raise
    
    def apply_noise_gate(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """Apply noise gate to audio."""
        try:
            # Convert threshold from dB to amplitude
            threshold_amp = 10 ** (self.threshold_db / 20)
            
            # Convert time parameters to samples
            attack_samples = int(self.attack_ms * sample_rate / 1000)
            release_samples = int(self.release_ms * sample_rate / 1000)
            
            # Calculate RMS envelope
            window_size = min(1024, len(audio) // 10)  # Adaptive window size
            rms = np.sqrt(np.convolve(audio ** 2, np.ones(window_size) / window_size, mode='same'))
            
            # Calculate gain reduction
            gain_reduction = np.ones_like(audio)
            
            # Apply threshold
            below_threshold = rms < threshold_amp
            
            # Calculate gain reduction based on ratio
            if self.ratio > 1:
                # Soft knee compression
                gain_reduction[below_threshold] = (rms[below_threshold] / threshold_amp) ** (1 / self.ratio)
            else:
                # Hard gate
                gain_reduction[below_threshold] = 0.0
            
            # Apply attack and release smoothing
            smoothed_gain = np.ones_like(gain_reduction)
            
            # Forward pass (attack)
            for i in range(1, len(smoothed_gain)):
                if gain_reduction[i] < smoothed_gain[i-1]:
                    # Attack phase
                    smoothed_gain[i] = smoothed_gain[i-1] - (smoothed_gain[i-1] - gain_reduction[i]) / attack_samples
                else:
                    # Release phase
                    smoothed_gain[i] = smoothed_gain[i-1] + (gain_reduction[i] - smoothed_gain[i-1]) / release_samples
            
            # Apply gain reduction
            gated_audio = audio * smoothed_gain
            
            # Clip to prevent overflow
            gated_audio = np.clip(gated_audio, -1.0, 1.0)
            
            logger.debug(f"Noise gate applied: threshold={self.threshold_db}dB, ratio={self.ratio}")
            return gated_audio
            
        except Exception as e:
            logger.error(f"Error applying noise gate: {e}")
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
        """Process single file: Load → Noise Gate → Save."""
        start_time = time.time()
        
        try:
            logger.info(f"Applying noise gate: {input_file.name}")
            
            # Load audio
            audio, sample_rate = self.load_audio(input_file)
            
            # Apply noise gate
            gated_audio = self.apply_noise_gate(audio, sample_rate)
            
            # Save
            self.save_audio(gated_audio, sample_rate, output_file)
            
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
        # Default noise gate settings
        return {
            "NOISE_GATE_THRESHOLD_DB": -25.0,
            "NOISE_GATE_ATTACK_MS": 10.0,
            "NOISE_GATE_RELEASE_MS": 500.0,
            "NOISE_GATE_RATIO": 10.0,
            "INPUT_DIRECTORY": "input",
            "OUTPUT_DIRECTORY": "output",
            "OUTPUT_FILE_PREFIX": "gated_"
        }

def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(description="Manual Noise Gate Script")
    parser.add_argument("--config", type=Path, help="Path to config file")
    parser.add_argument("--input", type=Path, help="Input audio file")
    parser.add_argument("--output", type=Path, help="Output audio file")
    parser.add_argument("--input-dir", type=Path, help="Input directory")
    parser.add_argument("--output-dir", type=Path, help="Output directory")
    parser.add_argument("--threshold", type=float, help="Noise gate threshold in dB")
    parser.add_argument("--attack", type=float, help="Attack time in milliseconds")
    parser.add_argument("--release", type=float, help="Release time in milliseconds")
    parser.add_argument("--ratio", type=float, help="Gate ratio (1.0 = hard gate, >1.0 = soft gate)")
    
    args = parser.parse_args()
    
    # Load config
    config = load_config(args.config)
    
    # Override config with command line arguments
    if args.threshold is not None:
        config["NOISE_GATE_THRESHOLD_DB"] = args.threshold
    if args.attack is not None:
        config["NOISE_GATE_ATTACK_MS"] = args.attack
    if args.release is not None:
        config["NOISE_GATE_RELEASE_MS"] = args.release
    if args.ratio is not None:
        config["NOISE_GATE_RATIO"] = args.ratio
    
    # Initialize processor
    processor = NoiseGateProcessor(
        threshold_db=config["NOISE_GATE_THRESHOLD_DB"],
        attack_ms=config["NOISE_GATE_ATTACK_MS"],
        release_ms=config["NOISE_GATE_RELEASE_MS"],
        ratio=config["NOISE_GATE_RATIO"]
    )
    
    # Single file processing
    if args.input and args.output:
        success = processor.process_file(args.input, args.output)
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
    
    logger.info(f"Found {len(audio_files)} audio files to process")
    logger.info(f"Input: {input_dir}")
    logger.info(f"Output: {output_dir}")
    logger.info(f"Threshold: {config['NOISE_GATE_THRESHOLD_DB']}dB")
    logger.info(f"Attack: {config['NOISE_GATE_ATTACK_MS']}ms")
    logger.info(f"Release: {config['NOISE_GATE_RELEASE_MS']}ms")
    logger.info(f"Ratio: {config['NOISE_GATE_RATIO']}")
    
    # Process all files
    successful = 0
    total = len(audio_files)
    
    for audio_file in tqdm(audio_files, desc="Applying noise gate"):
        # Create output filename
        output_filename = f"{config.get('OUTPUT_FILE_PREFIX', 'gated_')}{audio_file.name}"
        output_file = output_dir / output_filename
        
        if processor.process_file(audio_file, output_file):
            successful += 1
    
    # Summary
    logger.info(f"Noise gate processing complete: {successful}/{total} files successful")
    if successful < total:
        logger.warning(f"{total - successful} files failed to process")

if __name__ == "__main__":
    main()
