import csv
import sys
from pathlib import Path
from typing import List

FALSE_POSITIVES = {
    ("công", "cộng"),
    ("tiên", "tiến"),
    ("nhưng", "những"),
    # ("tưởng", "tượng"),  # Even though these 2 are different words, they should count
    ("tự", "tử"),
    ("năm", "năm"),
    ("đu", "đủ"),
    ("tính", "tình"),
    ("hạn", "hán"),
    ("các", "các"),
    ("của", "của"),
    ("con", "còn"),
    ("ba", "ba"),
    ("bà", "ba"),
    ("chị", "chỉ"),
    ("được", "được"),
    ("có", " có"),
    ("lạ", " là"),
    ("trong", "trong"),
    ("cũng", "cùng"),
    ("chôm", "chôm"),
    ("ngay", "ngày"),
}

VERIFIED_REDUPLICATES = {
    ("luôn", "luôn"),
    ("dần", "dần"),
    ("song", "song"),
    ("tưởng", "tượng"),
    ("từ", "từ"),
    ("mãi", "mãi"),
    ("chuồn", "chuồn"),
    ("bong", "bóng"),
    ("nho", "nhỏ"),
    ("ngày", "ngày"),
    ("ngoan", "ngoãn"),
    ("chung", "chung"),
    ("ai", "ai"),
    ("kha", "khá"),
    ("người", "người"),
    ("băng", "băng"),
    ("khăng", "khăng"),
    ("rưng", "rưng"),
    ("ầm", "ầm"),
    ("là", "là"),
    ("châu", "chấu"),
    ("đều", "đều"),
    ("xa", "xa"),
    ("lẳng", "lặng"),
    ("đau", "đáu"),
    ("lâu", "lâu"),
    ("đời", "đời"),
    ("cuồn", "cuộn"),
    ("sừng", "sững"),
    ("với", "với"),
    ("có", "có"),
    ("ào", "ào"),
    ("nhà", "nhà"),
    ("lạ", "là"),
    ("đâu", "đâu"),
    ("chăm", "chăm"),
    ("cho", "cho"),
    ("nhan", "nhản"),
    ("nêm", "nếm"),
    ("và", "và"),
    ("nhè", "nhẹ"),
    ("run", "run"),
    ("đêm", "đêm"),
    ("cay", "cay"),
    ("là", "lạ"),
    ("rất", "rất"),
    ("na", "ná"),
    ("chầm", "chậm"),
    ("xinh", "xinh"),
}

OCCURRENCE_MIN_THRESHOLD = 75


# ONLY SEARCHED WORDS WITH 75+ OCCURRENCES (looked at 68 words)
# TODO search words past 100 occurrences to 75

def main(_args: List[str]) -> int:
    if input("This will overwrite reduplicates.filtered.csv. Proceed? (y/N) ") != "y":
        return 1

    with Path("reduplicates.csv").open("r") as redup_file, Path("reduplicates.filtered.csv").open("w") as filtered_file:
        columns = ["count", "first-word", "second-word", "first-word-tone", "second-word-tone"]
        reader = csv.DictReader(redup_file)
        writer = csv.DictWriter(filtered_file, columns)
        writer.writeheader()

        for row in reader:
            if int(row["count"]) < OCCURRENCE_MIN_THRESHOLD:
                continue
            tup = (row["first-word"], row["second-word"])
            if tup in FALSE_POSITIVES:
                continue
            if tup not in VERIFIED_REDUPLICATES:
                raise ValueError(f"Pair {tup} has not been verified or excluded!")
            writer.writerow(row)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
