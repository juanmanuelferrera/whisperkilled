# 💀 WHISPER KILLER 🎙️

**Privacy-First Transcription & Translation Tool**

A powerful, user-friendly GUI application for transcribing YouTube videos and local video files using Apple's Speech Recognition, with AI-powered translation and summarization. Built to kill the competition with unmatched privacy and performance.

## ✨ Features

### 📺 YouTube Transcription
- **One-click YouTube processing**: Paste URL, click transcribe
- **Format options**: Plain text or SRT subtitles
- **Audio management**: Keep or auto-delete downloaded audio

### 🎬 Local Video Transcription
- **Drag & drop interface**: Easy file selection
- **Multiple formats**: MP4, MOV, AVI, MKV, WebM support
- **Direct transcription**: No intermediate files needed

### 🌍 Privacy-First Translation
- **Local Translation**: Uses translate-shell for offline translation
- **Paragraph Preservation**: Maintains original text structure and formatting
- **AI Enhancement Only**: OpenRouter used only for titles, emojis & intelligent paragraph analysis
- **10 Languages**: Spanish, French, German, Italian, Portuguese, Japanese, Korean, Chinese, Russian, Arabic
- **Maximum Privacy**: Original content never leaves your Mac for translation

### 🤖 AI Enhancement
- **Smart Titles**: Auto-generated titles with relevant emojis
- **Paragraph Formatting**: Clean, readable text structure
- **AI Summaries**: Concise summaries of transcribed content

### 🔐 Secure API Management
- **Encrypted Storage**: API keys encrypted with machine-specific info
- **GitHub-Safe**: Encrypted configs safe to commit publicly
- **Auto-loading**: Remembers your settings between sessions

## 💻 System Requirements

**macOS Only - Linux/Windows Not Supported**

- **macOS 13 Ventura or later** (required for Speech Recognition)
- **Python 3.7+**
- **Homebrew** for dependency management

### Why macOS Only?
- Uses Apple's Speech Recognition framework via the `yap` tool
- Leverages local translation tools for privacy
- Optimized for Apple's on-device AI capabilities

## 🚀 Quick Start

### Prerequisites
```bash
# Install core dependencies
brew install finnvoor/tools/yap
brew install yt-dlp
brew install translate-shell

# Optional: For AI features  
brew install llm
brew install uv
```

### Setup
1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd whisperkilled
   ```

2. **Launch Whisper Killer**
   ```bash
   # Global command (recommended)
   yapgui
   
   # Or from project directory
   python3 yap_gui.py
   ./run_yap_gui.sh
   ```

3. **Configure OpenRouter API** (for translation)
   - Go to Settings tab
   - Enter your [OpenRouter API key](https://openrouter.ai/keys)
   - Click "Save" to encrypt and store securely

## 📋 Usage

### YouTube Videos
1. Switch to **📺 YouTube** tab
2. Paste YouTube URL
3. Optional: Enable translation and/or AI summary
4. Click **🔽 Download & Transcribe**
5. View results in separate tabs: Original, Translation, SRT files, Summary

### Local Videos
1. Switch to **🎬 Local Video** tab
2. Browse or drag-drop your video file
3. Configure options as needed
4. Click **🎤 Transcribe Video**
5. View results in separate tabs: Original, Translation, SRT files, Summary

### Example Output
```
🎬 Tech Tutorial: Advanced Python Tips & Tricks
==============================================

📝 TRANSCRIPTION:
Welcome to today's Python tutorial. In this video, we'll explore advanced techniques that can make your code more efficient and readable.

We'll start with list comprehensions, which are a concise way to create lists. Instead of writing a traditional for loop, you can use this elegant syntax.

🌍 TRANSLATION (ES):
Bienvenidos al tutorial de Python de hoy. En este video, exploraremos técnicas avanzadas que pueden hacer que tu código sea más eficiente y legible.

Comenzaremos con las comprensiones de listas, que son una forma concisa de crear listas.

