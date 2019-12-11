
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
    return shifts, 0, num_shifts, num_comparisons

MATCH = -1

def fa_str_match(pattern, text):
    shifts = []
    num_comparisons = 0
    MATCH = len(set(pattern))
    # Get transitions
    fa, prep_cost = build_fa(pattern, set(pattern))
    q = 0 # Set state to start state

    # Pass text through our DFA
    for i in range(len(text)-len(pattern)):
        num_comparisons += 1
        try:
            q = fa[q, text[i]] # get next state
        except:
            q = 0
            continue
        if q == MATCH: 
            shifts.append(i-len(pattern)+1)

    return shifts, prep_cost, 0, num_comparisons

def build_fa(pattern, alphabet):
    prep_cost = 0
    fa = {}
    for q in range(len(alphabet)):
        for a in alphabet:
            k = min(len(alphabet), q+1)
            while(not(pattern[1:q] + a).endswith(pattern[1:k])):
                prep_cost += 1
                k -= 1
            fa[(q,a)] = k
    return fa, prep_cost

def KMP_str_match(pattern, text):
    pass # TODO

def main():
    print(naive_str_match("dog","A quick-brown dog jumped over \
    the lazy dog which was it’s own mother."))
    print(fa_str_match("dog","A quick-brown dog jumped over \
    the lazy dog which was it’s own mother."))
    print(len("A quick-brown dog jumped over \
    the lazy dog which was it’s own mother."))

main()
