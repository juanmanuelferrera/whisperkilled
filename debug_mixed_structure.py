#!/usr/bin/env python3

import sys
sys.path.append('.')

from yap_gui import YapGUI
import tkinter as tk

def debug_mixed_structure():
    print("=== DEBUGGING MIXED STRUCTURE CASE ===")
    
    root = tk.Tk()
    root.withdraw()
    app = YapGUI(root)
    
    mixed_text = """This paragraph has good structure and proper punctuation.

This is a very long paragraph that goes on and on without proper breaks making it hard to read and understand because it contains too much information in a single block which is typical of transcribed content that hasn't been properly formatted yet.

This paragraph is good again."""
    
    print("Analyzing mixed structure text:")
    paragraphs = mixed_text.split('\n\n')
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    
    print(f"Number of paragraphs: {len(paragraphs)}")
    
    word_counts = [len(p.split()) for p in paragraphs]
    print(f"Word counts: {word_counts}")
    
    avg_words = sum(word_counts) / len(word_counts)
    print(f"Average words: {avg_words}")
    
    min_words, max_words = min(word_counts), max(word_counts)
    print(f"Min words: {min_words}, Max words: {max_words}")
    print(f"Variety ratio: {max_words / min_words}")
    
    proper_endings = sum(1 for p in paragraphs if p.rstrip().endswith(('.', '!', '?', ':')))
    print(f"Proper endings: {proper_endings}/{len(paragraphs)} = {proper_endings/len(paragraphs)*100:.1f}%")
    
    for i, p in enumerate(paragraphs):
        print(f"P{i+1} ({len(p.split())} words): '{p[:50]}...'")
    
    result = app.has_good_paragraph_structure(mixed_text)
    print(f"\nFinal result: {result}")
    
    # Check if any paragraph is too long
    long_paragraphs = [i for i, count in enumerate(word_counts) if count > 50]
    if long_paragraphs:
        print(f"⚠️ Long paragraphs detected at indices: {long_paragraphs}")
        print("This should trigger AI processing for better structure.")
    
    root.destroy()

if __name__ == "__main__":
    debug_mixed_structure() 