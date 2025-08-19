"""
Main processor class that orchestrates the audio processing workflow.
"""

import logging
import time
from pathlib import Path
from typing import List, Tuple
from tqdm import tqdm

from ..config.settings import (
    DEFAULT_INPUT_DIR, DEFAULT_OUTPUT_DIR, SUPPORTED_FORMATS,
    OUTPUT_FILE_PREFIX
)
from ..utils.file_utils import ensure_directory_exists, get_audio_files, create_output_filename
from ..audio.processor import AudioProcessor

logger = logging.getLogger(__name__)

class CourtroomAudioProcessor:
    """Main processor class for courtroom audio files."""
    
    def __init__(self, input_dir: str = DEFAULT_INPUT_DIR, 
                 output_dir: str = DEFAULT_OUTPUT_DIR):
        """
        Initialize the processor.
        
        Args:
            input_dir: Input directory path
            output_dir: Output directory path
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        
        # Import configuration settings
        from ..config.settings import FORCE_CPU_PROCESSING
        self.audio_processor = AudioProcessor(force_cpu=FORCE_CPU_PROCESSING)
        
        # Create directories
        ensure_directory_exists(self.input_dir)
        ensure_directory_exists(self.output_dir)
        
        logger.info(f"Courtroom Audio Processor initialized")
        logger.info(f"Input directory: {self.input_dir}")
        logger.info(f"Output directory: {self.output_dir}")
    
    def get_audio_files(self) -> List[Path]:
        """Get all supported audio files from input directory."""
        return get_audio_files(self.input_dir)
    
    def process_single_file(self, input_file: Path, output_file: Path, 
                           noise_reduction_strength: float = 0.5) -> bool:
        """
        Process a single audio file.
        
        Args:
            input_file: Path to input file
            output_file: Path to output file
            noise_reduction_strength: Noise reduction strength
            
        Returns:
            True if successful, False otherwise
        """
        return self.audio_processor.process_audio_file(
            input_file, output_file, noise_reduction_strength
        )
    
    def process_all_files(self, noise_reduction_strength: float = 0.5) -> Tuple[int, int]:
        """
        Process all audio files in the input directory.
        
        Args:
            noise_reduction_strength: Strength of noise reduction (0.0 to 1.0)
            
        Returns:
            Tuple of (successful_count, total_count)
        """
        audio_files = self.get_audio_files()
        
        if not audio_files:
            logger.warning("No audio files found to process!")
            logger.info(f"Supported formats: {', '.join(SUPPORTED_FORMATS)}")
            logger.info(f"Please add audio files to: {self.input_dir}")
            return 0, 0
        
        logger.info(f"Processing {len(audio_files)} audio file(s):")
        for file in audio_files:
            logger.info(f"  - {file.name}")
        
        successful = 0
        total = len(audio_files)
        
        # Process files with progress bar
        for audio_file in tqdm(audio_files, desc="Processing audio files"):
            output_filename = create_output_filename(
                audio_file.name, OUTPUT_FILE_PREFIX
            )
            output_file = self.output_dir / output_filename
            
            if self.process_single_file(audio_file, output_file, noise_reduction_strength):
                successful += 1
        
        return successful, total
    
    def show_processing_summary(self, successful: int, total: int, 
                              processing_time: float) -> None:
        """
        Display processing summary.
        
        Args:
            successful: Number of successfully processed files
            total: Total number of files
            processing_time: Total processing time in seconds
        """
        logger.info("\n" + "="*50)
        logger.info(f"PROCESSING COMPLETE!")
        logger.info("="*50)
        logger.info(f"Total files processed: {total}")
        logger.info(f"Successfully processed: {successful}")
        logger.info(f"Failed to process: {total - successful}")
        logger.info(f"Total processing time: {processing_time:.2f} seconds")
        logger.info(f"Cleaned files saved to: {self.output_dir}")
        
        if successful > 0:
            success_rate = (successful / total) * 100
            logger.info(f"Success rate: {success_rate:.1f}%")
        
        logger.info("="*50)
    
    def get_processing_stats(self) -> dict:
        """
        Get statistics about the processing setup.
        
        Returns:
            Dictionary with processing statistics
        """
        audio_files = self.get_audio_files()
        total_size = sum(f.stat().st_size for f in audio_files)
        
        return {
            'input_directory': str(self.input_dir),
            'output_directory': str(self.output_dir),
            'file_count': len(audio_files),
            'total_size_bytes': total_size,
            'supported_formats': list(SUPPORTED_FORMATS)
        }

