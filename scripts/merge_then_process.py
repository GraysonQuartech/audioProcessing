#!/usr/bin/env python3
"""
🎵 Merge Then Process Pipeline
==============================

This script orchestrates the complete audio processing pipeline:
1. Merges audio files from sourceAudio folder
2. Processes the merged audio with noise reduction and normalization

Usage:
    python scripts/merge_then_process.py

Pipeline:
    sourceAudio/ → mergedAudio/ → outputAudio/
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import List, Optional
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AudioPipeline:
    """Orchestrates the complete audio processing pipeline."""
    
    def __init__(self):
        """Initialize the pipeline with correct paths."""
        # Get the project root directory (parent of scripts/)
        self.project_root = Path(__file__).parent.parent
        self.audio_files_dir = self.project_root / "audioFiles"
        
        # Define pipeline directories
        self.source_dir = self.audio_files_dir / "sourceAudio"
        self.merged_dir = self.audio_files_dir / "mergedAudio"
        self.output_dir = self.audio_files_dir / "outputAudio"
        
        # Define script paths
        self.merge_script = self.project_root / "audioProcesses" / "mergeToMp3" / "merge_to_mp3.py"
        self.process_script = self.project_root / "audioProcesses" / "processMergedMp3" / "process_merged_mp3.py"
        
        logger.info(f"Project root: {self.project_root}")
        logger.info(f"Source directory: {self.source_dir}")
        logger.info(f"Merged directory: {self.merged_dir}")
        logger.info(f"Output directory: {self.output_dir}")
    
    def check_prerequisites(self) -> bool:
        """Check if all required directories and files exist."""
        logger.info("Checking prerequisites...")
        
        # Check if source directory exists and has files
        if not self.source_dir.exists():
            logger.error(f"Source directory does not exist: {self.source_dir}")
            return False
        
        source_files = self.get_audio_files(self.source_dir)
        if not source_files:
            logger.error(f"No audio files found in source directory: {self.source_dir}")
            return False
        
        logger.info(f"Found {len(source_files)} audio files in source directory")
        
        # Check if scripts exist
        if not self.merge_script.exists():
            logger.error(f"Merge script not found: {self.merge_script}")
            return False
        
        if not self.process_script.exists():
            logger.error(f"Process script not found: {self.process_script}")
            return False
        
        logger.info("All prerequisites satisfied")
        return True
    
    def get_audio_files(self, directory: Path) -> List[Path]:
        """Get all supported audio files from a directory."""
        supported_formats = {'.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg'}
        audio_files = []
        
        if not directory.exists():
            return audio_files
        
        for file_path in directory.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_formats:
                audio_files.append(file_path)
        
        return sorted(audio_files)
    
    def run_merge_script(self) -> bool:
        """Run the merge script to combine source audio files."""
        logger.info("=" * 60)
        logger.info("STEP 1: MERGING AUDIO FILES")
        logger.info("=" * 60)
        
        try:
            # Create merged directory if it doesn't exist
            self.merged_dir.mkdir(parents=True, exist_ok=True)
            
            # Change to the merge script directory
            original_cwd = os.getcwd()
            merge_script_dir = self.merge_script.parent
            
            logger.info(f"Changing to directory: {merge_script_dir}")
            os.chdir(merge_script_dir)
            
            # Run the merge script
            logger.info(f"Running merge script: {self.merge_script.name}")
            start_time = time.time()
            
            result = subprocess.run(
                [sys.executable, self.merge_script.name],
                capture_output=True,
                text=True,
                cwd=merge_script_dir
            )
            
            # Restore original working directory
            os.chdir(original_cwd)
            
            processing_time = time.time() - start_time
            
            # Log output
            if result.stdout:
                logger.info("Merge script output:")
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        logger.info(f"  {line}")
            
            if result.stderr:
                logger.warning("Merge script warnings/errors:")
                for line in result.stderr.strip().split('\n'):
                    if line.strip():
                        logger.warning(f"  {line}")
            
            if result.returncode == 0:
                logger.info(f"✅ Merge completed successfully in {processing_time:.2f}s")
                
                # Check if merged file was created
                merged_files = self.get_audio_files(self.merged_dir)
                if merged_files:
                    logger.info(f"Created merged file: {merged_files[0].name}")
                    return True
                else:
                    logger.error("No merged file found in output directory")
                    return False
            else:
                logger.error(f"❌ Merge failed with return code: {result.returncode}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error running merge script: {e}")
            return False
    
    def run_process_script(self) -> bool:
        """Run the process script to clean the merged audio."""
        logger.info("=" * 60)
        logger.info("STEP 2: PROCESSING MERGED AUDIO")
        logger.info("=" * 60)
        
        try:
            # Create output directory if it doesn't exist
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            # Change to the process script directory
            original_cwd = os.getcwd()
            process_script_dir = self.process_script.parent
            
            logger.info(f"Changing to directory: {process_script_dir}")
            os.chdir(process_script_dir)
            
            # Run the process script
            logger.info(f"Running process script: {self.process_script.name}")
            start_time = time.time()
            
            result = subprocess.run(
                [sys.executable, self.process_script.name],
                capture_output=True,
                text=True,
                cwd=process_script_dir
            )
            
            # Restore original working directory
            os.chdir(original_cwd)
            
            processing_time = time.time() - start_time
            
            # Log output
            if result.stdout:
                logger.info("Process script output:")
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        logger.info(f"  {line}")
            
            if result.stderr:
                logger.warning("Process script warnings/errors:")
                for line in result.stderr.strip().split('\n'):
                    if line.strip():
                        logger.warning(f"  {line}")
            
            if result.returncode == 0:
                logger.info(f"✅ Processing completed successfully in {processing_time:.2f}s")
                
                # Check if processed file was created
                output_files = self.get_audio_files(self.output_dir)
                if output_files:
                    logger.info(f"Created processed file: {output_files[0].name}")
                    return True
                else:
                    logger.error("No processed file found in output directory")
                    return False
            else:
                logger.error(f"❌ Processing failed with return code: {result.returncode}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error running process script: {e}")
            return False
    
    def run_pipeline(self) -> bool:
        """Run the complete audio processing pipeline."""
        logger.info("🎵 Starting Audio Processing Pipeline")
        logger.info("=" * 60)
        
        # Check prerequisites
        if not self.check_prerequisites():
            logger.error("❌ Prerequisites check failed")
            return False
        
        # Step 1: Merge audio files
        if not self.run_merge_script():
            logger.error("❌ Merge step failed")
            return False
        
        # Step 2: Process merged audio
        if not self.run_process_script():
            logger.error("❌ Process step failed")
            return False
        
        # Pipeline completed successfully
        logger.info("=" * 60)
        logger.info("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        logger.info("=" * 60)
        
        # Summary
        source_files = self.get_audio_files(self.source_dir)
        merged_files = self.get_audio_files(self.merged_dir)
        output_files = self.get_audio_files(self.output_dir)
        
        logger.info("📊 Pipeline Summary:")
        logger.info(f"  Source files: {len(source_files)}")
        logger.info(f"  Merged files: {len(merged_files)}")
        logger.info(f"  Output files: {len(output_files)}")
        
        if output_files:
            logger.info(f"  Final output: {output_files[0].name}")
        
        return True

def main():
    """Main function to run the audio processing pipeline."""
    try:
        pipeline = AudioPipeline()
        success = pipeline.run_pipeline()
        
        if success:
            print("\n🎉 Pipeline completed successfully!")
            print("Check the outputAudio folder for your processed audio files.")
        else:
            print("\n❌ Pipeline failed!")
            print("Check the logs above for error details.")
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n⚠️  Pipeline interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
