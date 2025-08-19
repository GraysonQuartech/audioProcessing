# 🎵 Audio Processing Pipeline

A comprehensive Python-based audio processing system designed for merging multi-channel audio files and applying advanced noise reduction and normalization techniques.

## 🚀 Features

- **Multi-Channel Audio Merging**: Combines multiple audio channels into a single file
- **AI-Powered Noise Reduction**: Uses TorchGate for intelligent noise removal
- **Audio Normalization**: Automatic volume leveling to -24dB
- **Batch Processing**: Process multiple files efficiently
- **Flexible Pipeline**: Modular design for easy customization

## 📁 Project Structure

```
courtsaudio/
├── audioFiles/                 # Audio file storage (gitignored)
│   ├── sourceAudio/           # Input audio files
│   ├── mergedAudio/           # Merged audio files
│   └── outputAudio/           # Processed output files
├── audioProcesses/            # Processing modules
│   ├── mergeToMp3/           # Audio merging functionality
│   ├── processMergedMp3/     # Post-merge processing
│   ├── processMp3/           # Individual file processing
│   ├── noisegate.py          # Noise gate implementation
│   ├── normalize.py          # Audio normalization
│   └── torchgate.py          # AI noise reduction
├── scripts/                   # Pipeline orchestration
│   ├── merge_then_process.py # Complete pipeline script
│   └── process_then_merge.py # Alternative pipeline
├── src/                      # Core source code
│   ├── audio/               # Audio processing modules
│   ├── config/              # Configuration management
│   ├── core/                # Core functionality
│   └── utils/               # Utility functions
└── requirements.txt         # Python dependencies
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GraysonQuartech/audioProcessing.git
   cd audioProcessing
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up audio directories**:
   ```bash
   mkdir -p audioFiles/sourceAudio
   mkdir -p audioFiles/mergedAudio
   mkdir -p audioFiles/outputAudio
   ```

## 🎯 Usage

### Quick Start - Complete Pipeline

Run the full audio processing pipeline (merge + process):

```bash
python scripts/merge_then_process.py
```

This will:
1. Merge all audio files from `audioFiles/sourceAudio/`
2. Apply noise reduction and normalization
3. Save the final result to `audioFiles/outputAudio/`

### Individual Processing Steps

#### Merge Audio Files Only
```bash
cd audioProcesses/mergeToMp3
python merge_to_mp3.py
```

#### Process Merged Audio Only
```bash
cd audioProcesses/processMergedMp3
python process_merged_mp3.py
```

#### Process Individual Files
```bash
cd audioProcesses/processMp3
python run_processor.py
```

## ⚙️ Configuration

### Audio Processing Settings

The system uses configuration files in each processing module:

- **Merge Settings**: `audioProcesses/mergeToMp3/config.py`
- **Processing Settings**: `audioProcesses/processMergedMp3/config.py`
- **Individual Processing**: `audioProcesses/processMp3/config.py`

### Key Configuration Options

- **Noise Reduction**: Enable/disable TorchGate AI noise removal
- **Normalization**: Set target dB level (default: -24dB)
- **Audio Quality**: Configure sample rates and bit depths
- **File Formats**: Specify input/output formats

## 📊 Supported Audio Formats

### Input Formats
- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- FLAC (.flac)
- AAC (.aac)
- OGG (.ogg)

### Output Formats
- MP3 (.mp3) - Primary output format
- WAV (.wav) - Available for high-quality output

## 🔧 Advanced Features

### TorchGate AI Noise Reduction
- Uses machine learning for intelligent noise removal
- Configurable sensitivity and processing parameters
- CPU and GPU support

### Audio Normalization
- Automatic volume leveling
- Configurable target levels
- Peak detection and adjustment

### Multi-Channel Support
- Handles 8+ audio channels simultaneously
- Automatic channel synchronization
- Flexible mixing options

## 📝 Logging

The system provides comprehensive logging:
- Processing progress and timing
- File operations and status
- Error reporting and debugging
- Performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation in the `docs/` folder
- Review the configuration guides

## 🔄 Version History

- **v1.0.0**: Initial release with basic merging and processing
- **v1.1.0**: Added TorchGate AI noise reduction
- **v1.2.0**: Enhanced pipeline orchestration and logging

---

**Note**: Audio files in the `audioFiles/` directory are excluded from version control to keep the repository size manageable. Place your audio files in the appropriate subdirectories before running the processing scripts.

