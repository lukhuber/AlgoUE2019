#!/usr/bin/python3

import argparse
import sys

def Main():
    debug = False
    args = initArguments()

    global mismatch
    mismatch = args.mismatch
    global gap
    gap = args.gap
    global match
    match = args.match

    sequence1 = getFirstSequence()
    sequence2 = getSecondSequence()

    matrix = initMatrix(sequence1, sequence2)



    # ---------------
    seq1_len = len(sequence1[1])
    seq2_len = len(sequence2[1])

    shorter_seq = sequence1[1] if seq1_len < seq2_len else sequence2[1]
    longer_seq = sequence2[1] if seq1_len > seq2_len else sequence1[1]

    if seq1_len <= seq2_len:
        sequence1[1] = shorter_seq
        sequence2[1] = longer_seq
    else:
        sequence2[1] = shorter_seq
        sequence1[1] = longer_seq   

    #print(shorter_seq)
    #print(longer_seq)
    #print("")

    col = -1
    row = -1
    index_ss = 0
    index_ls = -1

    score = matrix[row][col]

    len_longer_seq = len(longer_seq)
    len_shorter_seq = len(shorter_seq)

    while row*-1 <= len_longer_seq and col*-1 <= len_shorter_seq:

            ## Get values from each possible step
            diag = matrix[row][col] + matrix[row-1][col-1]
            vert = matrix[row][col] + matrix[row-1][col]
            hrzt = matrix[row][col] + matrix[row][col-1]

            ## Get variable with highest value
            values = (diag, vert, hrzt)
            highest = values.index(max(values))
            
            ## Diagonal
            if highest == 0:
                ## Adjust index for string manipulation
                index_ls += -1
                index_ss += -1

                ## Adjust score
                score += matrix[row-1][col-1]

                ## Change current pos in matrix
                row += -1
                col += -1

            ## Vertical
            if highest == 1:


                ## Adjust score
                score += matrix[row-1][col]

                ## Change current pos in matrix
                row += -1

                ## Edit longer sequence
                longer_seq = longer_seq[:index_ls] + "-" + longer_seq[index_ls:]

                ## Adjust index for string manipulation
                index_ls += -2
                index_ss += -1

            ## Horizontal
            if highest == 2:

                ## Adjust score
                score += matrix[row][col-1]

                ## Change current pos in matrix
                col += -1

                ## Edit shorter sequence
                shorter_seq = shorter_seq[:index_ss] + "-" + shorter_seq[index_ss:]

                ## Adjust index for string manipulation
                index_ls += -1
                index_ss += -2

    sequence1[1] = longer_seq
    sequence2[1] = shorter_seq
    
    # ---------------

    printResult(sequence1, sequence2)

    if debug == True:
        DEBUG(sequence1, sequence2)

    for i, v in enumerate(matrix): # Nur temporär! Printet die Matrix
        print(matrix[i])

def printResult(seq1, seq2):
    lines = round(len(seq1[1]) / 60 + 0.5) # Beide Variablen werden benötigt um zu wissen, wieviele 60er Schritt-Zeilen notwendig sind.
    
    for i in range (1, lines + 1): # Printet die erste Sequenz in jeweils 60er Schritten
        if i == 1: 
            print(seq1[0], '  ', seq1[1][0:60])
            print(seq2[0], '  ', seq2[1][0:60])
            print("")
        else:
            print(seq1[0], '  ', seq1[1][i*60-60:i*60])
            print(seq2[0], '  ', seq2[1][i*60-60:i*60])
            print("")

def initMatrix(seq1, seq2):
    seq1_length = len(seq1[1])
    seq2_length = len(seq2[1])

    cols = seq1_length if seq1_length <= seq2_length else seq2_length
    rows = seq1_length if seq1_length >= seq2_length else seq2_length

    matrix = [[0 for x in range(cols+1)] for y in range(rows+1)]

    for i, v in enumerate(matrix):
        matrix[i][0] = i * -1
    
    for i, v in enumerate(matrix[0]):
        matrix[0][i] = i * -1

    matrix = fillMatrix(seq1, seq2, matrix)
    
    return matrix

