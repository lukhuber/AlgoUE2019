#!/usr/bin/python3

import argparse
import sys

def Main():
    debug = True
    args = initArguments()
    stdin = sys.stdin

    sequence1 = getFirstSequence()
    sequence2 = getSecondSequence()

    if debug == True:
        DEBUG(sequence1, sequence2)
     

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
    parser.add_argument('--gap', dest = 'gap', default = -2, type = int, help = 'Scoring value for a gap. Default = -2')

    return parser.parse_args()

def DEBUG(sequence1, sequence2):
    seq1_lines = round(len(sequence1[1]) / 60 + 0.5)
    seq2_lines = round(len(sequence2[1]) / 60 + 0.5)
    
    print(sequence1[0], ' --- ', sequence1[1])
    print(sequence2[0], ' --- ', sequence2[1])
    

if __name__ == "__main__":
    Main()