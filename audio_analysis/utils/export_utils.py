"""
Export Utilities Module

This module provides shared utilities for export directory handling and other
export-related functionality. It ensures consistent behavior across all
analyzer types and eliminates code duplication.

Key Benefits:
1. Single source of truth for export directory logic
2. Consistent behavior across AudioAnalyzer and ParallelAudioAnalyzer
3. Easy to modify export behavior in one place
4. Centralized export validation and error handling
"""

from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


def create_export_directory(export_dir: Optional[Path] = None, 
                          prefix: str = "audio_analysis") -> Path:
    """
    Create an export directory with timestamped subdirectory.
    
    This function handles the standard export directory creation pattern
    used across all analyzer types. It ensures consistent behavior and
    proper directory structure.
    
    Args:
        export_dir: Base directory for export (None = use current directory)
        prefix: Prefix for the timestamped directory name
        
    Returns:
        Path to the created timestamped export directory
        
    Examples:
        # Default behavior (current directory)
        create_export_directory() -> ./audio_analysis_20241214_143022/
        
        # With custom base directory
        create_export_directory(Path("./reports")) -> ./reports/audio_analysis_20241214_143022/
        
        # With custom prefix
        create_export_directory(Path("./reports"), "parallel_audio_analysis") 
        -> ./reports/parallel_audio_analysis_20241214_143022/
    """
    # Generate timestamp for unique directory names
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if export_dir is None:
        # Default behavior: create timestamped directory in current location
        final_export_dir = Path(f"{prefix}_{timestamp}")
    else:
        # When export_dir is provided, create timestamped subdirectory within it
        export_dir = Path(export_dir)
        export_dir.mkdir(exist_ok=True)  # Ensure parent directory exists
        final_export_dir = export_dir / f"{prefix}_{timestamp}"
    
    # Create the final export directory
    final_export_dir.mkdir(exist_ok=True)
    
    logger.info(f"Created export directory: {final_export_dir}")
    return final_export_dir


def create_export_subdirectories(export_dir: Path) -> Dict[str, Path]:
    """
    Create standard subdirectories within an export directory.
    
    This function creates the standard subdirectory structure used
    for organized export output.
    
    Args:
        export_dir: Base export directory
        
    Returns:
        Dictionary mapping subdirectory names to their paths
    """
    subdirectories = {
        'data': export_dir / "data",
        'images': export_dir / "images", 
        'reports': export_dir / "reports"
    }
    
    # Create all subdirectories
    for name, path in subdirectories.items():
        path.mkdir(exist_ok=True)
        logger.debug(f"Created subdirectory: {path}")
    
    return subdirectories


def validate_export_directory(export_dir: Path) -> bool:
    """
    Validate that an export directory is writable and accessible.
    
    Args:
        export_dir: Directory to validate
        
    Returns:
        True if directory is valid and writable, False otherwise
    """
    try:
        # Check if directory exists
        if not export_dir.exists():
            logger.error(f"Export directory does not exist: {export_dir}")
            return False
        
        # Check if it's actually a directory
        if not export_dir.is_dir():
            logger.error(f"Export path is not a directory: {export_dir}")
            return False
        
        # Test write permissions by creating a temporary file
        test_file = export_dir / ".export_test"
        try:
            test_file.touch()
            test_file.unlink()  # Clean up
        except (PermissionError, OSError) as e:
            logger.error(f"Export directory is not writable: {export_dir} - {e}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error validating export directory {export_dir}: {e}")
        return False


def get_export_summary_info(export_dir: Path, files_analyzed: int, 
                           analysis_stats: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate standardized export summary information.
    
    Args:
        export_dir: Export directory path
        files_analyzed: Number of files analyzed
        analysis_stats: Analysis statistics dictionary
        
    Returns:
        Dictionary with export summary information
    """
    return {
        'export_directory': str(export_dir),
        'export_timestamp': datetime.now().isoformat(),
        'files_analyzed': files_analyzed,
        'analysis_stats': analysis_stats
    }


def cleanup_empty_export_directories(base_dir: Path, max_age_hours: int = 24) -> int:
    """
    Clean up empty or old export directories.
    
    This utility function can be used to clean up failed or incomplete
    export attempts that leave empty directories.
    
    Args:
        base_dir: Base directory to search for export directories
        max_age_hours: Maximum age in hours for directories to keep
        
    Returns:
        Number of directories cleaned up
    """
    if not base_dir.exists():
        return 0
    
    cleaned_count = 0
    cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)
    
    try:
        for item in base_dir.iterdir():
            if item.is_dir() and (item.name.startswith('audio_analysis_') or 
                                 item.name.startswith('parallel_audio_analysis_')):
                # Check if directory is old enough
                if item.stat().st_mtime < cutoff_time:
                    # Check if directory is empty or contains only empty subdirectories
                    if _is_export_directory_empty(item):
                        logger.info(f"Cleaning up empty export directory: {item}")
                        _remove_directory_safely(item)
                        cleaned_count += 1
                        
    except Exception as e:
        logger.error(f"Error during export directory cleanup: {e}")
    
    return cleaned_count


def _is_export_directory_empty(directory: Path) -> bool:
    """
    Check if an export directory is effectively empty.
    
    Args:
        directory: Directory to check
        
    Returns:
        True if directory is empty or contains only empty subdirectories
    """
    try:
        for item in directory.rglob('*'):
            if item.is_file() and item.stat().st_size > 0:
                return False
        return True
    except Exception:
        return False


def _remove_directory_safely(directory: Path) -> None:
    """
    Safely remove a directory and its contents.
    
    Args:
        directory: Directory to remove
    """
    try:
        import shutil
        shutil.rmtree(directory)
    except Exception as e:
        logger.warning(f"Could not remove directory {directory}: {e}")