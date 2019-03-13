def z_algorithm(concat_str, p, t):
    z_val_arr = ['x']
    substr = concat_str[1::]
    for index in range(len(concat_str[1::])):
        counter = 0
        while counter < len(substr):
            if substr[counter] == concat_str[counter] and counter + 1 != len(substr):
                counter += 1
            elif (substr[counter] == concat_str[counter] and counter + 1 == len(substr))\
                    or (substr[counter] != concat_str[counter]):
                if substr[counter] == concat_str[counter] and counter + 1 == len(substr):
                    counter += 1
                z_val_arr.append(counter)
                counter = len(substr)
                substr = substr[1::]
    print("\tZ-Array of concatenated pattern and text: %s" % z_val_arr)
    if len(p) in z_val_arr:
        print("\tPattern present in text? : Yes.")
        t_idx = len(z_val_arr) - z_val_arr.index(len(p)) + 1
        match_indices = []

        for p_char in p:
            if p_char == t[t_idx]:
                match_indices.append((p_char, t_idx))
                t_idx += 1
        print("\tLocation of pattern characters in text: %s" % match_indices)
    else:
        print("Pattern present in text? : No.")

def kmp_algorithm(p, t):
    index = 2
    prefix_table = [0]
    t_idx = 0
    p_idx = 0
    for i in range(len(p) - 1):
        substr = [p_char for idx,p_char in zip(range(index), p)]
        substr_prefixes = []
        substr_suffixes = []
        temp = []
        prefix_temp = ""
        suffix_temp = ""
        for prefix,suffix,substr_idx in zip(substr,reversed(substr),range(len(substr) - 1)):
            prefix_temp += prefix
            suffix_temp = suffix + suffix_temp
            substr_prefixes.append(prefix_temp)
            substr_suffixes.append(suffix_temp)
        for prefix,suffix in zip(substr_prefixes,substr_suffixes):
            if prefix == suffix:
                temp.append(len(prefix))
            else:
                temp.append(0)
        prefix_table.append(max(temp))
        index += 1
    print("\tPrefix Table: %s" % prefix_table)
    while t_idx < len(t) and p_idx < len(p):
        if p[p_idx] == t[t_idx]:
            p_idx += 1
            t_idx += 1
        else:
            if prefix_table[p_idx] > 0:
                p_idx = prefix_table[p_idx] - 1
            else:
                p_idx = prefix_table[p_idx]
                t_idx += 1
    if p_idx == len(p):
        print("\tPattern present in text? : Yes.")
        match_indices = [(t[match], match + 1) for match in range(t_idx - len(p), t_idx)]
        print("\tLocation of pattern characters in text: %s" % match_indices)
    else:
        print("\tPattern present in text? : No.")

pattern = "ACACAGT"
text = "ACAT ACGACACAGT"
print("Z-Algorithm String Matching")
z_algorithm(pattern + "$" + text, pattern, text)
print("KMP Algorithm String Matching")
kmp_algorithm(pattern, text)