import string

def concordance (filename):
    infile = open(filename, "r")
    hist = {}    
    line_number = 0
    
    for line in infile:
        line_number = line_number + 1
        word_list = line.split()
        
        for word in word_list:
            w = word.strip(string.punctuation).lower()
            if w != '':
                lst = hist.get(w, [])  
                #print(lst)
                if line_number not in lst:
                    lst.append(line_number)
                    hist[w] = lst
    return hist
