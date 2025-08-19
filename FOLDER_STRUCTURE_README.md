# 🎛️ Audio Processing Folder Structure

This project now has a modular folder structure with separate config files for each processing step.

## 📁 Folder Structure

```
courtsaudio/
├── mergeRawToMp3/           # Step 1: Merge raw audio files to MP3
│   └── config.py            # Config for merging raw files
├── processRawMergedMp3/     # Step 2: Process merged MP3 with noise reduction
│   └── config.py            # Config for processing merged files (aggressive settings)
├── processRawMp3/           # Step 3: Process individual raw MP3 files
│   └── config.py            # Config for processing individual files (moderate settings)
├── mergeProcessedMp3/       # Step 4: Merge processed MP3 files to final output
│   └── config.py            # Config for final merging
├── config.py                # Original main config (kept for reference)
└── [other existing files]
```

## 🔄 Processing Workflows

### Workflow 1: Raw → Merged → Processed (Recommended)

1. **mergeRawToMp3**: Combine raw audio channels into single MP3
2. **processRawMergedMp3**: Apply aggressive noise reduction to merged file
   - Uses the aggressive settings that worked well for room hiss removal
   - `NOISE_REDUCTION_STRENGTH = 0.85`
   - `prop_decrease = 0.8`

### Workflow 2: Raw → Processed → Merged (Alternative)

1. **processRawMp3**: Process individual channels with moderate noise reduction
2. **mergeProcessedMp3**: Merge cleaned channels into final output

## 🎯 Config File Details

### mergeRawToMp3/config.py

- **Purpose**: Merge raw audio files into single MP3
- **Input**: `rawAudioGood` or `rawAudioBad`
- **Output**: `mergedAudio`
- **Key Settings**: Merge method, normalization, MP3 quality

### processRawMergedMp3/config.py

- **Purpose**: Apply aggressive noise reduction to merged files
- **Input**: `mergedAudio`
- **Output**: `cleanAudio`
- **Key Settings**:
  - `NOISE_REDUCTION_STRENGTH = 0.85` (aggressive)
  - `prop_decrease = 0.8` (maximum reduction)
  - Noise gate disabled to preserve speech

### processRawMp3/config.py

- **Purpose**: Process individual channels with moderate noise reduction
- **Input**: `rawAudioGood` or `rawAudioBad`
- **Output**: `cleanAudio`
- **Key Settings**:
  - `NOISE_REDUCTION_STRENGTH = 0.4` (moderate)
  - `prop_decrease = 0.3` (balanced reduction)
  - Multi-channel processing enabled

### mergeProcessedMp3/config.py

- **Purpose**: Create final output from processed channels
- **Input**: `cleanAudio`
- **Output**: `finalAudio`
- **Key Settings**: High-quality MP3 output, channel weighting, final enhancement

## 🚀 Usage Instructions

### For Workflow 1 (Recommended):

```bash
# Step 1: Merge raw files
cd mergeRawToMp3
python merge_to_mp3.py

# Step 2: Process merged file with aggressive noise reduction
cd ../processRawMergedMp3
python process_sum.py
```

### For Workflow 2 (Alternative):

```bash
# Step 1: Process individual channels
cd processRawMp3
python run_processor.py

# Step 2: Merge processed channels
cd ../mergeProcessedMp3
python merge_processed.py
```

## ⚙️ Key Differences Between Configs

| Setting             | mergeRawToMp3 | processRawMergedMp3 | processRawMp3  | mergeProcessedMp3 |
| ------------------- | ------------- | ------------------- | -------------- | ----------------- |
| **Noise Reduction** | None          | Aggressive (0.85)   | Moderate (0.4) | None              |
| **prop_decrease**   | N/A           | 0.8 (max)           | 0.3 (balanced) | N/A               |
| **Noise Gate**      | N/A           | Disabled            | Enabled        | N/A               |
| **MP3 Bitrate**     | 192 kbps      | N/A                 | N/A            | 256 kbps          |
| **Multi-channel**   | No            | No                  | Yes            | No                |

## 💡 Tips

1. **Start with Workflow 1** - it's simpler and uses the proven aggressive settings
2. **Adjust noise reduction** in `processRawMergedMp3/config.py` if needed
3. **Each config is self-contained** - modify settings without affecting other steps
4. **Keep the original config.py** for reference and testing

## 🔧 Customization

Each config file can be modified independently:

- **mergeRawToMp3**: Adjust merge method, MP3 quality, normalization
- **processRawMergedMp3**: Fine-tune noise reduction strength and TorchGate settings
- **processRawMp3**: Modify multi-channel processing and individual channel settings
- **mergeProcessedMp3**: Change final output quality and enhancement settings
