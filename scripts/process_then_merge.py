#!/usr/bin/env python3
"""
🎵 Process Then Merge Pipeline
=============================

This script orchestrates the reverse audio processing pipeline:
1. Processes individual audio files from sourceAudio folder
2. Merges the processed audio files into a single output

Usage:
    python scripts/process_then_merge.py

Pipeline:
    sourceAudio/ → workingAudio/ → outputAudio/
"""

import os
import sys
import subprocess
import logging
import shutil
from pathlib import Path
from typing import List, Optional
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ProcessThenMergePipeline:
    """Orchestrates the process-then-merge audio processing pipeline."""
    
    def __init__(self):
        """Initialize the pipeline with correct paths."""
        # Get the project root directory (parent of scripts/)
        self.project_root = Path(__file__).parent.parent
        self.audio_files_dir = self.project_root / "audioFiles"
        
        # Define pipeline directories
        self.source_dir = self.audio_files_dir / "sourceAudio"
        self.working_dir = self.audio_files_dir / "workingAudio"
        self.output_dir = self.audio_files_dir / "outputAudio"
        
        # Define script paths
        self.process_script = self.project_root / "audioProcesses" / "processMp3" / "process_raw_mp3.py"
        self.merge_script = self.project_root / "audioProcesses" / "mergeToMp3" / "merge_to_mp3.py"
        
        logger.info(f"Project root: {self.project_root}")
        logger.info(f"Source directory: {self.source_dir}")
        logger.info(f"Working directory: {self.working_dir}")
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
        if not self.process_script.exists():
            logger.error(f"Process script not found: {self.process_script}")
            return False
        
        if not self.merge_script.exists():
            logger.error(f"Merge script not found: {self.merge_script}")
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
    
    def setup_processing_environment(self) -> bool:
        """Set up the processing environment by creating directories."""
        logger.info("Setting up processing environment...")
        
        try:
            # Create working directory
            self.working_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created working directory: {self.working_dir}")
            
            # Create output directory
            self.output_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created output directory: {self.output_dir}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting up processing environment: {e}")
            return False
    
    def run_individual_processing(self) -> bool:
        """Run the processing script on individual audio files."""
        logger.info("=" * 60)
        logger.info("STEP 1: PROCESSING INDIVIDUAL AUDIO FILES")
        logger.info("=" * 60)
        
        try:
            # Create working directory if it doesn't exist
            self.working_dir.mkdir(parents=True, exist_ok=True)
            
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
                logger.info(f"✅ Individual processing completed successfully in {processing_time:.2f}s")
                
                # Check if processed files were created
                working_files = self.get_audio_files(self.working_dir)
                if working_files:
                    logger.info(f"Created {len(working_files)} processed files")
                    return True
                else:
                    logger.error("No processed files found in working directory")
                    return False
            else:
                logger.error(f"❌ Individual processing failed with return code: {result.returncode}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error running process script: {e}")
            return False
    
    def run_merge_script(self) -> bool:
        """Run the merge script to combine processed audio files."""
        logger.info("=" * 60)
        logger.info("STEP 2: MERGING PROCESSED AUDIO FILES")
        logger.info("=" * 60)
        
        try:
            # Create merged directory if it doesn't exist
            merged_dir = self.audio_files_dir / "mergedAudio"
            merged_dir.mkdir(parents=True, exist_ok=True)
            
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
                merged_files = self.get_audio_files(merged_dir)
                if merged_files:
                    logger.info(f"Created merged file: {merged_files[0].name}")
                    return True
                else:
                    logger.error("No merged file found in mergedAudio directory")
                    return False
            else:
                logger.error(f"❌ Merge failed with return code: {result.returncode}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error running merge script: {e}")
            return False
    
    def cleanup_intermediate_files(self) -> bool:
        """Clean up intermediate processed files (optional)."""
        logger.info("Cleaning up intermediate files...")
        
        try:
            if self.working_dir.exists():
                # Count files before cleanup
                working_files = self.get_audio_files(self.working_dir)
                logger.info(f"Removing {len(working_files)} intermediate processed files")
                
                # Remove the working directory and all its contents
                shutil.rmtree(self.working_dir)
                logger.info("✅ Cleanup completed")
                return True
            else:
                logger.info("No intermediate files to clean up")
                return True
                
        except Exception as e:
            logger.error(f"❌ Error during cleanup: {e}")
            return False
    
    def run_pipeline(self, cleanup: bool = True) -> bool:
        """Run the complete process-then-merge audio processing pipeline."""
        logger.info("🎵 Starting Process-Then-Merge Audio Pipeline")
        logger.info("=" * 60)
        
        # Check prerequisites
        if not self.check_prerequisites():
            logger.error("❌ Prerequisites check failed")
            return False
        
        # Set up processing environment
        if not self.setup_processing_environment():
            logger.error("❌ Environment setup failed")
            return False
        
        # Step 1: Process individual audio files
        if not self.run_individual_processing():
            logger.error("❌ Individual processing step failed")
            return False
        
        # Step 2: Merge processed audio files
        if not self.run_merge_script():
            logger.error("❌ Merge step failed")
            return False
        
        # Optional cleanup
        if cleanup:
            if not self.cleanup_intermediate_files():
                logger.warning("⚠️  Cleanup failed, but pipeline completed")
        
        # Pipeline completed successfully
        logger.info("=" * 60)
        logger.info("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        logger.info("=" * 60)
        
        # Summary
        source_files = self.get_audio_files(self.source_dir)
        merged_dir = self.audio_files_dir / "mergedAudio"
        merged_files = self.get_audio_files(merged_dir)
        
        logger.info("📊 Pipeline Summary:")
        logger.info(f"  Source files processed: {len(source_files)}")
        logger.info(f"  Merged files created: {len(merged_files)}")
        
        if merged_files:
            logger.info(f"  Final output: {merged_files[0].name}")
        
        return True

def main():
    """Main function to run the process-then-merge audio processing pipeline."""
    try:
        pipeline = ProcessThenMergePipeline()
        success = pipeline.run_pipeline()
        
        if success:
            print("\n🎉 Process-then-merge pipeline completed successfully!")
            print("Check the outputAudio folder for your merged processed audio file.")
        else:
            print("\n❌ Process-then-merge pipeline failed!")
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
