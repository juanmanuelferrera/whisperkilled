#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import subprocess
import os
import tempfile
import json
from pathlib import Path
from urllib.parse import urlparse
import base64
import hashlib

class YapGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Yap GUI - YouTube & Video Transcription Tool")
        self.root.geometry("900x800")
        
        # Variables
        self.current_operation = None
        self.output_dir = os.path.expanduser("~/Downloads/yap_output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Encryption key based on machine-specific info (safe for GitHub)
        self.encryption_key = self.generate_machine_key()
        
        self.setup_ui()
        self.check_dependencies()
        self.load_encrypted_api_key()
        
    def setup_ui(self):
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # YouTube Tab
        self.setup_youtube_tab(notebook)
        
        # Local Video Tab
        self.setup_local_video_tab(notebook)
        
        # Settings Tab
        self.setup_settings_tab(notebook)
        
    def setup_youtube_tab(self, notebook):
        youtube_frame = ttk.Frame(notebook)
        notebook.add(youtube_frame, text="📺 YouTube")
        
        main_frame = ttk.Frame(youtube_frame, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Video Transcription", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # URL Input
        url_frame = ttk.LabelFrame(main_frame, text="YouTube URL", padding="10")
        url_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(url_frame, text="Video URL:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.youtube_url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=self.youtube_url_var, width=60)
        url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        paste_button = ttk.Button(url_frame, text="Paste", command=self.paste_url)
        paste_button.pack(side=tk.RIGHT)
        
        # Options
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Output format
        format_frame = ttk.Frame(options_frame)
        format_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(format_frame, text="Output Format:").pack(side=tk.LEFT, padx=(0, 15))
        
        self.yt_output_format = tk.StringVar(value="txt")
        ttk.Radiobutton(format_frame, text="Text (.txt)", variable=self.yt_output_format, 
                       value="txt").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(format_frame, text="Subtitles (.srt)", variable=self.yt_output_format, 
                       value="srt").pack(side=tk.LEFT)
        
        # Additional options
        opts_frame = ttk.Frame(options_frame)
        opts_frame.pack(fill=tk.X)
        
        self.yt_summarize_var = tk.BooleanVar()
        ttk.Checkbutton(opts_frame, text="Generate AI Summary", 
                       variable=self.yt_summarize_var).pack(side=tk.LEFT, padx=(0, 15))
        
        self.yt_translate_var = tk.BooleanVar()
        ttk.Checkbutton(opts_frame, text="Translate text", 
                       variable=self.yt_translate_var).pack(side=tk.LEFT, padx=(0, 15))
        
        self.yt_keep_audio_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(opts_frame, text="Keep audio", 
                       variable=self.yt_keep_audio_var).pack(side=tk.LEFT)
        
        # Translation options
        translate_frame = ttk.Frame(options_frame)
        translate_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(translate_frame, text="Translate to:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.yt_target_lang = tk.StringVar(value="es")
        lang_combo = ttk.Combobox(translate_frame, textvariable=self.yt_target_lang, 
                                 values=["es", "fr", "de", "it", "pt", "ja", "ko", "zh", "ru", "ar"],
                                 width=5, state="readonly")
        lang_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Language labels
        lang_labels = {
            "es": "Spanish", "fr": "French", "de": "German", "it": "Italian", 
            "pt": "Portuguese", "ja": "Japanese", "ko": "Korean", 
            "zh": "Chinese", "ru": "Russian", "ar": "Arabic"
        }
        
        self.yt_lang_label = tk.StringVar(value=lang_labels.get("es", "Spanish"))
        ttk.Label(translate_frame, textvariable=self.yt_lang_label, 
                 font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Update label when language changes
        def update_lang_label(*args):
            self.yt_lang_label.set(lang_labels.get(self.yt_target_lang.get(), ""))
        self.yt_target_lang.trace_add('write', update_lang_label)
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.yt_download_button = ttk.Button(action_frame, text="🔽 Download & Transcribe", 
                                           command=self.download_and_transcribe,
                                           style="Accent.TButton")
        self.yt_download_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(action_frame, text="🗑️ Clear Output", 
                  command=self.clear_youtube_output).pack(side=tk.LEFT)
        
        # Progress
        self.yt_progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.yt_progress.pack(fill=tk.X, pady=(0, 10))
        
        # Status
        self.yt_status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(main_frame, textvariable=self.yt_status_var, 
                                font=("Arial", 10))
        status_label.pack(pady=(0, 10))
        
        # Output
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.yt_output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, 
                                                       height=12, font=("Consolas", 11))
        self.yt_output_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_local_video_tab(self, notebook):
        local_frame = ttk.Frame(notebook)
        notebook.add(local_frame, text="🎬 Local Video")
        
        main_frame = ttk.Frame(local_frame, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Local Video Transcription", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="Video File", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        file_inner_frame = ttk.Frame(file_frame)
        file_inner_frame.pack(fill=tk.X)
        
        ttk.Label(file_inner_frame, text="File:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.local_file_var = tk.StringVar()
        file_entry = ttk.Entry(file_inner_frame, textvariable=self.local_file_var, width=50)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_button = ttk.Button(file_inner_frame, text="Browse", command=self.browse_video_file)
        browse_button.pack(side=tk.RIGHT)
        
        # Drop zone
        drop_frame = ttk.Frame(file_frame)
        drop_frame.pack(fill=tk.X, pady=(10, 0))
        
        drop_label = ttk.Label(drop_frame, text="🎬 Drag and drop video files here", 
                              justify=tk.CENTER, font=("Arial", 11), 
                              background="#f0f0f0", relief="groove", padding="20")
        drop_label.pack(fill=tk.X)
        drop_label.bind("<Button-1>", lambda e: self.browse_video_file())
        
        # Options
        local_options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        local_options_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Output format
        local_format_frame = ttk.Frame(local_options_frame)
        local_format_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(local_format_frame, text="Output Format:").pack(side=tk.LEFT, padx=(0, 15))
        
        self.local_output_format = tk.StringVar(value="txt")
        ttk.Radiobutton(local_format_frame, text="Text (.txt)", variable=self.local_output_format, 
                       value="txt").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(local_format_frame, text="Subtitles (.srt)", variable=self.local_output_format, 
                       value="srt").pack(side=tk.LEFT)
        
        # Additional options
        local_opts_frame = ttk.Frame(local_options_frame)
        local_opts_frame.pack(fill=tk.X)
        
        self.local_summarize_var = tk.BooleanVar()
        ttk.Checkbutton(local_opts_frame, text="Generate AI Summary", 
                       variable=self.local_summarize_var).pack(side=tk.LEFT, padx=(0, 15))
        
        self.local_translate_var = tk.BooleanVar()
        ttk.Checkbutton(local_opts_frame, text="Translate text", 
                       variable=self.local_translate_var).pack(side=tk.LEFT)
        
        # Translation options for local video
        local_translate_frame = ttk.Frame(local_options_frame)
        local_translate_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(local_translate_frame, text="Translate to:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.local_target_lang = tk.StringVar(value="es")
        local_lang_combo = ttk.Combobox(local_translate_frame, textvariable=self.local_target_lang, 
                                       values=["es", "fr", "de", "it", "pt", "ja", "ko", "zh", "ru", "ar"],
                                       width=5, state="readonly")
        local_lang_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        self.local_lang_label = tk.StringVar(value="Spanish")
        ttk.Label(local_translate_frame, textvariable=self.local_lang_label, 
                 font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Update label when language changes
        def update_local_lang_label(*args):
            lang_labels = {
                "es": "Spanish", "fr": "French", "de": "German", "it": "Italian", 
                "pt": "Portuguese", "ja": "Japanese", "ko": "Korean", 
                "zh": "Chinese", "ru": "Russian", "ar": "Arabic"
            }
            self.local_lang_label.set(lang_labels.get(self.local_target_lang.get(), ""))
        self.local_target_lang.trace_add('write', update_local_lang_label)
        
        # Action buttons
        local_action_frame = ttk.Frame(main_frame)
        local_action_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.local_transcribe_button = ttk.Button(local_action_frame, text="🎤 Transcribe Video", 
                                                command=self.transcribe_local_video,
                                                style="Accent.TButton")
        self.local_transcribe_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(local_action_frame, text="💾 Save Output", 
                  command=self.save_local_output).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(local_action_frame, text="🗑️ Clear", 
                  command=self.clear_local_output).pack(side=tk.LEFT)
        
        # Progress
        self.local_progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.local_progress.pack(fill=tk.X, pady=(0, 10))
        
        # Status
        self.local_status_var = tk.StringVar(value="Ready")
        local_status_label = ttk.Label(main_frame, textvariable=self.local_status_var, 
                                      font=("Arial", 10))
        local_status_label.pack(pady=(0, 10))
        
        # Output
        local_output_frame = ttk.LabelFrame(main_frame, text="Transcription Output", padding="10")
        local_output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.local_output_text = scrolledtext.ScrolledText(local_output_frame, wrap=tk.WORD, 
                                                          height=12, font=("Consolas", 11))
        self.local_output_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_settings_tab(self, notebook):
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="⚙️ Settings")
        
        main_frame = ttk.Frame(settings_frame, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Settings & Dependencies", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # OpenRouter API Key
        api_frame = ttk.LabelFrame(main_frame, text="OpenRouter API Key", padding="10")
        api_frame.pack(fill=tk.X, pady=(0, 15))
        
        api_inner_frame = ttk.Frame(api_frame)
        api_inner_frame.pack(fill=tk.X)
        
        ttk.Label(api_inner_frame, text="API Key:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.openrouter_api_key = tk.StringVar()
        # Try to get from environment variable
        import os
        self.openrouter_api_key.set(os.environ.get('OPENROUTER_API_KEY', ''))
        
        api_entry = ttk.Entry(api_inner_frame, textvariable=self.openrouter_api_key, 
                             show="*", width=50)
        api_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(api_inner_frame, text="Save", command=self.save_api_key).pack(side=tk.RIGHT, padx=(0, 5))
        ttk.Button(api_inner_frame, text="Export for GitHub", command=self.export_for_github).pack(side=tk.RIGHT)
        
        # Model selection
        model_frame = ttk.Frame(api_frame)
        model_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(model_frame, text="Model:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.translation_model = tk.StringVar(value="anthropic/claude-3-haiku")
        model_combo = ttk.Combobox(model_frame, textvariable=self.translation_model, 
                                  values=[
                                      "anthropic/claude-3-haiku",
                                      "openai/gpt-3.5-turbo", 
                                      "openai/gpt-4o-mini",
                                      "meta-llama/llama-3.1-8b-instruct",
                                      "google/gemini-flash-1.5"
                                  ],
                                  width=30, state="readonly")
        model_combo.pack(side=tk.LEFT)
        
        # API info
        api_info = ttk.Label(api_frame, text="Enter your OpenRouter API key for translation. Get one at: https://openrouter.ai/keys\n🔒 Your key is encrypted with machine-specific info - safe for GitHub!", 
                            font=("Arial", 9), wraplength=600)
        api_info.pack(pady=(5, 0))
        
        # Output directory
        output_frame = ttk.LabelFrame(main_frame, text="Output Directory", padding="10")
        output_frame.pack(fill=tk.X, pady=(0, 15))
        
        dir_frame = ttk.Frame(output_frame)
        dir_frame.pack(fill=tk.X)
        
        ttk.Label(dir_frame, text="Save files to:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.output_dir_var = tk.StringVar(value=self.output_dir)
        dir_entry = ttk.Entry(dir_frame, textvariable=self.output_dir_var, width=50)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(dir_frame, text="Browse", command=self.browse_output_dir).pack(side=tk.RIGHT, padx=(0, 10))
        ttk.Button(dir_frame, text="Open", command=self.open_output_dir).pack(side=tk.RIGHT)
        
        # Dependencies status
        deps_frame = ttk.LabelFrame(main_frame, text="Dependencies Status", padding="10")
        deps_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.deps_text = scrolledtext.ScrolledText(deps_frame, wrap=tk.WORD, height=8, 
                                                  font=("Consolas", 10))
        self.deps_text.pack(fill=tk.BOTH, expand=True)
        
        # Refresh button
        ttk.Button(main_frame, text="🔄 Check Dependencies", 
                  command=self.check_dependencies).pack(pady=10)
    
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        def check():
            deps_status = []
            
            # Check yap
            try:
                result = subprocess.run(['yap', '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    deps_status.append("✅ yap: Available")
                else:
                    deps_status.append("❌ yap: Not found or error")
            except:
                deps_status.append("❌ yap: Not installed")
            
            # Check yt-dlp
            try:
                result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    deps_status.append(f"✅ yt-dlp: {version}")
                else:
                    deps_status.append("❌ yt-dlp: Error")
            except:
                deps_status.append("❌ yt-dlp: Not installed")
                deps_status.append("   Install with: brew install yt-dlp")
            
            # Check llm
            try:
                result = subprocess.run(['llm', '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    deps_status.append(f"✅ llm: {version}")
                else:
                    deps_status.append("❌ llm: Error")
            except:
                deps_status.append("❌ llm: Not installed")
                deps_status.append("   Install with: brew install llm")
            
            # Check uvx
            try:
                result = subprocess.run(['uvx', '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    deps_status.append("✅ uvx: Available")
                else:
                    deps_status.append("❌ uvx: Error")
            except:
                deps_status.append("❌ uvx: Not installed")
                deps_status.append("   Install with: brew install uv")
            
            # Check OpenRouter API key for translation
            api_key = os.environ.get('OPENROUTER_API_KEY') or self.openrouter_api_key.get().strip()
            if api_key:
                deps_status.append("✅ OpenRouter API: Configured for translation")
            else:
                deps_status.append("⚠️  OpenRouter API: Not configured (for translation)")
                deps_status.append("   Enter API key in Settings tab")
            
            # Check curl for API requests
            try:
                result = subprocess.run(['curl', '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    deps_status.append("✅ curl: Available for API requests")
                else:
                    deps_status.append("❌ curl: Error")
            except:
                deps_status.append("❌ curl: Not available (needed for OpenRouter API)")
                deps_status.append("   Install with: brew install curl")
            
            deps_status.append("")
            deps_status.append("Installation commands:")
            deps_status.append("brew install finnvoor/tools/yap")
            deps_status.append("brew install yt-dlp")
            deps_status.append("brew install llm")
            deps_status.append("brew install uv")
            deps_status.append("")
            deps_status.append("For translation:")
            deps_status.append("• Enter OpenAI API key in Settings tab (recommended)")
            deps_status.append("• Ensure curl is available (usually pre-installed)")
            
            # Update UI
            self.root.after(0, lambda: self.update_deps_display("\n".join(deps_status)))
        
        threading.Thread(target=check, daemon=True).start()
    
    def update_deps_display(self, text):
        self.deps_text.delete(1.0, tk.END)
        self.deps_text.insert(tk.END, text)
    
    def generate_machine_key(self):
        """Generate a machine-specific encryption key"""
        # Use machine-specific info that's consistent but unique
        import platform
        machine_info = f"{platform.node()}-{platform.system()}-{os.path.expanduser('~')}"
        return hashlib.sha256(machine_info.encode()).hexdigest()[:32]
    
    def encrypt_text(self, text):
        """Simple XOR encryption (sufficient for API key storage)"""
        if not text:
            return ""
        
        key = self.encryption_key
        encrypted = []
        
        for i, char in enumerate(text):
            key_char = key[i % len(key)]
            encrypted_char = chr(ord(char) ^ ord(key_char))
            encrypted.append(encrypted_char)
        
        # Base64 encode to make it safe for storage
        encrypted_string = ''.join(encrypted)
        return base64.b64encode(encrypted_string.encode()).decode()
    
    def decrypt_text(self, encrypted_text):
        """Decrypt XOR encrypted text"""
        if not encrypted_text:
            return ""
        
        try:
            # Base64 decode
            encrypted_string = base64.b64decode(encrypted_text).decode()
            
            key = self.encryption_key
            decrypted = []
            
            for i, char in enumerate(encrypted_string):
                key_char = key[i % len(key)]
                decrypted_char = chr(ord(char) ^ ord(key_char))
                decrypted.append(decrypted_char)
            
            return ''.join(decrypted)
        except:
            return ""
    
    def save_encrypted_api_key(self, api_key):
        """Save encrypted API key to a local file"""
        if not api_key:
            return
        
        encrypted_key = self.encrypt_text(api_key)
        config_file = os.path.join(self.output_dir, '.yap_config')
        
        try:
            with open(config_file, 'w') as f:
                f.write(encrypted_key)
        except:
            pass
    
    def load_encrypted_api_key(self):
        """Load and decrypt API key from local file"""
        config_file = os.path.join(self.output_dir, '.yap_config')
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    encrypted_key = f.read().strip()
                
                decrypted_key = self.decrypt_text(encrypted_key)
                if decrypted_key:
                    self.openrouter_api_key.set(decrypted_key)
                    os.environ['OPENROUTER_API_KEY'] = decrypted_key
            except:
                pass
    
    def paste_url(self):
        try:
            clipboard_content = self.root.clipboard_get()
            if clipboard_content:
                self.youtube_url_var.set(clipboard_content.strip())
        except:
            pass
    
    def browse_video_file(self):
        file_types = [
            ("Video files", "*.mp4 *.mov *.avi *.mkv *.webm *.m4v"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select video file",
            filetypes=file_types
        )
        
        if filename:
            self.local_file_var.set(filename)
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(
            title="Select output directory",
            initialdir=self.output_dir
        )
        
        if directory:
            self.output_dir = directory
            self.output_dir_var.set(directory)
    
    def open_output_dir(self):
        if os.path.exists(self.output_dir):
            subprocess.run(['open', self.output_dir])
        else:
            messagebox.showerror("Error", f"Output directory does not exist: {self.output_dir}")
    
    def save_api_key(self):
        """Save API key to environment and encrypted storage"""
        api_key = self.openrouter_api_key.get().strip()
        if api_key:
            # Save to environment for current session
            os.environ['OPENROUTER_API_KEY'] = api_key
            
            # Save encrypted to local file for persistence
            self.save_encrypted_api_key(api_key)
            
            messagebox.showinfo("Success", "OpenRouter API key saved and encrypted locally")
        else:
            messagebox.showwarning("Warning", "Please enter a valid API key")
    
    def export_for_github(self):
        """Export encrypted API key info for GitHub sharing"""
        api_key = self.openrouter_api_key.get().strip()
        if not api_key:
            messagebox.showwarning("Warning", "Please enter and save an API key first")
            return
        
        encrypted_key = self.encrypt_text(api_key)
        
        export_info = f"""# Encrypted API Key Export
# This encrypted key is safe to commit to GitHub
# It only works on the machine where it was encrypted

ENCRYPTED_OPENROUTER_KEY = "{encrypted_key}"

# To use: Copy the .yap_config file from your output directory
# Machine info hash: {self.encryption_key[:8]}...
"""
        
        # Copy to clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(export_info)
        
        # Also save to file
        export_file = os.path.join(self.output_dir, 'github_export.py')
        try:
            with open(export_file, 'w') as f:
                f.write(export_info)
            
            messagebox.showinfo("Export Complete", 
                               f"Encrypted key info copied to clipboard and saved to:\n{export_file}\n\n" +
                               "🔒 This encrypted data is safe to share on GitHub!\n" +
                               "📁 Also copy .yap_config file from output directory")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to save export file: {e}")
    
    def download_and_transcribe(self):
        url = self.youtube_url_var.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        if not self.is_valid_youtube_url(url):
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return
        
        self.yt_download_button.config(state='disabled')
        self.yt_progress.start()
        self.yt_status_var.set("Starting download...")
        self.yt_output_text.delete(1.0, tk.END)
        
        thread = threading.Thread(target=self.run_youtube_transcription, args=(url,))
        thread.daemon = True
        thread.start()
    
    def is_valid_youtube_url(self, url):
        parsed = urlparse(url)
        return (parsed.netloc in ['www.youtube.com', 'youtube.com', 'youtu.be'] or 
                'youtube.com' in url or 'youtu.be' in url)
    
    def run_youtube_transcription(self, url):
        try:
            output_format = self.yt_output_format.get()
            summarize = self.yt_summarize_var.get()
            keep_audio = self.yt_keep_audio_var.get()
            
            # Step 1: Download and transcribe with separate commands for cleaner output
            self.root.after(0, lambda: self.yt_status_var.set("Downloading video and extracting audio..."))
            
            # First, download the audio
            download_cmd = ['yt-dlp', url, '-x', '--audio-format', 'wav', 
                           '--output', f'{self.output_dir}/%(title)s.%(ext)s']
            
            download_result = subprocess.run(download_cmd, capture_output=True, text=True, timeout=300)
            
            if download_result.returncode != 0:
                self.root.after(0, self.on_youtube_error, f"Download failed: {download_result.stderr}")
                return
            
            # Find the downloaded audio file
            audio_files = list(Path(self.output_dir).glob("*.wav"))
            if not audio_files:
                self.root.after(0, self.on_youtube_error, "No audio file found after download")
                return
            
            # Use the most recent audio file
            audio_file = max(audio_files, key=os.path.getctime)
            
            # Step 2: Transcribe the audio
            self.root.after(0, lambda: self.yt_status_var.set("Transcribing audio..."))
            
            yap_cmd = ['yap', str(audio_file)]
            
            if output_format == "srt":
                output_file = audio_file.with_suffix('.srt')
                yap_cmd.extend(['--srt', '-o', str(output_file)])
            else:
                output_file = audio_file.with_suffix('.txt')
                yap_cmd.extend(['-o', str(output_file)])
            
            yap_result = subprocess.run(yap_cmd, capture_output=True, text=True, timeout=300)
            
            if yap_result.returncode != 0:
                self.root.after(0, self.on_youtube_error, f"Transcription failed: {yap_result.stderr}")
                return
            
            # Read the clean transcription from the output file
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    transcription_text = f.read().strip()
            except:
                transcription_text = yap_result.stdout.strip()
            
            # Clean up audio file if not keeping it
            if not keep_audio:
                try:
                    os.unlink(audio_file)
                except:
                    pass
            
            # Format transcription into paragraphs
            formatted_transcription = self.format_text_in_paragraphs(transcription_text)
            
            # Process additional features
            output_parts = []
            
            # Generate title and summary if requested
            if summarize and transcription_text:
                self.root.after(0, lambda: self.yt_status_var.set("Generating title and summary..."))
                title, summary = self.generate_title_and_summary(transcription_text)
                output_parts.append(f"{title}\n{'='*len(title)}")
            
            output_parts.append(f"📝 TRANSCRIPTION:\n{formatted_transcription}")
            
            if self.yt_translate_var.get() and transcription_text:
                self.root.after(0, lambda: self.yt_status_var.set("Translating text..."))
                target_lang = self.yt_target_lang.get()
                translation = self.translate_text(formatted_transcription, target_lang)
                formatted_translation = self.format_text_in_paragraphs(translation)
                output_parts.append(f"\n🌍 TRANSLATION ({target_lang.upper()}):\n{formatted_translation}")
            
            if summarize and transcription_text:
                output_parts.append(f"\n📋 SUMMARY:\n{summary}")
            
            output = "\n\n".join(output_parts) if len(output_parts) > 1 else formatted_transcription
            
            self.root.after(0, self.on_youtube_success, output)
            
        except subprocess.TimeoutExpired:
            self.root.after(0, self.on_youtube_error, "Operation timed out")
        except Exception as e:
            self.root.after(0, self.on_youtube_error, str(e))
    
    def find_latest_transcription(self, format_type):
        """Find the most recent transcription file in output directory"""
        try:
            pattern = "*.srt" if format_type == "srt" else "*.txt"
            files = list(Path(self.output_dir).glob(pattern))
            if files:
                latest_file = max(files, key=os.path.getctime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    return f.read()
        except:
            pass
        return "Transcription completed. Check output directory for files."
    
    def format_text_in_paragraphs(self, text):
        """Format text into readable paragraphs"""
        if not text or len(text.strip()) < 50:
            return text
        
        # Split by sentences and group into paragraphs
        sentences = text.replace('!', '.').replace('?', '.').split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        paragraphs = []
        current_paragraph = []
        sentence_count = 0
        
        for sentence in sentences:
            current_paragraph.append(sentence)
            sentence_count += 1
            
            # Create new paragraph every 3-4 sentences or if sentence is long
            if sentence_count >= 3 or len(sentence) > 100:
                if current_paragraph:
                    paragraphs.append('. '.join(current_paragraph) + '.')
                    current_paragraph = []
                    sentence_count = 0
        
        # Add remaining sentences
        if current_paragraph:
            paragraphs.append('. '.join(current_paragraph) + '.')
        
        return '\n\n'.join(paragraphs)
    
    def generate_title_and_summary(self, text):
        """Generate title with emojis and summary using llm"""
        try:
            # First, generate a title with emojis
            title_prompt = """Based on this transcript, create a catchy title with relevant emojis. 
            Use 2-3 emojis that match the content. Keep it under 60 characters.
            Just return the title, nothing else.
            
            Transcript:"""
            
            title_cmd = ['llm', '-m', 'mlx-community/Llama-3.2-1B-Instruct-4bit']
            title_result = subprocess.run(title_cmd, input=f"{title_prompt}\n{text}", 
                                        capture_output=True, text=True, timeout=60)
            
            title = "📝 Transcription Summary"  # Default title
            if title_result.returncode == 0 and title_result.stdout.strip():
                title = title_result.stdout.strip().split('\n')[0]  # Take first line only
            
            # Then generate summary
            summary_prompt = """Summarize this transcript in 2-3 clear paragraphs. 
            Focus on the main points and key information.
            
            Transcript:"""
            
            summary_cmd = ['llm', '-m', 'mlx-community/Llama-3.2-1B-Instruct-4bit']
            summary_result = subprocess.run(summary_cmd, input=f"{summary_prompt}\n{text}", 
                                          capture_output=True, text=True, timeout=120)
            
            if summary_result.returncode == 0:
                summary = summary_result.stdout.strip()
                return title, summary
            else:
                return title, f"⚠️ Summary generation failed.\n\nTo enable AI summaries, install LLM:\n\n🔧 brew install llm\n\nThen install the model:\n🔧 llm install mlx-community/Llama-3.2-1B-Instruct-4bit"
                
        except subprocess.TimeoutExpired:
            return "⏱️ Transcription Summary", "Summary generation timed out"
        except Exception as e:
            if "No such file or directory: 'llm'" in str(e):
                return "📝 Transcription Summary", f"⚠️ LLM not installed.\n\nTo enable AI summaries and titles:\n\n🔧 brew install llm\n🔧 llm install mlx-community/Llama-3.2-1B-Instruct-4bit"
            else:
                return "📝 Transcription Summary", f"Summary error: {str(e)}"
    
    def translate_text(self, text, target_lang):
        """Translate text using OpenRouter API"""
        try:
            api_key = os.environ.get('OPENROUTER_API_KEY') or self.openrouter_api_key.get().strip()
            
            if not api_key:
                return f"⚠️ OpenRouter API key required.\n\nPlease enter your API key in Settings tab or set OPENROUTER_API_KEY environment variable.\n\nGet a key at: https://openrouter.ai/keys"
            
            # Language mapping
            lang_names = {
                "es": "Spanish", "fr": "French", "de": "German", "it": "Italian",
                "pt": "Portuguese", "ja": "Japanese", "ko": "Korean", 
                "zh": "Chinese", "ru": "Russian", "ar": "Arabic"
            }
            
            target_lang_name = lang_names.get(target_lang, target_lang)
            model = self.translation_model.get()
            
            # Prepare the OpenRouter API request
            import json
            
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system", 
                        "content": f"You are a professional translator. Translate the following text to {target_lang_name}. Maintain the original formatting and structure. Only return the translation, no explanations."
                    },
                    {
                        "role": "user", 
                        "content": text
                    }
                ],
                "max_tokens": 2000,
                "temperature": 0.1
            }
            
            # Make the API request using curl (to avoid additional dependencies)
            import tempfile
            
            # Write payload to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(payload, f)
                payload_file = f.name
            
            try:
                # Use curl to make the request to OpenRouter
                curl_cmd = [
                    'curl', '-s', '-X', 'POST',
                    'https://openrouter.ai/api/v1/chat/completions',
                    '-H', f'Authorization: Bearer {api_key}',
                    '-H', 'Content-Type: application/json',
                    '-H', 'HTTP-Referer: https://github.com/yap-gui',  # Required by OpenRouter
                    '-H', 'X-Title: Yap GUI Translation',  # Optional: helps with tracking
                    '-d', f'@{payload_file}',
                    '--max-time', '60'
                ]
                
                result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=70)
                
                if result.returncode == 0:
                    response_data = json.loads(result.stdout)
                    
                    if 'choices' in response_data and len(response_data['choices']) > 0:
                        translation = response_data['choices'][0]['message']['content'].strip()
                        return translation
                    elif 'error' in response_data:
                        error_msg = response_data['error'].get('message', 'Unknown API error')
                        return f"⚠️ OpenRouter API Error: {error_msg}"
                    else:
                        return "⚠️ Unexpected API response format"
                else:
                    return f"⚠️ Translation request failed: {result.stderr}"
                    
            finally:
                # Clean up temp file
                try:
                    os.unlink(payload_file)
                except:
                    pass
                    
        except json.JSONDecodeError as e:
            return f"⚠️ Invalid API response: {str(e)}"
        except subprocess.TimeoutExpired:
            return "⚠️ Translation request timed out"
        except Exception as e:
            return f"⚠️ Translation error: {str(e)}"
    
    def transcribe_local_video(self):
        file_path = self.local_file_var.get().strip()
        
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid video file")
            return
        
        self.local_transcribe_button.config(state='disabled')
        self.local_progress.start()
        self.local_status_var.set("Transcribing video...")
        self.local_output_text.delete(1.0, tk.END)
        
        thread = threading.Thread(target=self.run_local_transcription, args=(file_path,))
        thread.daemon = True
        thread.start()
    
    def run_local_transcription(self, file_path):
        try:
            output_format = self.local_output_format.get()
            summarize = self.local_summarize_var.get()
            
            # Build yap command with output to file for clean results
            if output_format == "srt":
                output_file = os.path.join(self.output_dir, 
                                         f"{Path(file_path).stem}_captions.srt")
                cmd = ['yap', file_path, '--srt', '-o', output_file]
            else:
                output_file = os.path.join(self.output_dir, 
                                         f"{Path(file_path).stem}_transcript.txt")
                cmd = ['yap', file_path, '-o', output_file]
            
            # Run transcription
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode != 0:
                # If output file wasn't created, try to get error from stderr
                error_msg = result.stderr.strip() or result.stdout.strip() or "Unknown transcription error"
                self.root.after(0, self.on_local_error, f"Transcription failed: {error_msg}")
                return
            
            # Read the clean transcription from the output file
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    transcription_text = f.read().strip()
            except:
                # Fallback to stdout if file reading fails
                transcription_text = result.stdout.strip() or "Transcription completed. Check output directory."
            
            # Process additional features
            if not transcription_text.startswith("Transcription completed"):
                # Format transcription into paragraphs
                formatted_transcription = self.format_text_in_paragraphs(transcription_text)
                
                output_parts = []
                
                # Generate title and summary if requested
                if summarize and transcription_text:
                    self.root.after(0, lambda: self.local_status_var.set("Generating title and summary..."))
                    title, summary = self.generate_title_and_summary(transcription_text)
                    output_parts.append(f"{title}\n{'='*len(title)}")
                
                output_parts.append(f"📝 TRANSCRIPTION:\n{formatted_transcription}")
                
                if self.local_translate_var.get() and transcription_text:
                    self.root.after(0, lambda: self.local_status_var.set("Translating text..."))
                    target_lang = self.local_target_lang.get()
                    translation = self.translate_text(formatted_transcription, target_lang)
                    formatted_translation = self.format_text_in_paragraphs(translation)
                    output_parts.append(f"\n🌍 TRANSLATION ({target_lang.upper()}):\n{formatted_translation}")
                
                if summarize and transcription_text:
                    output_parts.append(f"\n📋 SUMMARY:\n{summary}")
                
                output = "\n\n".join(output_parts) if len(output_parts) > 1 else formatted_transcription
            else:
                output = transcription_text
            
            self.root.after(0, self.on_local_success, output, output_file)
            
        except subprocess.TimeoutExpired:
            self.root.after(0, self.on_local_error, "Transcription timed out")
        except Exception as e:
            self.root.after(0, self.on_local_error, str(e))
    
    def on_youtube_success(self, output):
        self.yt_progress.stop()
        self.yt_download_button.config(state='normal')
        self.yt_status_var.set("Download and transcription completed!")
        
        self.yt_output_text.delete(1.0, tk.END)
        self.yt_output_text.insert(tk.END, output)
    
    def on_youtube_error(self, error):
        self.yt_progress.stop()
        self.yt_download_button.config(state='normal')
        self.yt_status_var.set("Error occurred")
        
        self.yt_output_text.delete(1.0, tk.END)
        self.yt_output_text.insert(tk.END, f"Error: {error}")
        
        messagebox.showerror("Error", f"Operation failed: {error}")
    
    def on_local_success(self, output, output_file):
        self.local_progress.stop()
        self.local_transcribe_button.config(state='normal')
        self.local_status_var.set(f"Transcription saved to {os.path.basename(output_file)}")
        
        self.local_output_text.delete(1.0, tk.END)
        self.local_output_text.insert(tk.END, output)
    
    def on_local_error(self, error):
        self.local_progress.stop()
        self.local_transcribe_button.config(state='normal')
        self.local_status_var.set("Error occurred")
        
        self.local_output_text.delete(1.0, tk.END)
        self.local_output_text.insert(tk.END, f"Error: {error}")
        
        messagebox.showerror("Error", f"Transcription failed: {error}")
    
    def clear_youtube_output(self):
        self.yt_output_text.delete(1.0, tk.END)
        self.yt_status_var.set("Ready")
    
    def clear_local_output(self):
        self.local_output_text.delete(1.0, tk.END)
        self.local_status_var.set("Ready")
    
    def save_local_output(self):
        content = self.local_output_text.get(1.0, tk.END).strip()
        
        if not content:
            messagebox.showwarning("Warning", "No output to save")
            return
        
        # Determine default extension
        ext = ".srt" if self.local_output_format.get() == "srt" else ".txt"
        file_types = [
            ("SRT files", "*.srt") if ext == ".srt" else ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.asksaveasfilename(
            title="Save transcription",
            defaultextension=ext,
            filetypes=file_types,
            initialdir=self.output_dir
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Output saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

def main():
    root = tk.Tk()
    
    # Try to set a nice style
    try:
        style = ttk.Style()
        style.theme_use('aqua')  # macOS native look
    except:
        pass
    
    app = YapGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()