def fillMatrix(seq1, seq2, matrix):
    seq1_len = len(seq1[1])
    seq2_len = len(seq2[1])

    print(seq1_len, seq2_len)

    shorter_seq = seq1[1] if seq1_len < seq2_len else seq2[1]
    longer_seq = seq2[1] if seq1_len < seq2_len else seq1[1]

    cols = len(shorter_seq)
    rows = len(longer_seq)

    print(len(longer_seq), len(shorter_seq))
    print (rows, cols)

    counter = 0

    #try:
    for r in range(0, rows):
        for c in range(0, cols):
            if longer_seq[r] == shorter_seq[c]:
                rgh = matrix[r+1][c] + gap
                dwn = matrix[r][c+1] + gap
                dig = matrix[r][c] + match
            else:
                rgh = matrix[r+1][c] + gap
                dwn = matrix[r][c+1] + gap
                dig = matrix[r][c] + mismatch

            matrix[r+1][c+1] = max(rgh, dwn, dig)
            
            counter += 1
    #except:
    #    print(r, c)
    
    return matrix

def getFirstSequence():
    sequence = ['', '']
    found = False

    for line in sys.stdin:
        if line[0] == '>' and found == False:
            pos = line.find('|')
            sequence[0] = line[1:pos - 1]
            found = True
            continue
        
        if line[0] == '>' and found == True:
             # Breaks the for-loop, when second sequence starts
             break

        sequence[1] += line.replace('\n', '')
    
    sys.stdin.seek(0) # Reset STDIN for further parsing
    return sequence

def getSecondSequence():
    sequence = ['', '']
    found = False

    for line in sys.stdin:
        if line[0] == '>' and found == False:
            found = True
            continue

        if line[0] == '>' and found == True:
            pos = line.find('|')
            sequence[0] = line[1:pos - 1]
            continue

        if sequence[0] != '' and found == True:
            sequence[1] += line.replace('\n', '')
    
    sys.stdin.seek(0) # Reset STDIN for further parsing
    return sequence

def initArguments():
    parser = argparse.ArgumentParser(prog='lukhuber-NW.py', description='Aligns two different DNA sequences \
        Requires an input in form of a multi-fasta file via STDIN')

    parser.add_argument('--match', dest = 'match', default = 1, type = int, help = 'Scoring value for a match. Default = +1')
    parser.add_argument('--mismatch', dest = 'mismatch', default = -1, type = int, help = 'Scoring value for a mismatch. Default = -1')
    parser.add_argument('--gap', dest = 'gap', default = -1, type = int, help = 'Scoring value for a gap. Default = -2')

    return parser.parse_args()

def DEBUG(sequence1, sequence2):
    print("### DEBUG MODE IS ON! ###")
    print("--- Start of debug output ---")
    print("")

    seq1_lines = round(len(sequence1[1]) / 60 + 0.5) # Beide Variablen werden benötigt um zu wissen, wieviele 60er Schritt-Zeilen notwendig sind.
    seq2_lines = round(len(sequence2[1]) / 60 + 0.5)
    
    for i in range (1, seq1_lines + 1): # Printet die erste Sequenz in jeweils 60er Schritten
        if i == 1: 
            print(sequence1[0], '  ', sequence1[1][0:60])
        else:
            print(sequence1[0], '  ', sequence1[1][i*60-60:i*60])

    for i in range(0,75):  # Unschöne Lösung den Strich zwischen den beiden Sequenzen zu printen
        print("-", end='')
    print()

    for i in range (1, seq2_lines + 1): # Printet die erste Sequenz in jeweils 60er Schritten
        if i == 1: 
            print(sequence2[0], '  ', sequence2[1][0:60])
        else:
            print(sequence2[0], '  ', sequence2[1][i*60-60:i*60])
    
    print("")

    if len(sequence1[1]) != len(sequence2[1]):
        print("ERROR! Sequences are not equally long")
        print("Lenght Seq1: ", len(sequence1[1]))
        print("Length Seq2: ", len(sequence2[1]))
    print("--- END of debug output ---")
    print("")

if __name__ == "__main__":
    Main()