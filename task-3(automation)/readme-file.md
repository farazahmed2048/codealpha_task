# File Organizer

A Python automation script that organizes files in a directory by sorting them into folders based on their file extensions.

## Features

- Automatically sorts files into categorized folders (images, documents, videos, etc.)
- Handles file name conflicts with timestamp-based renaming
- Provides detailed logging of operations
- Offers recursive directory processing option
- Generates statistics after completion

## Installation

1. Clone this repository:
```bash
git clone https://github.com/your-username/file-organizer.git
cd file-organizer
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the script with a directory path to organize:

```bash
python file_organizer.py /path/to/directory
```

If no directory is specified, it will organize the current directory:

```bash
python file_organizer.py
```

### Command Line Options

- `-r, --recursive`: Process subdirectories recursively
- `--no-other`: Don't create an 'other' folder for unmatched files

### Examples

Organize the Downloads folder:
```bash
python file_organizer.py ~/Downloads
```

Organize the current directory and all subdirectories:
```bash
python file_organizer.py -r
```

## File Categories

The script organizes files into the following categories:

- **images**: .jpg, .jpeg, .png, .gif, .bmp, .svg, .tiff, .webp
- **documents**: .pdf, .doc, .docx, .txt, .rtf, .odt, .xls, .xlsx, .ppt, .pptx
- **videos**: .mp4, .mov, .avi, .mkv, .wmv, .flv, .webm
- **audio**: .mp3, .wav, .flac, .aac, .ogg, .m4a
- **archives**: .zip, .rar, .7z, .tar, .gz, .bz2
- **code**: .py, .js, .html, .css, .java, .cpp, .c, .h, .php, .rb, .json, .xml
- **other**: Any file extension not in the above categories

## Logs

Logs are saved in the `logs` directory with timestamps. Each log file contains details about:
- Files moved
- Files skipped
- Any errors encountered
- Execution time and statistics

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
