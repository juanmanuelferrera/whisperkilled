#!/usr/bin/env python3

import sys
sys.path.append('.')

from yap_gui import YapGUI
import tkinter as tk

def debug_paragraph_analysis():
    root = tk.Tk()
    root.withdraw()
    app = YapGUI(root)
    
    good_text = """This is the first paragraph about artificial intelligence. It introduces the main concept and provides some background information. AI has been developing rapidly in recent years, transforming various industries and sectors.

This is the second paragraph that discusses applications. We can see AI being used in various fields like healthcare, finance, and transportation. The technology continues to evolve and improve with each passing day.

This final paragraph talks about the future of artificial intelligence. Machine learning and deep learning are becoming more sophisticated with advanced algorithms. The potential for AI to transform society is enormous and exciting."""
    
    print("=== DEBUGGING PARAGRAPH ANALYSIS ===")
    
    paragraphs = good_text.split('\n\n')
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
        print(f"P{i+1} ends with: '{p[-3:]}'")
    
    result = app.has_good_paragraph_structure(good_text)
    print(f"\nFinal result: {result}")
    
    root.destroy()

if __name__ == "__main__":
    debug_paragraph_analysis()