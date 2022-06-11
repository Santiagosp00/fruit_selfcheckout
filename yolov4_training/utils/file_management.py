import re
from os import fsync

def update_simple(filename,dico):

    RE = '(('+'|'.join(dico.keys())+')\s*=)[^\r\n]*?(\r?\n|\r)'
    pat = re.compile(RE)

    def jojo(mat,dic = dico ):
        return dic[mat.group(2)].join(mat.group(1,3))

    with open(filename,'rb') as f:
        content = f.read().decode('utf-8')

    with open(filename,'wb') as f:
        f.write(pat.sub(jojo,content).encode('utf-8'))

def update_multiple_pattern(filename, old, new):
    #read input file
    fin = open(filename, "rt")
    #read file contents to string
    data = fin.read()
    #replace all occurrences of the required string
    data = data.replace(old, new)
    #close the input file
    fin.close()
    #open the input file in write mode
    fin = open(filename, "wt")
    #overrite the input file with the resulting data
    fin.write(data)
    #close the file
    fin.close()

def create_file_from_content(filename, content):
    fin = open(filename, "wt")
    #overrite the input file with the resulting data
    fin.write(content)
    #close the file
    fin.close()

def create_file_from_list(filename, data):
    data.sort()
    fin = open(filename, "w")
    lenght = len(data)
    for i, element in enumerate(data):
        if i == lenght-1:
            fin.write(element)
        else:
            fin.write(element + "\n")
    fin.close()
    
