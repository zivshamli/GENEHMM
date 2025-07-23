# HMM-Based Gene Sequence Modeling and Synthetic Gene Generation

This project applies a **Hidden Markov Model (HMM)** to genomic gene sequences, with the dual goal of:
- Learning the statistical structure of real gene sequences.
- Generating synthetic gene sequences that mimic real biological patterns.

The project includes full HMM implementation (training and decoding) and uses **Baum-Welch** and **Viterbi** algorithms to model gene structure and generate novel artificial sequences.

## 🧬 Project Overview

We trained an HMM with 5 hidden biological states representing gene structure:

| State        | Description |
|--------------|-------------|
| `P` - Promoter   | Regulatory start region of the gene. |
| `E` - Exon       | Coding region that remains in final mRNA. |
| `I` - Intron     | Non-coding region between exons, spliced out. |
| `T` - Terminator | Region marking the end of transcription. |
| `O` - Other      | Intergenic or undefined areas. |

The model is trained on real DNA sequences using unsupervised learning, and later used to generate realistic artificial gene-like sequences.

---

## 🔬 Methodology

1. **Data Collection**:
   - 11 real bacterial genomes (FASTA format), including annotation for known genes.
2. **Model Structure**:
   - HMM with 5 hidden states (`P`, `E`, `I`, `T`, `O`) and 4 emissions (`A`, `C`, `G`, `T`).
3. **Training**:
   - Initial probability matrices (π, A, B) were seeded with biological heuristics or uniform/random values.
   - Model parameters trained using **Baum-Welch algorithm** (an EM variant).
4. **Prediction**:
   - Gene detection performed via **Viterbi algorithm**.
5. **Sequence Generation**:
   - Artificial gene sequences created by sampling from the trained HMM, using transition and emission probabilities.
6. **Evaluation**:
   - Precision and biological plausibility of synthetic genes were evaluated vs real data.

---

## 🛠️ Installation

### Requirements

```bash
pip install numpy  matplotlib



