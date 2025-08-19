"""
Audio processing module for courtroom audio cleanup.
Simplified version with AI noise reduction only.
"""

import time
import numpy as np
import torch
import librosa
import soundfile as sf
from pathlib import Path
from typing import Optional, Tuple
from ..utils.logger import get_logger

logger = get_logger(__name__)

class AudioProcessor:
    """
    Simplified audio processor that only applies AI noise reduction.
    """
    
    def __init__(self, force_cpu: bool = False):
        """
        Initialize the audio processor.
        
        Args:
            force_cpu: Force CPU processing even if GPU is available
        """
        self.device = torch.device('cpu') if force_cpu else torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {self.device}")
    
    def load_audio(self, file_path: Path) -> Tuple[np.ndarray, int]:
        """
        Load audio file using librosa.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        try:
            logger.debug(f"Loading audio file: {file_path}")
            audio, sample_rate = librosa.load(str(file_path), sr=None)
            logger.debug(f"Loaded audio: {len(audio)} samples at {sample_rate}Hz")
            return audio, sample_rate
        except Exception as e:
            logger.error(f"Error loading audio file {file_path}: {e}")
            raise
    

    
    def apply_noise_reduction(self, audio: np.ndarray, sample_rate: int, 
                            strength: float = 0.5) -> np.ndarray:
        """
        Apply AI-powered noise reduction using PyTorch TorchGate.
        SINGLE PASS: Conservative settings for stability and speed.
        
        Args:
            audio: Audio data as numpy array
            sample_rate: Sample rate of the audio
            strength: Noise reduction strength (0.0 to 1.0)
            
        Returns:
            Processed audio data
        """
        try:
            # Import here to avoid issues if torch is not available
            from noisereduce.torchgate import TorchGate
            
            # Convert to torch tensor - ensure array is contiguous to avoid stride issues
            audio_tensor = torch.tensor(audio.copy(), dtype=torch.float32, device=self.device)
            
            # Add batch dimension if needed
            if audio_tensor.dim() == 1:
                audio_tensor = audio_tensor.unsqueeze(0)
            
            # Import configuration settings
            from ..config.settings import TORCHGATE_SETTINGS
            
            # Single TorchGate pass with conservative settings
            logger.debug("Applying single-pass TorchGate noise reduction")
            tg = TorchGate(
                sr=sample_rate,
                nonstationary=TORCHGATE_SETTINGS.get("nonstationary", False),
                n_std_thresh_stationary=TORCHGATE_SETTINGS.get("n_std_thresh_stationary", 1.5),
                n_thresh_nonstationary=TORCHGATE_SETTINGS.get("n_thresh_nonstationary", 1.3),
                temp_coeff_nonstationary=TORCHGATE_SETTINGS.get("temp_coeff_nonstationary", 0.1),
                n_movemean_nonstationary=TORCHGATE_SETTINGS.get("n_movemean_nonstationary", 20),
                freq_mask_smooth_hz=TORCHGATE_SETTINGS.get("freq_mask_smooth_hz", 500),
                time_mask_smooth_ms=TORCHGATE_SETTINGS.get("time_mask_smooth_ms", 50),
                prop_decrease=TORCHGATE_SETTINGS.get("prop_decrease", 0.02)
            ).to(self.device)
            
            # Apply noise reduction
            enhanced_audio = tg(audio_tensor)
            
            # Convert back to numpy and remove batch dimension
            if enhanced_audio.dim() > 1:
                enhanced_audio = enhanced_audio.squeeze(0)
            
            cleaned_audio = enhanced_audio.cpu().numpy()
            
            # Validate the output - check for infinite or NaN values
            from ..config.settings import VALIDATE_AUDIO_OUTPUT
            
            if VALIDATE_AUDIO_OUTPUT and not np.isfinite(cleaned_audio).all():
                logger.warning("TorchGate produced invalid values, using fallback processing")
                return self._apply_fallback_noise_reduction(audio, sample_rate, strength)
            
            logger.debug("Single-pass noise reduction completed")
            return cleaned_audio
            
        except Exception as e:
            logger.error(f"Error applying noise reduction: {e}")
            logger.info("Falling back to alternative noise reduction method")
            return self._apply_fallback_noise_reduction(audio, sample_rate, strength)
    
    def _apply_fallback_noise_reduction(self, audio: np.ndarray, sample_rate: int, 
                                      strength: float = 0.5) -> np.ndarray:
        """
        Fallback noise reduction using traditional spectral gating.
        
        Args:
            audio: Audio data as numpy array
            sample_rate: Sample rate of the audio
            strength: Noise reduction strength (0.0 to 1.0)
            
        Returns:
            Cleaned audio data
        """
        try:
            logger.debug("Applying fallback noise reduction")
            
            # Use traditional noisereduce with spectral gating
            import noisereduce as nr
            
            # Import configuration settings
            from ..config.settings import SPECTRAL_SETTINGS
            
            # Apply noise reduction with configured parameters - ensure array is contiguous
            cleaned_audio = nr.reduce_noise(
                y=audio.copy(), 
                sr=sample_rate,
                stationary=SPECTRAL_SETTINGS.get("stationary", True),
                prop_decrease=SPECTRAL_SETTINGS.get("prop_decrease", strength),
                n_fft=SPECTRAL_SETTINGS.get("n_fft", 2048),
                win_length=SPECTRAL_SETTINGS.get("win_length", 2048),
                hop_length=SPECTRAL_SETTINGS.get("hop_length", 512)
            )
            
            # Validate output
            from ..config.settings import VALIDATE_AUDIO_OUTPUT
            
            if VALIDATE_AUDIO_OUTPUT and not np.isfinite(cleaned_audio).all():
                logger.warning("Fallback noise reduction also produced invalid values, returning original audio")
                return audio
            
            logger.debug("Fallback noise reduction completed")
            return cleaned_audio
            
        except Exception as e:
            logger.error(f"Error in fallback noise reduction: {e}")
            return audio
    
    def normalize_audio(self, audio: np.ndarray) -> np.ndarray:
        """
        Normalize audio to prevent clipping.
        
        Args:
            audio: Audio data as numpy array
            
        Returns:
            Normalized audio data
        """
        from ..config.settings import ENABLE_NORMALIZATION, VALIDATE_AUDIO_OUTPUT
        
        # Skip normalization if disabled
        if not ENABLE_NORMALIZATION:
            logger.debug("Normalization disabled, returning original audio")
            return audio
        
        try:
            logger.debug("Normalizing audio")
            
            # Check for invalid values before normalization
            if VALIDATE_AUDIO_OUTPUT and not np.isfinite(audio).all():
                logger.warning("Invalid values detected before normalization, cleaning...")
                audio = np.nan_to_num(audio, nan=0.0, posinf=0.0, neginf=0.0)
            
            # Import configuration settings
            from ..config.settings import NORMALIZATION_TARGET_DB, MAX_AUDIO_AMPLITUDE
            
            # Convert target dB to linear scale
            target_amplitude = 10 ** (NORMALIZATION_TARGET_DB / 20)
            
            # Calculate current RMS
            rms = np.sqrt(np.mean(audio ** 2))
            
            if rms > 0:
                # Calculate scaling factor
                scale_factor = target_amplitude / rms
                
                # Check if scaling would cause clipping
                max_current_amplitude = np.max(np.abs(audio))
                if max_current_amplitude * scale_factor > MAX_AUDIO_AMPLITUDE:
                    # Adjust scale factor to prevent clipping
                    safe_scale_factor = MAX_AUDIO_AMPLITUDE / max_current_amplitude
                    scale_factor = min(scale_factor, safe_scale_factor)
                    logger.debug(f"Adjusted scale factor to prevent clipping: {scale_factor:.3f}")
                
                # Apply scaling with maximum amplitude limit
                normalized_audio = audio * scale_factor
                
                # Clip to prevent overflow (safety measure)
                normalized_audio = np.clip(normalized_audio, -MAX_AUDIO_AMPLITUDE, MAX_AUDIO_AMPLITUDE)
                
                logger.debug(f"Normalized audio: RMS {rms:.6f} -> {np.sqrt(np.mean(normalized_audio ** 2)):.6f}")
                return normalized_audio
            else:
                logger.warning("Audio has zero RMS, skipping normalization")
                return audio
                
        except Exception as e:
            logger.error(f"Error normalizing audio: {e}")
            return audio
    
    def apply_frequency_filtering(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """
        Apply frequency-domain filtering for mic isolation.
        Boosts speech frequencies and cuts problematic ranges.
        
        Args:
            audio: Audio data as numpy array
            sample_rate: Sample rate of the audio
            
        Returns:
            Frequency-filtered audio data
        """
        from ..config.settings import (
            ENABLE_FREQUENCY_FILTERING, FREQ_LOW_CUTOFF, FREQ_HIGH_CUTOFF,
            FREQ_SPEECH_BOOST_LOW, FREQ_SPEECH_BOOST_HIGH, FREQ_SPEECH_BOOST_AMOUNT
        )
        
        if not ENABLE_FREQUENCY_FILTERING:
            return audio
            
        try:
            logger.debug("Applying frequency filtering for mic isolation")
            
            # Import librosa for frequency domain processing
            import librosa
            
            # Convert to frequency domain
            stft = librosa.stft(audio, n_fft=2048, hop_length=512, win_length=2048)
            
            # Get frequency bins
            freqs = librosa.fft_frequencies(sr=sample_rate, n_fft=2048)
            
            # Create frequency mask
            freq_mask = np.ones_like(stft)
            
            # Low frequency cutoff (remove rumble, HVAC)
            low_cutoff_mask = freqs > FREQ_LOW_CUTOFF
            freq_mask[:, :] *= low_cutoff_mask[:, np.newaxis]
            
            # High frequency cutoff (remove hiss, high-frequency bleed)
            high_cutoff_mask = freqs < FREQ_HIGH_CUTOFF
            freq_mask[:, :] *= high_cutoff_mask[:, np.newaxis]
            
            # Speech frequency boost
            speech_mask = (freqs >= FREQ_SPEECH_BOOST_LOW) & (freqs <= FREQ_SPEECH_BOOST_HIGH)
            boost_factor = 10 ** (FREQ_SPEECH_BOOST_AMOUNT / 20)  # Convert dB to linear
            freq_mask[speech_mask, :] *= boost_factor
            
            # Apply frequency mask
            filtered_stft = stft * freq_mask
            
            # Convert back to time domain
            filtered_audio = librosa.istft(filtered_stft, hop_length=512, win_length=2048)
            
            # Ensure same length as original
            if len(filtered_audio) > len(audio):
                filtered_audio = filtered_audio[:len(audio)]
            elif len(filtered_audio) < len(audio):
                filtered_audio = np.pad(filtered_audio, (0, len(audio) - len(filtered_audio)))
            
            logger.debug("Frequency filtering completed")
            return filtered_audio
            
        except Exception as e:
            logger.error(f"Error applying frequency filtering: {e}")
            return audio

    def apply_pre_normalization_gate(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """
        Apply pre-normalization noise gate to remove speech peaks from other mics.
        This prevents normalization from amplifying bleed from other channels.
        
        Args:
            audio: Audio data as numpy array
            sample_rate: Sample rate of the audio
            
        Returns:
            Pre-gated audio data
        """
        from ..config.settings import PRE_GATE_THRESHOLD_DB, PRE_GATE_ATTACK_MS, PRE_GATE_RELEASE_MS
        
        try:
            logger.debug("Applying pre-normalization gate")
            
            # Convert dB threshold to linear scale
            threshold = 10 ** (PRE_GATE_THRESHOLD_DB / 20)
            
            # Convert attack/release times to samples
            attack_samples = int(PRE_GATE_ATTACK_MS * sample_rate / 1000)
            release_samples = int(PRE_GATE_RELEASE_MS * sample_rate / 1000)
            
            # Calculate RMS envelope with smaller window for peak detection
            window_size = min(512, len(audio) // 20)  # Smaller window for peak detection
            rms = np.sqrt(np.convolve(audio ** 2, np.ones(window_size) / window_size, mode='same'))
            
            # Create gate control signal
            gate_control = np.zeros_like(rms)
            
            # Apply attack and release curves
            for i in range(1, len(rms)):
                if rms[i] > threshold:
                    # Signal above threshold - attack
                    if gate_control[i-1] < 1.0:
                        gate_control[i] = min(1.0, gate_control[i-1] + 1.0 / attack_samples)
                    else:
                        gate_control[i] = 1.0
                else:
                    # Signal below threshold - release
                    if gate_control[i-1] > 0.0:
                        gate_control[i] = max(0.0, gate_control[i-1] - 1.0 / release_samples)
                    else:
                        gate_control[i] = 0.0
            
            # Apply gate to audio
            pre_gated_audio = audio * gate_control
            
            logger.debug("Pre-normalization gate completed")
            return pre_gated_audio
            
        except Exception as e:
            logger.error(f"Error applying pre-normalization gate: {e}")
            return audio

    def apply_noise_gate(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """
        Apply noise gate to remove low-level noise and silence.
        
        Args:
            audio: Audio data as numpy array
            sample_rate: Sample rate of the audio
            
        Returns:
            Gated audio data
        """
        from ..config.settings import ENABLE_NOISE_GATE, NOISE_GATE_THRESHOLD_DB, NOISE_GATE_ATTACK_MS, NOISE_GATE_RELEASE_MS
        
        # Skip noise gate if disabled
        if not ENABLE_NOISE_GATE:
            logger.debug("Noise gate disabled, returning original audio")
            return audio
        
        try:
            logger.debug("Applying noise gate")
            
            # Convert dB threshold to linear scale
            threshold = 10 ** (NOISE_GATE_THRESHOLD_DB / 20)
            
            # Convert attack/release times to samples
            attack_samples = int(NOISE_GATE_ATTACK_MS * sample_rate / 1000)
            release_samples = int(NOISE_GATE_RELEASE_MS * sample_rate / 1000)
            
            # Calculate RMS envelope
            window_size = min(1024, len(audio) // 10)  # Adaptive window size
            rms = np.sqrt(np.convolve(audio ** 2, np.ones(window_size) / window_size, mode='same'))
            
            # Create gate control signal
            gate_control = np.zeros_like(rms)
            
            # Apply attack and release curves
            for i in range(1, len(rms)):
                if rms[i] > threshold:
                    # Signal above threshold - attack
                    if gate_control[i-1] < 1.0:
                        gate_control[i] = min(1.0, gate_control[i-1] + 1.0 / attack_samples)
                    else:
                        gate_control[i] = 1.0
                else:
                    # Signal below threshold - release
                    if gate_control[i-1] > 0.0:
                        gate_control[i] = max(0.0, gate_control[i-1] - 1.0 / release_samples)
                    else:
                        gate_control[i] = 0.0
            
            # Apply gate to audio
            gated_audio = audio * gate_control
            
            logger.debug("Noise gate completed")
            return gated_audio
            
        except Exception as e:
            logger.error(f"Error applying noise gate: {e}")
            return audio
    
    def save_audio(self, audio: np.ndarray, sample_rate: int, 
                  output_path: Path) -> None:
        """
        Save processed audio to file.
        
        Args:
            audio: Audio data to save
            sample_rate: Sample rate of the audio
            output_path: Path where to save the file
        """
        try:
            logger.debug(f"Saving audio to: {output_path}")
            sf.write(str(output_path), audio, sample_rate)
            logger.debug("Audio saved successfully")
        except Exception as e:
            logger.error(f"Error saving audio to {output_path}: {e}")
            raise
    
    def process_audio_file(self, input_file: Path, output_file: Path, 
                          noise_reduction_strength: float = 0.5) -> bool:
        """
        Process a single audio file with noise reduction.
        
        Args:
            input_file: Path to input audio file
            output_file: Path to output cleaned audio file
            noise_reduction_strength: Strength of noise reduction (0.0 to 1.0)
            
        Returns:
            True if successful, False otherwise
        """
        start_time = time.time()
        
        try:
            logger.info(f"Processing: {input_file.name}")
            
            # STEP 1: Load and prepare audio
            audio, sample_rate = self.load_audio(input_file)
            
            # STEP 2: Initial normalization (brings levels up for better processing)
            normalized_audio = self.normalize_audio(audio)
            
            # STEP 3: Main noise gate (removes background noise)
            from ..config.settings import ENABLE_NOISE_GATE
            if ENABLE_NOISE_GATE:
                gated_audio = self.apply_noise_gate(normalized_audio, sample_rate)
            else:
                gated_audio = normalized_audio
            
            # STEP 4: Single TorchGate pass (conservative processing)
            processed_audio = self.apply_noise_reduction(gated_audio, sample_rate, noise_reduction_strength)
            
            # STEP 5: Sample rate conversion (if needed)
            from ..config.settings import OUTPUT_SAMPLE_RATE
            if OUTPUT_SAMPLE_RATE is not None and OUTPUT_SAMPLE_RATE != sample_rate:
                final_audio = self.convert_sample_rate(processed_audio, sample_rate, OUTPUT_SAMPLE_RATE)
                sample_rate = OUTPUT_SAMPLE_RATE
            else:
                final_audio = processed_audio
            
            # STEP 6: Save processed audio
            self.save_audio(final_audio, sample_rate, output_file)
            
            processing_time = time.time() - start_time
            logger.info(f"Completed: {output_file.name} ({processing_time:.2f}s)")
            
            return True
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"❌ Error processing {input_file.name}: {str(e)}")
            return False
    
    def get_audio_duration(self, file_path: Path) -> Optional[float]:
        """
        Get the duration of an audio file in seconds.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Duration in seconds, or None if error
        """
        try:
            audio, sample_rate = self.load_audio(file_path)
            duration = len(audio) / sample_rate
            return duration
        except Exception as e:
            logger.error(f"Error getting duration for {file_path}: {e}")
            return None
