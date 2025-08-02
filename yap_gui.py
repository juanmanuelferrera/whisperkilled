#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import subprocess
import os
import tempfile
import json
import time
from pathlib import Path
from urllib.parse import urlparse
import base64
import hashlib
import sys
import traceback

# Try to import Apple's Translation framework
try:
    import objc
    from Foundation import NSBundle
    
    # Load the Translation framework
    translation_bundle = NSBundle.bundleWithPath_('/System/Library/Frameworks/Translation.framework')
    if translation_bundle:
        objc.loadBundle('Translation', globals(), bundle_path='/System/Library/Frameworks/Translation.framework')
        APPLE_TRANSLATION_AVAILABLE = True
    else:
        APPLE_TRANSLATION_AVAILABLE = False
except ImportError:
    APPLE_TRANSLATION_AVAILABLE = False

class YapGUI:
    def __init__(self, root):
        try:
            self.root = root
            self.root.title("Whisper Killer - YouTube & Video Transcription Tool")
            self.root.geometry("900x800")
            
            # Variables
            self.current_operation = None
            self.output_dir = os.path.expanduser("~/Downloads/yap_output")
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Encryption key based on machine-specific info (safe for GitHub)
            self.encryption_key = self.generate_machine_key()
            
            print("Setting up UI...", file=sys.stderr)
            self.setup_ui()
            print("Loading language preferences...", file=sys.stderr)
            self.load_language_preferences()
            print("Checking dependencies...", file=sys.stderr)
            self.check_dependencies()
            print("Loading API key...", file=sys.stderr)
            self.load_encrypted_api_key()
            print("Whisper Killer initialization complete", file=sys.stderr)
            
        except Exception as e:
            print(f"INIT ERROR: {e}", file=sys.stderr)
            traceback.print_exc()
            raise
        
    def setup_ui(self):
        # Main title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        main_title = ttk.Label(title_frame, text="💀 WHISPER KILLER 🎙️", 
                              font=("Arial", 20, "bold"))
        main_title.pack()
        
        subtitle = ttk.Label(title_frame, text="Privacy-First Transcription & Translation Tool", 
                            font=("Arial", 11), foreground="gray")
        subtitle.pack(pady=(0, 10))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # YouTube Tab
        self.setup_youtube_tab(notebook)
        
        # Local Video Tab
        self.setup_local_video_tab(notebook)
        
        # Text Translation Tab
        self.setup_text_translation_tab(notebook)
        
        # Settings Tab
        self.setup_settings_tab(notebook)
        
    def setup_youtube_tab(self, notebook):
        youtube_frame = ttk.Frame(notebook)
        notebook.add(youtube_frame, text="📺 Online Videos")
        
        main_frame = ttk.Frame(youtube_frame, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL Input
        url_frame = ttk.LabelFrame(main_frame, text="🔗 Video URL (YouTube, Facebook, Vimeo)", padding="10")
        url_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(url_frame, text="Video URL:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.youtube_url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=self.youtube_url_var, width=60)
        url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        paste_button = ttk.Button(url_frame, text="Paste", command=self.paste_url)
        paste_button.pack(side=tk.RIGHT)
        
        # Options
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ Options", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Options
        opts_frame = ttk.Frame(options_frame)
        opts_frame.pack(fill=tk.X)
        
        self.yt_summarize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(opts_frame, text="Generate AI Summary", 
                       variable=self.yt_summarize_var).pack(side=tk.LEFT, padx=(0, 15))
        
        self.yt_translate_var = tk.BooleanVar(value=True)
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
                                 values=self.get_apple_language_list(),
                                 width=8, state="readonly")
        lang_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Language label
        self.yt_lang_label = tk.StringVar(value=self.get_language_name("es"))
        ttk.Label(translate_frame, textvariable=self.yt_lang_label, 
                 font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Update label when language changes
        def update_lang_label(*args):
            self.yt_lang_label.set(self.get_language_name(self.yt_target_lang.get()))
            self.save_language_preferences()  # Save preferences when changed
        self.yt_target_lang.trace_add('write', update_lang_label)
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.yt_download_button = ttk.Button(action_frame, text="🔽 Download & Transcribe", 
                                           command=self.download_and_transcribe,
                                           style="Accent.TButton")
        self.yt_download_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(action_frame, text="🗑️ Clear Output", 
                  command=self.clear_online_video_output).pack(side=tk.LEFT)
        
        # Progress
        self.yt_progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.yt_progress.pack(fill=tk.X, pady=(0, 10))
        
        # Status
        self.yt_status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(main_frame, textvariable=self.yt_status_var, 
                                font=("Arial", 10))
        status_label.pack(pady=(0, 10))
        
        # Output with tabs
        output_frame = ttk.LabelFrame(main_frame, text="📄 Results", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for output tabs
        self.yt_output_notebook = ttk.Notebook(output_frame)
        self.yt_output_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Original transcription tab
        yt_original_frame = ttk.Frame(self.yt_output_notebook)
        self.yt_output_notebook.add(yt_original_frame, text="📝 Original")
        
        yt_orig_button_frame = ttk.Frame(yt_original_frame)
        yt_orig_button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(yt_orig_button_frame, text="📋 Copy", 
                  command=lambda: self.copy_to_clipboard(self.yt_original_text)).pack(side=tk.RIGHT)
        
        self.yt_original_text = scrolledtext.ScrolledText(yt_original_frame, wrap=tk.WORD, 
                                                         height=12, font=("Consolas", 11))
        self.yt_original_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Translation tab
        yt_translation_frame = ttk.Frame(self.yt_output_notebook)
        self.yt_output_notebook.add(yt_translation_frame, text="🌍 Translation")
        
        yt_trans_button_frame = ttk.Frame(yt_translation_frame)
        yt_trans_button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(yt_trans_button_frame, text="📋 Copy", 
                  command=lambda: self.copy_to_clipboard(self.yt_translation_text)).pack(side=tk.RIGHT)
        
        self.yt_translation_text = scrolledtext.ScrolledText(yt_translation_frame, wrap=tk.WORD, 
                                                            height=12, font=("Consolas", 11))
        self.yt_translation_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Original SRT tab
        yt_orig_srt_frame = ttk.Frame(self.yt_output_notebook)
        self.yt_output_notebook.add(yt_orig_srt_frame, text="🎬 Original SRT")
        
        yt_orig_srt_button_frame = ttk.Frame(yt_orig_srt_frame)
        yt_orig_srt_button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(yt_orig_srt_button_frame, text="📋 Copy", 
                  command=lambda: self.copy_to_clipboard(self.yt_orig_srt_text)).pack(side=tk.RIGHT, padx=(0, 5))
        ttk.Button(yt_orig_srt_button_frame, text="💾 Save SRT", 
                  command=lambda: self.save_srt_file(self.yt_orig_srt_text)).pack(side=tk.RIGHT)
        
        self.yt_orig_srt_text = scrolledtext.ScrolledText(yt_orig_srt_frame, wrap=tk.WORD, 
                                                         height=12, font=("Monaco", 10))
        self.yt_orig_srt_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Translated SRT tab
        yt_trans_srt_frame = ttk.Frame(self.yt_output_notebook)
        self.yt_output_notebook.add(yt_trans_srt_frame, text="🌍 Translated SRT")
        
        yt_trans_srt_button_frame = ttk.Frame(yt_trans_srt_frame)
        yt_trans_srt_button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(yt_trans_srt_button_frame, text="📋 Copy", 
                  command=lambda: self.copy_to_clipboard(self.yt_trans_srt_text)).pack(side=tk.RIGHT, padx=(0, 5))
        ttk.Button(yt_trans_srt_button_frame, text="💾 Save SRT", 
                  command=lambda: self.save_srt_file(self.yt_trans_srt_text)).pack(side=tk.RIGHT)
        
        self.yt_trans_srt_text = scrolledtext.ScrolledText(yt_trans_srt_frame, wrap=tk.WORD, 
                                                          height=12, font=("Monaco", 10))
        self.yt_trans_srt_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Summary tab (when enabled)
        yt_summary_frame = ttk.Frame(self.yt_output_notebook)
        self.yt_output_notebook.add(yt_summary_frame, text="📋 Summary")
        
        yt_summ_button_frame = ttk.Frame(yt_summary_frame)
        yt_summ_button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(yt_summ_button_frame, text="📋 Copy", 
                  command=lambda: self.copy_to_clipboard(self.yt_summary_text)).pack(side=tk.RIGHT)
        
        self.yt_summary_text = scrolledtext.ScrolledText(yt_summary_frame, wrap=tk.WORD, 
                                                        height=12, font=("Consolas", 11))
        self.yt_summary_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
    def setup_text_translation_tab(self, notebook):
        text_frame = ttk.Frame(notebook)
        notebook.add(text_frame, text="📝 Text Translation")
        
        main_frame = ttk.Frame(text_frame, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input Section
        input_frame = ttk.LabelFrame(main_frame, text="📄 Input Text", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Text input area
        text_input_frame = ttk.Frame(input_frame)
        text_input_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text widget with scrollbar
        text_frame_inner = ttk.Frame(text_input_frame)
        text_frame_inner.pack(fill=tk.BOTH, expand=True)
        
        self.text_input = tk.Text(text_frame_inner, wrap=tk.WORD, height=10, font=("Arial", 11))
        text_scrollbar = ttk.Scrollbar(text_frame_inner, orient=tk.VERTICAL, command=self.text_input.yview)
        self.text_input.configure(yscrollcommand=text_scrollbar.set)
        
        self.text_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Input buttons frame
        input_buttons_frame = ttk.Frame(input_frame)
        input_buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Paste button
        paste_text_button = ttk.Button(input_buttons_frame, text="📋 Paste Text", 
                                      command=self.paste_text)
        paste_text_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Import file button
        import_file_button = ttk.Button(input_buttons_frame, text="📁 Import File", 
                                       command=self.import_text_file)
        import_file_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        clear_text_button = ttk.Button(input_buttons_frame, text="🗑️ Clear", 
                                      command=self.clear_text_input)
        clear_text_button.pack(side=tk.LEFT)
        
        # Translation Options
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ Translation Options", padding="5")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Language selection
        lang_frame = ttk.Frame(options_frame)
        lang_frame.pack(fill=tk.X)
        
        # Source language selection
        source_lang_frame = ttk.Frame(lang_frame)
        source_lang_frame.pack(fill=tk.X, pady=(0, 2))
        
        ttk.Label(source_lang_frame, text="From:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.text_source_lang = tk.StringVar(value="en")
        source_lang_combo = ttk.Combobox(source_lang_frame, textvariable=self.text_source_lang, 
                                        values=self.get_apple_language_list(), width=15, state="readonly")
        source_lang_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        self.text_source_lang_label = tk.StringVar(value="English")
        ttk.Label(source_lang_frame, textvariable=self.text_source_lang_label, 
                 font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Target language selection
        target_lang_frame = ttk.Frame(lang_frame)
        target_lang_frame.pack(fill=tk.X)
        
        ttk.Label(target_lang_frame, text="To:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.text_target_lang = tk.StringVar(value="es")
        target_lang_combo = ttk.Combobox(target_lang_frame, textvariable=self.text_target_lang, 
                                        values=self.get_apple_language_list(), width=15, state="readonly")
        target_lang_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        self.text_target_lang_label = tk.StringVar(value="Spanish")
        ttk.Label(target_lang_frame, textvariable=self.text_target_lang_label, 
                 font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Update labels when languages change
        def update_text_source_lang_label(*args):
            self.text_source_lang_label.set(self.get_language_name(self.text_source_lang.get()))
            self.save_language_preferences()  # Save preferences when changed
        self.text_source_lang.trace_add('write', update_text_source_lang_label)
        
        def update_text_target_lang_label(*args):
            self.text_target_lang_label.set(self.get_language_name(self.text_target_lang.get()))
            self.save_language_preferences()  # Save preferences when changed
        self.text_target_lang.trace_add('write', update_text_target_lang_label)
        
        # Translation engine options
        engine_frame = ttk.Frame(options_frame)
        engine_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.text_use_apple_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(engine_frame, text="Use Apple Translation Engine", 
                       variable=self.text_use_apple_var).pack(side=tk.LEFT, padx=(0, 15))
        
        self.text_enhance_paragraphs_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(engine_frame, text="Enhance Paragraphs with AI", 
                       variable=self.text_enhance_paragraphs_var).pack(side=tk.LEFT)
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.text_translate_button = ttk.Button(action_frame, text="🔄 Translate Text", 
                                              command=self.translate_input_text)
        self.text_translate_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.text_clear_output_button = ttk.Button(action_frame, text="🗑️ Clear Output", 
                                                 command=self.clear_text_output)
        self.text_clear_output_button.pack(side=tk.LEFT)
        
        # Output Section
        output_frame = ttk.LabelFrame(main_frame, text="📤 Translation Output", padding="5")
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Output notebook for tabs
        self.text_output_notebook = ttk.Notebook(output_frame)
        self.text_output_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Normal translation tab
        normal_translated_frame = ttk.Frame(self.text_output_notebook)
        self.text_output_notebook.add(normal_translated_frame, text="Normal Translation")
        
        # Normal translated text widget with scrollbar
        normal_text_frame = ttk.Frame(normal_translated_frame)
        normal_text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.text_normal_output = tk.Text(normal_text_frame, wrap=tk.WORD, 
                                        height=10, font=("Arial", 11))
        normal_scrollbar = ttk.Scrollbar(normal_text_frame, orient=tk.VERTICAL, 
                                       command=self.text_normal_output.yview)
        self.text_normal_output.configure(yscrollcommand=normal_scrollbar.set)
        
        self.text_normal_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        normal_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Normal translation buttons (inside the tab)
        normal_buttons_frame = ttk.Frame(normal_translated_frame)
        normal_buttons_frame.pack(fill=tk.X, pady=(0, 5))
        
        copy_normal_button = tk.Button(normal_buttons_frame, text="📋 Copy to Clipboard", 
                                     command=lambda: self.copy_to_clipboard(self.text_normal_output),
                                     bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                                     height=2, width=18)
        copy_normal_button.pack(side=tk.LEFT, padx=(0, 10))
        
        save_normal_button = ttk.Button(normal_buttons_frame, text="💾 Save as File", 
                                      command=lambda: self.save_text_file(self.text_normal_output))
        save_normal_button.pack(side=tk.LEFT, padx=(0, 10))
        
        create_org_normal_button = ttk.Button(normal_buttons_frame, text="📝 Create Org File", 
                                            command=lambda: self.create_org_file(self.text_normal_output))
        create_org_normal_button.pack(side=tk.LEFT)
        
        # Enhanced translation tab (with title and emojis)
        enhanced_translated_frame = ttk.Frame(self.text_output_notebook)
        self.text_output_notebook.add(enhanced_translated_frame, text="Enhanced Translation")
        
        # Enhanced translated text widget with scrollbar
        enhanced_text_frame = ttk.Frame(enhanced_translated_frame)
        enhanced_text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.text_enhanced_output = tk.Text(enhanced_text_frame, wrap=tk.WORD, 
                                          height=10, font=("Arial", 11))
        enhanced_scrollbar = ttk.Scrollbar(enhanced_text_frame, orient=tk.VERTICAL, 
                                         command=self.text_enhanced_output.yview)
        self.text_enhanced_output.configure(yscrollcommand=enhanced_scrollbar.set)
        
        self.text_enhanced_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        enhanced_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enhanced translation buttons (inside the tab)
        enhanced_buttons_frame = ttk.Frame(enhanced_translated_frame)
        enhanced_buttons_frame.pack(fill=tk.X, pady=(0, 5))
        
        copy_enhanced_button = tk.Button(enhanced_buttons_frame, text="📋 Copy to Clipboard", 
                                       command=lambda: self.copy_to_clipboard(self.text_enhanced_output),
                                       bg="#2196F3", fg="white", font=("Arial", 11, "bold"),
                                       height=2, width=18)
        copy_enhanced_button.pack(side=tk.LEFT, padx=(0, 10))
        
        save_enhanced_button = ttk.Button(enhanced_buttons_frame, text="💾 Save as File", 
                                        command=lambda: self.save_text_file(self.text_enhanced_output))
        save_enhanced_button.pack(side=tk.LEFT, padx=(0, 10))
        
        create_org_enhanced_button = ttk.Button(enhanced_buttons_frame, text="📝 Create Org File", 
                                              command=lambda: self.create_org_file(self.text_enhanced_output))
        create_org_enhanced_button.pack(side=tk.LEFT)
        
        # Status
        self.text_status_var = tk.StringVar(value="Ready to translate")
        text_status_label = ttk.Label(main_frame, textvariable=self.text_status_var, 
                                     font=("Arial", 9), foreground="gray")
        text_status_label.pack(pady=(5, 0))

    def setup_local_video_tab(self, notebook):
        local_frame = ttk.Frame(notebook)
        notebook.add(local_frame, text="🎬 Local Video")
        
        main_frame = ttk.Frame(local_frame, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="📁 Video File", padding="10")
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
        local_options_frame = ttk.LabelFrame(main_frame, text="⚙️ Options", padding="10")
        local_options_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Options
        local_opts_frame = ttk.Frame(local_options_frame)
        local_opts_frame.pack(fill=tk.X)
        
        self.local_summarize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(local_opts_frame, text="Generate AI Summary", 
                       variable=self.local_summarize_var).pack(side=tk.LEFT, padx=(0, 15))
        
        self.local_translate_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(local_opts_frame, text="Translate text", 
                       variable=self.local_translate_var).pack(side=tk.LEFT)
        
        # Translation options for local video
        local_translate_frame = ttk.Frame(local_options_frame)
        local_translate_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(local_translate_frame, text="Translate to:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.local_target_lang = tk.StringVar(value="es")
        local_lang_combo = ttk.Combobox(local_translate_frame, textvariable=self.local_target_lang, 
                                       values=self.get_apple_language_list(),
                                       width=8, state="readonly")
        local_lang_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        self.local_lang_label = tk.StringVar(value=self.get_language_name("es"))
        ttk.Label(local_translate_frame, textvariable=self.local_lang_label, 
                 font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Update label when language changes
        def update_local_lang_label(*args):
            self.local_lang_label.set(self.get_language_name(self.local_target_lang.get()))
            self.save_language_preferences()  # Save preferences when changed
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
        
        # Output with tabs
        local_output_frame = ttk.LabelFrame(main_frame, text="📄 Results", padding="10")
        local_output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for output tabs
        self.local_output_notebook = ttk.Notebook(local_output_frame)
        self.local_output_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Original transcription tab
        local_original_frame = ttk.Frame(self.local_output_notebook)
        self.local_output_notebook.add(local_original_frame, text="📝 Original")
        
        local_orig_button_frame = ttk.Frame(local_original_frame)
        local_orig_button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(local_orig_button_frame, text="📋 Copy", 
                  command=lambda: self.copy_to_clipboard(self.local_original_text)).pack(side=tk.RIGHT)
        
        self.local_original_text = scrolledtext.ScrolledText(local_original_frame, wrap=tk.WORD, 
                                                            height=12, font=("Consolas", 11))
        self.local_original_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Translation tab
        local_translation_frame = ttk.Frame(self.local_output_notebook)
        self.local_output_notebook.add(local_translation_frame, text="🌍 Translation")
        
        local_trans_button_frame = ttk.Frame(local_translation_frame)
        local_trans_button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(local_trans_button_frame, text="📋 Copy", 
                  command=lambda: self.copy_to_clipboard(self.local_translation_text)).pack(side=tk.RIGHT)
        
        self.local_translation_text = scrolledtext.ScrolledText(local_translation_frame, wrap=tk.WORD, 
                                                               height=12, font=("Consolas", 11))
        self.local_translation_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Original SRT tab
        local_orig_srt_frame = ttk.Frame(self.local_output_notebook)
        self.local_output_notebook.add(local_orig_srt_frame, text="🎬 Original SRT")
        
        local_orig_srt_button_frame = ttk.Frame(local_orig_srt_frame)
        local_orig_srt_button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(local_orig_srt_button_frame, text="📋 Copy", 
                  command=lambda: self.copy_to_clipboard(self.local_orig_srt_text)).pack(side=tk.RIGHT, padx=(0, 5))
        ttk.Button(local_orig_srt_button_frame, text="💾 Save SRT", 
                  command=lambda: self.save_srt_file(self.local_orig_srt_text)).pack(side=tk.RIGHT)
        
        self.local_orig_srt_text = scrolledtext.ScrolledText(local_orig_srt_frame, wrap=tk.WORD, 
                                                            height=12, font=("Monaco", 10))
        self.local_orig_srt_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Translated SRT tab
        local_trans_srt_frame = ttk.Frame(self.local_output_notebook)
        self.local_output_notebook.add(local_trans_srt_frame, text="🌍 Translated SRT")
        
        local_trans_srt_button_frame = ttk.Frame(local_trans_srt_frame)
        local_trans_srt_button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(local_trans_srt_button_frame, text="📋 Copy", 
                  command=lambda: self.copy_to_clipboard(self.local_trans_srt_text)).pack(side=tk.RIGHT, padx=(0, 5))
        ttk.Button(local_trans_srt_button_frame, text="💾 Save SRT", 
                  command=lambda: self.save_srt_file(self.local_trans_srt_text)).pack(side=tk.RIGHT)
        
        self.local_trans_srt_text = scrolledtext.ScrolledText(local_trans_srt_frame, wrap=tk.WORD, 
                                                             height=12, font=("Monaco", 10))
        self.local_trans_srt_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Summary tab (when enabled)
        local_summary_frame = ttk.Frame(self.local_output_notebook)
        self.local_output_notebook.add(local_summary_frame, text="📋 Summary")
        
        local_summ_button_frame = ttk.Frame(local_summary_frame)
        local_summ_button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(local_summ_button_frame, text="📋 Copy", 
                  command=lambda: self.copy_to_clipboard(self.local_summary_text)).pack(side=tk.RIGHT)
        
        self.local_summary_text = scrolledtext.ScrolledText(local_summary_frame, wrap=tk.WORD, 
                                                           height=12, font=("Consolas", 11))
        self.local_summary_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
    def setup_settings_tab(self, notebook):
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="⚙️ Settings")
        
        main_frame = ttk.Frame(settings_frame, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # OpenRouter API Key
        api_frame = ttk.LabelFrame(main_frame, text="🤖 OpenRouter API Key", padding="10")
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
        
        # Translation Architecture Info
        architecture_frame = ttk.LabelFrame(api_frame, text="🔄 Translation Architecture", padding="10")
        architecture_frame.pack(fill=tk.X, pady=(10, 0))
        
        architecture_info = ttk.Label(architecture_frame, 
                                    text="1. 🧠 Smart Analysis: Detects if text has good paragraph structure\n" +
                                         "2. 🍎 Good Structure: Apple Live Translation + minimal AI enhancement\n" +
                                         "3. 🤖 Poor Structure: Full AI translation with smart paragraph creation\n" +
                                         "4. 🔒 Privacy: Prioritizes local translation when structure allows", 
                                    font=("Arial", 9), wraplength=600)
        architecture_info.pack()
        
        # API info
        api_info = ttk.Label(api_frame, text="Enter your OpenRouter API key for title/formatting enhancement. Get one at: https://openrouter.ai/keys\n🔒 Your key is encrypted with machine-specific info - safe for GitHub!", 
                            font=("Arial", 9), wraplength=600)
        api_info.pack(pady=(5, 0))
        
        # Output directory
        output_frame = ttk.LabelFrame(main_frame, text="📂 Output Directory", padding="10")
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
        deps_frame = ttk.LabelFrame(main_frame, text="🔧 Dependencies Status", padding="10")
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
    
    def save_language_preferences(self):
        """Save language preferences to local file"""
        # Don't save if we're currently loading preferences
        if hasattr(self, '_loading_preferences') and self._loading_preferences:
            return
            
        try:
            prefs_file = os.path.join(self.output_dir, '.yap_language_prefs')
            prefs = {
                'text_source_lang': self.text_source_lang.get(),
                'text_target_lang': self.text_target_lang.get(),
                'youtube_target_lang': self.yt_target_lang.get(),
                'local_target_lang': self.local_target_lang.get()
            }
            
            with open(prefs_file, 'w') as f:
                json.dump(prefs, f)
        except Exception as e:
            print(f"Failed to save language preferences: {e}", file=sys.stderr)
    
    def load_language_preferences(self):
        """Load language preferences from local file"""
        try:
            prefs_file = os.path.join(self.output_dir, '.yap_language_prefs')
            if os.path.exists(prefs_file):
                with open(prefs_file, 'r') as f:
                    prefs = json.load(f)
                    
                    # Temporarily disable automatic saving
                    self._loading_preferences = True
                    
                    # Set text translation preferences
                    if 'text_source_lang' in prefs:
                        self.text_source_lang.set(prefs['text_source_lang'])
                    if 'text_target_lang' in prefs:
                        self.text_target_lang.set(prefs['text_target_lang'])
                    
                    # Set YouTube translation preferences
                    if 'youtube_target_lang' in prefs:
                        self.yt_target_lang.set(prefs['youtube_target_lang'])
                    
                    # Set local video translation preferences
                    if 'local_target_lang' in prefs:
                        self.local_target_lang.set(prefs['local_target_lang'])
                    
                    # Re-enable automatic saving
                    self._loading_preferences = False
                        
        except Exception as e:
            print(f"Failed to load language preferences: {e}", file=sys.stderr)
            self._loading_preferences = False
    
    def paste_url(self):
        try:
            clipboard_content = self.root.clipboard_get()
            if clipboard_content:
                self.youtube_url_var.set(clipboard_content.strip())
        except:
            pass
    
    def paste_text(self):
        """Paste text from clipboard"""
        try:
            text = self.root.clipboard_get()
            self.text_input.delete(1.0, tk.END)
            self.text_input.insert(1.0, text)
        except:
            messagebox.showwarning("Warning", "No text found in clipboard")
    
    def import_text_file(self):
        """Import text from file"""
        file_path = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_input.delete(1.0, tk.END)
                    self.text_input.insert(1.0, content)
                    self.text_status_var.set(f"Imported: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import file: {str(e)}")
    
    def clear_text_input(self):
        """Clear the text input area"""
        self.text_input.delete(1.0, tk.END)
        self.text_status_var.set("Input cleared")
    
    def clear_text_output(self):
        """Clear the text output areas"""
        self.text_normal_output.delete(1.0, tk.END)
        self.text_enhanced_output.delete(1.0, tk.END)
        self.text_status_var.set("Output cleared")
    
    def translate_input_text(self):
        """Translate the input text"""
        text = self.text_input.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to translate")
            return
        
        source_lang = self.text_source_lang.get()
        target_lang = self.text_target_lang.get()
        use_apple = self.text_use_apple_var.get()
        enhance_paragraphs = self.text_enhance_paragraphs_var.get()
        
        # Disable translate button during processing
        self.text_translate_button.config(state='disabled')
        self.text_status_var.set("Translating...")
        
        # Run translation in a separate thread
        def translate_thread():
            try:
                # Generate normal translation (without title/emojis)
                if use_apple:
                    normal_result = self.translate_with_apple_live_translation(text, source_lang, target_lang)
                    if normal_result.startswith("⚠️"):
                        normal_result = self.translate_with_local_tool_fallback(text, source_lang, target_lang)
                else:
                    # For AI-only, get the translation without title
                    normal_result = self.translate_with_apple_live_translation(text, source_lang, target_lang)
                    if normal_result.startswith("⚠️"):
                        normal_result = self.translate_with_local_tool_fallback(text, source_lang, target_lang)
                
                # Generate enhanced translation (with title and emojis)
                if enhance_paragraphs:
                    enhanced_result = self.translate_locally_then_enhance(text, source_lang, target_lang)
                else:
                    enhanced_result = self.translate_with_title_and_paragraphs(text, source_lang, target_lang)
                
                # Update UI in main thread
                self.root.after(0, lambda: self.on_text_translation_complete(normal_result, enhanced_result))
                
            except Exception as e:
                error_msg = f"Translation error: {str(e)}"
                self.root.after(0, lambda: self.on_text_translation_error(error_msg))
        
        threading.Thread(target=translate_thread, daemon=True).start()
    
    def on_text_translation_complete(self, normal_result, enhanced_result):
        """Handle completion of text translation"""
        # Update normal translation output
        self.text_normal_output.delete(1.0, tk.END)
        self.text_normal_output.insert(1.0, normal_result)
        
        # Update enhanced translation output
        self.text_enhanced_output.delete(1.0, tk.END)
        self.text_enhanced_output.insert(1.0, enhanced_result)
        
        self.text_translate_button.config(state='normal')
        self.text_status_var.set("Translation completed - Both versions ready")
    
    def on_text_translation_error(self, error_msg):
        """Handle text translation error"""
        self.text_normal_output.delete(1.0, tk.END)
        self.text_normal_output.insert(1.0, error_msg)
        self.text_enhanced_output.delete(1.0, tk.END)
        self.text_enhanced_output.insert(1.0, error_msg)
        self.text_translate_button.config(state='normal')
        self.text_status_var.set("Translation failed")
    
    def get_apple_language_list(self):
        """Get list of Apple Live Translation supported languages"""
        return [
            "en", "es", "fr", "de", "it", "pt", "ja", "ko", "zh", "zh-TW", "ru", "ar",
            "nl", "pl", "tr", "th", "vi", "hi", "id", "ms", "sv", "da", "no", "fi",
            "cs", "sk", "hu", "ro", "bg", "hr", "sl", "et", "lv", "lt", "el", "he",
            "fa", "ur", "bn", "ta", "te", "mr", "gu", "kn", "ml", "pa", "si", "my",
            "km", "lo", "ka", "am", "sw", "zu", "af", "is", "mt", "cy", "ga", "eu",
            "ca", "gl", "sq", "mk", "sr", "bs", "me", "mn", "ky", "uz", "kk", "tg",
            "tk", "az", "hy", "ne", "dz", "bo", "ug", "ps", "sd", "ks"
        ]
    
    def get_language_name(self, code):
        """Get language name from code"""
        lang_names = {
            "en": "English", "es": "Spanish", "fr": "French", "de": "German", "it": "Italian",
            "pt": "Portuguese", "ja": "Japanese", "ko": "Korean", "zh": "Chinese (Simplified)",
            "zh-TW": "Chinese (Traditional)", "ru": "Russian", "ar": "Arabic", "nl": "Dutch",
            "pl": "Polish", "tr": "Turkish", "th": "Thai", "vi": "Vietnamese", "hi": "Hindi",
            "id": "Indonesian", "ms": "Malay", "sv": "Swedish", "da": "Danish", "no": "Norwegian",
            "fi": "Finnish", "cs": "Czech", "sk": "Slovak", "hu": "Hungarian", "ro": "Romanian",
            "bg": "Bulgarian", "hr": "Croatian", "sl": "Slovenian", "et": "Estonian", "lv": "Latvian",
            "lt": "Lithuanian", "el": "Greek", "he": "Hebrew", "fa": "Persian", "ur": "Urdu",
            "bn": "Bengali", "ta": "Tamil", "te": "Telugu", "mr": "Marathi", "gu": "Gujarati",
            "kn": "Kannada", "ml": "Malayalam", "pa": "Punjabi", "si": "Sinhala", "my": "Burmese",
            "km": "Khmer", "lo": "Lao", "ka": "Georgian", "am": "Amharic", "sw": "Swahili",
            "zu": "Zulu", "af": "Afrikaans", "is": "Icelandic", "mt": "Maltese", "cy": "Welsh",
            "ga": "Irish", "eu": "Basque", "ca": "Catalan", "gl": "Galician", "sq": "Albanian",
            "mk": "Macedonian", "sr": "Serbian", "bs": "Bosnian", "me": "Montenegrin",
            "mn": "Mongolian", "ky": "Kyrgyz", "uz": "Uzbek", "kk": "Kazakh", "tg": "Tajik",
            "tk": "Turkmen", "az": "Azerbaijani", "hy": "Armenian", "ne": "Nepali", "dz": "Dzongkha",
            "bo": "Tibetan", "ug": "Uyghur", "ps": "Pashto", "sd": "Sindhi", "ks": "Kashmiri"
        }
        return lang_names.get(code, code)
    
    def get_apple_lang_code(self, code):
        """Get Apple language code from short code"""
        apple_codes = {
            "en": "en-US", "es": "es-ES", "fr": "fr-FR", "de": "de-DE", "it": "it-IT",
            "pt": "pt-PT", "ja": "ja-JP", "ko": "ko-KR", "zh": "zh-CN", "zh-TW": "zh-TW",
            "ru": "ru-RU", "ar": "ar-SA", "nl": "nl-NL", "pl": "pl-PL", "tr": "tr-TR",
            "th": "th-TH", "vi": "vi-VN", "hi": "hi-IN", "id": "id-ID", "ms": "ms-MY",
            "sv": "sv-SE", "da": "da-DK", "no": "no-NO", "fi": "fi-FI", "cs": "cs-CZ",
            "sk": "sk-SK", "hu": "hu-HU", "ro": "ro-RO", "bg": "bg-BG", "hr": "hr-HR",
            "sl": "sl-SI", "et": "et-EE", "lv": "lv-LV", "lt": "lt-LT", "el": "el-GR",
            "he": "he-IL", "fa": "fa-IR", "ur": "ur-PK", "bn": "bn-BD", "ta": "ta-IN",
            "te": "te-IN", "mr": "mr-IN", "gu": "gu-IN", "kn": "kn-IN", "ml": "ml-IN",
            "pa": "pa-IN", "si": "si-LK", "my": "my-MM", "km": "km-KH", "lo": "lo-LA",
            "ka": "ka-GE", "am": "am-ET", "sw": "sw-TZ", "zu": "zu-ZA", "af": "af-ZA",
            "is": "is-IS", "mt": "mt-MT", "cy": "cy-GB", "ga": "ga-IE", "eu": "eu-ES",
            "ca": "ca-ES", "gl": "gl-ES", "sq": "sq-AL", "mk": "mk-MK", "sr": "sr-RS",
            "bs": "bs-BA", "me": "me-ME", "mn": "mn-MN", "ky": "ky-KG", "uz": "uz-UZ",
            "kk": "kk-KZ", "tg": "tg-TJ", "tk": "tk-TM", "az": "az-AZ", "hy": "hy-AM",
            "ne": "ne-NP", "dz": "dz-BT", "bo": "bo-CN", "ug": "ug-CN", "ps": "ps-AF",
            "sd": "sd-PK", "ks": "ks-IN"
        }
        return apple_codes.get(code, code)
    
    def save_text_file(self, text_widget):
        """Save text widget content to file"""
        content = text_widget.get(1.0, tk.END).strip()
        
        if not content:
            messagebox.showwarning("Warning", "No content to save")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Translation",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                messagebox.showinfo("Success", f"Translation saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def create_org_file(self, text_widget):
        """Create an Org mode file from text widget content"""
        content = text_widget.get(1.0, tk.END).strip()
        
        if not content:
            messagebox.showwarning("Warning", "No content to convert to Org file")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Create Org File",
            defaultextension=".org",
            filetypes=[
                ("Org files", "*.org"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Convert content to Org mode format
                org_content = self.convert_to_org_format(content)
                
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(org_content)
                messagebox.showinfo("Success", f"Org file created at:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create Org file: {str(e)}")
    
    def convert_to_org_format(self, content):
        """Convert plain text content to Org mode format"""
        lines = content.split('\n')
        org_lines = []
        
        # Add header
        org_lines.append("#+TITLE: Translation")
        org_lines.append(f"#+DATE: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        org_lines.append("")
        
        # Process content
        for line in lines:
            line = line.strip()
            if not line:
                org_lines.append("")
                continue
            
            # Check if line looks like a title (starts with emoji or is short)
            if (line.startswith(('🌟', '✨', '🎯', '📝', '🌍', '🔍', '✅', '⚠️', '🚀', '📋', '💾', '📝')) or 
                len(line) < 100 and line.endswith((':', '!', '?'))):
                # Convert to Org heading
                org_lines.append(f"* {line}")
            elif line.startswith('=') and line.endswith('='):
                # This is already a separator line, convert to Org separator
                org_lines.append("")
                org_lines.append("---")
                org_lines.append("")
            else:
                # Regular paragraph
                org_lines.append(line)
        
        return '\n'.join(org_lines)
    
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
    
    def copy_to_clipboard(self, text_widget):
        """Copy content from text widget to clipboard"""
        try:
            content = text_widget.get(1.0, tk.END).strip()
            if content:
                self.root.clipboard_clear()
                self.root.clipboard_append(content)
                # Brief feedback
                self.root.after(0, lambda: messagebox.showinfo("Copied", "Content copied to clipboard!"))
            else:
                messagebox.showwarning("Warning", "No content to copy")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy: {e}")
    
    def save_srt_file(self, text_widget):
        """Save SRT content to file"""
        try:
            content = text_widget.get(1.0, tk.END).strip()
            if not content or content == "No content available for SRT generation":
                messagebox.showwarning("Warning", "No SRT content to save")
                return
            
            filename = filedialog.asksaveasfilename(
                title="Save SRT Subtitles",
                defaultextension=".srt",
                filetypes=[("SRT files", "*.srt"), ("All files", "*.*")],
                initialdir=self.output_dir
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Success", f"SRT file saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save SRT file: {e}")
    
    def download_and_transcribe(self):
        url = self.youtube_url_var.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a video URL")
            return
        
        if not self.is_valid_video_url(url):
            messagebox.showerror("Error", "Please enter a valid URL from YouTube, Facebook, or Vimeo")
            return
        
        self.yt_download_button.config(state='disabled')
        self.yt_progress.start()
        self.yt_status_var.set("Starting download...")
        # Clear all online video output tabs
        self.yt_original_text.delete(1.0, tk.END)
        self.yt_translation_text.delete(1.0, tk.END)
        self.yt_orig_srt_text.delete(1.0, tk.END)
        self.yt_trans_srt_text.delete(1.0, tk.END)
        self.yt_summary_text.delete(1.0, tk.END)
        
        thread = threading.Thread(target=self.run_online_video_transcription, args=(url,))
        thread.daemon = True
        thread.start()
    
    def get_platform_from_url(self, url):
        """Detect the platform from the URL"""
        url_lower = url.lower()
        if any(domain in url_lower for domain in ['youtube.com', 'youtu.be']):
            return 'YouTube'
        elif any(domain in url_lower for domain in ['facebook.com', 'fb.com']):
            return 'Facebook'
        elif any(domain in url_lower for domain in ['vimeo.com']):
            return 'Vimeo'
        else:
            return 'Unknown'
    
    def is_valid_video_url(self, url):
        parsed = urlparse(url)
        # YouTube URLs
        youtube_domains = ['www.youtube.com', 'youtube.com', 'youtu.be']
        # Facebook URLs
        facebook_domains = ['www.facebook.com', 'facebook.com', 'fb.com', 'www.fb.com']
        # Vimeo URLs
        vimeo_domains = ['www.vimeo.com', 'vimeo.com', 'player.vimeo.com']
        
        # Check if URL contains any of the supported platforms
        return (parsed.netloc in youtube_domains + facebook_domains + vimeo_domains or
                any(domain in url for domain in ['youtube.com', 'youtu.be', 'facebook.com', 'fb.com', 'vimeo.com']))
    
    def run_online_video_transcription(self, url):
        try:
            summarize = self.yt_summarize_var.get()
            keep_audio = self.yt_keep_audio_var.get()
            platform = self.get_platform_from_url(url)
            
            # Step 1: Download and transcribe with separate commands for cleaner output
            self.root.after(0, lambda: self.yt_status_var.set(f"Downloading {platform} video and extracting audio..."))
            
            # First, download the audio
            download_cmd = ['yt-dlp', url, '-x', '--audio-format', 'wav', 
                           '--output', f'{self.output_dir}/%(title)s.%(ext)s']
            
            download_result = subprocess.run(download_cmd, capture_output=True, text=True, timeout=300)
            
            if download_result.returncode != 0:
                self.root.after(0, self.on_online_video_error, f"{platform} download failed: {download_result.stderr}")
                return
            
            # Find the downloaded audio file
            audio_files = list(Path(self.output_dir).glob("*.wav"))
            if not audio_files:
                self.root.after(0, self.on_online_video_error, f"No audio file found after {platform} download")
                return
            
            # Use the most recent audio file
            audio_file = max(audio_files, key=os.path.getctime)
            
            # Step 2: Transcribe the audio
            self.root.after(0, lambda: self.yt_status_var.set("Transcribing audio..."))
            
            yap_cmd = ['yap', str(audio_file)]
            output_file = audio_file.with_suffix('.txt')
            yap_cmd.extend(['-o', str(output_file)])
            
            yap_result = subprocess.run(yap_cmd, capture_output=True, text=True, timeout=300)
            
            if yap_result.returncode != 0:
                self.root.after(0, self.on_online_video_error, f"{platform} transcription failed: {yap_result.stderr}")
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
            
            # Prepare results dictionary
            results = {
                'original': formatted_transcription,
                'original_srt': self.create_srt_from_text(formatted_transcription)
            }
            
            # Generate translation if requested
            if self.yt_translate_var.get() and transcription_text:
                self.root.after(0, lambda: self.yt_status_var.set("Translating text..."))
                target_lang = self.yt_target_lang.get()
                # For online videos, assume source language is English (most common)
                source_lang = "en"
                translation = self.translate_text(formatted_transcription, source_lang, target_lang)
                results['translation'] = translation
                results['translated_srt'] = self.create_srt_from_text(translation, is_translation=True)
            
            # Generate summary if requested  
            if summarize and transcription_text:
                self.root.after(0, lambda: self.yt_status_var.set("Generating title and summary..."))
                title, summary = self.generate_title_and_summary(transcription_text)
                results['summary'] = f"{title}\n{summary}"
            
            self.root.after(0, self.on_online_video_success, results)
            
        except subprocess.TimeoutExpired:
            self.root.after(0, self.on_online_video_error, f"{platform} operation timed out")
        except Exception as e:
            self.root.after(0, self.on_online_video_error, f"{platform} error: {str(e)}")
    
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
    
    def create_srt_from_text(self, text, is_translation=False):
        """Convert text to SRT subtitle format"""
        if not text or text.startswith("⚠️"):
            return "No content available for SRT generation"
        
        # Clean text and split into sentences
        clean_text = text
        if is_translation and "TITLE:" in text:
            # Extract just the translation part
            lines = text.split('\n')
            translation_lines = []
            found_translation = False
            for line in lines:
                if line.startswith("TRANSLATION:"):
                    found_translation = True
                elif found_translation and line.strip() and not line.startswith("="):
                    translation_lines.append(line.strip())
            clean_text = ' '.join(translation_lines) if translation_lines else text
        
        # Split into sentences for SRT timing
        sentences = []
        for delimiter in ['. ', '! ', '? ']:
            clean_text = clean_text.replace(delimiter, delimiter + '|SPLIT|')
        
        raw_sentences = clean_text.split('|SPLIT|')
        for sentence in raw_sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 10:  # Only include substantial sentences
                sentences.append(sentence)
        
        if not sentences:
            return "No suitable content for SRT generation"
        
        # Generate SRT format
        srt_content = ""
        duration_per_subtitle = 4  # 4 seconds per subtitle
        
        for i, sentence in enumerate(sentences):
            start_time = i * duration_per_subtitle
            end_time = (i + 1) * duration_per_subtitle
            
            # Format time as SRT timestamp (HH:MM:SS,mmm)
            def format_time(seconds):
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                secs = seconds % 60
                return f"{hours:02d}:{minutes:02d}:{secs:02d},000"
            
            start_srt = format_time(start_time)
            end_srt = format_time(end_time)
            
            # Add subtitle entry
            srt_content += f"{i+1}\n{start_srt} --> {end_srt}\n{sentence.strip()}\n\n"
        
        return srt_content.strip()
    
    def generate_title_and_summary(self, text):
        """Generate title with emojis and article-style summary using OpenRouter API"""
        try:
            api_key = os.environ.get('OPENROUTER_API_KEY') or self.openrouter_api_key.get().strip()
            
            if not api_key:
                return "⚠️ OpenRouter API key required for AI summaries.\n\nPlease enter your API key in Settings tab."
            
            model = self.translation_model.get()
            
            # Generate article-style summary with title and content
            article_payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system", 
                        "content": """You are an expert content writer specializing in creating engaging article summaries. Create a concise article (maximum 200 words) with:

1. Create a catchy, relevant title with 2-3 emojis based on the transcript content
2. Write a concise summary in 2-3 clear paragraphs:
   - Focus on the main points and key information
   - Use engaging, natural prose
   - Keep the total word count to a maximum of 200 words
   - Make the content informative and easy to read
   - Preserve important details and technical terms
3. DO NOT include any labels, qualifiers, or prefixes like "TITLE:", "SUMMARY:", "ARTICLE:", etc.

Return ONLY the content in this format:
[Title with emojis]

[First paragraph - main topic or introduction]

[Second paragraph - key points or details]

[Third paragraph - additional information or conclusion if needed]"""
                    },
                    {
                        "role": "user", 
                        "content": text
                    }
                ],
                "max_tokens": 600,
                "temperature": 0.2
            }
            
            result = self.make_openrouter_request(article_payload)
            
            if result.startswith("⚠️"):
                return "⚠️ API Error", result
            
            # Parse the result to extract title and summary (no labels expected)
            lines = result.split('\n')
            title = ""
            summary_lines = []
            
            # First non-empty line is the title
            for line in lines:
                if line.strip():
                    title = line.strip()
                    break
            
            # All subsequent non-empty lines are the summary content
            for line in lines[1:]:
                if line.strip():
                    summary_lines.append(line.strip())
            
            if title and summary_lines:
                summary_text = '\n\n'.join([line for line in summary_lines if line])
                return title, summary_text
            else:
                # Fallback: just return the result as-is if parsing fails
                return "Summary", result
                
        except Exception as e:
            return "Summary Error", f"Summary error: {str(e)}"
    
    def make_openrouter_request(self, payload):
        """Make a request to OpenRouter API"""
        try:
            api_key = os.environ.get('OPENROUTER_API_KEY') or self.openrouter_api_key.get().strip()
            
            import tempfile
            import json
            
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
                    '-H', 'HTTP-Referer: https://github.com/yap-gui',
                    '-H', 'X-Title: Yap GUI AI Summary',
                    '-d', f'@{payload_file}',
                    '--max-time', '60'
                ]
                
                result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=70)
                
                if result.returncode == 0:
                    response_data = json.loads(result.stdout)
                    
                    if 'choices' in response_data and len(response_data['choices']) > 0:
                        return response_data['choices'][0]['message']['content'].strip()
                    elif 'error' in response_data:
                        error_msg = response_data['error'].get('message', 'Unknown API error')
                        return f"⚠️ OpenRouter API Error: {error_msg}"
                    else:
                        return "⚠️ Unexpected API response format"
                else:
                    return f"⚠️ API request failed: {result.stderr}"
                    
            finally:
                # Clean up temp file
                try:
                    os.unlink(payload_file)
                except:
                    pass
                    
        except json.JSONDecodeError as e:
            return f"⚠️ Invalid API response: {str(e)}"
        except subprocess.TimeoutExpired:
            return "⚠️ API request timed out"
        except Exception as e:
            return f"⚠️ API error: {str(e)}"
    
    def has_good_paragraph_structure(self, text):
        """Analyze if text already has good paragraph structure"""
        paragraphs = text.split('\n\n')
        
        # Remove empty paragraphs
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        # Check various indicators of good paragraph structure
        if len(paragraphs) < 2:
            return False  # Single block of text
        
        # Check if paragraphs have reasonable length (not too short or too long)
        word_counts = [len(p.split()) for p in paragraphs]
        avg_words = sum(word_counts) / len(word_counts)
        
        # Good paragraphs: 10-250 words on average (more flexible)
        if avg_words < 10 or avg_words > 250:
            return False
        
        # Check for variety in paragraph lengths (more lenient)
        min_words, max_words = min(word_counts), max(word_counts)
        variety_ratio = max_words / min_words if min_words > 0 else 1
        
        # Check for mixed structure (very short and very long paragraphs)
        short_paragraphs = sum(1 for count in word_counts if count < 10)  # Reduced threshold
        long_paragraphs = sum(1 for count in word_counts if count > 40)  # Back to 40 for better detection
        
        # If we have both very short and very long paragraphs, it's mixed structure
        if short_paragraphs > 0 and long_paragraphs > 0:
            return False
        
        # More flexible variety check - allow similar lengths for well-structured content
        if variety_ratio < 1.1:  # Reduced from 1.3 to 1.1
            # Additional check: if paragraphs are very similar in length but have good punctuation
            proper_endings = sum(1 for p in paragraphs if p.rstrip().endswith(('.', '!', '?', ':')))
            if proper_endings / len(paragraphs) >= 0.8:  # High punctuation quality
                return True
            return False
        
        # Check if paragraphs end with proper punctuation (more lenient)
        proper_endings = sum(1 for p in paragraphs if p.rstrip().endswith(('.', '!', '?', ':')))
        if proper_endings / len(paragraphs) < 0.5:  # Reduced from 0.6 to 0.5
            return False
        
        return True
    
    def translate_locally_then_enhance(self, text, source_lang, target_lang):
        """Hybrid approach: Preserve good paragraphs or create smart ones with AI"""
        try:
            # Step 1: Analyze paragraph structure
            has_good_paragraphs = self.has_good_paragraph_structure(text)
            
            if has_good_paragraphs:
                # Good structure exists - use local translation + minimal enhancement
                local_translation = self.translate_with_apple_live_translation(text, source_lang, target_lang)
                
                if local_translation.startswith("⚠️"):
                    # If local translation fails, fallback to full OpenRouter translation
                    return self.translate_with_title_and_paragraphs(text, source_lang, target_lang)
                
                # Use OpenRouter only for title generation and formatting
                return self.enhance_translation_with_openrouter(local_translation, target_lang)
            
            else:
                # Poor structure - use full OpenRouter for smart paragraph creation
                print("Poor paragraph structure detected, using AI for smart paragraphs", file=sys.stderr)
                return self.translate_with_title_and_paragraphs(text, source_lang, target_lang)
            
        except Exception as e:
            return f"⚠️ Translation error: {str(e)}"
    
    def translate_with_apple_live_translation(self, text, source_lang, target_lang):
        """Use Apple's native Live Translation framework"""
        try:
            if not APPLE_TRANSLATION_AVAILABLE:
                return self.translate_with_local_tool_fallback(text, source_lang, target_lang)
            
            # Try to use Apple's Translation framework
            try:
                # Import Translation framework classes
                from Translation import _LTTranslator
                
                # Create translator instance
                translator = _LTTranslator.alloc().init()
                
                # Get Apple language codes
                source_code = self.get_apple_lang_code(source_lang)
                target_code = self.get_apple_lang_code(target_lang)
                
                # Split text by paragraphs to preserve structure
                paragraphs = text.split('\n\n')
                translated_chunks = []
                
                for paragraph in paragraphs:
                    if not paragraph.strip():
                        continue
                    
                    # Translate with Apple's framework
                    translated = translator.translateText_fromLocale_toLocale_(
                        paragraph.strip(), source_code, target_code)
                    
                    if translated:
                        translated_chunks.append(str(translated))
                    else:
                        translated_chunks.append(paragraph.strip())
                
                # Combine translated paragraphs
                full_translation = '\n\n'.join(translated_chunks)
                return full_translation
                
            except Exception as e:
                print(f"Apple Translation error: {e}", file=sys.stderr)
                return self.translate_with_local_tool_fallback(text, source_lang, target_lang)
                
        except Exception as e:
            return f"⚠️ Apple Translation error: {str(e)}"
    
    def translate_with_local_tool_fallback(self, text, source_lang, target_lang):
        """Fallback to translate-shell when Apple Translation is not available"""
        try:
            # Check if translate-shell is available
            try:
                result = subprocess.run(['/opt/homebrew/bin/trans', '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode != 0:
                    return "⚠️ translate-shell not available. Install with: brew install translate-shell"
            except:
                return "⚠️ Cannot check translate-shell availability."
            
            # Language mapping for translate-shell
            translate_lang_codes = {
                "en": "en", "es": "es", "fr": "fr", "de": "de", "it": "it",
                "pt": "pt", "ja": "ja", "ko": "ko", 
                "zh": "zh", "ru": "ru", "ar": "ar"
            }
            
            target_code = translate_lang_codes.get(target_lang, target_lang)
            
            # Split text by paragraphs to preserve structure
            paragraphs = text.split('\n\n')
            max_chunk_size = 4000  # Conservative limit for command line
            chunks = []
            
            for paragraph in paragraphs:
                paragraph = paragraph.strip()
                if not paragraph:
                    continue
                    
                # If paragraph is too long, split it by sentences
                if len(paragraph) > max_chunk_size:
                    sentences = paragraph.replace('. ', '.\n').split('\n')
                    current_chunk = []
                    current_size = 0
                    
                    for sentence in sentences:
                        sentence = sentence.strip()
                        if not sentence:
                            continue
                            
                        sentence_size = len(sentence) + 1
                        if current_size + sentence_size > max_chunk_size and current_chunk:
                            chunks.append(' '.join(current_chunk))
                            current_chunk = [sentence]
                            current_size = sentence_size
                        else:
                            current_chunk.append(sentence)
                            current_size += sentence_size
                    
                    if current_chunk:
                        chunks.append(' '.join(current_chunk))
                else:
                    chunks.append(paragraph)
            
            # Translate each chunk
            translated_chunks = []
            for i, chunk in enumerate(chunks):
                try:
                    # Use translate-shell command with auto-detection for source language
                    if target_code == 'en':
                        # When translating TO English, auto-detect source language
                        cmd = ['/opt/homebrew/bin/trans', '-b', f':{target_code}']
                    else:
                        # When translating FROM English, specify English as source
                        cmd = ['/opt/homebrew/bin/trans', '-b', f'en:{target_code}']
                    result = subprocess.run(cmd, input=chunk, capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0 and result.stdout.strip():
                        translated_chunks.append(result.stdout.strip())
                    else:
                        return f"⚠️ Local translation failed for chunk {i+1}: {result.stderr}"
                        
                except subprocess.TimeoutExpired:
                    return f"⚠️ Translation timeout for chunk {i+1}"
                except Exception as e:
                    return f"⚠️ Translation error for chunk {i+1}: {str(e)}"
            
            # Combine all translated chunks preserving paragraph structure
            full_translation = '\n\n'.join(translated_chunks)
            return full_translation
            
        except Exception as e:
            return f"⚠️ Local translation error: {str(e)}"
    
    def enhance_translation_with_openrouter(self, translated_text, target_lang):
        """Use OpenRouter only for title generation and paragraph formatting of already-translated text"""
        try:
            api_key = os.environ.get('OPENROUTER_API_KEY') or self.openrouter_api_key.get().strip()
            
            if not api_key:
                # Return the translation without enhancement if no API key
                return translated_text
            
            # Get language name
            target_lang_name = self.get_language_name(target_lang)
            model = self.translation_model.get()
            
            # Enhanced prompt for creating an article with title, emojis, and prose paragraphs (max 200 words)
            enhancement_prompt = f"""You are an expert content writer and editor specializing in creating engaging articles. The text below is ALREADY translated to {target_lang_name}.

Your task is to create a concise article (maximum 200 words) with:
1. Create a catchy, relevant title with 2-3 emojis based on the content (in {target_lang_name})
2. Write the content in clear, engaging prose with well-structured paragraphs:
   - Break the content into 2-4 coherent paragraphs
   - Each paragraph should focus on a specific aspect or theme
   - Use smooth transitions between paragraphs
   - Write in a natural, flowing style that's easy to read
   - Maintain the key information and main points from the original
3. DO NOT retranslate - only restructure and enhance the existing translation
4. Keep the total word count to a maximum of 200 words
5. Preserve important details, names, numbers, and technical terms
6. Make the content engaging and informative while being concise
7. DO NOT include any labels, qualifiers, or prefixes like "TITLE:", "ARTICLE:", "TRANSLATION:", "SUMMARY:", etc.

Return ONLY the content in this format:
[Title with emojis]

[First paragraph - introduction or main topic, engaging opening]

[Second paragraph - supporting details or development of ideas]

[Third paragraph - additional points or conclusion if needed]

Here is the already-translated text to create an article from:"""
            
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system", 
                        "content": enhancement_prompt
                    },
                    {
                        "role": "user", 
                        "content": translated_text
                    }
                ],
                "max_tokens": 2500,
                "temperature": 0.3
            }
            
            result = self.make_openrouter_request(payload)
            
            # Parse the result to extract title and formatted text
            if result.startswith("⚠️"):
                # Return local translation if enhancement fails
                return translated_text
            
            # Extract title and article content (no labels expected)
            lines = result.split('\n')
            title = ""
            article_lines = []
            
            # First non-empty line is the title
            for line in lines:
                if line.strip():
                    title = line.strip()
                    break
            
            # All subsequent non-empty lines are the article content
            for line in lines[1:]:
                if line.strip():
                    article_lines.append(line.strip())
            
            if title and article_lines:
                article_text = '\n\n'.join([line for line in article_lines if line])
                # Return just the title and content without any labels
                return f"{title}\n\n{article_text}"
            else:
                # Fallback: return the local translation without any labels
                return translated_text
                
        except Exception as e:
            # Return local translation if enhancement fails
            return translated_text

    def translate_with_title_and_paragraphs(self, text, source_lang, target_lang):
        """Translate text with title generation and paragraph formatting using OpenRouter API (fallback method)"""
        try:
            api_key = os.environ.get('OPENROUTER_API_KEY') or self.openrouter_api_key.get().strip()
            
            if not api_key:
                return f"⚠️ OpenRouter API key required.\n\nPlease enter your API key in Settings tab or set OPENROUTER_API_KEY environment variable.\n\nGet a key at: https://openrouter.ai/keys"
            
            # Get language names
            source_lang_name = self.get_language_name(source_lang)
            target_lang_name = self.get_language_name(target_lang)
            model = self.translation_model.get()
            
            # Enhanced prompt for creating an article with translation, title, and emojis (max 200 words)
            enhanced_prompt = f"""You are a professional translator and expert content writer specializing in creating engaging articles. Please:

1. Create a catchy, relevant title with 2-3 emojis based on the content (in {target_lang_name})
2. Translate the entire text from {source_lang_name} to {target_lang_name} with high accuracy and natural flow
3. Create a concise article (maximum 200 words) with clear, engaging prose:
   - Break the content into 2-4 coherent paragraphs
   - Each paragraph should focus on a specific aspect or theme
   - Use smooth transitions between paragraphs
   - Write in a natural, flowing style that's easy to read
   - Maintain the key information and main points from the original
4. Keep the total word count to a maximum of 200 words
5. Preserve important details, names, numbers, and technical terms
6. Make the content engaging and informative while being concise
7. DO NOT include any labels, qualifiers, or prefixes like "TITLE:", "ARTICLE:", "TRANSLATION:", "SUMMARY:", etc.

Return ONLY the content in this format:
[Title with emojis]

[First paragraph - introduction or main topic, engaging opening]

[Second paragraph - supporting details or development of ideas]

[Third paragraph - additional points or conclusion if needed]

Here is the text to translate and create an article from:"""
            
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system", 
                        "content": enhanced_prompt
                    },
                    {
                        "role": "user", 
                        "content": text
                    }
                ],
                "max_tokens": 2500,
                "temperature": 0.2  # Slightly higher for more creative titles
            }
            
            result = self.make_openrouter_request(payload)
            
            # Parse the result to extract title and translation
            if result.startswith("⚠️"):
                return result
            
            # Extract title and article from formatted response (no labels expected)
            lines = result.split('\n')
            title = ""
            article_lines = []
            
            # First non-empty line is the title
            for line in lines:
                if line.strip():
                    title = line.strip()
                    break
            
            # All subsequent non-empty lines are the article content
            for line in lines[1:]:
                if line.strip():
                    article_lines.append(line.strip())
            
            if title and article_lines:
                article_text = '\n\n'.join([line for line in article_lines if line])
                return f"{title}\n\n{article_text}"
            else:
                # Fallback: just return the result as-is if parsing fails
                return result
                    
        except Exception as e:
            return f"⚠️ Translation error: {str(e)}"
    
    def translate_text(self, text, source_lang, target_lang):
        """Main translation method - uses local macOS translation then OpenRouter for enhancement"""
        return self.translate_locally_then_enhance(text, source_lang, target_lang)
    
    def transcribe_local_video(self):
        file_path = self.local_file_var.get().strip()
        
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid video file")
            return
        
        self.local_transcribe_button.config(state='disabled')
        self.local_progress.start()
        self.local_status_var.set("Transcribing video...")
        # Clear all local video output tabs
        self.local_original_text.delete(1.0, tk.END)
        self.local_translation_text.delete(1.0, tk.END)
        self.local_orig_srt_text.delete(1.0, tk.END)
        self.local_trans_srt_text.delete(1.0, tk.END)
        self.local_summary_text.delete(1.0, tk.END)
        
        thread = threading.Thread(target=self.run_local_transcription, args=(file_path,))
        thread.daemon = True
        thread.start()
    
    def run_local_transcription(self, file_path):
        try:
            summarize = self.local_summarize_var.get()
            
            # Build yap command with output to file for clean results  
            output_file = os.path.join(self.output_dir, 
                                     f"{Path(file_path).stem}_transcription.txt")
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
                
                # Prepare results dictionary
                results = {
                    'original': formatted_transcription,
                    'original_srt': self.create_srt_from_text(formatted_transcription)
                }
                
                # Generate translation if requested
                if self.local_translate_var.get() and transcription_text:
                    self.root.after(0, lambda: self.local_status_var.set("Translating text..."))
                    target_lang = self.local_target_lang.get()
                    # For local videos, assume source language is English (most common)
                    source_lang = "en"
                    translation = self.translate_text(formatted_transcription, source_lang, target_lang)
                    results['translation'] = translation
                    results['translated_srt'] = self.create_srt_from_text(translation, is_translation=True)
                
                # Generate summary if requested
                if summarize and transcription_text:
                    self.root.after(0, lambda: self.local_status_var.set("Generating title and summary..."))
                    title, summary = self.generate_title_and_summary(transcription_text)
                    results['summary'] = f"{title}\n{summary}"
            else:
                results = {'original': transcription_text}
            
            self.root.after(0, self.on_local_success, results, output_file)
            
        except subprocess.TimeoutExpired:
            self.root.after(0, self.on_local_error, "Transcription timed out")
        except Exception as e:
            self.root.after(0, self.on_local_error, str(e))
    
    def on_online_video_success(self, results):
        self.yt_progress.stop()
        self.yt_download_button.config(state='normal')
        self.yt_status_var.set("Download and transcription completed!")
        
        # Clear all tabs
        self.clear_online_video_output()
        
        # Populate tabs with results
        if 'original' in results:
            self.yt_original_text.insert(tk.END, results['original'])
        
        if 'translation' in results:
            self.yt_translation_text.insert(tk.END, results['translation'])
        
        if 'original_srt' in results:
            self.yt_orig_srt_text.insert(tk.END, results['original_srt'])
        
        if 'translated_srt' in results:
            self.yt_trans_srt_text.insert(tk.END, results['translated_srt'])
        
        if 'summary' in results:
            self.yt_summary_text.insert(tk.END, results['summary'])
    
    def on_online_video_error(self, error):
        self.yt_progress.stop()
        self.yt_download_button.config(state='normal')
        self.yt_status_var.set("Error occurred")
        
        self.clear_online_video_output()
        self.yt_original_text.insert(tk.END, f"Error: {error}")
        
        messagebox.showerror("Error", f"Operation failed: {error}")
    
    def on_local_success(self, results, output_file):
        self.local_progress.stop()
        self.local_transcribe_button.config(state='normal')
        self.local_status_var.set(f"Transcription saved to {os.path.basename(output_file)}")
        
        # Clear all tabs
        self.clear_local_output()
        
        # Populate tabs with results
        if 'original' in results:
            self.local_original_text.insert(tk.END, results['original'])
        
        if 'translation' in results:
            self.local_translation_text.insert(tk.END, results['translation'])
        
        if 'original_srt' in results:
            self.local_orig_srt_text.insert(tk.END, results['original_srt'])
        
        if 'translated_srt' in results:
            self.local_trans_srt_text.insert(tk.END, results['translated_srt'])
        
        if 'summary' in results:
            self.local_summary_text.insert(tk.END, results['summary'])
    
    def on_local_error(self, error):
        self.local_progress.stop()
        self.local_transcribe_button.config(state='normal')
        self.local_status_var.set("Error occurred")
        
        self.clear_local_output()
        self.local_original_text.insert(tk.END, f"Error: {error}")
        
        messagebox.showerror("Error", f"Transcription failed: {error}")
    
    def clear_online_video_output(self):
        self.yt_original_text.delete(1.0, tk.END)
        self.yt_translation_text.delete(1.0, tk.END)
        self.yt_orig_srt_text.delete(1.0, tk.END)
        self.yt_trans_srt_text.delete(1.0, tk.END)
        self.yt_summary_text.delete(1.0, tk.END)
        self.yt_status_var.set("Ready")
    
    def clear_local_output(self):
        self.local_original_text.delete(1.0, tk.END)
        self.local_translation_text.delete(1.0, tk.END)
        self.local_orig_srt_text.delete(1.0, tk.END)
        self.local_trans_srt_text.delete(1.0, tk.END)
        self.local_summary_text.delete(1.0, tk.END)
        self.local_status_var.set("Ready")
    
    def save_local_output(self):
        # Get content from the original text tab (main output)
        content = self.local_original_text.get(1.0, tk.END).strip()
        
        if not content:
            messagebox.showwarning("Warning", "No output to save")
            return
        
        # Default to text file
        ext = ".txt" 
        file_types = [
            ("Text files", "*.txt"),
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

def handle_exception(exc_type, exc_value, exc_traceback):
    """Global exception handler"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    error_msg = f"Uncaught exception: {exc_type.__name__}: {exc_value}\n"
    error_msg += "".join(traceback.format_tb(exc_traceback))
    
    print(f"ERROR: {error_msg}", file=sys.stderr)
    
    # Try to show in GUI if possible
    try:
        messagebox.showerror("Application Error", 
                           f"An unexpected error occurred:\n{exc_type.__name__}: {exc_value}\n\nCheck terminal for details.")
    except:
        pass

def main():
    try:
        # Set global exception handler
        sys.excepthook = handle_exception
        
        root = tk.Tk()
        
        # Add protocol handler for window close
        def on_closing():
            try:
                root.quit()
                root.destroy()
            except:
                pass
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Try to set a nice style
        try:
            style = ttk.Style()
            style.theme_use('aqua')  # macOS native look
        except:
            pass
        
        app = YapGUI(root)
        
        # Keep the app responsive
        def keep_alive():
            try:
                root.after(1000, keep_alive)  # Check every second
            except:
                pass
        
        keep_alive()
        
        print("Starting Whisper Killer...", file=sys.stderr)
        root.mainloop()
        print("Whisper Killer closed normally", file=sys.stderr)
        
    except Exception as e:
        print(f"MAIN ERROR: {e}", file=sys.stderr)
        traceback.print_exc()

if __name__ == "__main__":
    main()