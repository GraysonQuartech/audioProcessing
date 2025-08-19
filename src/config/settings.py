"""
Configuration settings for the Courtroom Audio Processor.
Loads settings from the main config.py file.
"""

import sys
from pathlib import Path
from typing import Set

# Import the main configuration
try:
    import sys
    import os
    # Add the current directory to the path so we can import config.py
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    import config
    CONFIG = config.get_config()
except ImportError:
    print("⚠️  Warning: config.py not found, using default settings")
    CONFIG = {}

# Directory settings
DEFAULT_INPUT_DIR = CONFIG.get("INPUT_DIRECTORY", "rawAudio")
DEFAULT_OUTPUT_DIR = CONFIG.get("OUTPUT_DIRECTORY", "cleanAudio")
LOGS_DIR = CONFIG.get("LOGS_DIRECTORY", "logs")

# Supported audio formats
SUPPORTED_FORMATS: Set[str] = CONFIG.get("SUPPORTED_AUDIO_FORMATS", {'.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg'})

# Processing settings
DEFAULT_NOISE_REDUCTION_STRENGTH = CONFIG.get("NOISE_REDUCTION_STRENGTH", 0.5)
MIN_NOISE_REDUCTION_STRENGTH = 0.0
MAX_NOISE_REDUCTION_STRENGTH = 1.0

# Noise reduction method settings
PRIMARY_NOISE_REDUCTION_METHOD = CONFIG.get("PRIMARY_NOISE_REDUCTION_METHOD", "torchgate")
FALLBACK_NOISE_REDUCTION_METHOD = CONFIG.get("FALLBACK_NOISE_REDUCTION_METHOD", "spectral")
# TorchGate specific settings
TORCHGATE_SETTINGS = CONFIG.get("TORCHGATE_SETTINGS", {"nonstationary": False, "use_gpu": True})

# Single TorchGate settings (removed double-pass processing)
# Note: These settings were removed from config.py for simplified processing
SPECTRAL_SETTINGS = CONFIG.get("SPECTRAL_SETTINGS", {
    "stationary": True,
    "prop_decrease": 0.5,
    "n_fft": 2048,
    "win_length": 2048,
    "hop_length": 512
})

# Audio quality settings
ENABLE_NORMALIZATION = CONFIG.get("ENABLE_NORMALIZATION", True)
NORMALIZATION_TARGET_DB = CONFIG.get("NORMALIZATION_TARGET_DB", -20.0)
OUTPUT_SAMPLE_RATE = CONFIG.get("OUTPUT_SAMPLE_RATE", None)
OUTPUT_BIT_DEPTH = CONFIG.get("OUTPUT_BIT_DEPTH", 16)

# Performance settings
CHUNK_SIZE = CONFIG.get("CHUNK_SIZE_MB", 1) * 1024 * 1024  # Convert MB to bytes
FORCE_CPU_PROCESSING = CONFIG.get("FORCE_CPU_PROCESSING", False)
MAX_MEMORY_USAGE_GB = CONFIG.get("MAX_MEMORY_USAGE_GB", 4)

# Logging settings
LOG_FILE = f"{LOGS_DIR}/audio_processing.log"
LOG_FORMAT = CONFIG.get("LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s")
LOG_LEVEL = CONFIG.get("LOG_LEVEL", "INFO")
LOG_TO_FILE = CONFIG.get("LOG_TO_FILE", True)

# Progress and output settings
SHOW_PROGRESS_BAR = CONFIG.get("SHOW_PROGRESS_BAR", True)
VERBOSE_OUTPUT = CONFIG.get("VERBOSE_OUTPUT", False)

# Error handling settings
CONTINUE_ON_ERROR = CONFIG.get("CONTINUE_ON_ERROR", True)
SKIP_EXISTING_FILES = CONFIG.get("SKIP_EXISTING_FILES", False)

# Audio validation settings
VALIDATE_AUDIO_OUTPUT = CONFIG.get("VALIDATE_AUDIO_OUTPUT", True)
MAX_AUDIO_AMPLITUDE = CONFIG.get("MAX_AUDIO_AMPLITUDE", 1.0)

# Noise gate settings
ENABLE_NOISE_GATE = CONFIG.get("ENABLE_NOISE_GATE", True)
NOISE_GATE_THRESHOLD_DB = CONFIG.get("NOISE_GATE_THRESHOLD_DB", -40.0)
NOISE_GATE_ATTACK_MS = CONFIG.get("NOISE_GATE_ATTACK_MS", 5)
NOISE_GATE_RELEASE_MS = CONFIG.get("NOISE_GATE_RELEASE_MS", 100)

# Pre-normalization noise gate settings
ENABLE_PRE_NORMALIZATION_GATE = CONFIG.get("ENABLE_PRE_NORMALIZATION_GATE", False)
PRE_GATE_THRESHOLD_DB = CONFIG.get("PRE_GATE_THRESHOLD_DB", -40.0)
PRE_GATE_ATTACK_MS = CONFIG.get("PRE_GATE_ATTACK_MS", 5)
PRE_GATE_RELEASE_MS = CONFIG.get("PRE_GATE_RELEASE_MS", 100)

# Frequency filtering settings
ENABLE_FREQUENCY_FILTERING = CONFIG.get("ENABLE_FREQUENCY_FILTERING", False)
FREQ_LOW_CUTOFF = CONFIG.get("FREQ_LOW_CUTOFF", 100)
FREQ_HIGH_CUTOFF = CONFIG.get("FREQ_HIGH_CUTOFF", 7000)
FREQ_SPEECH_BOOST_LOW = CONFIG.get("FREQ_SPEECH_BOOST_LOW", 500)
FREQ_SPEECH_BOOST_HIGH = CONFIG.get("FREQ_SPEECH_BOOST_HIGH", 3000)
FREQ_SPEECH_BOOST_AMOUNT = CONFIG.get("FREQ_SPEECH_BOOST_AMOUNT", 2.0)

# Speech detection settings
ENABLE_SPEECH_DETECTION = CONFIG.get("ENABLE_SPEECH_DETECTION", False)
REMOVE_SILENCE = CONFIG.get("REMOVE_SILENCE", False)
SILENCE_THRESHOLD_DB = CONFIG.get("SILENCE_THRESHOLD_DB", -40.0)
MIN_SPEECH_DURATION_MS = CONFIG.get("MIN_SPEECH_DURATION_MS", 500)
MIN_SILENCE_DURATION_MS = CONFIG.get("MIN_SILENCE_DURATION_MS", 300)
ENHANCE_SPEECH_CLARITY = CONFIG.get("ENHANCE_SPEECH_CLARITY", True)
SPEECH_FREQUENCY_RANGE = CONFIG.get("SPEECH_FREQUENCY_RANGE", (80, 8000))

# File naming
OUTPUT_FILE_PREFIX = CONFIG.get("OUTPUT_FILE_PREFIX", "cleaned_")

