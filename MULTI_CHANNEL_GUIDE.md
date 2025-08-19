# 🎤 Multi-Channel Audio Processing Guide

## Overview

This guide explains the optimizations made for processing **8 multi-channel audio files** from the same event, with specific focus on **mic bleed reduction** and **stable TorchGate processing**.

## 🚨 Key Changes Made

### 1. **Fixed TorchGate Parameters**

- **Problem**: Previous configuration used invalid parameters that don't exist in TorchGate
- **Solution**: Updated to use only valid parameters from the actual TorchGate implementation
- **Result**: Eliminates parameter errors and reduces fallback usage

### 2. **Improved Noise Gate for Mic Bleed**

- **Previous**: `-40dB` threshold (too low for mic bleed)
- **New**: `-25dB` threshold (better for reducing mic bleed)
- **Attack**: `5ms` (faster response to speech)
- **Release**: `100ms` (smoother transitions)

### 3. **Optimized Processing Order**

```
BEFORE: Load → Noise Gate → AI Processing → Normalize → Save
AFTER:  Load → Normalize → Noise Gate → AI Processing → Normalize → Save
```

**Why this matters**: Normalizing BEFORE noise reduction helps the AI algorithms work more effectively.

### 4. **Conservative TorchGate Settings**

- **Nonstationary**: `False` (more conservative, better for voice)
- **Strength**: `0.4` (reduced from 0.7 for voice preservation)
- **All parameters**: Set to TorchGate defaults for stability

## 🎯 Multi-Channel Specific Optimizations

### Mic Bleed Reduction

- **Higher noise gate threshold** (-25dB vs -40dB)
- **Frequency filtering options** (80Hz-8kHz focus)
- **Conservative noise reduction** to preserve voice clarity

### Processing Pipeline

1. **Initial Normalization**: Balances levels before processing
2. **Noise Gate**: Removes low-level mic bleed
3. **AI Noise Reduction**: TorchGate with conservative settings
4. **Final Normalization**: Ensures consistent output levels
5. **Sample Rate Conversion**: If needed
6. **Save**: Processed audio

## 📊 Configuration Settings

### Noise Gate (Critical for Mic Bleed)

```python
NOISE_GATE_THRESHOLD_DB = -25.0        # Higher threshold for mic bleed
NOISE_GATE_ATTACK_MS = 5               # Fast attack for speech
NOISE_GATE_RELEASE_MS = 100            # Slow release for smoothness
```

### TorchGate (Stable AI Processing)

```python
TORCHGATE_SETTINGS = {
    "nonstationary": False,            # Conservative mode
    "n_std_thresh_stationary": 1.5,    # Default value
    "n_thresh_nonstationary": 1.3,     # Default value
    "temp_coeff_nonstationary": 0.1,   # Default value
    "n_movemean_nonstationary": 20,    # Default value
    "freq_mask_smooth_hz": 500,        # Default value
    "time_mask_smooth_ms": 50,         # Default value
    "prop_decrease": 0.4,              # Matches NOISE_REDUCTION_STRENGTH
}
```

### Multi-Channel Settings

```python
MULTI_CHANNEL_MODE = True              # Enable multi-channel optimizations
ENABLE_MIC_BLEED_REDUCTION = True      # Apply mic bleed reduction
MIC_BLEED_FREQUENCY_FILTER = True      # Frequency filtering
MIC_BLEED_LOW_FREQ_CUTOFF = 80         # Hz - reduce rumble
MIC_BLEED_HIGH_FREQ_CUTOFF = 8000      # Hz - reduce hiss
```

## 🔧 Usage Instructions

### 1. **Test with One File First**

```bash
# Process a single channel to test settings
py run_processor.py
```

### 2. **Monitor the Logs**

Check `logs/audio_processing.log` for:

- ✅ "Noise reduction completed" (TorchGate success)
- ⚠️ "TorchGate produced invalid values" (fallback used)
- ❌ "Error applying noise reduction" (parameter issues)

### 3. **Adjust Settings if Needed**

**If TorchGate still fails too often:**

```python
# Make even more conservative
NOISE_REDUCTION_STRENGTH = 0.3
TORCHGATE_SETTINGS["nonstationary"] = False
```

**If mic bleed is still too strong:**

```python
# Increase noise gate threshold
NOISE_GATE_THRESHOLD_DB = -20.0
```

**If voice clarity is lost:**

```python
# Reduce noise reduction strength
NOISE_REDUCTION_STRENGTH = 0.2
```

## 🎵 Expected Results

### For Multi-Channel Audio:

- **Reduced mic bleed** between channels
- **Preserved voice clarity** on each channel
- **Consistent levels** across all channels
- **Stable processing** with fewer TorchGate failures

### Processing Time:

- **Faster**: Valid TorchGate parameters = less fallback
- **More reliable**: Conservative settings = fewer errors
- **Better quality**: Optimized processing order

## 🚨 Troubleshooting

### TorchGate Still Failing?

1. Check that all parameters are valid (use defaults)
2. Reduce `NOISE_REDUCTION_STRENGTH` to 0.2-0.3
3. Set `nonstationary = False`

### Too Much Mic Bleed?

1. Increase `NOISE_GATE_THRESHOLD_DB` to -20dB
2. Enable `MIC_BLEED_FREQUENCY_FILTER`
3. Adjust frequency cutoffs

### Voice Sounds Distorted?

1. Reduce `NOISE_REDUCTION_STRENGTH` to 0.2
2. Set `nonstationary = False`
3. Increase `NOISE_GATE_RELEASE_MS` to 150

## 📈 Performance Tips

1. **Process channels independently** for better results
2. **Use consistent settings** across all channels
3. **Monitor logs** for any processing issues
4. **Test on short segments** before full processing

---

**Ready to process your 8-channel audio files with optimized mic bleed reduction!** 🎤✨
