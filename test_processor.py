#!/usr/bin/env python3
"""
Simple test script for the Courtroom Audio Processor.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__} imported successfully")
        print(f"   Device available: {torch.device('cuda' if torch.cuda.is_available() else 'cpu')}")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        import librosa
        print(f"✅ Librosa {librosa.__version__} imported successfully")
    except ImportError as e:
        print(f"❌ Librosa import failed: {e}")
        return False
    
    try:
        import soundfile as sf
        print(f"✅ Soundfile imported successfully")
    except ImportError as e:
        print(f"❌ Soundfile import failed: {e}")
        return False
    
    try:
        from noisereduce.torchgate import TorchGate
        print("✅ Noisereduce TorchGate imported successfully")
    except ImportError as e:
        print(f"❌ Noisereduce import failed: {e}")
        return False
    
    try:
        from src.audio.processor import AudioProcessor
        print("✅ AudioProcessor imported successfully")
    except ImportError as e:
        print(f"❌ AudioProcessor import failed: {e}")
        return False
    
    return True

def test_processor():
    """Test the audio processor initialization."""
    print("\n🧪 Testing processor initialization...")
    
    try:
        from src.audio.processor import AudioProcessor
        processor = AudioProcessor()
        print("✅ AudioProcessor initialized successfully")
        return True
    except Exception as e:
        print(f"❌ AudioProcessor initialization failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🎧 Courtroom Audio Processor - Test Suite")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please install dependencies:")
        print("   pip install -r requirements.txt")
        return False
    
    # Test processor
    if not test_processor():
        print("\n❌ Processor test failed.")
        return False
    
    print("\n🎉 All tests passed! Your audio processor is ready to use.")
    print("\n📝 Next steps:")
    print("   1. Add audio files to the 'rawAudio' folder")
    print("   2. Run: python run_processor.py")
    print("   3. Find cleaned files in the 'cleanAudio' folder")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

