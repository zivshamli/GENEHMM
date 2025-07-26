import numpy as np

annotation_map = {'P': 0, 'E': 1, 'I': 2, 'T': 3, 'O': 4}
genome_map = {'A': 0, 'T': 1, 'C': 2, 'G': 3}
state_map_inv = {v: k for k, v in annotation_map.items()}
obs_map_inv = {v: k for k, v in genome_map.items()}

def normalize_probs(arr):
    arr = np.asarray(arr)
    row_sums = arr.sum(axis=-1, keepdims=True)
    return arr / np.where(row_sums == 0, 1, row_sums)

def sample_from_prob(prob_dist):
    prob_dist = np.array(prob_dist, dtype=np.float64)
    prob_dist /= prob_dist.sum()
    return np.random.choice(len(prob_dist), p=prob_dist)

def generate_and_save_gene_streaming(p, A, B, length,
                                     state_map_inv, obs_map_inv,
                                     gene_filename="synthetic_gene.txt",
                                     annotation_filename="synthetic_annotation.txt",
                                     line_length=60):
    """
    Generate a synthetic gene sequence and annotation using HMM parameters
    and stream output to files.
    """
    # Normalize probabilities
    p = normalize_probs(p)
    A = normalize_probs(A)
    B = normalize_probs(B)

    with open(gene_filename, 'w') as f_gene, open(annotation_filename, 'w') as f_ann:
        count = 0
        z = sample_from_prob(p)
        x = sample_from_prob(B[z])

        f_gene.write(obs_map_inv[x])
        f_ann.write(state_map_inv[z])
        count += 1

        for _ in range(1, length):
            z = sample_from_prob(A[z])
            x = sample_from_prob(B[z])

            f_gene.write(obs_map_inv[x])
            f_ann.write(state_map_inv[z])
            count += 1

            if count % line_length == 0:
                f_gene.write('\n')
                f_ann.write('\n')

        if count % line_length != 0:
            f_gene.write('\n')
            f_ann.write('\n')

    print(f"Saved gene sequence to '{gene_filename}' and annotation to '{annotation_filename}'")

def main():
    p = np.load("p.npy")
    A = np.load("A.npy")
    B = np.load("B.npy")

    gene_length = 4000000

    generate_and_save_gene_streaming(p, A, B, gene_length,
                                     state_map_inv, obs_map_inv,
                                     gene_filename="synthetic_gene.txt",
                                     annotation_filename="synthetic_annotation.txt",
                                     line_length=60)

if __name__ == "__main__":
    main()
