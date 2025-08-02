<img width="904" height="820" alt="Captura de pantalla 2025-08-02 a las 20 40 27" src="https://github.com/user-attachments/assets/9e0c154f-d9e6-437b-8450-de5960ddd9e6" />

# 💀 WHISPER KILLER 🎙️


**Privacy-First Transcription & Translation Tool**

A powerful, user-friendly GUI application for transcribing YouTube videos and local video files using Apple's Speech Recognition, with AI-powered translation and summarization. Built to kill the competition with unmatched privacy and performance.

## ✨ Features

### 📺 Online Video Transcription
- **Multi-platform support**: YouTube, Facebook, and Vimeo
- **One-click processing**: Paste URL, click transcribe
- **Format options**: Plain text or SRT subtitles
- **Audio management**: Keep or auto-delete downloaded audio

### 🎬 Local Video Transcription
- **Drag & drop interface**: Easy file selection
- **Multiple formats**: MP4, MOV, AVI, MKV, WebM support
- **Direct transcription**: No intermediate files needed

### 🌍 **NEW: Text Translation**
- **Direct text input**: Paste or import text files
- **82 Language Support**: Full Apple Live Translation coverage
- **Dual Output System**: Normal and enhanced translations
- **Smart Export Options**: Copy, save, and Org file creation
- **Language Memory**: Remembers your language preferences

### 🌐 **Enhanced Translation Engine**
- **82 Languages**: Complete Apple Live Translation support
- **Smart Paragraph Analysis**: Automatically detects text structure quality
- **Hybrid Approach**: Apple Live Translation for good structure, AI for poor structure
- **Maximum Privacy**: Prioritizes local translation when possible
- **Adaptive Enhancement**: Uses AI only when needed for smart paragraph creation
- **Best of Both Worlds**: Privacy + intelligent formatting

### 🤖 AI Enhancement
- **Smart Titles**: Auto-generated titles with relevant emojis
- **Paragraph Formatting**: Clean, readable text structure
- **AI Summaries**: Concise summaries of transcribed content

### 🔐 Secure API Management
- **Encrypted Storage**: API keys encrypted with machine-specific info
- **GitHub-Safe**: Encrypted configs safe to commit publicly
- **Auto-loading**: Remembers your settings between sessions

### 🚀 **NEW: Smart Launcher**
- **Single Instance**: Automatically detects and closes running instances
- **Updated Alias**: `yap` command with instance management
- **Clean Startup**: Always starts fresh without conflicts

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

2. **Launch Whisper Killer** (NEW: Single-instance management)
   ```bash
   # Global command with instance management (recommended)
   yap
   
   # Or use launcher scripts
   python3 run_yap_gui.py
   ./run_yap_gui.sh
   
   # Direct launch (legacy)
   python3 yap_gui.py
   ```

