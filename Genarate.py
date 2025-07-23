import numpy as np

# Inverse mappings from indices to states and nucleotides
annotation_map = {'P': 0, 'E': 1, 'I': 2, 'T': 3, 'O': 4}
genome_map = {'A': 0, 'T': 1, 'C': 2, 'G': 3}
state_map_inv = {v: k for k, v in annotation_map.items()}
obs_map_inv = {v: k for k, v in genome_map.items()}

def generate_and_save_gene_streaming(p, A, B, length,
                                     state_map_inv, obs_map_inv,
                                     gene_filename="synthetic_gene.txt",
                                     annotation_filename="synthetic_annotation.txt",
                                     line_length=60):
    """
    Generate a synthetic gene sequence and annotation from HMM parameters
    and save directly to files while streaming (writing chars as they are generated).

    Args:
        p, A, B: trained HMM parameters (numpy arrays)
        length: length of sequence to generate (int)
        state_map_inv, obs_map_inv: inverse mappings dicts
        gene_filename: output filename for nucleotide sequence
        annotation_filename: output filename for hidden states
        line_length: number of chars per line in output files
    """
    with open(gene_filename, 'w') as f_gene, open(annotation_filename, 'w') as f_ann:
        count = 0
        # Sample initial state and observation
        z = np.random.choice(len(p), p=p)
        x = np.random.choice(B.shape[1], p=B[z])

        f_gene.write(obs_map_inv[x])
        f_ann.write(state_map_inv[z])
        count += 1

        for _ in range(1, length):
            z = np.random.choice(len(p), p=A[z])
            x = np.random.choice(B.shape[1], p=B[z])

            f_gene.write(obs_map_inv[x])
            f_ann.write(state_map_inv[z])
            count += 1

            if count % line_length == 0:
                f_gene.write('\n')
                f_ann.write('\n')

        # Add final newline if needed
        if count % line_length != 0:
            f_gene.write('\n')
            f_ann.write('\n')

    print(f"Saved gene sequence to '{gene_filename}' and annotation to '{annotation_filename}'")

def main():
    # Load trained HMM parameters from .npy files
    p = np.load("p.npy")
    A = np.load("A.npy")
    B = np.load("B.npy")

    # Length of synthetic gene to generate
    gene_length = 4000000

    # Generate and save gene sequence + annotation
    generate_and_save_gene_streaming(p, A, B, gene_length,
                                     state_map_inv, obs_map_inv,
                                     gene_filename="synthetic_gene.txt",
                                     annotation_filename="synthetic_annotation.txt",
                                     line_length=60)

if __name__ == "__main__":
    main()
