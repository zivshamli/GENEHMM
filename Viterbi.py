# -*- coding: utf-8 -*-
"""
After Baum Welch training, we use viterbi to find the most possible hidden sequences for 
the first five genome sequences, and evaluate the accruacy
"""
import numpy as np
import pandas as pd
from Two_Directions_Process import drtprocess
from hmm_main import read_genomes, read_annotation


##suppose we have already have the converged initial probbability, transition matrix and emission matrix
annotation_map = {'P': 0,'E':1,'I':2,'T':3,'O':4}
genome_map = {'A' : 0, 'T' : 1, 'C' : 2, 'G' : 3 }
genomes = read_genomes('./data')
annotations = read_annotation('./data')
print('genomes and annotations read successfully')
##change False to True when finding reversed genes
genomes, annotations = drtprocess(genomes, annotations, False)
genomes = [pd.Series(x) for x in genomes]
annotations = [pd.Series(x) for x in annotations]


genomes_test = genomes[0:len(annotations)]
genomes_test = [x.map(genome_map) for x in genomes_test]
genomes_test = genomes_test[0:1]  # For testing, use only the first genome

annotations = [x.map(annotation_map) for x in annotations]
annotations=annotations[0:1]  # For testing, use only the first annotation
epsilon = 1e-12



def viterbi(genomes, A, B, p):
    D = len(genomes)
    T = [len(x) for x in genomes]
    print("Number of genomes: ", D)
    print("Number of time steps: ", T)
    
    sequences = []
    for d in range(D):
        obs = genomes[d]
        
        seqs = np.zeros((A.shape[0], T[d]))
        traces = np.zeros((A.shape[0], T[d]), dtype = int)
        best_seq = np.zeros(T[d], dtype = int)
        
        ##to avoid underflow, we work in log space 
        seqs[:, 0] = np.log(p + epsilon) + np.log(B[:, obs[0]] + epsilon)

        
        traces[:, 0] = 0
        for t in range(1, T[d]):
            for j in range(A.shape[0]):
                seqs[j,t] = (seqs[:,t-1] + np.log(A[:,j] + epsilon) + np.log(B[j, obs[t]] + epsilon)).max()
                traces[j,t] = (seqs[:,t-1] + np.log(A[:,j] + epsilon) + np.log(B[j, obs[t]] + epsilon)).argmax()

        
        ##back-tracking to find the best hidden sequence
        best_seq[T[d] - 1] = (seqs[:,T[d] - 1]).argmax()
        for i in reversed(range(T[d] - 1)):
            from_idx = traces[:,(i+1)][best_seq[i+1]]
            best_seq[i] = from_idx

        sequences.append(best_seq)
    
    return sequences


def main():
    p = np.load("p.npy")
    A = np.load("A.npy")
    B = np.load("B.npy")
    print("Parameters loaded successfully from p.npy, A.npy, B.npy")
    print('start viterbi...')
    annotations_test = viterbi(genomes_test, A, B, p)
    precision = np.mean([np.mean(x == y) for x,y in zip(annotations_test, annotations)])  
    
    print('Precision of Hidden States prediction for the first five genomes is %.2f' %precision)
    return annotations_test
    
if __name__ == "__main__":
    main()