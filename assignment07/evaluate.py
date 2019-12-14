from pathlib import Path
import re
import os
import pandas as pd

string_matching = __import__("string-matching")

# Get paths for inputs
text_paths = list(Path('.').glob('corpus/*.txt'))
pattern_paths = list(Path('.').glob('patterns/*.txt'))

text_data = {}
pattern_data = {}

# Read data into memory
for d in text_paths:
    with d.open() as f:
        text_data[d.stem] = ("".join(f.readlines()))
for d in pattern_paths:
    with d.open() as f:
        pattern_data[d.stem] = [pattern[0:-1] for pattern in f.readlines()]

# Get the outputs for each variant
naive_data = {}
fa_data    = {}
kmp_data   = {}

for k in text_data:
    patterns = pattern_data[k]
    text = text_data[k]
    text = text.lower()
    naive_data[k] = []
    fa_data   [k] = []
    kmp_data  [k] = []
    for pattern in patterns:
        pattern = pattern.lower()
        naive_data[k].append((pattern, string_matching.naive_str_match(pattern, text)))
        fa_data   [k].append((pattern, string_matching.fa_str_match(pattern, text)))
        kmp_data  [k].append((pattern, string_matching.KMP_str_match(pattern, text)))

os.makedirs('results', exist_ok = True)

with open('./results/data.csv', 'w') as f, open('./results/data_no_indices.csv', 'w') as f1: 
    f.write("file algorithm indexes pattern num_shifts num_comparisons prep_cost\n")
    f1.write("file algorithm pattern num_shifts num_comparisons prep_cost\n")
    for i in range(5):
        for fname in naive_data:
            algorithm   = "naive"
            pattern     = naive_data[fname][i][0]
            indexes     = naive_data[fname][i][1]['indexes']
            prep_cost   = naive_data[fname][i][1]['prep_cost']
            num_shifts  = naive_data[fname][i][1]['num_shifts']
            num_comparisons = naive_data[fname][i][1]['num_comparisons']

            f.write(f'{fname} {algorithm} {indexes} {pattern} {num_shifts} {num_comparisons} {prep_cost}\n')
            f1.write(f'{fname} {algorithm} {pattern} {num_shifts} {num_comparisons} {prep_cost}\n')
        for fname in fa_data:
            algorithm   = "finite_automata"
            pattern     = fa_data[fname][i][0]
            indexes     = fa_data[fname][i][1]['indexes']
            prep_cost   = fa_data[fname][i][1]['prep_cost']
            num_shifts  = fa_data[fname][i][1]['num_shifts']
            num_comparisons = fa_data[fname][i][1]['num_comparisons']
            f.write(f'{fname} {algorithm} {indexes} {pattern} {num_shifts} {num_comparisons} {prep_cost}\n')
            f1.write(f'{fname} {algorithm} {pattern} {num_shifts} {num_comparisons} {prep_cost}\n')
        for fname in kmp_data:
            algorithm   = "KMP"
            pattern     = kmp_data[fname][i][0]
            indexes     = kmp_data[fname][i][1]['indexes']
            prep_cost   = kmp_data[fname][i][1]['prep_cost']
            num_shifts  = kmp_data[fname][i][1]['num_shifts']
            num_comparisons = kmp_data[fname][i][1]['num_comparisons']

            f.write(f'{fname} {algorithm} {indexes} {pattern} {num_shifts} {num_comparisons} {prep_cost}\n')
            f1.write(f'{fname} {algorithm} {pattern} {num_shifts} {num_comparisons} {prep_cost}\n')

print("Raw data stored to results/data.csv. Summary statistics stored to results/means.csv")
pd.set_option('display.max_columns', None)  
raw = pd.read_csv('results/data_no_indices.csv', delimiter = ' ')
print(raw.groupby('algorithm').describe())

raw.to_html('results/data_no_indices.html')

with open('results/means.csv', 'w') as f:
    f.write(str(raw.groupby('algorithm').mean()))