3. **Configure OpenRouter API** (for translation)
   - Go to Settings tab
   - Enter your [OpenRouter API key](https://openrouter.ai/keys)
   - Click "Save" to encrypt and store securely

## 📋 Usage

### Online Videos (YouTube, Facebook, Vimeo)
1. Switch to **📺 Online Videos** tab
2. Paste video URL from any supported platform
3. Optional: Enable translation and/or AI summary
4. Click **🔽 Download & Transcribe**
5. View results in separate tabs: Original, Translation, SRT files, Summary

### Local Videos
1. Switch to **🎬 Local Video** tab
2. Browse or drag-drop your video file
3. Configure options as needed
4. Click **🎤 Transcribe Video**
5. View results in separate tabs: Original, Translation, SRT files, Summary

### **NEW: Text Translation**
1. Switch to **🌍 Text Translation** tab
2. **Input Options**:
   - Paste text directly
   - Import text file
   - Clear input/output
3. **Language Selection**:
   - Choose source language (From:)
   - Choose target language (To:)
   - 82 languages available
4. **Translation Options**:
   - Apple Live Translation (privacy-first)
   - AI Enhancement (smart formatting)
5. **Export Results**:
   - **📋 Copy**: Instant clipboard copy
   - **💾 Save as File**: Save as text file
   - **📝 Create Org File**: Export as Org mode file

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

## 🌐 **NEW: 82 Language Support**

### Available Languages
- **Major Languages**: English, Spanish, French, German, Italian, Portuguese, Japanese, Korean, Chinese (Simplified/Traditional), Russian, Arabic
- **European Languages**: Dutch, Polish, Turkish, Swedish, Danish, Norwegian, Finnish, Czech, Slovak, Hungarian, Romanian, Bulgarian, Croatian, Slovenian, Estonian, Latvian, Lithuanian, Greek, Hebrew, Icelandic, Maltese, Welsh, Irish, Basque, Catalan, Galician, Albanian, Macedonian, Serbian, Bosnian, Montenegrin
- **Asian Languages**: Thai, Vietnamese, Hindi, Indonesian, Malay, Mongolian, Kyrgyz, Uzbek, Kazakh, Tajik, Turkmen, Azerbaijani, Armenian, Nepali, Dzongkha, Tibetan, Uyghur, Pashto, Sindhi, Kashmiri
- **African Languages**: Amharic, Swahili, Zulu, Afrikaans
- **Indian Languages**: Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Sinhala, Burmese, Khmer, Lao, Georgian

### Language Features
- **Source & Target Selection**: Choose any language pair
- **Language Memory**: Preferences saved between sessions
- **Real-time Labels**: See language names as you select
- **Apple Integration**: Uses native Apple Live Translation

## 📁 **NEW: Export Options**

### Copy to Clipboard
- **Instant Copy**: No dialogs, immediate clipboard access
- **Full Content**: Copies entire translation text
- **Cross-Platform**: Works on macOS, Windows, Linux

### Save as File
- **Text Files**: Save as `.txt` files
- **File Dialog**: Choose destination and filename
- **UTF-8 Encoding**: Proper character support

### Create Org File
- **Org Mode**: Export as `.org` files for Emacs
- **Smart Formatting**: Automatic Org mode conversion
- **Metadata**: Adds title and date headers
- **Structure**: Converts titles and separators

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

### **NEW: Language Preferences**
- **Automatic Saving**: Language choices remembered
- **Cross-Tab Support**: All translation tabs remember preferences
- **JSON Storage**: Preferences stored in `.yap_language_prefs`

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
├── run_yap_gui.py          # Python launcher (recommended)
├── run_yap_gui.sh          # Shell script launcher
├── test_facebook_vimeo_support.py  # Platform support testing
├── docs/                   # 📚 Complete documentation
│   ├── INDEX.md           # Documentation overview
│   ├── README.md          # This file
│   ├── FACEBOOK_VIMEO_SUPPORT.md  # Multi-platform support docs
│   └── [feature docs...]  # Detailed feature documentation
├── .gitignore              # Git ignore rules
├── .yap_config             # Encrypted API key (safe to commit)
└── .yap_language_prefs     # Language preferences (safe to commit)
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
- **Text translation**: Free with Apple Live Translation (82 languages)
- **Multi-platform support**: YouTube, Facebook, Vimeo all supported
- **No AI enhancement**: No API costs
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
- **Languages**: Extend Apple Live Translation support

## 📝 License

This project is open source. See license for details.

## 🙏 Acknowledgments

- **[Yap](https://github.com/finnvoor/yap)**: Core transcription engine by [@finnvoor](https://github.com/finnvoor) - The amazing Swift-based tool that powers all transcription functionality
- **Apple Speech Recognition**: On-device speech processing
- **Apple Live Translation**: 82-language translation support
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

**Multiple instances running**
- Use `yap` command (automatically manages instances)
- Or use launcher scripts: `python3 run_yap_gui.py`

### Getting Help
- Check the Settings tab for dependency status
- Enable verbose logging by running from terminal
- Report issues with sample files when possible
- See `docs/` folder for detailed feature documentation

---

**💀 WHISPER KILLER 🎙️** - *Transcription that kills the competition*

Made with ❤️ for content creators, researchers, and accessibility advocates.
