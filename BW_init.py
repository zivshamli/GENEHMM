# -*- coding: utf-8 -*-
import numpy as np

"""
Initalize Baum - Welch parameters p, A, B
"""

def init_sim(hid_num, obs_num):
    """
    hid_num is the number of hidden states, in our project only two states, coding(C)
               and non-coding (N). In the reversed sequence, there is also a reversed state(R)
    obs_num is the number of observation states, we have four states (ATCG) in our project.
    """    

## initialize initial probability of hidden states p
    p = np.array([0,0,0,0,1])


## initialize transition matrix A
    A =  np.array([
    [0.95964685, 0.021879948, 0.008732786, 0.000143947, 0.009596468],
    [0.018512383, 0.828294542, 0.134680692, 0.018470968, 0.0000414147],
    [0.006487174, 0.138308247, 0.847996608, 0.007207971, 0],
    [0.000672043, 0.02078533, 0.006864439, 0.960061444, 0.011616743],
    [0.010861057, 0, 0, 0.010665362, 0.978473581]
])
   # A = A / A.sum(1).reshape((hid_num, 1))

## initialize emission matrix B
    B = np.array([
    [0.3, 0.3, 0.2, 0.2],  # 0: P - Promoter
    [0.1, 0.1, 0.4, 0.4],  # 1: E - Exon
    [0.2, 0.2, 0.3, 0.3],  # 2: I - Intron
    [0.3, 0.2, 0.3, 0.2],  # 3: T - Terminator
    [0.25, 0.25, 0.25, 0.25]  # 4: O - Other
    ])
   # B = np.random.random((hid_num, obs_num))
    #B = B / B.sum(1).reshape((hid_num, 1))
    
    return (p, A, B)