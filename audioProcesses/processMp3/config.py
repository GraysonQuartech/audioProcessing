"""
🎛️ PROCESS RAW MP3 CONFIGURATION
=================================

This config is specifically for processing individual raw MP3 files with noise reduction.
Use this when you want to clean up individual audio channels before merging.

HOW TO USE:
1. Edit the values below to change processing behavior
2. Save the file
3. Run: py process_raw_mp3.py

TIPS:
- Adjust noise reduction strength based on your audio quality
- This uses aggressive settings that worked well for room hiss removal
"""

# =============================================================================
# 📁 FILE AND DIRECTORY SETTINGS
# =============================================================================

# Input and output directories
INPUT_DIRECTORY = "../../audioFiles/outputAudio"         # Folder containing your individual MP3 files
OUTPUT_DIRECTORY = "../../audioFiles/mergedAudio"         # Folder where cleaned files will be saved

# File naming
OUTPUT_FILE_PREFIX = "processed_"         # Prefix added to cleaned files (e.g., "processed_audio.mp3")

# =============================================================================
# 🎵 NOISE REDUCTION SETTINGS
# =============================================================================

# Noise gate settings (runs BEFORE AI processing)
# DISABLED FOR INDIVIDUAL FILES: Noise gate is too aggressive and cutting off main speakers
ENABLE_NOISE_GATE = True              # False = skip noise gate to preserve all speech
NOISE_GATE_THRESHOLD_DB = -35.0        # Much lower threshold if gate is re-enabled
NOISE_GATE_ATTACK_MS = 20              # Very slow attack to prevent choppy audio
NOISE_GATE_RELEASE_MS = 1200           # Very long release to prevent word cutting

# TorchGate specific settings (AI-powered noise reduction)
# MAXIMUM AGGRESSIVE PROCESSING: Extreme noise removal to eliminate room hiss
TORCHGATE_SETTINGS = {
    "nonstationary": False,            # False = more stable, faster processing
    "n_std_thresh_stationary": 0.7,    # Extremely low threshold for maximum processing
    "n_thresh_nonstationary": 0.5,     # Extremely low threshold for maximum processing
    "temp_coeff_nonstationary": 0.4,   # Higher temp for maximum processing
    "n_movemean_nonstationary": 8,     # Fewer frames for maximum processing
    "freq_mask_smooth_hz": 150,        # Less smoothing for maximum processing
    "time_mask_smooth_ms": 20,         # Less smoothing for maximum processing
    "prop_decrease": 0.8,              # Maximum reduction to eliminate room hiss
}

# =============================================================================
# 🔊 AUDIO QUALITY SETTINGS
# =============================================================================

# Audio normalization
NORMALIZATION_TARGET_DB = -24.0       # Target loudness in dB

# =============================================================================
# ⚡ PERFORMANCE SETTINGS
# =============================================================================

# GPU/CPU settings
FORCE_CPU_PROCESSING = False           # True = force CPU only, False = use GPU if available

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
    print("🎛️ Current Process Raw MP3 Configuration:")
    print("=" * 50)
    
    config = get_config()
    for key, value in config.items():
        if not key.startswith('_'):
            print(f"{key}: {value}")
    
    print("\n💡 To use this configuration, run: py process_raw_mp3.py")
