#!/usr/bin/env python3

import sys
sys.path.append('.')

from yap_gui import YapGUI
import tkinter as tk

def test_paragraph_algorithm():
    print("=== COMPREHENSIVE PARAGRAPH ALGORITHM TEST ===")
    
    # Create a mock GUI instance for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    app = YapGUI(root)
    
    # Test cases with expected results
    test_cases = [
        {
            "name": "Good Structure - Similar Lengths",
            "text": """This is the first paragraph about artificial intelligence. It introduces the main concept and provides some background information. AI has been developing rapidly in recent years, transforming various industries and sectors.

This is the second paragraph that discusses applications. We can see AI being used in various fields like healthcare, finance, and transportation. The technology continues to evolve and improve with each passing day.

This final paragraph talks about the future of artificial intelligence. Machine learning and deep learning are becoming more sophisticated with advanced algorithms. The potential for AI to transform society is enormous and exciting.""",
            "expected": True,
            "reason": "Well-structured paragraphs with good punctuation"
        },
        {
            "name": "Poor Structure - Single Block",
            "text": """Hello this is a test of the transcription system and we're going to see how it works with a long block of text that doesn't have proper paragraph breaks because that's what usually happens when you transcribe audio or video content and the system just puts everything in one long continuous stream of text without any logical breaks or structure which makes it hard to read and understand so we need to use AI to create proper paragraphs from this mess of words that goes on and on without proper punctuation or breaks.""",
            "expected": False,
            "reason": "Single block of text without paragraph breaks"
        },
        {
            "name": "Good Structure - Varied Lengths",
            "text": """This is a short introduction paragraph.

This is a much longer paragraph that contains significantly more content and detail. It goes into depth about the topic and provides comprehensive information that would typically be found in a well-written article or document. The length variation helps demonstrate that the algorithm can handle different paragraph sizes effectively.

Short conclusion.""",
            "expected": True,
            "reason": "Good variety in paragraph lengths with proper structure"
        },
        {
            "name": "Poor Structure - Too Short Paragraphs",
            "text": """This is too short.

This one too.

And this.

Very short paragraphs.""",
            "expected": False,
            "reason": "Paragraphs are too short (less than 10 words average)"
        },
        {
            "name": "Poor Structure - Missing Punctuation",
            "text": """This paragraph has no ending punctuation

This one also lacks proper ending

And this one too

Making it hard to read properly""",
            "expected": False,
            "reason": "Missing proper punctuation endings"
        },
        {
            "name": "Good Structure - Technical Content",
            "text": """The algorithm processes input data through multiple stages. First, it analyzes the text structure and identifies potential paragraph boundaries. Then, it applies various heuristics to determine if the existing structure is adequate.

In the second stage, the system evaluates paragraph quality metrics including length distribution, punctuation patterns, and semantic coherence. These metrics help determine whether the text requires AI-powered restructuring or can be processed with minimal enhancement.

Finally, the algorithm makes a decision about the translation approach. If the structure is deemed good, it uses local translation with minimal AI enhancement. Otherwise, it employs full AI processing to create intelligent paragraph breaks and improve overall readability.""",
            "expected": True,
            "reason": "Technical content with good structure and punctuation"
        }
    ]
    
    # Run tests
    passed = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['name']} ---")
        
        # Analyze the text
        paragraphs = test_case['text'].split('\n\n')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        word_counts = [len(p.split()) for p in paragraphs]
        avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
        min_words, max_words = min(word_counts), max(word_counts) if word_counts else (0, 0)
        variety_ratio = max_words / min_words if min_words > 0 else 1
        
        proper_endings = sum(1 for p in paragraphs if p.rstrip().endswith(('.', '!', '?', ':')))
        punctuation_ratio = proper_endings / len(paragraphs) if paragraphs else 0
        
        print(f"Paragraphs: {len(paragraphs)}")
        print(f"Word counts: {word_counts}")
        print(f"Average words: {avg_words:.1f}")
        print(f"Variety ratio: {variety_ratio:.2f}")
        print(f"Punctuation ratio: {punctuation_ratio:.2f}")
        
        # Test the algorithm
        result = app.has_good_paragraph_structure(test_case['text'])
        expected = test_case['expected']
        
        print(f"Result: {result}")
        print(f"Expected: {expected}")
        print(f"Status: {'✅ PASS' if result == expected else '❌ FAIL'}")
        print(f"Reason: {test_case['reason']}")
        
        if result == expected:
            passed += 1
    
    print(f"\n=== SUMMARY ===")
    print(f"Passed: {passed}/{total} tests ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! The algorithm is working correctly.")
    else:
        print("⚠️ Some tests failed. Algorithm may need further adjustment.")
    
    root.destroy()

if __name__ == "__main__":
    test_paragraph_algorithm() 