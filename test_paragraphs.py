#!/usr/bin/env python3

import sys
sys.path.append('.')

from yap_gui import YapGUI
import tkinter as tk

def test_paragraph_preservation():
    print("Testing paragraph preservation in translation...")
    
    # Create a mock GUI instance for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    app = YapGUI(root)
    
    # Test text with paragraphs
    test_text = """This is the first paragraph about artificial intelligence. It introduces the main concept and provides some background information. AI has been developing rapidly in recent years.

This is the second paragraph that discusses applications. We can see AI being used in various fields like healthcare, finance, and transportation. The technology continues to evolve and improve.

This final paragraph talks about the future. Machine learning and deep learning are becoming more sophisticated. The potential for AI to transform society is enormous."""
    
    print("Original text structure:")
    print(f"Paragraphs: {len(test_text.split(chr(10)+chr(10)))}")
    print(f"Total length: {len(test_text)}")
    print()
    
    # Test local translation
    result = app.translate_with_local_tool(test_text, "es")
    print(f"Local translation result:")
    print(f"Paragraphs in result: {len(result.split(chr(10)+chr(10)))}")
    print(f"First 200 chars: {result[:200]}...")
    print()
    
    root.destroy()

if __name__ == "__main__":
    test_paragraph_preservation()