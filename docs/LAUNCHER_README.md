# Whisper Killer Launcher Scripts

## Overview

These launcher scripts ensure that only one instance of Whisper Killer runs at a time by automatically detecting and closing any existing instances before starting a new one.

## 🚀 **Available Launchers**

### **Python Launcher** (Recommended)
```bash
python3 run_yap_gui.py
```

### **Shell Script Launcher**
```bash
./run_yap_gui.sh
```

## ✨ **Features**

### **Instance Detection**
- Automatically finds any running Whisper Killer processes
- Identifies processes by `yap_gui.py` in the command line
- Works across different Python versions and execution methods

### **Graceful Shutdown**
- Attempts graceful termination first (SIGTERM)
- Falls back to force kill (SIGKILL) if needed
- Waits for processes to close properly
- Provides detailed status messages

### **Error Handling**
- Handles permission errors gracefully
- Continues even if some processes can't be closed
- Provides clear feedback on what's happening

## 📋 **Usage**

### **Basic Usage**
```bash
# Using Python launcher (recommended)
python3 run_yap_gui.py

# Using shell script launcher
./run_yap_gui.sh
```

### **What Happens**
1. **Detection**: Script checks for running instances
2. **Notification**: Shows how many instances were found
3. **Shutdown**: Gracefully closes existing instances
4. **Startup**: Launches new Whisper Killer instance
5. **Status**: Reports success or failure

## 🔧 **Example Output**

```
🔍 Checking for running Whisper Killer instances...
⚠️  Found 1 running instance(s)
🔄 Closing existing instance(s)...
   Stopping process 12345...
   ✅ Process 12345 closed gracefully
✅ Existing instances closed
🚀 Starting Whisper Killer...

Setting up UI...
Loading language preferences...
Checking dependencies...
Loading API key...
Whisper Killer initialization complete
Starting Whisper Killer...

✅ Whisper Killer started successfully
```

## 🛠 **Technical Details**

### **Python Launcher** (`run_yap_gui.py`)
- Uses `psutil` library for process management
- Cross-platform compatibility
- Better error handling and process detection
- Recommended for most users

### **Shell Script Launcher** (`run_yap_gui.sh`)
- Uses `pgrep` and `kill` commands
- Works on Unix-like systems (macOS, Linux)
- No additional dependencies required
- Faster execution

## ⚠️ **Requirements**

### **Python Launcher**
- Python 3.6+
- `psutil` library (usually pre-installed)
- Cross-platform

### **Shell Script Launcher**
- Unix-like system (macOS, Linux)
- `pgrep` and `kill` commands (standard)
- Bash shell

## 🎯 **Benefits**

1. **Single Instance**: Prevents multiple app windows
2. **Resource Management**: Avoids memory/CPU conflicts
3. **User Experience**: Clean startup every time
4. **Stability**: Prevents potential conflicts between instances
5. **Convenience**: No manual process management needed

## 🔄 **Integration**

The launcher scripts work seamlessly with:
- **Language Preferences**: Preserved across restarts
- **API Keys**: Maintained in encrypted storage
- **Output Directory**: Same location for all instances
- **Settings**: All user preferences maintained

## 🚨 **Troubleshooting**

### **Permission Issues**
```bash
# Make scripts executable
chmod +x run_yap_gui.sh
chmod +x run_yap_gui.py
```

### **Missing psutil**
```bash
# Install psutil if needed
pip3 install psutil
```

### **Process Not Found**
- The launcher will continue and start a new instance
- This is normal if no previous instances were running

Use these launcher scripts to ensure a clean, single-instance experience with Whisper Killer! 