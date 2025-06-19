# -*- coding: utf-8 -*-
"""
Process DNA genomes and annotation tracks.
Simulates biological dual-strand reading (reverse-complement logic).
"""

def drtprocess(genomes, annotations, reverse=False):
    """
    Processes genomes and annotations.
    If reverse=True, reverses sequences and treats annotations accordingly.

    Annotation codes:
        P → Promoter
        E → Exon
        I → Intron
        T → Terminator
        O → Other
    """

    if reverse:
        # Reverse genome and annotations
        genomes = [reverse_complement(seq) for seq in genomes]
        annotations = [seq[::-1] for seq in annotations]

        # Annotation stays semantically the same, only reversed in order
        # If needed, you can flip direction-specific markers (not in use here)
    else:
        pass  # No reverse: return as-is

    return genomes, annotations


def reverse_complement(seq):
    """
    Simulates reverse-complement of a DNA strand.
    """
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement.get(base, base) for base in reversed(seq))
