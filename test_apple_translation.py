#!/usr/bin/env python3

import sys
sys.path.append('.')

from yap_gui import YapGUI, APPLE_TRANSLATION_AVAILABLE
import tkinter as tk

def test_apple_translation():
    print("Testing Apple Live Translation...")
    print(f"Apple Translation Available: {APPLE_TRANSLATION_AVAILABLE}")
    
    # Create a mock GUI instance for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    app = YapGUI(root)
    
    # Test text
    test_text = """Hello, this is a test of Apple's Live Translation system. 

This is a second paragraph to test paragraph preservation.

And this is a third paragraph to ensure the translation maintains proper structure."""
    
    print("Original text:")
    print(test_text)
    print()
    
    # Test Apple Live Translation
    result = app.translate_with_apple_live_translation(test_text, "es")
    print(f"Apple Live Translation result:")
    print(result)
    print()
    
    # Test if fallback works
    if result.startswith("⚠️"):
        print("Apple Translation failed, testing fallback...")
        fallback_result = app.translate_with_local_tool_fallback(test_text, "es")
        print(f"Fallback result: {fallback_result}")
    else:
        print("Apple Live Translation successful!")
    
    root.destroy()

if __name__ == "__main__":
    test_apple_translation()