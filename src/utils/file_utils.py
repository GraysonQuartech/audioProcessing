"""
File utility functions for the Courtroom Audio Processor.
"""

import os
from pathlib import Path
from typing import List
import logging

from ..config.settings import SUPPORTED_FORMATS

logger = logging.getLogger(__name__)

def ensure_directory_exists(directory_path: Path) -> None:
    """Create directory if it doesn't exist."""
    directory_path.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {directory_path}")

def get_audio_files(input_directory: Path) -> List[Path]:
    """
    Get all supported audio files from the input directory.
    
    Args:
        input_directory: Path to the input directory
        
    Returns:
        List of Path objects for supported audio files
    """
    audio_files = []
    
    if not input_directory.exists():
        logger.warning(f"Input directory {input_directory} does not exist!")
        return audio_files
    
    for file_path in input_directory.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_FORMATS:
            audio_files.append(file_path)
    
    logger.info(f"Found {len(audio_files)} audio files to process")
    return audio_files

def format_file_size(bytes_size: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        bytes_size: Size in bytes
        
    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    if bytes_size == 0:
        return "0 Bytes"
    
    size_names = ["Bytes", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(bytes_size, 1024)))
    p = math.pow(1024, i)
    s = round(bytes_size / p, 2)
    return f"{s} {size_names[i]}"

def get_file_info(file_path: Path) -> dict:
    """
    Get information about an audio file.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        Dictionary with file information
    """
    try:
        stat = file_path.stat()
        return {
            'name': file_path.name,
            'size': stat.st_size,
            'size_formatted': format_file_size(stat.st_size),
            'extension': file_path.suffix.lower(),
            'path': file_path
        }
    except Exception as e:
        logger.error(f"Error getting file info for {file_path}: {e}")
        return None

def create_output_filename(input_filename: str, prefix: str = "cleaned_") -> str:
    """
    Create output filename with prefix.
    
    Args:
        input_filename: Original filename
        prefix: Prefix to add to filename
        
    Returns:
        New filename with prefix
    """
    return f"{prefix}{input_filename}"

def validate_audio_file(file_path: Path) -> bool:
    """
    Validate that a file is a supported audio file.
    
    Args:
        file_path: Path to the file to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not file_path.exists():
        logger.warning(f"File does not exist: {file_path}")
        return False
    
    if not file_path.is_file():
        logger.warning(f"Path is not a file: {file_path}")
        return False
    
    if file_path.suffix.lower() not in SUPPORTED_FORMATS:
        logger.warning(f"Unsupported file format: {file_path.suffix}")
        return False
    
    return True

