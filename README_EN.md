# BiliVagent-tool

[中文](README.md) | English

Intelligent Bilibili Video Analysis Tool based on Python and LangChain

## Documentation

- 📖 [Quick Start](docs/QUICKSTART.md)
- 🏗️ [Architecture](docs/ARCHITECTURE.md)
- 🤝 [Contributing Guide](CONTRIBUTING_EN.md)
- 📝 [Changelog](CHANGELOG.md)

## Introduction

BiliVagent is an intelligent tool for analyzing Bilibili videos, powered by Large Language Models from SiliconFlow API. It can automatically complete tasks such as video download, content analysis, comment analysis, and ultimately generate detailed video analysis reports.

## Features

### Complete Analysis Pipeline

1. **Video Parsing and Download**
   - Support BV number and video link parsing
   - Automatic video file download
   - Retrieve video metadata (title, category, tags, etc.)

2. **Comment and Danmaku Crawling**
   - Crawl video comments
   - Crawl danmaku content
   - Text desensitization processing

3. **Video Content Analysis**
   - Audio extraction
   - Speech recognition (using Vosk library)
   - Generate content summary
   - Extract keywords

4. **Visual Analysis**
   - Randomly extract 3 video frames
   - Analyze video style using Qwen3-VL multimodal model

5. **Text Analysis**
   - Keyword extraction
   - Sentiment analysis
   - Generate discussion summary

### Generated Analysis Report Contains

- BV Number
- Video Title
- Summary
- Keywords (Top 10)
- Video Style
- Discussion Sentiment
- Discussion Keywords
- Related Discussions

## GUI Interface

The project now includes a user-friendly GUI interface built with Tkinter, providing:

- **Visual Input**: Easy input of video links or BV numbers
- **Real-time Progress**: View analysis progress in real-time
- **Multi-tab Display**: Separate tabs for logs and reports
- **Report Export**: Save analysis reports as JSON or text files
- **Status Indicators**: Clear visual feedback on analysis status

### Using the GUI

```bash
python gui.py
```

The GUI provides:
- 📋 **Run Log Tab**: Real-time analysis process logs
- 📊 **Analysis Report Tab**: Formatted analysis results
- 💾 **Save Function**: Export reports to files
- 🗑 **Clear Function**: Clear logs for new analysis

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/HeDaas-Code/BiliVagent-tool.git
cd BiliVagent-tool
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install yt-dlp (for video download)

```bash
pip install yt-dlp
```

Or install using system package manager:

```bash
# Ubuntu/Debian
sudo apt install yt-dlp

# macOS
brew install yt-dlp
```

### 4. Download Vosk Speech Recognition Model (Optional)

If you need speech recognition functionality, download the Chinese model:

```bash
# Create model directory
mkdir -p models

# Download and extract model
wget https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip
unzip vosk-model-cn-0.22.zip -d models/
```

