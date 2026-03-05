"""
wordify_parsers.py: Parses the JSON files with text data.
Author: Joshua Moy
"""
import json
from collections import Counter

def json_parser(filename):
    """ Parser for JSON files containing text data """
    with open(filename, 'r', encoding='utf-8') as f:
        raw = json.load(f)

    text = raw['text']
    words = text.split()
    wc = Counter(words)
    num = len(words)

    return {
        'wordcount': wc,
        'numwords': num,
        'raw_text': text
    }