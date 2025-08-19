# 🎛️ Audio Processing Configuration Guide

## Quick Start

1. **Edit the configuration**: Open `config.py` and modify the settings
2. **Test your settings**: Run `py config.py` to see current configuration
3. **Process audio**: Run `py run_processor.py` to use your settings

## 🎤 Multi-Channel Audio Processing Guide

### **Key Changes for Multi-Channel Audio:**

1. **Simplified Processing Chain**:

   - **Single Normalization**: Only at the beginning to bring levels up
   - **Conservative TorchGate**: Single-pass AI noise reduction
   - **No Double Normalization**: Prevents clipping issues

2. **Optimized Processing Order**:

   ```
   Load → Normalize → Noise Gate → TorchGate → Sample Rate Conversion → Save
   ```

3. **Enhanced Configuration Settings**:
   - `ENABLE_SECOND_TORCHGATE = False` - Single-pass processing for speed
   - `ENABLE_FREQUENCY_FILTERING = False` - Disabled for speed
   - `ENABLE_PRE_NORMALIZATION_GATE = False` - Disabled for speed
   - Conservative TorchGate settings for stability

### **Configuration Settings:**

```python
# Single TorchGate Settings (Simplified for Speed and Stability)
ENABLE_SECOND_TORCHGATE = False        # False = single pass for speed

# Conservative TorchGate Settings
TORCHGATE_SETTINGS = {
    "nonstationary": False,            # False = more stable, faster processing
    "n_std_thresh_stationary": 1.2,    # Lower threshold for stability
    "n_thresh_nonstationary": 1.1,     # Lower threshold for stability
    "temp_coeff_nonstationary": 0.2,   # Higher temp for stability
    "n_movemean_nonstationary": 25,    # More frames for stability
    "freq_mask_smooth_hz": 800,        # More smoothing for stability
    "time_mask_smooth_ms": 100,        # More smoothing for stability
    "prop_decrease": 0.2,              # Very gentle reduction for speed
}

# Noise Reduction Strength
NOISE_REDUCTION_STRENGTH = 0.1         # Very conservative for speed and stability

# Disabled Features (for speed)
ENABLE_FREQUENCY_FILTERING = False     # False = skip for speed
ENABLE_PRE_NORMALIZATION_GATE = False  # False = skip for speed
```

### **How It Works:**

1. **Load Audio** - Load the audio file into memory
2. **Initial Normalization** - Bring audio levels up to `-24.0 dB` target
3. **Main Noise Gate** - Remove audio below `-20.0 dB` threshold
4. **Single TorchGate Pass** - Conservative AI noise reduction with gentle settings
5. **Sample Rate Conversion** - Convert to target sample rate if needed
6. **Save** - Write the processed file to output folder

### **Expected Results:**

- **Fast Processing** - Simplified chain for quick results
- **Basic Noise Reduction** - Gentle cleaning without artifacts
- **Consistent Levels** - Single normalization prevents clipping
- **Stable Operation** - Conservative settings for reliability

### **Troubleshooting:**

- **Too Much Bleed**: Increase `TORCHGATE_SETTINGS["prop_decrease"]` or `SECOND_TORCHGATE_SETTINGS["prop_decrease"]`
- **Choppy Audio**: Increase `NOISE_GATE_RELEASE_MS` or decrease `NOISE_REDUCTION_STRENGTH`
- **Lost Speech**: Decrease `TORCHGATE_SETTINGS["n_std_thresh_stationary"]` or `SECOND_TORCHGATE_SETTINGS["n_std_thresh_stationary"]`
- **Slow Processing**: Set `ENABLE_SECOND_TORCHGATE = False` for single-pass processing

### **Performance Tips:**

- **Single Pass**: Set `ENABLE_SECOND_TORCHGATE = False` for faster processing
- **Conservative Settings**: Use `TORCHGATE_SETTINGS["nonstationary"] = False` for stability
- **GPU Processing**: Ensure `FORCE_CPU_PROCESSING = False` for faster processing

## Key Settings to Adjust

### 🎵 Noise Reduction Strength

```python
NOISE_REDUCTION_STRENGTH = 0.2  # 0.0 = no reduction, 1.0 = maximum
```

- **0.1-0.3**: Gentle cleaning (good for already decent audio)
- **0.3-0.5**: Moderate cleaning (typical courtroom audio)
- **0.5+**: Aggressive cleaning (very noisy audio)

### 🔧 Processing Method

```python
PRIMARY_NOISE_REDUCTION_METHOD = "torchgate"  # AI-powered (faster)
FALLBACK_NOISE_REDUCTION_METHOD = "spectral"  # Traditional (more stable)
```

### ⚡ Performance Settings

```python
FORCE_CPU_PROCESSING = False  # True = slower but more stable
CHUNK_SIZE_MB = 1             # Larger = faster but uses more memory
```

## Common Configurations

### For Gentle Cleaning

```python
NOISE_REDUCTION_STRENGTH = 0.1
TORCHGATE_SETTINGS = {"nonstationary": False}
ENABLE_NORMALIZATION = True
```

### For Moderate Cleaning

```python
NOISE_REDUCTION_STRENGTH = 0.3
TORCHGATE_SETTINGS = {"nonstationary": False}
ENABLE_NORMALIZATION = True
```

### For Aggressive Cleaning

```python
NOISE_REDUCTION_STRENGTH = 0.6
TORCHGATE_SETTINGS = {"nonstationary": True}
ENABLE_NORMALIZATION = True
```

### For Fast Processing

```python
FORCE_CPU_PROCESSING = True
CHUNK_SIZE_MB = 2
VERBOSE_OUTPUT = False
```

## Troubleshooting

### If audio sounds distorted:

- Lower `NOISE_REDUCTION_STRENGTH` (try 0.1-0.2)
- Set `TORCHGATE_SETTINGS["nonstationary"] = False`
- Enable `VALIDATE_AUDIO_OUTPUT = True`

### If processing is too slow:

- Set `FORCE_CPU_PROCESSING = True`
- Increase `CHUNK_SIZE_MB`
- Set `VERBOSE_OUTPUT = False`

### If you get errors:

- Set `CONTINUE_ON_ERROR = True`
- Enable `VALIDATE_AUDIO_OUTPUT = True`
- Check `LOG_LEVEL = "DEBUG"` for more details

## File Structure

```
courtsaudio/
├── config.py              # 🎛️ Main configuration file
├── run_processor.py       # Main processing script
├── rawAudio/              # Input audio files
├── cleanAudio/            # Output cleaned files
└── logs/                  # Processing logs
```

## Tips

- Always test on a small audio file first
- Start with conservative settings and increase gradually
- Check the logs in the `logs/` folder for detailed information
- Use `py config.py` to verify your settings before processing