More models available at [Vosk Models](https://alphacephei.com/vosk/models).

## Configuration

### 1. Create Configuration File

```bash
cp .env.example .env
```

### 2. Edit .env File

```bash
# SiliconFlow API Configuration
SILICONFLOW_API_KEY=your_api_key_here
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1

# Model Configuration
LLM_MODEL=Qwen/Qwen2.5-32B-Instruct
VLM_MODEL=Qwen/Qwen2-VL-7B-Instruct

# Vosk Model Path
VOSK_MODEL_PATH=./models/vosk-model-cn-0.22

# Output Configuration
OUTPUT_DIR=./output
TEMP_DIR=./temp
```

**Important:** Register at [SiliconFlow](https://siliconflow.cn) and obtain an API Key.

## Usage

### Command Line Interface

#### Basic Usage

```bash
# Using BV number
python main.py BV1xx411c7mD

# Using full URL
python main.py https://www.bilibili.com/video/BV1xx411c7mD
```

#### Command Line Arguments

```bash
python main.py [-h] [-o OUTPUT] [--no-download] video

Positional arguments:
  video                 Bilibili video link or BV number

Optional arguments:
  -h, --help            Show help message
  -o OUTPUT, --output OUTPUT
                        Output directory (default: ./output)
  --no-download         Skip video download (analyze only comments and danmaku)
```

### GUI Interface

Launch the graphical interface:

```bash
python gui.py
```

Features:
1. Enter video URL or BV number in the input field
2. Click "🔍 Start Analysis" button
3. View real-time progress in the log tab
4. Check formatted report in the report tab
5. Save report using "💾 Save Report" button

### Example Output

```
============================================================
BiliVagent - Bilibili Video Analysis
============================================================

[1/8] Parsing BV number...
BV Number: BV1xx411c7mD

[2/8] Fetching video information...
Title: Example Video Title
Category: Technology

[3/8] Downloading video...
Video saved to: ./temp/BV1xx411c7mD.mp4

[4/8] Processing video content...
Extracting audio from video...
Transcribing audio to text...
Generating summary from transcription...
Extracting video frames...
Analyzing video style...

[5/8] Fetching comments...
Fetched 100 comments

[6/8] Fetching danmaku...
Fetched 523 danmaku

[7/8] Processing text content (comments and danmaku)...
Desensitizing text content...
Extracting keywords from comments and danmaku...
Analyzing sentiment...
Generating discussion summary...

[8/8] Generating final report...

✓ Report saved to: ./output/BV1xx411c7mD_report.json

============================================================
Analysis Report
============================================================

BV Number: BV1xx411c7mD
Video Title: Example Video Title

Summary:
This is a video about...

Keywords (Top 10):
  1. Keyword1
  2. Keyword2
  ...

Video Style: High quality, vibrant colors, professional composition

Discussion Sentiment: Positive

Discussion Keywords:
  1. Discussion keyword1
  2. Discussion keyword2
  ...

Related Discussions:
Viewers mainly discuss...

Metadata:
  Category: Technology
  Uploader: Uploader Name
  Comments: 100
  Danmaku: 523
============================================================

✓ Analysis completed!
```

## Technical Architecture

### Core Technology Stack

- **Python 3.8+**: Main programming language
- **LangChain**: Agent framework
- **SiliconFlow API**: Large language model service
  - Qwen3-32B: Text analysis model
  - Qwen3-VL: Visual multimodal model
- **Vosk**: Speech recognition library
- **MoviePy**: Video and audio processing
- **OpenCV**: Video frame extraction
- **jieba**: Chinese word segmentation and keyword extraction
- **bilibili-api-python**: Bilibili API interface
- **yt-dlp**: Video download tool
- **Tkinter**: GUI framework

### Project Structure

```
BiliVagent-tool/
├── bilivagent/              # Main package
│   ├── __init__.py
│   ├── config.py            # Configuration management
│   ├── agents/              # Agent implementation
│   │   ├── __init__.py
│   │   └── bilivagent.py    # Main Agent
│   ├── processors/          # Content processors
│   │   ├── __init__.py
│   │   ├── video_content.py # Video content processing
│   │   └── text_content.py  # Text content processing
│   └── utils/               # Utility modules
│       ├── __init__.py
│       ├── bilibili.py      # Bilibili API wrapper
│       ├── video.py         # Video processing
│       ├── audio.py         # Audio processing
│       ├── text.py          # Text processing
│       └── siliconflow.py   # SiliconFlow API client
├── models/                  # Model files directory
├── output/                  # Output directory
├── temp/                    # Temporary files directory
├── main.py                  # CLI entry point
├── gui.py                   # GUI entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Configuration file example
├── README.md               # Chinese documentation
└── README_EN.md            # English documentation
```

## Workflow

```
Bilibili Video Link
    ↓
Parse BV Number
    ↓
Fetch Video Info (Title, Category, Tags)
    ↓
Video Download ──→ Comment Crawling ──→ Danmaku Crawling
    ↓                  ↓                     ↓
Audio Extraction   Desensitization      Desensitization
    ↓                  ↓                     ↓
Speech Recognition Text Merge ←─────────────┘
    ↓                  ↓
Summary Generation Keyword Extraction
    ↓                  ↓
Keyword Cloud      Sentiment Analysis
    ↓                  ↓
Frame Extraction   Discussion Analysis
    ↓                  ↓
Style Analysis ←───────┴────┘
    ↓
Generate Final Report
```

## API Reference

### SiliconFlow API

This project uses API services provided by SiliconFlow:

- **API Documentation**: https://docs.siliconflow.cn/
- **Model List**: https://docs.siliconflow.cn/llms-full.txt
- **Registration**: https://siliconflow.cn

### Models Used

1. **Qwen/Qwen2.5-32B-Instruct**: For text analysis, summary generation, keyword extraction
2. **Qwen/Qwen2-VL-7B-Instruct**: For video frame analysis and style recognition

## Important Notes

1. **API Key**: Must configure a valid SiliconFlow API Key before use
2. **Network Environment**: Requires access to Bilibili and SiliconFlow API
3. **Vosk Model**: Speech recognition requires downloading the Vosk model
4. **Video Download**: Requires installation of yt-dlp tool
5. **Storage Space**: Video download and processing require sufficient disk space
6. **Processing Time**: Complete analysis of a video may take several minutes

## Troubleshooting

### Q: How to obtain SiliconFlow API Key?

A: Visit https://siliconflow.cn to register an account, and create an API Key in the console.

### Q: Video download fails?

A: Ensure yt-dlp is installed and check network connection. Some videos may have regional restrictions.

### Q: Speech recognition doesn't work?

A: Confirm that the Vosk model has been downloaded and VOSK_MODEL_PATH is correctly configured.

### Q: Can I batch process multiple videos?

A: The current version doesn't support batch processing. It's recommended to use a script to call in a loop.

### Q: GUI doesn't launch?

A: Ensure Tkinter is installed. On Linux, you may need to install: `sudo apt-get install python3-tk`

### Q: How to change the analysis language?

A: The analysis results language is determined by the LLM model. You can modify prompts in the code to adjust output language.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Issues and Pull Requests are welcome!

Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Acknowledgments

- [SiliconFlow](https://siliconflow.cn) for API services
- [Vosk](https://alphacephei.com/vosk/) speech recognition engine
- [bilibili-api-python](https://github.com/Nemo2011/bilibili-api) Bilibili API library
- [LangChain](https://github.com/langchain-ai/langchain) Agent framework

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.
