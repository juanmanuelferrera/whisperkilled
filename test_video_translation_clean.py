#!/usr/bin/env python3

"""
Test script to verify clean video translation format without TRADUCCIÓN text
"""

import sys
import os

# Add the current directory to the path so we can import yap_gui
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from yap_gui import YapGUI
import tkinter as tk

def test_video_translation_clean():
    """Test that video translations have clean format without TRADUCCIÓN text"""
    print("🧪 Testing Clean Video Translation Format")
    print("=" * 45)
    
    # Create a minimal root window for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create YapGUI instance
    app = YapGUI(root)
    
    # Test text for translation
    test_text = """Artificial intelligence has revolutionized the way we interact with technology. From virtual assistants like Siri and Alexa to advanced machine learning algorithms that power recommendation systems, AI is becoming increasingly integrated into our daily lives.

Machine learning, a subset of AI, allows computers to learn from data without being explicitly programmed. This has led to breakthroughs in fields such as healthcare, where AI systems can analyze medical images to detect diseases, and in finance, where algorithms can predict market trends. The ability of AI to process vast amounts of data quickly and identify patterns has made it invaluable for research and development across various industries.

However, the rapid advancement of AI technology also raises important questions about privacy, job displacement, and ethical considerations. As AI systems become more sophisticated, there are concerns about how they collect and use personal data, as well as the potential impact on employment as automation increases. It's crucial for society to address these challenges while continuing to harness the benefits that AI offers for improving human life and solving complex problems."""
    
    print("Testing video translation with clean format...")
    print()
    print("Original text length:", len(test_text.split()), "words")
    print()
    
    # Test the translation functions
    try:
        # Test enhanced translation (local + AI enhancement)
        enhanced_result = app.translate_locally_then_enhance(test_text, "en", "es")
        
        print("Enhanced Translation Result:")
        print("-" * 40)
        print(enhanced_result)
        print("-" * 40)
        print()
        
        # Check for unwanted text
        if "TRADUCCIÓN:" in enhanced_result:
            print("❌ Enhanced translation contains 'TRADUCCIÓN:' text")
        else:
            print("✅ Enhanced translation does not contain 'TRADUCCIÓN:' text")
        
        if "TRANSLATION:" in enhanced_result:
            print("❌ Enhanced translation contains 'TRANSLATION:' text")
        else:
            print("✅ Enhanced translation does not contain 'TRANSLATION:' text")
        
        # Check for equals signs (should not be present)
        if "=" in enhanced_result:
            print("❌ Enhanced translation contains equals signs")
        else:
            print("✅ Enhanced translation does not contain equals signs")
        
        # Check for clean formatting
        if enhanced_result.startswith("🔒"):
            print("✅ Enhanced translation has proper 🔒 prefix")
        else:
            print("⚠️ Enhanced translation may be missing 🔒 prefix")
        
        # Test full AI translation
        full_ai_result = app.translate_with_title_and_paragraphs(test_text, "en", "es")
        
        print()
        print("Full AI Translation Result:")
        print("-" * 40)
        print(full_ai_result)
        print("-" * 40)
        print()
        
        # Check for unwanted text
        if "TRADUCCIÓN:" in full_ai_result:
            print("❌ Full AI translation contains 'TRADUCCIÓN:' text")
        else:
            print("✅ Full AI translation does not contain 'TRADUCCIÓN:' text")
        
        if "TRANSLATION:" in full_ai_result:
            print("❌ Full AI translation contains 'TRANSLATION:' text")
        else:
            print("✅ Full AI translation does not contain 'TRANSLATION:' text")
        
        # Check for equals signs (should not be present)
        if "=" in full_ai_result:
            print("❌ Full AI translation contains equals signs")
        else:
            print("✅ Full AI translation does not contain equals signs")
        
        # Check for clean formatting
        if "🔒" in full_ai_result:
            print("✅ Full AI translation has proper 🔒 prefix")
        else:
            print("⚠️ Full AI translation may be missing 🔒 prefix")
        
        # Count words in the translations
        enhanced_words = len(enhanced_result.split())
        full_ai_words = len(full_ai_result.split())
        
        print()
        print(f"Enhanced translation word count: {enhanced_words} words")
        print(f"Full AI translation word count: {full_ai_words} words")
        
        if enhanced_words <= 300:  # Allow some extra words for title and formatting
            print("✅ Enhanced translation is reasonably concise")
        else:
            print(f"⚠️ Enhanced translation may be too long ({enhanced_words} words)")
        
        if full_ai_words <= 300:  # Allow some extra words for title and formatting
            print("✅ Full AI translation is reasonably concise")
        else:
            print(f"⚠️ Full AI translation may be too long ({full_ai_words} words)")
        
    except Exception as e:
        print(f"❌ Error testing video translation: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("🎉 Clean video translation test completed!")
    
    # Clean up
    root.destroy()

if __name__ == "__main__":
    test_video_translation_clean() 