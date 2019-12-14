import sys
#naive approach
def naive_str_match(pattern, text):
    indexes = []
    num_shifts = 0
    num_comparisons = 0
    valid = True
    # Loop over possible indexes
    for i in range(len(text) - len(pattern) + 1):
        # Check validity of current shift
        for j in range(len(pattern)):
            num_shifts += 1 
            num_comparisons += 1
            if(text[j+i] != pattern[j]):
                valid = False
                break
        if valid:
            indexes.append(i)
        valid = True
    return {'indexes' : indexes, 'prep_cost' : 0, 'num_shifts' : num_shifts, 'num_comparisons' : num_comparisons}

#finite automata approach
def fa_str_match(pattern, text):
    indexes = []
    num_shifts = 0
    num_comparisons = 0
    MATCH = len(pattern)
    # Get transitions
    trans_table, prep_cost = build_trans(pattern, set(pattern))
    # print("Transition table: " + str(trans_table))
    q = 0 # Set state to start state

    # Pass text through our DFA
    for i in range(len(text)): 
        num_shifts += 1
        try:
            num_comparisons += 1
            q = trans_table[q, text[i]] # get next state #is this a type of comparison?
        except:
            q = 0
            continue
        # print(str(i) + " arrives at : " + str(q))
        if q == MATCH: 
            indexes.append(i-len(pattern)+1)

    return {'indexes' : indexes, 'prep_cost' : prep_cost, 'num_shifts' : num_shifts, 'num_comparisons' : num_comparisons}

# calculate the transition function tables
def build_trans(pattern, alphabet):
    prep_cost = 0
    trans_table = {}
    # print("Alphabet: " + str(alphabet))
    for q in range(len(pattern) + 1): #cur state
        for a in alphabet:
            q_next, prep_cost = get_next_state(pattern, q, a, prep_cost)
            trans_table[(q,a)] = q_next
    return trans_table, prep_cost

# find the output of the transition function
def get_next_state(pattern, q, a, prep_cost):
    if (q < len(pattern) and a == pattern[q]): # the ideal next state
        return q + 1, prep_cost + 1
    q_next = q
    while q_next > 0: #start from the largest possible state
        prep_cost += 1
        if pattern[q_next - 1] == a: 
            prep_cost += 1
            i = 0
            while i < (q_next - 1): # check the rest of the pattern-ix
                prep_cost += 1
                if (pattern[i] != pattern[q - q_next + i + 1]): 
                    break
                i += 1
            prep_cost += 1
            if i == q_next - 1:
                return q_next, prep_cost
        q_next -= 1
    return 0, prep_cost

# generate the table containing the "effort saving" index to check
def KMP_preprocess(pattern):
    jump_table = []
    preprocess_cost = 0
    l = len(pattern)
    if l == 0:
        return jump_table, preprocess_cost
    jump_table.append(0)
    preprocess_cost += 1
    if l == 1:
        return jump_table, preprocess_cost
    i = 0
    j = 1
    while j < l:
        preprocess_cost += 1 # comparison; remaining work is in constant
        if pattern[i] == pattern[j]: 
            jump_table.append(i + 1)
            j = j + 1
            i = i + 1
        else: 
            if i == 0:
                jump_table.append(0)
                j = j + 1
            i = jump_table[i - 1] #keep jumping back until the other conditions are hited
            
    return jump_table, preprocess_cost

#KMP approach
def KMP_str_match(pattern, text):
    indexes = []
    num_shifts = 0
    num_comparisons = 0
    jump_table, preprocess_cost = KMP_preprocess(pattern)
    l_text = len(text)
    l_pattern = len(pattern)
    p = 0
    i = 0
    while i < l_text: # always start with new ptrs, but have not check yet
        if p == l_pattern: #found it
            indexes.append(i - l_pattern)
            p = jump_table[p - 1]
        else: 
            num_comparisons += 1
            if (pattern[p] == text[i]): 
                p = p + 1
                num_shifts += 1
                i = i + 1
            else: 
                if p == 0:
                    num_shifts += 1
                    i = i + 1
                else: 
                    p = jump_table[p - 1]
     
    if p == l_pattern:
        indexes.append(i - l_pattern)
    return {'indexes' : indexes, 'prep_cost' : preprocess_cost, 'num_shifts' : num_shifts, 'num_comparisons' : num_comparisons}

def pattern_matching():
    if (len(sys.argv) != 3):
        print("Invalid usage. " + sys.argv[0] + "<text> <pattern>")
        exit()

    text = sys.argv[1]
    pattern = sys.argv[2]
    print("text is: " + str(text))
    print("pattern is: " + str(pattern))
    print("\nResult of Naive approach")
    result = naive_str_match(pattern, text)
    print("found in indexes: " + str(result['indexes']))
    print("preprocess cost: " + str(result['prep_cost']))
    print("number of shifts: " + str(result['num_shifts']))
    print("number of comparisons: " + str(result['num_comparisons']))

    print("\nResult of DFA approach")
    result = fa_str_match(pattern, text)
    print("found in indexes: " + str(result['indexes']))
    print("preprocess cost: " + str(result['prep_cost']))
    print("number of shifts: " + str(result['num_shifts']))
    print("number of comparisons: " + str(result['num_comparisons']))

    print("\nResult of KMP approach")
    result = KMP_str_match(pattern, text)
    print("found in indexes: " + str(result['indexes']))
    print("preprocess cost: " + str(result['prep_cost']))
    print("number of shifts: " + str(result['num_shifts']))
    print("number of comparisons: " + str(result['num_comparisons']))

if __name__ == "__main__":
    pattern_matching()