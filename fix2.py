import sys
import os

def write_lines_of_length60(sequence, file):
    for i in range(0, len(sequence), 60):
        file.write(sequence[i:i+60] + "\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python format_to_60.py input.txt")
        return

    input_path = sys.argv[1]
    output_path = os.path.splitext(input_path)[0] + "_60.txt"

    with open(input_path, "r") as infile:
        # מסיר רווחים, שורות ריקות ומחבר הכל לרצף אחד
        sequence = "".join([line.strip() for line in infile])

    with open(output_path, "w") as outfile:
        write_lines_of_length60(sequence, outfile)

    print(f"שמור קובץ עם שורות של 60 תווים בשם: {output_path}")

if __name__ == "__main__":
    main()
