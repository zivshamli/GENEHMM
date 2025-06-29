import sys
import os

def write_lines_of_length60(sequence, file):
    for i in range(0, len(sequence), 60):
        file.write(sequence[i:i+60] + "\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python remove_n_and_fix_annotation.py genome.txt annotation.txt")
        return

    genome_path = sys.argv[1]
    annotation_path = sys.argv[2]

    genome_out_path = os.path.splitext(genome_path)[0] + "_clean.txt"
    annotation_out_path = os.path.splitext(annotation_path)[0] + "_clean.txt"

    # קריאת הגנום
    with open(genome_path, "r") as genome_file:
        genome_lines = [line.strip() for line in genome_file]

    # קריאת האנוטציה
    with open(annotation_path, "r") as annotation_file:
        annotation_lines = [line.strip() for line in annotation_file]

    genome_seq = "".join(genome_lines)
    annotation_seq = "".join(annotation_lines)

    # בדיקת אורך הגנום והאנוטציה
    print(f"אורך הגנום: {len(genome_seq)}")
    print(f"אורך האנוטציה: {len(annotation_seq)}")

    if len(genome_seq) != len(annotation_seq):
        raise ValueError("מספר התווים בגנום שונה ממספר שורות באנוטציה!")

    clean_genome = []
    clean_annotation = []

    for base, ann in zip(genome_seq, annotation_seq):
        if base.upper() != "N":
            clean_genome.append(base)
            clean_annotation.append(ann)

    # כתיבה לקבצים חדשים
    with open(genome_out_path, "w") as genome_out:
        write_lines_of_length60("".join(clean_genome), genome_out)

    with open(annotation_out_path, "w") as annotation_out:
        for ann in clean_annotation:
            annotation_out.write(ann + "\n")

    print(f"נוצרו הקבצים: {genome_out_path}, {annotation_out_path}")

if __name__ == "__main__":
    main()
