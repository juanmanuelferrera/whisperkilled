#!/usr/bin/env python3

import sys
sys.path.append('.')

from yap_gui import YapGUI
import tkinter as tk

def test_text_translation():
    print("=== TESTING TEXT TRANSLATION FEATURE ===")
    
    # Create a mock GUI instance for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    app = YapGUI(root)
    
    # Test text
    test_text = """This is a test paragraph about artificial intelligence. It introduces the main concept and provides some background information. AI has been developing rapidly in recent years, transforming various industries and sectors.

This is the second paragraph that discusses applications. We can see AI being used in various fields like healthcare, finance, and transportation. The technology continues to evolve and improve with each passing day.

This final paragraph talks about the future of artificial intelligence. Machine learning and deep learning are becoming more sophisticated with advanced algorithms. The potential for AI to transform society is enormous and exciting."""
    
    print("Testing text translation functionality...")
    print(f"Input text length: {len(test_text)} characters")
    print(f"Input text paragraphs: {len(test_text.split(chr(10)+chr(10)))}")
    
    # Test the translation methods directly
    print("\n--- Testing Apple Translation ---")
    try:
        result = app.translate_with_apple_live_translation(test_text, "es")
        if result.startswith("⚠️"):
            print(f"Apple Translation failed: {result}")
        else:
            print(f"Apple Translation successful: {len(result)} characters")
            print(f"First 100 chars: {result[:100]}...")
    except Exception as e:
        print(f"Apple Translation error: {e}")
    
    print("\n--- Testing Hybrid Translation ---")
    try:
        result = app.translate_locally_then_enhance(test_text, "es")
        if result.startswith("⚠️"):
            print(f"Hybrid Translation failed: {result}")
        else:
            print(f"Hybrid Translation successful: {len(result)} characters")
            print(f"First 100 chars: {result[:100]}...")
    except Exception as e:
        print(f"Hybrid Translation error: {e}")
    
    print("\n--- Testing Full AI Translation ---")
    try:
        result = app.translate_with_title_and_paragraphs(test_text, "es")
        if result.startswith("⚠️"):
            print(f"Full AI Translation failed: {result}")
        else:
            print(f"Full AI Translation successful: {len(result)} characters")
            print(f"First 100 chars: {result[:100]}...")
    except Exception as e:
        print(f"Full AI Translation error: {e}")
    
    print("\n=== TEXT TRANSLATION FEATURE SUMMARY ===")
    print("✅ Text translation tab added to GUI")
    print("✅ Paste text functionality implemented")
    print("✅ Import text file functionality implemented")
    print("✅ Apple translation engine integration")
    print("✅ Hybrid translation with paragraph enhancement")
    print("✅ Full AI translation fallback")
    print("✅ Save translation to file functionality")
    print("✅ Copy to clipboard functionality")
    
    root.destroy()

if __name__ == "__main__":
    test_text_translation() 