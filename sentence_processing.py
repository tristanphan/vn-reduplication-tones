import subprocess
import sys
from pathlib import Path
from typing import List, Callable


# Calls JVnTokenizer on the file to create a .tkn file
def tokenize(file: Path):
    completed_process = subprocess.run([
        "java",
        "-cp", "bin:lib/lbfgs.jar:lib/args4j.jar",
        "jvntokenizer.JVnTokenizer",
        "-inputfile", str(file.absolute()),
    ], cwd="JVnTextPro-v.2.0")
    if completed_process.returncode != 0:
        print("JVnTokenizerresulted in an error!")
        exit(1)


# Calls JVnSegmenter on the file to create a .wseg file
def segment(file: Path):
    completed_process = subprocess.run([
        "java",
        "-cp", "bin:lib/lbfgs.jar:lib/args4j.jar",
        "jvnsegmenter.WordSegmenting",
        "-modeldir", "models/jvnsegmenter",
        "-inputfile", str(file.absolute()),
    ], cwd="JVnTextPro-v.2.0")
    if completed_process.returncode != 0:
        print("JVnSegmenter resulted in an error!")
        exit(1)


# Segments the file
def split(src_file: Path, n: int, dest_filename: Callable[[int], str]):
    dest_files: List[Path] = []
    for i in range(n):
        dest_files.append(src_file.parent.absolute() / dest_filename(i))

    with src_file.open("r") as src:
        open_dest_files = [f.open("w") for f in dest_files]

        for index, line in enumerate(src):
            open_dest_files[index % len(open_dest_files)].write(line)

        _ = [o.close() for o in open_dest_files]


# Undo segmentation
def unsplit(src_filename: Callable[[int], str], n: int, dest_file: Path):
    src_files: List[Path] = []
    for i in range(n):
        src_files.append(dest_file.parent.absolute() / src_filename(i))

    with dest_file.open("w") as dest:
        for src_file in src_files:
            with src_file.open("r") as src:
                for line in src:
                    dest.write(line)


def clean_up_splits(n: int):
    for split_index in range(n):
        tokened_split = Path(f"sentences.txt.tkn.{split_index}")
        segmented_split = Path(f"sentences.txt.tkn.{split_index}.wseg")
        if tokened_split.is_file():
            tokened_split.unlink()
            print(f"Removed file {str(tokened_split.absolute())}")
        else:
            print(f"ERROR: File does not exist: {str(tokened_split.absolute())}")

        if segmented_split.is_file():
            segmented_split.unlink()
            print(f"Removed file {str(segmented_split.absolute())}")
        else:
            print(f"ERROR: File does not exist: {str(segmented_split.absolute())}")


def main(_args: List[str]) -> int:
    if input("This will overwrite sentences.txt.tkn, sentences.txt.tkn.wseg, and any intermediate split files."
             " Proceed? (y/N) ") != "y":
        return 1

    split_count = 10

    try:
        # sentences.txt -> sentences.txt.tkn
        print("Tokenizer START!")
        tokenize(Path("sentences.txt"))
        print("Tokenizer DONE!")

        # sentences.txt.tkn -> sentences.txt.tkn.[1,2,3...]
        print("Splitting START!")
        split(Path("sentences.txt.tkn"), split_count, lambda index: f"sentences.txt.tkn.{index}")
        print("Splitting END!")

        # sentences.txt.tkn.[1,2,3...] -> sentences.txt.tkn.[1,2,3...].wseg
        for split_index in range(split_count):
            print(f"Word Segmenter START! ({split_index + 1}/{split_count})")
            segment(Path(f"sentences.txt.tkn.{split_index}"))
            print(f"Word Segmenter END! ({split_index + 1}/{split_count})")

        # sentences.txt.tkn.[1,2,3...].wseg -> sentences.txt.tkn.wseg
        print("Unsplitting START!")
        unsplit(lambda index: f"sentences.txt.tkn.{index}.wseg", 10, Path("sentences.txt.tkn.wseg"))
        print("Unsplitting END!")

    finally:
        # removing sentences.txt.tkn.[1,2,3...] and sentences.txt.tkn.[1,2,3...].wseg
        print("Cleaning up splits!")
        clean_up_splits(split_count)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
