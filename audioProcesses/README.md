# 🎵 Shared Audio Processing Scripts

This folder contains reusable audio processing scripts that can be used by any workflow.

## 📁 Available Scripts

### `01_normalize.py` - Audio Normalization

**Purpose**: Normalize audio volume to a target loudness level

**Usage**:

```bash
# Single file
python 01_normalize.py --input input.wav --output output.wav --target-db -24.0

# Batch processing
python 01_normalize.py --config config.py --input-dir input/ --output-dir output/
```

**Key Parameters**:

- `--target-db`: Target loudness in dB (default: -24.0)
- `--max-amplitude`: Maximum amplitude (default: 1.0)

### `02_torchgate.py` - TorchGate AI Noise Reduction

**Purpose**: Apply AI-powered noise reduction using TorchGate

**Usage**:

```bash
# Single file
python 02_torchgate.py --input input.wav --output output.wav --prop-decrease 0.8

# Batch processing
python 02_torchgate.py --config config.py --input-dir input/ --output-dir output/
```

**Key Parameters**:

- `--prop-decrease`: Proportion of noise to decrease (0.0-1.0)
- `--nonstationary`: Enable nonstationary processing
- `--device`: Device to use (cpu/cuda)

## 🔧 Configuration

Both scripts can use a config file or command-line arguments:

### Config File Usage:

```bash
python 01_normalize.py --config ../processRawMergedMp3/config.py --input-dir input/ --output-dir output/
```

### Command Line Override:

```bash
python 01_normalize.py --config config.py --target-db -20.0 --input-dir input/ --output-dir output/
```

## 📋 Supported Audio Formats

- `.wav` - Waveform Audio File Format
- `.mp3` - MPEG Audio Layer III
- `.m4a` - MPEG-4 Audio
- `.flac` - Free Lossless Audio Codec
- `.aac` - Advanced Audio Coding
- `.ogg` - Ogg Vorbis

## 🚀 Integration with Pipelines

These scripts are designed to work with pipeline orchestrators:

```bash
# From any workflow folder
python scripts/03_pipeline.py --steps torchgate,normalize --config config.py
```

## ⚙️ Default Settings

### Normalization Defaults:

- Target dB: -24.0
- Max amplitude: 1.0
- Output prefix: "normalized\_"

### TorchGate Defaults:

- Nonstationary: False
- n_std_thresh_stationary: 1.5
- n_thresh_nonstationary: 1.3
- prop_decrease: 0.1
- Output prefix: "torchgate\_"

## 🔄 Workflow Integration

These scripts can be used in any of these workflows:

1. **processRawMergedMp3** - Process merged MP3 files
2. **processRawMp3** - Process individual raw MP3 files
3. **mergeProcessedMp3** - Final processing before merging
4. **Custom workflows** - Any other audio processing needs

## 💡 Tips

1. **Test on single files first** before batch processing
2. **Use config files** for consistent settings across workflows
3. **Monitor logs** for processing status and errors
4. **Adjust parameters** based on your specific audio quality needs
5. **Use pipelines** for multi-step processing workflows
