#!/usr/bin/env python3

import sys
sys.path.append('.')

from yap_gui import YapGUI
import tkinter as tk

# Simple test of the translation methods
def test_local_translation():
    print("Testing macOS local translation...")
    
    # Create a mock GUI instance for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    app = YapGUI(root)
    
    # Test text
    test_text = "Hello, this is a test of the translation system."
    
    # Test local translation
    result = app.translate_with_local_tool(test_text, "es")
    print(f"Local translation result: {result}")
    
    # Test if fallback works
    if result.startswith("⚠️"):
        print("Local translation not available, fallback to OpenRouter expected")
    else:
        print("Local translation successful!")
    
    root.destroy()

if __name__ == "__main__":
    test_local_translation()