#!/usr/bin/env python3
"""
TorchGate Noise Reduction Script
================================

Standalone script for TorchGate AI noise reduction that accepts config parameters.
Can be run independently or as part of a processing pipeline.

Usage:
    python 02_torchgate.py --input input.wav --output output.wav --prop-decrease 0.8
    python 02_torchgate.py --config config.py --input-dir input/ --output-dir output/
"""

import argparse
import logging
import time
from pathlib import Path
from typing import Tuple, Optional, Dict, Any
import numpy as np
import librosa
import soundfile as sf
import torch
from tqdm import tqdm

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TorchGateProcessor:
    """Standalone TorchGate noise reduction processor."""
    
    def __init__(self, torchgate_settings: Dict[str, Any], device: str = "cpu"):
        """Initialize TorchGate processor with settings."""
        self.torchgate_settings = torchgate_settings
        self.device = torch.device(device)
        logger.info(f"TorchGate initialized: device={device}")
        logger.info(f"Settings: {torchgate_settings}")
    
    def load_audio(self, file_path: Path) -> Tuple[np.ndarray, int]:
        """Load audio file using librosa."""
        try:
            logger.debug(f"Loading: {file_path.name}")
            audio, sample_rate = librosa.load(str(file_path), sr=None)
            return audio, sample_rate
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            raise
    
    def apply_torchgate(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """Apply TorchGate AI noise removal."""
        try:
            from noisereduce.torchgate import TorchGate
            
            # Convert to torch tensor
            audio_tensor = torch.tensor(audio.copy(), dtype=torch.float32, device=self.device)
            
            # Add batch dimension if needed
            if audio_tensor.dim() == 1:
                audio_tensor = audio_tensor.unsqueeze(0)
            
            logger.debug("Applying TorchGate AI noise removal")
            tg = TorchGate(
                sr=sample_rate,
                nonstationary=self.torchgate_settings.get("nonstationary", False),
                n_std_thresh_stationary=self.torchgate_settings.get("n_std_thresh_stationary", 1.5),
                n_thresh_nonstationary=self.torchgate_settings.get("n_thresh_nonstationary", 1.3),
                temp_coeff_nonstationary=self.torchgate_settings.get("temp_coeff_nonstationary", 0.1),
                n_movemean_nonstationary=self.torchgate_settings.get("n_movemean_nonstationary", 20),
                freq_mask_smooth_hz=self.torchgate_settings.get("freq_mask_smooth_hz", 500),
                time_mask_smooth_ms=self.torchgate_settings.get("time_mask_smooth_ms", 50),
                prop_decrease=self.torchgate_settings.get("prop_decrease", 0.1)
            ).to(self.device)
            
            # Apply noise reduction
            enhanced_audio = tg(audio_tensor)
            
            # Convert back to numpy
            if enhanced_audio.dim() > 1:
                enhanced_audio = enhanced_audio.squeeze(0)
            
            cleaned_audio = enhanced_audio.cpu().numpy()
            
            # Validate output
            if not np.isfinite(cleaned_audio).all():
                logger.warning("TorchGate produced invalid values, using original audio")
                return audio
            
            logger.debug("TorchGate completed")
            return cleaned_audio
            
        except Exception as e:
            logger.error(f"Error in TorchGate: {e}")
            logger.info("Using original audio")
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
        """Process single file: Load → TorchGate → Save."""
        start_time = time.time()
        
        try:
            logger.info(f"Processing with TorchGate: {input_file.name}")
            
            # Load audio
            audio, sample_rate = self.load_audio(input_file)
            
            # Apply TorchGate
            cleaned_audio = self.apply_torchgate(audio, sample_rate)
            
            # Save
            self.save_audio(cleaned_audio, sample_rate, output_file)
            
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
        # Default TorchGate settings
        return {
            "TORCHGATE_SETTINGS": {
                "nonstationary": False,
                "n_std_thresh_stationary": 1.5,
                "n_thresh_nonstationary": 1.3,
                "temp_coeff_nonstationary": 0.1,
                "n_movemean_nonstationary": 20,
                "freq_mask_smooth_hz": 500,
                "time_mask_smooth_ms": 50,
                "prop_decrease": 0.1
            },
            "FORCE_CPU_PROCESSING": False,
            "INPUT_DIRECTORY": "input",
            "OUTPUT_DIRECTORY": "output",
            "OUTPUT_FILE_PREFIX": "torchgate_"
        }

def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(description="TorchGate Noise Reduction Script")
    parser.add_argument("--config", type=Path, help="Path to config file")
    parser.add_argument("--input", type=Path, help="Input audio file")
    parser.add_argument("--output", type=Path, help="Output audio file")
    parser.add_argument("--input-dir", type=Path, help="Input directory")
    parser.add_argument("--output-dir", type=Path, help="Output directory")
    parser.add_argument("--prop-decrease", type=float, help="Proportion of noise to decrease")
    parser.add_argument("--nonstationary", action="store_true", help="Enable nonstationary processing")
    parser.add_argument("--device", type=str, default="cpu", help="Device to use (cpu/cuda)")
    
    args = parser.parse_args()
    
    # Load config
    config = load_config(args.config)
    
    # Override config with command line arguments
    if args.prop_decrease is not None:
        config["TORCHGATE_SETTINGS"]["prop_decrease"] = args.prop_decrease
    if args.nonstationary:
        config["TORCHGATE_SETTINGS"]["nonstationary"] = True
    if args.device:
        config["FORCE_CPU_PROCESSING"] = (args.device == "cpu")
    
    # Determine device
    device = "cpu" if config.get("FORCE_CPU_PROCESSING", False) else args.device
    
    # Initialize processor
    processor = TorchGateProcessor(
        torchgate_settings=config["TORCHGATE_SETTINGS"],
        device=device
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
    logger.info(f"Device: {device}")
    
    # Process all files
    successful = 0
    total = len(audio_files)
    
    for audio_file in tqdm(audio_files, desc="Processing with TorchGate"):
        # Create output filename
        output_filename = f"{config.get('OUTPUT_FILE_PREFIX', 'torchgate_')}{audio_file.name}"
        output_file = output_dir / output_filename
        
        if processor.process_file(audio_file, output_file):
            successful += 1
    
    # Summary
    logger.info(f"TorchGate processing complete: {successful}/{total} files successful")
    if successful < total:
        logger.warning(f"{total - successful} files failed to process")

if __name__ == "__main__":
    main()
