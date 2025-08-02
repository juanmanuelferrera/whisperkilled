#!/usr/bin/env python3

import sys
sys.path.append('.')

from yap_gui import YapGUI
import tkinter as tk

def test_hybrid_paragraph_detection():
    print("Testing Hybrid Paragraph Detection...")
    
    # Create a mock GUI instance for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    app = YapGUI(root)
    
    # Test 1: Good paragraph structure
    good_text = """This is the first paragraph about artificial intelligence. It introduces the main concept and provides some background information. AI has been developing rapidly in recent years, transforming various industries and sectors.

This is the second paragraph that discusses applications. We can see AI being used in various fields like healthcare, finance, and transportation. The technology continues to evolve and improve with each passing day.

This final paragraph talks about the future of artificial intelligence. Machine learning and deep learning are becoming more sophisticated with advanced algorithms. The potential for AI to transform society is enormous and exciting."""
    
    # Test 2: Poor paragraph structure (typical transcription)
    poor_text = """Hello this is a test of the transcription system and we're going to see how it works with a long block of text that doesn't have proper paragraph breaks because that's what usually happens when you transcribe audio or video content and the system just puts everything in one long continuous stream of text without any logical breaks or structure which makes it hard to read and understand so we need to use AI to create proper paragraphs from this mess of words that goes on and on without proper punctuation or breaks."""
    
    print("\n=== Test 1: Good Paragraph Structure ===")
    print(f"Text has {len(good_text.split(chr(10)+chr(10)))} paragraphs")
    has_good = app.has_good_paragraph_structure(good_text)
    print(f"Has good structure: {has_good}")
    print(f"Expected: True (should use Apple Translation + minimal enhancement)")
    
    print("\n=== Test 2: Poor Paragraph Structure ===")
    print(f"Text has {len(poor_text.split(chr(10)+chr(10)))} paragraphs")
    has_poor = app.has_good_paragraph_structure(poor_text)
    print(f"Has good structure: {has_poor}")
    print(f"Expected: False (should use full AI for smart paragraphs)")
    
    print("\n=== Test 3: Translation Workflow ===")
    print("Testing translation with good structure...")
    result_good = app.translate_locally_then_enhance(good_text[:200] + "...", "es")
    print(f"Good structure result: {'Uses Apple Translation' if not result_good.startswith('⚠️') else 'Error'}")
    
    print("\nTesting translation with poor structure...")
    result_poor = app.translate_locally_then_enhance(poor_text[:200] + "...", "es")
    print(f"Poor structure result: {'Uses AI Paragraphs' if not result_poor.startswith('⚠️') else 'Error'}")
    
    root.destroy()

if __name__ == "__main__":
    test_hybrid_paragraph_detection()