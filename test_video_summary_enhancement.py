#!/usr/bin/env python3

"""
Test script to verify the enhanced video summary article feature
"""

import sys
import os

# Add the current directory to the path so we can import yap_gui
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from yap_gui import YapGUI
import tkinter as tk

def test_video_summary_enhancement():
    """Test the enhanced video summary article feature"""
    print("🧪 Testing Enhanced Video Summary Article Feature")
    print("=" * 55)
    
    # Create a minimal root window for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create YapGUI instance
    app = YapGUI(root)
    
    # Test transcript text for summary generation
    test_transcript = """Welcome to today's comprehensive guide on artificial intelligence and machine learning. In this video, we'll explore the fundamental concepts that are shaping the future of technology. Artificial intelligence has become an integral part of our daily lives, from the smartphones we use to the cars we drive.

Machine learning, a subset of AI, enables computers to learn from data without being explicitly programmed. We'll discuss various algorithms including neural networks, decision trees, and support vector machines. These technologies are revolutionizing industries such as healthcare, finance, and transportation.

The video covers practical applications like image recognition, natural language processing, and autonomous systems. We'll also address important ethical considerations and the impact of AI on employment and society. Understanding these concepts is crucial for anyone interested in the future of technology and innovation."""
    
    print("Testing video summary with article format...")
    print()
    print("Original transcript length:", len(test_transcript.split()), "words")
    print()
    
    # Test the generate_title_and_summary function
    try:
        title, summary = app.generate_title_and_summary(test_transcript)
        
        print("Generated Title:")
        print("-" * 40)
        print(title)
        print("-" * 40)
        print()
        
        print("Generated Summary:")
        print("-" * 40)
        print(summary)
        print("-" * 40)
        print()
        
        # Check if the result has the expected format
        if "TITLE:" in title or "📝" in title:
            print("✅ Title format looks correct")
        else:
            print("⚠️ Title format may need adjustment")
        
        # Check for equals signs (should not be present)
        if "=" in summary:
            print("❌ Summary contains equals signs (should be removed)")
        else:
            print("✅ Summary does not contain equals signs")
        
        # Check for summary text (should not be present)
        if "Here is a 2-3 paragraph summary" in summary:
            print("❌ Summary contains unwanted text")
        else:
            print("✅ Summary does not contain unwanted text")
        
        # Count words in the summary
        word_count = len(summary.split())
        print(f"Summary word count: {word_count} words")
        
        if word_count <= 200:
            print("✅ Summary is within 200-word limit")
        else:
            print(f"⚠️ Summary exceeds 200-word limit ({word_count} words)")
        
        # Check for emojis in title
        if any(emoji in title for emoji in ['📝', '🤖', '💡', '🎯', '🚀', '⭐', '🌟', '📚', '🔬', '💻']):
            print("✅ Title contains emojis")
        else:
            print("⚠️ Title may be missing emojis")
        
        # Check for paragraph structure
        if summary.count('\n\n') >= 1:
            print("✅ Summary has proper paragraph structure")
        else:
            print("⚠️ Summary paragraph structure may need improvement")
        
        # Test the formatted output
        formatted_summary = f"{title}\n\n{summary}"
        print()
        print("Formatted Output:")
        print("-" * 40)
        print(formatted_summary)
        print("-" * 40)
        
    except Exception as e:
        print(f"❌ Error testing video summary: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("🎉 Video summary enhancement test completed!")
    
    # Clean up
    root.destroy()

if __name__ == "__main__":
    test_video_summary_enhancement() 