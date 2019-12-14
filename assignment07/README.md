Ben Gafford, Xinya Yang
# Pattern Matching
## Problem Description
Pattern matching is a very important question in computer science. A classic/essential type of this question is to find a specific substring (pattern) in a long text and record where the instances are found. In this assignment, we implemented three pattern matching algorithm: naive approach, DFA based approach, and KMP approach. The algorithms are implemented in a case insensitive way.   

## Get started
- If you want to pass in text and pattern as arguments
```python3 string-matching.py "<text>" "<pattern>"```  
- If you want to generate the result with the provided corpus and patterns
```python3 evaluate.py```  
This stores results in a `results` directory as follows:
* Generates an html version of the data table
* Generates a csv version of the data table (one with indices and one without)
* Generates summary statistics for the data. 

## Some sample input & output
- ```python3 string-matching.py "abc abc" "a"```
text is: abc abc  
pattern is: a  

Result of Naive approach  
found in indexes: [0, 4]  
preprocess cost: 0  
number of shifts: 12  
number of comparisons: 6  

Result of DFA approach  
found in indexes: [0, 4]  
preprocess cost: 4  
number of shifts: 7  
number of comparisons: 7  

Result of KMP approach  
found in indexes: [0, 4]  
preprocess cost: 1  
number of shifts: 7  
number of comparisons: 7  

- ```python3 string-matching.py "abababaaa" "abababababaaaabaabbbbabbababababbbabababbbbbbbbabababbbbbbabbabababbbbaaaaabbabababaaaaa"```  
text is: abababaaa
pattern is: abababababaaaabaabbbbabbababababbbabababbbbbbbbabababbbbbbabbabababbbbaaaaabbabababaaaaa

Result of Naive approach
found in indexes: []
preprocess cost: 0
number of shifts: 0
number of comparisons: 0

Result of DFA approach
found in indexes: []
preprocess cost: 12369
number of shifts: 9
number of comparisons: 9

Result of KMP approach
found in indexes: []
preprocess cost: 125
number of shifts: 9
number of comparisons: 14

- ```python3 string-matching.py "abababababaaaabaabbbbabbababababbbabababbbbbbbbabababbbbbbabbabababbbbaaaaabbabababaaaaa" "abababaaa"```  
text is: abababababaaaabaabbbbabbababababbbabababbbbbbbbabababbbbbbabbabababbbbaaaaabbabababaaaaa
pattern is: abababaaa

Result of Naive approach
found in indexes: [4, 77]
preprocess cost: 0
number of shifts: 270
number of comparisons: 191

Result of DFA approach
found in indexes: [4, 77]
preprocess cost: 141
number of shifts: 88
number of comparisons: 88

Result of KMP approach
found in indexes: [4, 77]
preprocess cost: 13
number of shifts: 88
number of comparisons: 116
## Discussion
The experience was good, it was interesting to investigate these algorithms using empirical methods. It's also interesting to notice how empirical methods can fall short in certain analyses if there is not sufficient background knowledge in the area. For example, if we only used small patterns, then we might not have collected data that reflected the preprocessing costs in the KMP vs automata string matching algorithms. 
