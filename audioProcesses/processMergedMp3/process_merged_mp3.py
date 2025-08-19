#!/usr/bin/env python3
"""
Simple audio processor that applies TorchGate AI noise removal and volume normalization.
Uses the specific processing classes from individual processing files.
"""

import logging
import time
from pathlib import Path
from typing import Tuple
import numpy as np
import librosa
import soundfile as sf
import torch
from tqdm import tqdm

# Import configuration
import config
CONFIG = config.get_config()

# Import processing classes directly from individual files
import sys
sys.path.append('..')
from normalize import AudioNormalizer
from torchgate import TorchGateProcessor
from noisegate import NoiseGateProcessor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimpleAudioProcessor:
    """Simple processor: TorchGate → Normalize (using specific processing classes)"""
    
    def __init__(self):
        """Initialize the processor with config settings."""
        # Use config for device selection
        force_cpu = CONFIG.get("FORCE_CPU_PROCESSING", False)
        if force_cpu:
            device = "cpu"
        else:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize processing components with config settings
        self.torchgate_processor = TorchGateProcessor(
            torchgate_settings=CONFIG.get("TORCHGATE_SETTINGS", {}),
            device=device
        )
        
        self.normalizer = AudioNormalizer(
            target_db=CONFIG.get("NORMALIZATION_TARGET_DB", -24.0),
            max_amplitude=1.0
        )
        
        # Initialize noise gate if enabled in config
        self.noise_gate_enabled = CONFIG.get("ENABLE_NOISE_GATE", False)
        if self.noise_gate_enabled:
            self.noise_gate = NoiseGateProcessor(
                threshold_db=CONFIG.get("NOISE_GATE_THRESHOLD_DB", -35.0),
                attack_ms=CONFIG.get("NOISE_GATE_ATTACK_MS", 20.0),
                release_ms=CONFIG.get("NOISE_GATE_RELEASE_MS", 1200.0),
                ratio=10.0
            )
        
        logger.info(f"Processor initialized with device: {device}")
        logger.info(f"Noise gate enabled: {self.noise_gate_enabled}")
    
    def load_audio(self, file_path: Path) -> Tuple[np.ndarray, int]:
        """Load audio file using librosa."""
        try:
            logger.debug(f"Loading: {file_path.name}")
            audio, sample_rate = librosa.load(str(file_path), sr=None)
            return audio, sample_rate
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            raise
    
    def save_audio(self, audio: np.ndarray, sample_rate: int, output_path: Path) -> None:
        """Save audio to file."""
        try:
            sf.write(str(output_path), audio, sample_rate)
            logger.debug(f"Saved: {output_path.name}")
        except Exception as e:
            logger.error(f"Error saving {output_path}: {e}")
            raise
    
    def process_file(self, input_file: Path, output_file: Path) -> bool:
        """Process single file using specific processing classes."""
        start_time = time.time()
        
        try:
            logger.info(f"Processing: {input_file.name}")
            
            # STEP 1: Load audio
            audio, sample_rate = self.load_audio(input_file)
            
            # STEP 2: Apply noise gate (if enabled)
            if self.noise_gate_enabled:
                logger.info("Applying noise gate...")
                audio = self.noise_gate.apply_noise_gate(audio, sample_rate)
            
            # STEP 3: Apply TorchGate AI noise removal
            logger.info("Applying TorchGate AI noise removal...")
            audio = self.torchgate_processor.apply_torchgate(audio, sample_rate)
            
            # STEP 4: Normalize volume
            logger.info("Normalizing audio...")
            audio = self.normalizer.normalize_audio(audio)
            
            # STEP 5: Save processed audio
            self.save_audio(audio, sample_rate, output_file)
            
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

def main():
    """Main processing function."""
    # Use config settings for directories
    input_dir = Path(CONFIG.get("INPUT_DIRECTORY", "../../audioFiles/mergedAudio"))
    output_dir = Path(CONFIG.get("OUTPUT_DIRECTORY", "../../audioFiles/outputAudio"))
    
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
    
    # Initialize processor
    processor = SimpleAudioProcessor()
    
    # Process all files
    successful = 0
    total = len(audio_files)
    
    for audio_file in tqdm(audio_files, desc="Processing files"):
        # Create output filename using config prefix
        prefix = CONFIG.get("OUTPUT_FILE_PREFIX", "sum_")
        output_filename = f"{prefix}{audio_file.name}"
        output_file = output_dir / output_filename
        
        if processor.process_file(audio_file, output_file):
            successful += 1
    
    # Summary
    logger.info(f"Processing complete: {successful}/{total} files successful")
    if successful < total:
        logger.warning(f"{total - successful} files failed to process")

if __name__ == "__main__":
    main()