📋 SUMMARY:
This tutorial covers advanced Python techniques focusing on code efficiency and readability. The main topics include list comprehensions as an alternative to traditional loops, and various syntax improvements for cleaner code.
```

## ⚙️ Configuration

### Model Selection
Choose from multiple AI models in Settings:
- **Claude Haiku** (fast, cost-effective)
- **GPT-3.5 Turbo** (balanced)
- **GPT-4o Mini** (high quality)
- **Llama 3.1 8B** (open source)
- **Gemini Flash** (Google's model)

### Output Directory
- Default: `~/Downloads/yap_output/`
- Customizable in Settings tab
- Contains encrypted config and processed files

## 🔒 Security & Privacy

### API Key Encryption
- **Machine-specific encryption**: Uses your computer's unique info
- **Safe for GitHub**: Encrypted data is meaningless on other machines
- **No plaintext storage**: Keys never stored in readable format

### Privacy Features
- **100% local processing**: Speech recognition uses Apple's on-device AI
- **Local translation**: Text translation done locally via translate-shell
- **Limited API usage**: Only titles/formatting sent to OpenRouter (not original content)
- **Fallback transparency**: Full OpenRouter translation only when local translation fails
- **No telemetry**: No usage data collection or tracking
- **Secure storage**: All sensitive data encrypted locally

## 🛠️ Development

### Project Structure
```
whisperkilled/
├── yap_gui.py              # Main Whisper Killer application
├── run_yap_gui.sh          # Launch script
├── yap                     # Local launcher
├── .gitignore              # Git ignore rules
├── .yap_config             # Encrypted API key (safe to commit)
└── README.md               # This file
```

### Dependencies Status
The app includes a built-in dependency checker in the Settings tab that shows:
- ✅ Required tools installed
- ⚠️ Optional features available
- ❌ Missing dependencies with install commands

## 💰 Cost Considerations

### OpenRouter Pricing (approximate)
- **Claude Haiku**: ~$0.001-0.002 per transcription
- **GPT-3.5 Turbo**: ~$0.002-0.005 per transcription
- **Other models**: Varies by provider

### Free Alternatives
- **Core transcription**: Free with Apple Speech Recognition
- **No translation/summaries**: No API costs
- **Local processing**: No ongoing fees

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Adding New Features
- **Translation providers**: Add to `translate_text()` method
- **Output formats**: Extend format options
- **New models**: Add to model dropdown in Settings

## 📝 License

This project is open source. See license for details.

## 🙏 Acknowledgments

- **[Yap](https://github.com/finnvoor/yap)**: Core transcription engine by [@finnvoor](https://github.com/finnvoor) - The amazing Swift-based tool that powers all transcription functionality
- **Apple Speech Recognition**: On-device speech processing
- **OpenRouter**: Multi-model API access
- **yt-dlp**: YouTube download capabilities

### Special Thanks
This GUI application is built on top of the excellent [Yap transcription tool](https://github.com/finnvoor/yap) created by [@finnvoor](https://github.com/finnvoor). Yap provides fast, accurate, local speech recognition using Apple's Speech framework. This project simply adds a user-friendly interface and additional features like translation and AI summaries on top of that solid foundation.

## 🆘 Troubleshooting

### Common Issues

**"Speech recognition not available"**
- Grant microphone permissions in System Preferences
- Restart the application

**"No transcription result"**  
- Check audio quality and volume
- Ensure file format is supported
- Try converting to .wav format

**Translation not working**
- Verify OpenRouter API key in Settings
- Check internet connection
- Ensure curl is available (`brew install curl`)

**GUI not appearing**
- Install tkinter: `brew install python-tk`
- Run from terminal to see error messages

### Getting Help
- Check the Settings tab for dependency status
- Enable verbose logging by running from terminal
- Report issues with sample files when possible

---

**💀 WHISPER KILLER 🎙️** - *Transcription that kills the competition*

Made with ❤️ for content creators, researchers, and accessibility advocates.