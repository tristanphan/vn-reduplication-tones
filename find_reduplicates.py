import csv
import sys
from pathlib import Path
from typing import List, Iterable, Tuple, Dict, Literal

Tone = Literal["A1", "A2", "B1", "B2", "C1", "C2"]

VIETNAMESE_ALPHABET: str = "aăâbcdđeêghiklmnoôơpqrstuưvxyáàảãạăắằẳẵặâấầẩẫậđéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ"
VIETNAMESE_TONES_TRANSLATION_TABLE: Dict[int, int] = {
    ord(tonal): ord(collection[0])
    for collection in ["aáàảãạ", "ăắằẳẵặ", "âấầẩẫậ", "eéèẻẽẹ", "êếềểễệ", "iíìỉĩị",
                       "oóòỏõọ", "ôốồổỗộ", "ơớờởỡợ", "uúùủũụ", "ưứừửữự", "yýỳỷỹỵ"]
    for tonal in collection[1:]
}

# A1_TONES are anything that don't have a tone
A2_TONES = "àằầèềìòồờùừỳ"  # huyền
B1_TONES = "áắấéếíóốớúứý"  # sắc
B2_TONES = "ạặậẹệịọộợụựỵ"  # nặng
C1_TONES = "ảẳẩẻểỉỏổởủửỷ"  # hỏi
C2_TONES = "ãẵẫẽễĩõỗỡũữỹ"  # ngã


def is_vietic(string: str) -> bool:
    if len(string) == 0:
        return False
    for character in string:
        if character not in VIETNAMESE_ALPHABET:
            return False
    return True


def remove_tones(string: str) -> str:
    return string.translate(VIETNAMESE_TONES_TRANSLATION_TABLE)


def lines_in_file(file: Path):
    with file.open("r") as fp:
        for line in fp:
            yield line.strip()


def get_tone_of_word(word: str) -> Tone:
    for character in word:
        if character in A2_TONES:
            return "A2"
        if character in B1_TONES:
            return "B1"
        if character in B2_TONES:
            return "B2"
        if character in C1_TONES:
            return "C1"
        if character in C2_TONES:
            return "C2"
    return "A1"


def bigrams(line: str) -> Iterable[Tuple[str, str]]:
    tokens = list(filter(lambda tk: len(tk) != 0, line.strip().split()))
    for first, second in zip(tokens, tokens[1:]):
        yield first, second


def main(_args: List[str]) -> int:
    if input("This will overwrite reduplicates.csv. Proceed? (y/N) ") != "y":
        return 1

    bigram_histogram: Dict[Tuple[str, str], int] = dict()

    def process_bigram(first_word: str, second_word: str):
        if not first_word.isprintable() or not second_word.isprintable():
            return
        if not is_vietic(first_word) or not is_vietic(second_word):
            return
        if remove_tones(first_word) == remove_tones(second_word):
            key = (first_word, second_word)
            bigram_histogram[key] = bigram_histogram.get(key, 0) + 1

    # Process independent-word bigrams
    for index, line in enumerate(lines_in_file(Path("sentences.txt.tkn.wseg")), 1):
        print(f"\r{index:,} lines processed (independent-word bigrams)", end="", file=sys.stderr)
        for first_word, second_word in bigrams(line):
            process_bigram(first_word, second_word)
    print(file=sys.stderr)

    # Process grouped-word bigrams
    for index, line in enumerate(lines_in_file(Path("sentences.txt.tkn.wseg")), 1):
        print(f"\r{index:,} lines processed (grouped-word bigrams)", end="", file=sys.stderr)
        for word in line.strip().split():
            if word.count("_") != 1:
                continue
            first_word, second_word = word.split("_")
            process_bigram(first_word, second_word)
    print(file=sys.stderr)

    sorted_bigram_histogram: List[Tuple[str, str, int]] = sorted(
        ((first_word, second_word, count) for (first_word, second_word), count in bigram_histogram.items()),
        key=lambda tup: tup[2], reverse=True
    )

    with Path("reduplicates.csv").open("w") as redup_file:
        columns = ["count", "first-word", "second-word", "first-word-tone", "second-word-tone"]
        writer = csv.DictWriter(redup_file, columns)
        writer.writeheader()
        for first_word, second_word, count in sorted_bigram_histogram:
            writer.writerow({
                "count": count,
                "first-word": first_word,
                "second-word": second_word,
                "first-word-tone": get_tone_of_word(first_word),
                "second-word-tone": get_tone_of_word(second_word),
            })

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
