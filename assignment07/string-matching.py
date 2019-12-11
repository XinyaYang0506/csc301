
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

def KMP_str_match(pattern, text):
    pass # TODO

def main():
    print(naive_str_match("dog","A quick-brown dog jumped over \
    the lazy dog which was it’s own mother."))
