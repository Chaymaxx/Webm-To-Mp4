# WebM to MP4 Converter

## 📝 Overview

**WebM to MP4 Converter** is an elegant, cross-platform desktop application that allows you to easily convert WebM video files to the widely supported MP4 format. Built with Python and Tkinter, it provides a seamless conversion experience with a clean, intuitive interface.

WebM files are commonly found when downloading videos from certain websites or when working with specific video editing tools. However, MP4 is more universally compatible with media players, editing software, and mobile devices. This converter bridges that gap with just a few clicks.

## ✨ Features

- **Simple, Intuitive Interface**: Clean design that's easy to navigate
- **Batch Conversion**: Convert multiple WebM files simultaneously
- **Custom Output Location**: Choose where your MP4 files will be saved
- **Progress Tracking**: Real-time progress bar and status updates
- **High-Quality Conversion**: Preserves video and audio quality
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **FFmpeg Integration**: Leverages the power of FFmpeg for reliable conversions
- **Error Handling**: Comprehensive error reporting and recovery
- **Free and Open Source**: Available for anyone to use and modify


## 🚀 Quick Start Guide

### Option 1: Run the Python Script

If you're comfortable with Python, you can run the script directly:

1. **Prerequisites**:
   - Python 3.6 or higher
   - Tkinter (usually included with Python)
   - FFmpeg installed and in your PATH

2. **Installation**:
   ```bash
   # Clone or download the repository
   git clone https://github.com/Chaymaxx/webm-to-mp4-converter.git
   
   # Navigate to the directory
   cd webm-to-mp4-converter
   
   # Install FFmpeg if not already installed
   # On Ubuntu/Debian:
   sudo apt install ffmpeg
   
   # On Windows (using chocolatey):
   choco install ffmpeg
   
   # On macOS (using homebrew):
   brew install ffmpeg
   ```

3. **Run the application**:
   ```bash
   python webm_to_mp4.py
   ```

### Option 2: Download and Run the Executable

For users who prefer not to install Python:

#### Windows

1. Download the `WebmToMp4Converter.exe` from the [Releases](https://github.com/Chaymaxx/webm-to-mp4-converter/executable_app) page
2. Double-click the executable to run
3. If Windows SmartScreen appears, click "More info" and then "Run anyway" (The application is safe, but Windows may not recognize the publisher)

#### Linux

1. Download the `WebmToMp4Converter` executable from the [Releases](https://github.com/Chaymaxx/webm-to-mp4-converter/executable_app) page
2. Open a terminal and navigate to the download location
3. Make the file executable:
   ```bash
   chmod +x WebmToMp4Converter
   ```
4. Run the application:
   ```bash
   ./WebmToMp4Converter
   ```

> **Note**: The executable versions already include FFmpeg bundled, so you don't need to install it separately.

## 📋 How to Use

1. **Select Files**: Click the "Select Files" button to choose one or more WebM files
2. **Choose Output Directory**: (Optional) Change where your converted MP4 files will be saved
3. **Convert**: Click the "Convert" button to start the conversion process
4. **Monitor Progress**: Watch the progress bar and status updates
5. **Access Files**: Once complete, your MP4 files will be available in the chosen output directory

## 🔧 Technical Details

The application uses:

- **Python**: Core programming language
- **Tkinter**: For the graphical user interface
- **FFmpeg**: Professional-grade tool for video conversion
- **Threading**: To keep the UI responsive during conversions
- **PyInstaller**: To package the application as standalone executables


## 🔍 Troubleshooting

### Common Issues

1. **"FFmpeg not found" error**:
   - Ensure FFmpeg is installed and added to your system PATH
   - Restart the application after installing FFmpeg

2. **Application doesn't start**:
   - Check you have the necessary permissions to run the executable
   - For Linux/macOS, ensure the file is marked as executable

3. **Conversion fails**:
   - Verify your WebM files aren't corrupted
   - Ensure you have write permissions for the output directory
   - Check you have sufficient disk space


### Command-Line Interface

Advanced users can also run the converter from the command line:

```bash
# Basic usage
python webm_to_mp4.py

# With command line arguments (if implemented)
python webm_to_mp4.py --input video.webm --output converted.mp4
```

### Custom FFmpeg Parameters

If you want to modify the conversion parameters, you can edit the `convert_files` method in the code:

```python
# Find this section in the code
result = subprocess.run(
    [
        "ffmpeg",
        "-i", file_path,
        "-c:v", "libx264",  # Video codec
        "-crf", "23",       # Quality setting (lower = better quality, larger file)
        "-preset", "medium", # Encoding speed preset
        "-c:a", "aac",      # Audio codec
        "-b:a", "128k",     # Audio bitrate
        "-y",              # Overwrite output file if it exists
        output_file
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
```

Made with ❤️ by [Chayma Alabdi]

*Last updated: May 7, 2025*
