# -*- coding: utf-8 -*-
"""
This project is about using a hidden Markov model for gene finding in prokaryotes 

We have a data set containing 11 Staphylococcus genomes, each containing several 
genes (i.e. substring) obeying the "gene syntax". The genomes are between 1.8 million 
and 2.8 million nucleotides. For 5 of the genomes, we also know the location of 
the genes. For the remaining 6 genomes, we only know that they contain genes according 
to the "gene syntax". The genomes and their annontations are given in FASTA format. 

In this project, we will train a hidden markov model on the 11 genomes with Baum-Welch 
Algorithm. After that, we will use viterbi algorithm to infer the most possible hidden states
(i.e, genes or not) of the fist five genomes. Finally we will compare the predictions with the true 
gene coding and calculate the precision of the prediction.
"""
import numpy as np
import pandas as pd
import glob
import re
import torch
from Two_Directions_Process import drtprocess
from BW_init import init_sim
from BW_pars import BW_alpha, BW_beta, BW_r, BW_s, annotation_map, genome_map
from BW_update import update


def read_genomes(path):
    genomes = []
    files = glob.glob(path + '/genome*.txt')
    sortfun = lambda x: int(re.findall('genome(.*).txt', x).pop())
    files = sorted(files, key = sortfun)
     
    for file in files:
        genome = open(file).readlines()
        genome = [x.strip('\n') for x in genome]
        genomes.append(list(''.join(genome)))
    
    return genomes

def read_annotation(path):
    annotations = []
    
    files = glob.glob(path + '/annotation*.txt')
    sortfun = lambda x: int(re.findall('annotation(.*).txt', x).pop())
    files = sorted(files, key = sortfun)
     
    for file in files:
        annotation = open(file).readlines()
        annotation = [x.strip('\n') for x in annotation]
        annotations.append(list(''.join(annotation)))
    
    return annotations
'''
def encode_sequence(seq_list, alphabet):
    
    Encodes list of character sequences into integer tensors using a given alphabet.
    
    char2idx = {ch: i for i, ch in enumerate(alphabet)}
    encoded = [torch.tensor([char2idx[ch] for ch in seq], dtype=torch.long) for seq in seq_list]
    return encoded

def read_genomes_torch(path, alphabet='ACGTN'):
    genomes = []
    files = sorted(glob.glob(path + '/genome*.txt'), key=lambda x: int(re.findall(r'genome(.*).txt', x)[0]))
    for file in files:
        with open(file) as f:
            seq = ''.join([line.strip() for line in f.readlines()])
            genomes.append(list(seq))
    return encode_sequence(genomes, alphabet)

def read_annotations_torch(path, labels='OEPIT'):
    annotations = []
    files = sorted(glob.glob(path + '/annotation*.txt'), key=lambda x: int(re.findall(r'annotation(.*).txt', x)[0]))
    for file in files:
        with open(file) as f:
            ann = ''.join([line.strip() for line in f.readlines()])
            annotations.append(list(ann))
    return encode_sequence(annotations,labels)
'''                        
def main():
    '''
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tensor = tensor.to(device)
    '''
    genomes = read_genomes('./data')
    annotations = read_annotation('./data')
    print('genomes and annotations read successfully')
    ##change False to True when finding reversed genes
    genomes, annotations = drtprocess(genomes, annotations, False)
    genomes = [pd.Series(x) for x in genomes]
    annotations = [pd.Series(x) for x in annotations]
    print('genomes and annotations processed successfully')
    p0, A0, B0 = init_sim(len(np.unique(annotations[0])), len(np.unique(genomes[0])))
    print(p0)
    print(A0)
    print(B0)
    print('start training...')
    ##EM - Loop until p, A, B convergence, we set the convergence threshold as 0.01
    while True:
        alphas = BW_alpha(genomes, A0, B0, p0)
        print("alphas: "+str(alphas))
        betas = BW_beta(genomes, A0, B0)
        print("betas: "+str(betas))
        rs = BW_r(alphas, betas, A0, B0)
        print("rs: "+str(rs))
        ss = BW_s(genomes, alphas, betas, A0, B0)
        print("ss: "+str(ss))
        p, A, B = update(genomes, rs, ss)
        if (abs(B - B0) < 0.03).all() and (abs(A - A0) < 0.03).all() and (abs(p - p0) < 0.03).all():
            break
        else:
            p0 = p
            A0 = A
            B0 = B
            print(p)
            print(A)
            print(B)

    
    # Save parameters to files
    np.save('p.npy', p)
    np.save('A.npy', A)
    np.save('B.npy', B)
    print("Parameters saved successfully to p.npy, A.npy, B.npy")
    
    
    
if __name__ == "__main__":
    main()