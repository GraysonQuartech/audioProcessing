"""
🎛️ MERGE RAW TO MP3 CONFIGURATION
==================================

This config is specifically for merging raw audio files into a single MP3.
Use this when you want to combine multiple raw audio channels into one file.

HOW TO USE:
1. Edit the values below to change merge behavior
2. Save the file
3. Run: py merge_to_mp3.py
"""

# =============================================================================
# 📁 FILE AND DIRECTORY SETTINGS
# =============================================================================

# Input and output directories
INPUT_DIRECTORY = "audioFiles/workingAudio"     # Folder containing your original audio files
OUTPUT_DIRECTORY = "audioFiles/outputAudio"    # Folder where merged files will be saved

# File naming
OUTPUT_FILE_PREFIX = "merged_"         # Prefix added to merged files (e.g., "merged_audio.mp3")

# Supported audio formats for merging
SUPPORTED_AUDIO_FORMATS = {
    '.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg'
}

# =============================================================================
# 🔊 AUDIO QUALITY SETTINGS
# =============================================================================

# Output format settings
OUTPUT_SAMPLE_RATE = 44100             # Sample rate for output MP3 (Hz)
OUTPUT_BIT_DEPTH = 16                  # Bit depth for output (16 or 24)
OUTPUT_CHANNELS = 1                    # 1 = mono, 2 = stereo

# MP3 specific settings
MP3_BITRATE = 192                      # Bitrate in kbps (128, 192, 256, 320)
MP3_QUALITY = 0                        # 0 = best quality, 9 = worst quality

# =============================================================================
# ⚠️  DO NOT MODIFY BELOW THIS LINE
# =============================================================================

def get_config():
    """Return all configuration settings as a dictionary."""
    config = {}
    
    # Get all variables from this module
    import sys
    current_module = sys.modules[__name__]
    
    for name in dir(current_module):
        if not name.startswith('_') and name.isupper():
            value = getattr(current_module, name)
            if not callable(value):
                config[name] = value
    
    return config

if __name__ == "__main__":
    # Print current configuration when run directly
    print("🎛️ Current Merge Raw to MP3 Configuration:")
    print("=" * 50)
    
    config = get_config()
    for key, value in config.items():
        if not key.startswith('_'):
            print(f"{key}: {value}")
    
    print("\n💡 To use this configuration, run: py merge_to_mp3.py")
