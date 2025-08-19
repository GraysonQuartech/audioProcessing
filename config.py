"""
🎛️ AUDIO PROCESSING CONTROL PANEL
================================

This file contains all the configurable parameters for the courtroom audio processor.
Modify these settings to customize the audio processing behavior.

HOW TO USE:
1. Edit the values below to change processing behavior
2. Save the file
3. Run: py run_processor.py

TIPS:
- Start with conservative settings (low noise reduction strength)
- Test on a small audio file first
- Adjust parameters based on your specific audio quality needs
"""

# =============================================================================
# 📁 FILE AND DIRECTORY SETTINGS
# =============================================================================

# Input and output directories
# Choose which audio quality folder to process
USE_GOOD_QUALITY_AUDIO = True         # True = use rawAudioGood, False = use rawAudioBad
INPUT_DIRECTORY = "rawAudioGood" if USE_GOOD_QUALITY_AUDIO else "rawAudioBad"  # Folder containing your original audio files
OUTPUT_DIRECTORY = "cleanAudio"        # Folder where cleaned files will be saved

# File naming
OUTPUT_FILE_PREFIX = "cleaned_"        # Prefix added to cleaned files (e.g., "cleaned_audio.mp3")

# Supported audio formats (don't change unless you know what you're doing)
SUPPORTED_AUDIO_FORMATS = {
    '.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg'
}

# =============================================================================
# 🎤 MULTI-CHANNEL AUDIO SETTINGS (for mic bleed reduction)
# =============================================================================

# Multi-channel processing settings
# These settings are optimized for processing multiple microphone channels from the same event
MULTI_CHANNEL_MODE = True              # True = optimize for multi-channel audio, False = single channel

# Mic bleed reduction settings
ENABLE_MIC_BLEED_REDUCTION = True      # True = apply additional processing for mic bleed
MIC_BLEED_FREQUENCY_FILTER = True      # True = apply frequency filtering to reduce bleed
MIC_BLEED_LOW_FREQ_CUTOFF = 80         # Hz - cut frequencies below this (reduces rumble bleed)
MIC_BLEED_HIGH_FREQ_CUTOFF = 8000      # Hz - cut frequencies above this (reduces hiss bleed)

# Channel-specific processing
PROCESS_CHANNELS_INDEPENDENTLY = True   # True = each channel processed separately, False = batch processing
ENABLE_CROSS_CHANNEL_NOISE_REFERENCE = False  # True = use other channels as noise reference (experimental)

# =============================================================================
# 🎵 NOISE REDUCTION SETTINGS
# =============================================================================

# Noise gate settings (runs BEFORE AI processing)
# DISABLED FOR MONO SUM: Noise gate is too aggressive and cutting off main speakers
# Set to False to preserve all speech content
ENABLE_NOISE_GATE = False              # False = skip noise gate to preserve all speech (was True)
NOISE_GATE_THRESHOLD_DB = -35.0        # Much lower threshold if gate is re-enabled (was -25.0)
NOISE_GATE_ATTACK_MS = 20              # Very slow attack to prevent choppy audio (was 15)
NOISE_GATE_RELEASE_MS = 1200           # Very long release to prevent word cutting (was 800)

# Pre-normalization noise gate (removes speech peaks from other mics before normalization)
ENABLE_PRE_NORMALIZATION_GATE = False  # False = skip for speed (was True)

# Frequency-domain filtering for mic isolation
ENABLE_FREQUENCY_FILTERING = False     # False = skip for speed (was True)
FREQ_LOW_CUTOFF = 100                  # Hz - remove rumble and HVAC noise
FREQ_HIGH_CUTOFF = 7000                # Hz - remove hiss and high-frequency bleed
FREQ_SPEECH_BOOST_LOW = 500            # Hz - boost lower speech frequencies
FREQ_SPEECH_BOOST_HIGH = 3000          # Hz - boost upper speech frequencies
FREQ_SPEECH_BOOST_AMOUNT = 2.0         # dB - amount to boost speech frequencies

