#!/usr/bin/env python3
"""
Courtroom Audio Processor - Main Script
Local AI-powered noise reduction for courtroom audio files.
All processing happens locally - no data leaves your computer!
"""

import sys
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Import local config
from config import (
    INPUT_DIRECTORY, OUTPUT_DIRECTORY, NOISE_REDUCTION_STRENGTH,
    NOISE_REDUCTION_METHOD, ENABLE_NORMALIZATION, NORMALIZATION_TARGET_DB,
    VERBOSE_LOGGING, SHOW_PROGRESS_BAR, CONTINUE_ON_ERROR,
    SKIP_EXISTING_FILES, SUPPORTED_AUDIO_FORMATS
)

from src.utils.logger import setup_logging
from src.core.processor import CourtroomAudioProcessor

def validate_strength(strength: float) -> bool:
    """Validate noise reduction strength value."""
    return 0.0 <= strength <= 1.0

def main():
    """Main function to run the audio processor."""
    
    # Validate noise reduction strength
    if not validate_strength(NOISE_REDUCTION_STRENGTH):
        print(f"❌ Error: Noise reduction strength must be between 0.0 and 1.0 (current: {NOISE_REDUCTION_STRENGTH})")
        sys.exit(1)
    
    # Setup logging
    setup_logging(VERBOSE_LOGGING)
    
    # Initialize processor
    try:
        processor = CourtroomAudioProcessor(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
    except Exception as e:
        print(f"❌ Error initializing processor: {e}")
        sys.exit(1)
    
    # Show configuration
    print("🎛️ Processing Configuration:")
    print(f"   Input Directory: {INPUT_DIRECTORY}")
    print(f"   Output Directory: {OUTPUT_DIRECTORY}")
    print(f"   Noise Reduction Strength: {NOISE_REDUCTION_STRENGTH}")
    print(f"   Noise Reduction Method: {NOISE_REDUCTION_METHOD}")
    print(f"   Normalization: {'Enabled' if ENABLE_NORMALIZATION else 'Disabled'}")
    if ENABLE_NORMALIZATION:
        print(f"   Normalization Target: {NORMALIZATION_TARGET_DB} dB")
    print()
    
    # Show statistics
    stats = processor.get_processing_stats()
    print("📊 Processing Statistics:")
    print(f"   Audio Files Found: {stats['file_count']}")
    print(f"   Supported Formats: {', '.join(stats['supported_formats'])}")
    if stats['file_count'] > 0:
        total_size_mb = stats['total_size_bytes'] / (1024 * 1024)
        print(f"   Total Size: {total_size_mb:.1f} MB")
    print()
    
    # Process files
    try:
        start_time = time.time()
        successful, total = processor.process_all_files(NOISE_REDUCTION_STRENGTH)
        processing_time = time.time() - start_time
        
        # Show summary
        processor.show_processing_summary(successful, total, processing_time)
        
        # Exit with appropriate code
        if successful == total and total > 0:
            print("🎉 All files processed successfully!")
            sys.exit(0)
        elif total == 0:
            print("📝 No files to process.")
            sys.exit(0)
        else:
            print(f"⚠️  {total - successful} files failed to process")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

