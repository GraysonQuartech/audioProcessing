# 🎧 Courtroom Audio Processor (Python)

**Local AI-powered noise reduction for courtroom audio files. All processing happens on your computer - no data leaves Canada! 🇨🇦**

## 🔒 Privacy & Security

- ✅ **100% Local Processing** - No internet required
- ✅ **No Data Transmission** - Files never leave your computer
- ✅ **Canadian Data Sovereignty** - Perfect for legal requirements
- ✅ **Open Source** - Transparent and auditable code

## 🚀 Quick Start

### 1. Install Python Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### 2. Add Your Audio Files

```bash
# Create input directory (or it will be created automatically)
mkdir rawAudio

# Add your courtroom audio files to the rawAudio folder
# Supported formats: WAV, MP3, M4A, FLAC, AAC, OGG
```

### 3. Process Audio Files

```bash
# Process all files with default settings
python audio_processor.py

# Or with custom options
python audio_processor.py --input my_audio_folder --output cleaned_audio --strength 0.7
```

## 📁 File Structure

```
courtsaudio/
├── audio_processor.py      # Main processing script
├── requirements.txt        # Python dependencies
├── rawAudio/              # Input audio files (auto-created)
├── cleanAudio/            # Output cleaned files (auto-created)
├── audio_processing.log   # Processing log (auto-created)
└── README_PYTHON.md       # This file
```

## 🎛️ Usage Options

### Basic Usage

```bash
# Process all files in rawAudio folder
python audio_processor.py
```

### Advanced Usage

```bash
# Custom input/output directories
python audio_processor.py --input my_audio --output cleaned_audio

# Adjust noise reduction strength (0.0 to 1.0)
python audio_processor.py --strength 0.8

# Enable verbose logging
python audio_processor.py --verbose

# Combine options
python audio_processor.py --input court_recordings --output processed --strength 0.6 --verbose
```

### Command Line Options

- `--input, -i`: Input directory (default: `rawAudio`)
- `--output, -o`: Output directory (default: `cleanAudio`)
- `--strength, -s`: Noise reduction strength 0.0-1.0 (default: `0.5`)
- `--verbose, -v`: Enable detailed logging

## 🎯 What It Does

### AI-Powered Noise Reduction

- **Background Noise Removal** - HVAC, paper shuffling, etc.
- **Voice Enhancement** - Improves speech clarity
- **Echo Reduction** - Minimizes room reverberation
- **Audio Normalization** - Prevents clipping and distortion

### Perfect for Courtroom Audio

- **Speech Preservation** - Maintains voice quality
- **Legal Compliance** - Keeps data in Canada
- **Batch Processing** - Handle multiple files efficiently
- **Quality Control** - Detailed logging and progress tracking

## 📊 Supported Audio Formats

- **WAV** - Uncompressed audio
- **MP3** - Compressed audio
- **M4A** - Apple audio format
- **FLAC** - Lossless compression
- **AAC** - Advanced audio coding
- **OGG** - Open source format

## 🔧 Technical Details

### Processing Pipeline

1. **Load Audio** - Read file with original sample rate
2. **Noise Analysis** - AI identifies noise patterns
3. **Spectral Reduction** - Remove noise while preserving speech
4. **Normalization** - Adjust levels to prevent clipping
5. **Save Output** - Write cleaned audio with `cleaned_` prefix

### Performance

- **Processing Speed**: ~2-5x real-time (depends on file length)
- **Memory Usage**: ~100-200MB per file
- **CPU Usage**: Moderate (uses all available cores)

## 🛠️ Troubleshooting

### Common Issues

**"No audio files found"**

```bash
# Make sure you have audio files in the input directory
ls rawAudio/
```

**"Module not found" errors**

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**"Permission denied" errors**

```bash
# Make sure you have write permissions to the output directory
chmod 755 cleanAudio/
```

### Log Files

- **audio_processing.log** - Detailed processing log
- **Console output** - Real-time progress and status

## 🆚 Comparison with Other Tools

| Feature         | This Tool            | Krisp          | NoiseTorch    |
| --------------- | -------------------- | -------------- | ------------- |
| **Cost**        | ✅ Free              | ❌ Paid        | ✅ Free       |
| **Platform**    | ✅ Windows/Mac/Linux | ✅ Web/Desktop | ❌ Linux only |
| **Privacy**     | ✅ 100% Local        | ❌ Cloud-based | ✅ 100% Local |
| **Ease of Use** | ✅ Simple            | ✅ Easy        | ⚠️ Complex    |
| **Quality**     | ✅ Good              | ✅ Excellent   | ✅ Good       |

## 🎉 Example Output

```
🎧 Courtroom Audio Processor initialized
📁 Input directory: rawAudio
📁 Output directory: cleanAudio
Found 3 audio files to process
🎵 Processing 3 audio file(s):
  - court_session_1.wav
  - witness_testimony.mp3
  - judge_ruling.m4a

Processing audio files: 100%|██████████| 3/3 [00:45<00:00, 15.2s/file]

==================================================
🎉 PROCESSING COMPLETE!
==================================================
📊 Total files processed: 3
✅ Successfully processed: 3
❌ Failed to process: 0
⏱️  Total processing time: 45.67 seconds
📁 Cleaned files saved to: cleanAudio
🎯 Success rate: 100.0%
==================================================
🎉 All files processed successfully!
```

## 🤝 Contributing

This is a simple, focused tool for courtroom audio processing. Feel free to:

- Report bugs
- Suggest improvements
- Add support for additional audio formats

## 📄 License

This project is open source and free to use for any purpose.

