#!/usr/bin/env python3
"""
File Organizer

This script automatically organizes files in a directory by sorting them into folders
based on their file extensions.
"""

import os
import shutil
import argparse
import logging
from datetime import datetime
import time
from pathlib import Path


def setup_logger():
    """Set up logging configuration."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"file_organizer_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


class FileOrganizer:
    """Class to organize files based on their extensions."""
    
    # Define the mapping of file types to extensions
    EXTENSION_MAP = {
        "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".tiff", ".webp"],
        "documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
        "videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"],
        "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
        "archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".php", ".rb", ".json", ".xml"],
    }
    
    def __init__(self, directory, logger, create_other_folder=True, recursive=False):
        """Initialize the FileOrganizer class.
        
        Args:
            directory (str): The directory to organize
            logger (Logger): Logger instance
            create_other_folder (bool): Whether to create an 'other' folder for unmatched files
            recursive (bool): Whether to process subdirectories recursively
        """
        self.directory = Path(directory)
        self.logger = logger
        self.create_other_folder = create_other_folder
        self.recursive = recursive
        self.stats = {
            "total_files": 0,
            "moved_files": 0,
            "skipped_files": 0,
            "errors": 0
        }
    
    def get_category_for_extension(self, extension):
        """Determine the category for a given file extension.
        
        Args:
            extension (str): The file extension including the dot
            
        Returns:
            str: The category name, or 'other' if not found
        """
        extension = extension.lower()
        
        for category, extensions in self.EXTENSION_MAP.items():
            if extension in extensions:
                return category
        
        return "other"
    
    def organize(self):
        """Organize the files in the directory."""
        if not self.directory.exists():
            self.logger.error(f"Directory does not exist: {self.directory}")
            return
        
        self.logger.info(f"Starting file organization in: {self.directory}")
        start_time = time.time()
        
        if self.recursive:
            self._organize_recursive(self.directory)
        else:
            self._organize_directory(self.directory)
        
        duration = time.time() - start_time
        self.logger.info(f"File organization completed in {duration:.2f} seconds")
        self.logger.info(f"Total files: {self.stats['total_files']}")
        self.logger.info(f"Moved files: {self.stats['moved_files']}")
        self.logger.info(f"Skipped files: {self.stats['skipped_files']}")
        self.logger.info(f"Errors: {self.stats['errors']}")
    
    def _organize_recursive(self, directory):
        """Recursively organize files in the directory and its subdirectories.
        
        Args:
            directory (Path): The directory to organize
        """
        self._organize_directory(directory)
        
        # Process subdirectories
        for item in directory.iterdir():
            if item.is_dir():
                # Skip the category folders we're creating
                if item.name not in list(self.EXTENSION_MAP.keys()) + ["other"]:
                    self._organize_recursive(item)
    
    def _organize_directory(self, directory):
        """Organize files in a specific directory.
        
        Args:
            directory (Path): The directory to organize
        """
        self.logger.info(f"Processing directory: {directory}")
        
        for item in directory.iterdir():
            # Skip directories and hidden files
            if item.is_dir() or item.name.startswith('.'):
                continue
                
            self.stats["total_files"] += 1
            
            try:
                # Get the file extension and category
                extension = item.suffix
                category = self.get_category_for_extension(extension)
                
                # Skip if category is 'other' and we don't want to create that folder
                if category == "other" and not self.create_other_folder:
                    self.logger.info(f"Skipping unknown type file: {item.name}")
                    self.stats["skipped_files"] += 1
                    continue
                
                # Create the category directory if it doesn't exist
                category_dir = directory / category
                category_dir.mkdir(exist_ok=True)
                
                # Create the destination path
                dest_path = category_dir / item.name
                
                # Handle file name conflicts
                if dest_path.exists():
                    base_name = item.stem
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_name = f"{base_name}_{timestamp}{extension}"
                    dest_path = category_dir / new_name
                    self.logger.warning(f"File already exists, renaming to: {new_name}")
                
                # Move the file
                shutil.move(str(item), str(dest_path))
                self.logger.info(f"Moved: {item.name} -> {category}/{dest_path.name}")
                self.stats["moved_files"] += 1
                
            except Exception as e:
                self.logger.error(f"Error processing {item.name}: {str(e)}")
                self.stats["errors"] += 1


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Organize files in a directory based on their types.")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to organize (default: current directory)")
    parser.add_argument("-r", "--recursive", action="store_true", help="Process subdirectories recursively")
    parser.add_argument("--no-other", action="store_true", help="Don't create 'other' folder for unmatched files")
    args = parser.parse_args()
    
    logger = setup_logger()
    
    organizer = FileOrganizer(
        directory=args.directory,
        logger=logger,
        create_other_folder=not args.no_other,
        recursive=args.recursive
    )
    
    organizer.organize()


if __name__ == "__main__":
    main()
