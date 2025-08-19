"""
🎛️ PROCESS RAW MP3 CONFIGURATION
=================================

This config is specifically for processing individual raw MP3 files with noise reduction.
Use this when you want to clean up individual audio channels before merging.

HOW TO USE:
1. Edit the values below to change processing behavior
2. Save the file
3. Run: python run_processor.py
"""

# =============================================================================
# 📁 FILE AND DIRECTORY SETTINGS
# =============================================================================

# Input and output directories
INPUT_DIRECTORY = "audioFiles/sourceAudio"  # Folder containing your original audio files
OUTPUT_DIRECTORY = "audioFiles/outputAudio"  # Folder where cleaned files will be saved

# =============================================================================
# 🎵 NOISE REDUCTION SETTINGS
# =============================================================================

# Noise reduction strength (0.0 = no reduction, 1.0 = maximum reduction)
NOISE_REDUCTION_STRENGTH = 0.4

# Noise reduction method
NOISE_REDUCTION_METHOD = "torchgate"  # Options: "torchgate", "spectral", "normalize"

# =============================================================================
# 🔊 AUDIO QUALITY SETTINGS
# =============================================================================

# Audio normalization
ENABLE_NORMALIZATION = True
NORMALIZATION_TARGET_DB = -24.0

# =============================================================================
# 📊 LOGGING AND MONITORING
# =============================================================================

# Logging settings
VERBOSE_LOGGING = False  # True = detailed processing info, False = summary only
SHOW_PROGRESS_BAR = True

# =============================================================================
# 🔧 ADVANCED SETTINGS
# =============================================================================

# Error handling
CONTINUE_ON_ERROR = True
SKIP_EXISTING_FILES = False

# Supported audio formats
SUPPORTED_AUDIO_FORMATS = {'.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg'}