# Primary noise reduction strength (0.0 = no reduction, 1.0 = maximum reduction)
# MAXIMUM AGGRESSIVE PROCESSING: Extreme noise removal to eliminate room hiss
NOISE_REDUCTION_STRENGTH = 0.85        # Maximum aggressive reduction to eliminate room hiss (was 0.7)

# Noise reduction method priority (the script will try these in order)
# Options: "torchgate" (AI-powered, faster), "spectral" (traditional, more stable)
PRIMARY_NOISE_REDUCTION_METHOD = "torchgate"
FALLBACK_NOISE_REDUCTION_METHOD = "spectral"

# TorchGate specific settings (AI-powered noise reduction)
# MAXIMUM AGGRESSIVE PROCESSING: Extreme noise removal to eliminate room hiss
# Note: Only one TorchGate pass is used for faster processing
TORCHGATE_SETTINGS = {
    "nonstationary": False,            # False = more stable, faster processing
    "n_std_thresh_stationary": 0.7,    # Extremely low threshold for maximum processing (was 1.0)
    "n_thresh_nonstationary": 0.5,     # Extremely low threshold for maximum processing (was 0.8)
    "temp_coeff_nonstationary": 0.4,   # Higher temp for maximum processing (was 0.3)
    "n_movemean_nonstationary": 8,     # Fewer frames for maximum processing (was 10)
    "freq_mask_smooth_hz": 150,        # Less smoothing for maximum processing (was 200)
    "time_mask_smooth_ms": 20,         # Less smoothing for maximum processing (was 30)
    "prop_decrease": 0.8,              # Maximum reduction to eliminate room hiss (was 0.6)
}

# Spectral gating settings (traditional noise reduction)
SPECTRAL_SETTINGS = {
    "stationary": True,                # True = less aggressive, False = more aggressive
    "prop_decrease": 0.15,             # Much gentler reduction (was 0.3)
    "n_fft": 2048,                     # FFT window size (higher = better quality)
    "win_length": 2048,                # Window length for analysis
    "hop_length": 512,                 # Step size between windows
}

# =============================================================================
# 🗣️ SPEECH DETECTION SETTINGS
# =============================================================================

# Speech detection and filtering
ENABLE_SPEECH_DETECTION = False         # True = detect and keep only speech, False = keep all audio
REMOVE_SILENCE = False                  # True = remove silence periods, False = keep silence
SILENCE_THRESHOLD_DB = -30.0            # Below this level is considered silence (lower = more sensitive)
MIN_SPEECH_DURATION_MS = 500            # Minimum speech segment duration (shorter = more aggressive)
MIN_SILENCE_DURATION_MS = 300           # Minimum silence duration to remove (shorter = more aggressive)

# Speech enhancement
ENHANCE_SPEECH_CLARITY = True          # True = apply speech-specific enhancement, False = standard processing
SPEECH_FREQUENCY_RANGE = (80, 8000)     # Focus on human speech frequencies (Hz)

# =============================================================================
# 🔊 AUDIO QUALITY SETTINGS
# =============================================================================

# Audio normalization
ENABLE_NORMALIZATION = True          # True = normalize audio levels, False = keep original levels
NORMALIZATION_TARGET_DB = -24.0       # Target loudness in dB (higher = louder, less compression)

# Audio format settings
OUTPUT_SAMPLE_RATE = None             # Higher sample rate for better quality (None = keep original)
OUTPUT_BIT_DEPTH = 24                  # 16 or 24 bit audio quality

# =============================================================================
# ⚡ PERFORMANCE SETTINGS
# =============================================================================

# Processing chunk size (for large files)
CHUNK_SIZE_MB = 1                      # Process files in chunks of this size (in MB)

# GPU/CPU settings
FORCE_CPU_PROCESSING = False           # True = force CPU only, False = use GPU if available
MAX_MEMORY_USAGE_GB = 4                # Maximum memory usage (in GB)

