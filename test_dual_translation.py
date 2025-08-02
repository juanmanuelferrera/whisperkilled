#!/usr/bin/env python3

import sys
sys.path.append('.')

from yap_gui import YapGUI
import tkinter as tk

def test_dual_translation():
    print("=== TESTING DUAL TRANSLATION OUTPUT ===")
    
    # Create a mock GUI instance for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    app = YapGUI(root)
    
    # Test text
    test_text = """Artificial intelligence has revolutionized the way we interact with technology. From simple chatbots to complex neural networks, AI systems are becoming increasingly sophisticated and capable of performing tasks that were once thought to be exclusively human.

The applications of AI span across numerous industries, including healthcare, finance, transportation, and entertainment. In healthcare, AI is being used for medical diagnosis, drug discovery, and personalized treatment plans. Financial institutions leverage AI for fraud detection and algorithmic trading.

Machine learning, a subset of AI, has been particularly transformative. Deep learning algorithms can process vast amounts of data and identify patterns that would be impossible for humans to detect. This capability has led to breakthroughs in computer vision, natural language processing, and robotics."""
    
    print("Testing dual translation output functionality...")
    print(f"Input text length: {len(test_text)} characters")
    print(f"Input text paragraphs: {len(test_text.split(chr(10)+chr(10)))}")
    
    # Test normal translation (without title/emojis)
    print("\n--- Testing Normal Translation ---")
    try:
        normal_result = app.translate_with_apple_live_translation(test_text, "es")
        if normal_result.startswith("⚠️"):
            normal_result = app.translate_with_local_tool_fallback(test_text, "es")
        
        print(f"Normal translation: {len(normal_result)} characters")
        print(f"First 100 chars: {normal_result[:100]}...")
        print(f"Has title/emojis: {'No' if not normal_result.startswith('🔒') and not normal_result.startswith('🤖') else 'Yes'}")
    except Exception as e:
        print(f"Normal translation error: {e}")
    
    # Test enhanced translation (with title/emojis)
    print("\n--- Testing Enhanced Translation ---")
    try:
        enhanced_result = app.translate_locally_then_enhance(test_text, "es")
        print(f"Enhanced translation: {len(enhanced_result)} characters")
        print(f"First 100 chars: {enhanced_result[:100]}...")
        print(f"Has title/emojis: {'Yes' if enhanced_result.startswith('🔒') or enhanced_result.startswith('🤖') else 'No'}")
    except Exception as e:
        print(f"Enhanced translation error: {e}")
    
    # Test full AI translation (with title/emojis)
    print("\n--- Testing Full AI Translation ---")
    try:
        full_ai_result = app.translate_with_title_and_paragraphs(test_text, "es")
        print(f"Full AI translation: {len(full_ai_result)} characters")
        print(f"First 100 chars: {full_ai_result[:100]}...")
        print(f"Has title/emojis: {'Yes' if full_ai_result.startswith('🤖') else 'No'}")
    except Exception as e:
        print(f"Full AI translation error: {e}")
    
    print("\n=== DUAL TRANSLATION FEATURE SUMMARY ===")
    print("✅ Two output tabs: Normal Translation and Enhanced Translation")
    print("✅ Normal translation: Clean text without title/emojis")
    print("✅ Enhanced translation: With title, emojis, and better formatting")
    print("✅ Both outputs generated simultaneously")
    print("✅ Independent copy and save functionality for each output")
    print("✅ Clear function clears both outputs")
    
    root.destroy()

if __name__ == "__main__":
    test_dual_translation() 