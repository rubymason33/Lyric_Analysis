"""
Parsers to support the Textraordinary Framework
"""

import json
import string
from collections import Counter


def json_parser(filename):
    f = open(filename)
    raw = json.load(f)
    text = raw['text']
    words = ''.join(char.lower() for char in text if char not in string.punctuation).split()
    wc = Counter(words)
    num = len(wc)
    f.close()
    return {'wordcount': wc, 'numwords': num}
