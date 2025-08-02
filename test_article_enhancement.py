#!/usr/bin/env python3

"""
Test script to verify the enhanced translation article feature
"""

import sys
import os

# Add the current directory to the path so we can import yap_gui
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from yap_gui import YapGUI
import tkinter as tk

def test_article_enhancement():
    """Test the enhanced translation article feature"""
    print("🧪 Testing Enhanced Translation Article Feature")
    print("=" * 55)
    
    # Create a minimal root window for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create YapGUI instance
    app = YapGUI(root)
    
    # Test text for translation
    test_text = """Artificial intelligence has revolutionized the way we interact with technology. From virtual assistants like Siri and Alexa to advanced machine learning algorithms that power recommendation systems, AI is becoming increasingly integrated into our daily lives. The technology has made significant strides in natural language processing, computer vision, and robotics, enabling computers to understand and respond to human input in more natural ways than ever before.

Machine learning, a subset of AI, allows computers to learn from data without being explicitly programmed. This has led to breakthroughs in fields such as healthcare, where AI systems can analyze medical images to detect diseases, and in finance, where algorithms can predict market trends. The ability of AI to process vast amounts of data quickly and identify patterns has made it invaluable for research and development across various industries.

However, the rapid advancement of AI technology also raises important questions about privacy, job displacement, and ethical considerations. As AI systems become more sophisticated, there are concerns about how they collect and use personal data, as well as the potential impact on employment as automation increases. It's crucial for society to address these challenges while continuing to harness the benefits that AI offers for improving human life and solving complex problems."""
    
    print("Testing enhanced translation with article format...")
    print()
    print("Original text length:", len(test_text.split()), "words")
    print()
    
    # Test the enhance_translation_with_openrouter function
    try:
        # First, we need to simulate a translated text (since the function expects already-translated text)
        # For testing purposes, we'll use the original text as if it were translated
        enhanced_result = app.enhance_translation_with_openrouter(test_text, "es")
        
        print("Enhanced Result:")
        print("-" * 40)
        print(enhanced_result)
        print("-" * 40)
        
        # Check if the result has the expected format
        if "🔒" in enhanced_result and "=" in enhanced_result:
            print("✅ Enhanced translation format looks correct")
        else:
            print("⚠️ Enhanced translation format may need adjustment")
        
        # Count words in the article part (after the title)
        lines = enhanced_result.split('\n')
        article_started = False
        word_count = 0
        
        for line in lines:
            if line.startswith('='):
                article_started = True
            elif article_started and line.strip():
                word_count += len(line.split())
        
        print(f"Article word count: {word_count} words")
        
        if word_count <= 200:
            print("✅ Article is within 200-word limit")
        else:
            print(f"⚠️ Article exceeds 200-word limit ({word_count} words)")
        
        # Check for emojis in title
        if any(emoji in enhanced_result for emoji in ['🔒', '📝', '🤖', '💡', '🎯', '🚀', '⭐', '🌟']):
            print("✅ Article contains emojis")
        else:
            print("⚠️ Article may be missing emojis")
        
        # Check for paragraph structure
        if enhanced_result.count('\n\n') >= 2:
            print("✅ Article has proper paragraph structure")
        else:
            print("⚠️ Article paragraph structure may need improvement")
        
    except Exception as e:
        print(f"❌ Error testing enhanced translation: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("🎉 Article enhancement test completed!")
    
    # Clean up
    root.destroy()

if __name__ == "__main__":
    test_article_enhancement() 