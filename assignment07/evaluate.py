from pathlib import Path
import re

string_matching = __import__("string-matching")

text_paths = list(Path('.').glob('corpus/*.txt'))
pattern_paths = list(Path('.').glob('patterns/*.txt'))

print(text_paths)

text_data = {}
pattern_data = {}

for d in text_paths:
    with d.open() as f:
        text_data[d.stem] = ("".join(f.readlines()))
        
for d in pattern_paths:
    with d.open() as f:
        pattern_data[d.stem] = [pattern[0:-1] for pattern in f.readlines()]

print(text_data)
print(pattern_data)