# =============================================================================
# 📊 LOGGING AND MONITORING
# =============================================================================

# Logging settings
LOG_LEVEL = "INFO"                     # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# Progress reporting
SHOW_PROGRESS_BAR = True               # True = show progress bar, False = minimal output
VERBOSE_OUTPUT = False                 # True = detailed processing info, False = summary only

# =============================================================================
# 🔧 ADVANCED SETTINGS (Only change if you know what you're doing)
# =============================================================================

# Error handling
CONTINUE_ON_ERROR = True               # True = continue processing other files if one fails
SKIP_EXISTING_FILES = False            # True = skip files that already exist in output folder

# Audio validation
VALIDATE_AUDIO_OUTPUT = True           # True = check for invalid audio values, False = skip validation
MAX_AUDIO_AMPLITUDE = 1.0              # Maximum allowed audio amplitude (prevent clipping)

# =============================================================================
# 🎯 PRESET CONFIGURATIONS
# =============================================================================

# Quick preset configurations - uncomment one to use it

# PRESET_GENTLE = {
#     "NOISE_REDUCTION_STRENGTH": 0.1,
#     "TORCHGATE_SETTINGS": {"nonstationary": False},
#     "SPECTRAL_SETTINGS": {"stationary": True, "prop_decrease": 0.3},
#     "ENABLE_NORMALIZATION": True,
#     "NORMALIZATION_TARGET_DB": -18.0
# }

# PRESET_MODERATE = {
#     "NOISE_REDUCTION_STRENGTH": 0.3,
#     "TORCHGATE_SETTINGS": {"nonstationary": False},
#     "SPECTRAL_SETTINGS": {"stationary": True, "prop_decrease": 0.5},
#     "ENABLE_NORMALIZATION": True,
#     "NORMALIZATION_TARGET_DB": -20.0
# }

# PRESET_AGGRESSIVE = {
#     "NOISE_REDUCTION_STRENGTH": 0.7,
#     "TORCHGATE_SETTINGS": {"nonstationary": True},
#     "SPECTRAL_SETTINGS": {"stationary": False, "prop_decrease": 0.8},
#     "ENABLE_NORMALIZATION": True,
#     "NORMALIZATION_TARGET_DB": -22.0
# }

# =============================================================================
# 📝 USAGE EXAMPLES
# =============================================================================

"""
EXAMPLE CONFIGURATIONS:

1. GENTLE CLEANING (for already good audio):
   - NOISE_REDUCTION_STRENGTH = 0.1
   - TORCHGATE_SETTINGS["nonstationary"] = False
   - ENABLE_NORMALIZATION = True

2. MODERATE CLEANING (for typical courtroom audio):
   - NOISE_REDUCTION_STRENGTH = 0.3
   - TORCHGATE_SETTINGS["nonstationary"] = False
   - ENABLE_NORMALIZATION = True

3. AGGRESSIVE CLEANING (for very noisy audio):
   - NOISE_REDUCTION_STRENGTH = 0.6
   - TORCHGATE_SETTINGS["nonstationary"] = True
   - ENABLE_NORMALIZATION = True

4. FAST PROCESSING (sacrifice quality for speed):
   - FORCE_CPU_PROCESSING = True
   - CHUNK_SIZE_MB = 2
   - VERBOSE_OUTPUT = False

5. HIGH QUALITY (sacrifice speed for quality):
   - OUTPUT_SAMPLE_RATE = 48000
   - OUTPUT_BIT_DEPTH = 24
   - MAX_MEMORY_USAGE_GB = 8
"""

# =============================================================================
# ⚠️  DO NOT MODIFY BELOW THIS LINE
# =============================================================================

# This section ensures the configuration is properly loaded
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
    print("🎛️ Current Audio Processing Configuration:")
    print("=" * 50)
    
    config = get_config()
    for key, value in config.items():
        if not key.startswith('_'):
            print(f"{key}: {value}")
    
    print("\n💡 To use this configuration, run: py run_processor.py")
