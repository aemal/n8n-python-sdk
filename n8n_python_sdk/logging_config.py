"""
n8n Python SDK - Logging Configuration

This module provides logging configuration utilities for the n8n Python SDK.
It allows users to easily configure logging levels, formats, and output destinations.
"""

import logging
import logging.handlers
import sys
from typing import Optional, Union, TextIO
from pathlib import Path


def configure_logging(
    level: Union[int, str] = logging.INFO,
    format_string: Optional[str] = None,
    output: Union[str, TextIO, None] = None,
    enable_file_logging: bool = False,
    log_file_path: Optional[str] = None,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Configure logging for the n8n Python SDK.
    
    Args:
        level: The logging level to use. Can be an integer (e.g., logging.DEBUG)
               or a string (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        format_string: Custom format string for log messages. If None, uses default format
        output: Output destination. Can be:
                - None: Output to console (sys.stdout)
                - 'stderr': Output to sys.stderr
                - File path as string: Output to file
                - TextIO object: Output to custom stream
        enable_file_logging: Whether to enable additional file logging
        log_file_path: Path for the log file (if enable_file_logging is True)
        max_file_size: Maximum size of log file before rotation (bytes)
        backup_count: Number of backup files to keep during rotation
        
    Returns:
        Configured logger instance for the SDK
        
    Examples:
        >>> # Basic console logging
        >>> logger = configure_logging(level='DEBUG')
        
        >>> # Log to file with rotation
        >>> logger = configure_logging(
        ...     level=logging.INFO,
        ...     enable_file_logging=True,
        ...     log_file_path='n8n_sdk.log'
        ... )
        
        >>> # Custom format and output
        >>> logger = configure_logging(
        ...     level='WARNING',
        ...     format_string='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        ...     output='stderr'
        ... )
    """
    # Get the root SDK logger
    sdk_logger = logging.getLogger('n8n_sdk')
    
    # Clear any existing handlers to avoid duplicates
    for handler in sdk_logger.handlers[:]:
        sdk_logger.removeHandler(handler)
    
    # Convert string level to logging constant
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    
    sdk_logger.setLevel(level)
    
    # Set default format if none provided
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    formatter = logging.Formatter(format_string)
    
    # Configure console handler
    if output is None or output == 'stdout':
        console_handler = logging.StreamHandler(sys.stdout)
    elif output == 'stderr':
        console_handler = logging.StreamHandler(sys.stderr)
    elif isinstance(output, str):
        # Output is a file path
        console_handler = logging.FileHandler(output, encoding='utf-8')
    else:
        # Output is a TextIO object
        console_handler = logging.StreamHandler(output)
    
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    sdk_logger.addHandler(console_handler)
    
    # Configure file logging if enabled
    if enable_file_logging:
        if log_file_path is None:
            log_file_path = 'n8n_sdk.log'
        
        # Create directory if it doesn't exist
        log_path = Path(log_file_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use rotating file handler to manage log file size
        file_handler = logging.handlers.RotatingFileHandler(
            log_file_path,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        sdk_logger.addHandler(file_handler)
    
    # Log the configuration
    sdk_logger.info(f"Logging configured - Level: {logging.getLevelName(level)}, "
                   f"Console: {type(console_handler).__name__}, "
                   f"File: {'Enabled' if enable_file_logging else 'Disabled'}")
    
    return sdk_logger


def get_logger(name: str = 'n8n_sdk') -> logging.Logger:
    """
    Get a logger instance for the SDK.
    
    Args:
        name: Name of the logger. Should start with 'n8n_sdk' to inherit configuration
        
    Returns:
        Logger instance
        
    Example:
        >>> logger = get_logger('n8n_sdk.workflow')
        >>> logger.info('Workflow created successfully')
    """
    return logging.getLogger(name)


def set_log_level(level: Union[int, str]) -> None:
    """
    Change the logging level for all SDK loggers.
    
    Args:
        level: New logging level (integer or string)
        
    Example:
        >>> set_log_level('DEBUG')  # Enable debug logging
        >>> set_log_level(logging.WARNING)  # Only show warnings and errors
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    
    sdk_logger = logging.getLogger('n8n_sdk')
    sdk_logger.setLevel(level)
    
    # Update all handlers
    for handler in sdk_logger.handlers:
        handler.setLevel(level)
    
    sdk_logger.info(f"Log level changed to: {logging.getLevelName(level)}")


def disable_logging() -> None:
    """
    Disable all SDK logging by setting level to CRITICAL+1.
    
    This effectively disables all log output from the SDK.
    
    Example:
        >>> disable_logging()  # No more log messages
    """
    sdk_logger = logging.getLogger('n8n_sdk')
    sdk_logger.setLevel(logging.CRITICAL + 1)


def enable_debug_logging() -> None:
    """
    Enable debug logging for troubleshooting.
    
    This is a convenience function to quickly enable verbose logging.
    
    Example:
        >>> enable_debug_logging()  # Show all debug messages
    """
    set_log_level(logging.DEBUG)


# Pre-configure basic logging when module is imported
# This ensures there's always some logging available even if configure_logging isn't called
_default_configured = False

def _ensure_default_logging():
    """Ensure basic logging is configured if configure_logging hasn't been called."""
    global _default_configured
    if not _default_configured:
        # Only add handler if none exist
        sdk_logger = logging.getLogger('n8n_sdk')
        if not sdk_logger.handlers:
            configure_logging(level=logging.WARNING)  # Default to WARNING level
        _default_configured = True

# Configure default logging on import
_ensure_default_logging()