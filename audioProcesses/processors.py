"""
Audio Processing Classes Module
==============================

This module imports and exports the processing classes from individual processing files
for use in the main processing pipeline.
"""

# Import processing classes from individual files
from .normalize import AudioNormalizer
from .torchgate import TorchGateProcessor  
from .noisegate import NoiseGateProcessor

__all__ = ['AudioNormalizer', 'TorchGateProcessor', 'NoiseGateProcessor']
