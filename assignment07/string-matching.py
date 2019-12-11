
def naive_str_match(pattern, text):
    shifts = []
    num_shifts = 0
    num_comparisons = 0
    valid = True
    # Loop over possible shifts
    for i in range(len(text)-len(pattern)):
        num_shifts += 1
        # Check validity of current shift
        for j in range(len(pattern)):
            num_comparisons += 1
            if(text[j+i] != pattern[j]):
                valid = False
                break
        if valid:
            shifts.append(i)
        valid = True
    return shifts, num_shifts, num_comparisons

MATCH = -1

def fa_str_match(pattern, text):
    shifts = []
    num_comparisons = 0 # TODO
    # Get transitions
    fa, prep_cost = build_fa(pattern)
    q = 0 # Set state to start state

    # Pass text through our DFA
    for i in range(len(text)):
        q = fa[q, text[i]] # get next state
        if q == MATCH: 
            shifts.append(i)

    return shifts, prep_cost, num_comparisons

def build_fa(pattern):
    fa = {}
    # TODO



def KMP_preprocess(pattern):
    tql = []
    l = len(pattern)
    if l == 0:
        return tql
    tql.append(0)
    if l == 1:
        return tql
    i = 0
    j = 1
    while j < l:
        if pattern[i] == pattern[j]: 
            tql.append(i + 1)
            j = j + 1
            i = i + 1
        else: 
            if i == 0:
                tql.append(0)
                j = j + 1
            i = tql[i - 1]
            
    print('tql: ' + str(tql))
    return tql

def KMP_str_match(pattern, text):
    indexes = []
    tql = KMP_preprocess(pattern)
    l_text = len(text)
    l_pattern = len(pattern)
    p = 0
    i = 0
    while i < l_text: # always start with new ptrs, but have not check yet
        if p == l_pattern:
            indexes.append(i - l_pattern)
            p = tql[p - 1]
        else: 
            if (pattern[p] == text[i]): 
                p = p + 1
                i = i + 1
            else: 
                if p == 0:
                    i = i + 1
                else: 
                    p = tql[p - 1]
     
    if p == l_pattern:
        indexes.append(i - l_pattern)
    return indexes

def main():
    print(KMP_str_match("dog","A quick-brown dog jumped over the lazy dog which was it’s own mother."))

main()