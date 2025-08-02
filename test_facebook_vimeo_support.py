#!/usr/bin/env python3

"""
Test script to verify Facebook and Vimeo support in Whisper Killer
"""

import sys
import os

# Add the current directory to the path so we can import yap_gui
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from yap_gui import YapGUI
import tkinter as tk

def test_url_validation():
    """Test URL validation for different platforms"""
    print("🧪 Testing URL Validation and Platform Detection")
    print("=" * 50)
    
    # Create a minimal root window for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create YapGUI instance
    app = YapGUI(root)
    
    # Test URLs
    test_urls = [
        # YouTube URLs
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "YouTube"),
        ("https://youtu.be/dQw4w9WgXcQ", "YouTube"),
        ("https://youtube.com/watch?v=dQw4w9WgXcQ", "YouTube"),
        
        # Facebook URLs
        ("https://www.facebook.com/watch?v=123456789", "Facebook"),
        ("https://facebook.com/watch?v=123456789", "Facebook"),
        ("https://fb.com/watch?v=123456789", "Facebook"),
        ("https://www.fb.com/watch?v=123456789", "Facebook"),
        ("https://www.facebook.com/video.php?v=123456789", "Facebook"),
        
        # Vimeo URLs
        ("https://www.vimeo.com/123456789", "Vimeo"),
        ("https://vimeo.com/123456789", "Vimeo"),
        ("https://player.vimeo.com/video/123456789", "Vimeo"),
        
        # Invalid URLs
        ("https://example.com/video", "Invalid"),
        ("https://twitter.com/status/123456789", "Invalid"),
        ("not a url", "Invalid"),
    ]
    
    print("Testing URL validation and platform detection:")
    print()
    
    for url, expected_platform in test_urls:
        is_valid = app.is_valid_video_url(url)
        detected_platform = app.get_platform_from_url(url)
        
        status = "✅ PASS" if is_valid and detected_platform == expected_platform else "❌ FAIL"
        
        print(f"{status} URL: {url}")
        print(f"   Valid: {is_valid}")
        print(f"   Detected Platform: {detected_platform}")
        print(f"   Expected Platform: {expected_platform}")
        print()
    
    # Test edge cases
    print("Testing edge cases:")
    print()
    
    edge_cases = [
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", "YouTube"),
        ("https://www.facebook.com/photo.php?v=123456789", "Facebook"),
        ("https://vimeo.com/channels/staffpicks/123456789", "Vimeo"),
        ("https://www.youtube.com/playlist?list=PL123456789", "YouTube"),
    ]
    
    for url, expected_platform in edge_cases:
        is_valid = app.is_valid_video_url(url)
        detected_platform = app.get_platform_from_url(url)
        
        status = "✅ PASS" if is_valid and detected_platform == expected_platform else "❌ FAIL"
        
        print(f"{status} Edge Case: {url}")
        print(f"   Valid: {is_valid}")
        print(f"   Detected Platform: {detected_platform}")
        print(f"   Expected Platform: {expected_platform}")
        print()
    
    # Test language support
    print("Testing language support:")
    print()
    
    languages = app.get_apple_language_list()
    print(f"Total supported languages: {len(languages)}")
    print(f"First 10 languages: {languages[:10]}")
    print()
    
    # Test language name resolution
    test_languages = ["en", "es", "fr", "de", "ja", "zh", "ar", "hi", "th", "vi"]
    print("Testing language name resolution:")
    for lang_code in test_languages:
        lang_name = app.get_language_name(lang_code)
        print(f"  {lang_code} -> {lang_name}")
    
    print()
    print("🎉 URL validation and platform detection tests completed!")
    
    # Clean up
    root.destroy()

if __name__ == "__main__":
    test_url_validation() 