import csv
import sys
from pathlib import Path
from typing import Any, List

import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.axes import Axes
from matplotlib.figure import Figure

LABELS = [
    "Flat",  # A1
    "Deep (◌̀)",  # A2
    "Sharp (◌́)",  # B1
    "Heavy (◌̣)",  # B2
    "Asking (◌̉)",  # C1
    "Tumbling (◌̃)",  # C2
]

TONE_INDEXES = {tone: index
                for index, tone in enumerate(("A1", "A2", "B1", "B2", "C1", "C2"))}


def main(_args: List[str]):
    if input("This will overwrite distribution_matrix.svg. Proceed? (y/N) ") != "y":
        return 1

    # Collect total data
    data: np.ndarray[Any, np.dtype[np.float64]] = np.zeros((len(LABELS), len(LABELS)))
    with Path("reduplicates.filtered.csv").open("r") as redup_file:
        reader = csv.DictReader(redup_file)
        for row in reader:
            first_tone = TONE_INDEXES[row["first-word-tone"]]
            second_tone = TONE_INDEXES[row["second-word-tone"]]
            data[second_tone, first_tone] += int(row["count"])

    # Fix LogNorm not working on zero values
    render_data: np.ndarray[Any, np.dtype[np.float64]] = data + 5.0

    # Use LogNorm to make color differences between no and few occurrences more obvious
    norm = colors.LogNorm(vmin=render_data.min(), vmax=render_data.max())

    fig: Figure
    ax: Axes
    fig, ax = plt.subplots()
    ax.imshow(render_data, interpolation="none", norm=norm)

    # Label all ticks
    ax.set_xticks(list(range(len(LABELS))), labels=LABELS, fontfamily="Noto Sans", fontsize=14)
    ax.set_yticks(list(range(len(LABELS))), labels=LABELS, fontfamily="Noto Sans", fontsize=14)

    # Rotate the x-axis tick labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # # Set labels
    # ax.set_title("Tone distribution of words in a reduplicative pair (# of occurrences)")
    # ax.set_xlabel("Tone of the First Word")
    # ax.set_ylabel("Tone of the Second Word")

    # Add numbers to each cell
    for row_number in range(len(TONE_INDEXES)):
        for column_number in range(len(TONE_INDEXES)):
            count: int = int(data[row_number, column_number])
            ax.text(
                column_number, row_number, f"{count}",
                ha="center", va="center",
                color="black" if count != 0 else "white",
                path_effects=[pe.withStroke(linewidth=2, foreground="white")] if count != 0 else None,
                fontfamily="Noto Sans",
                fontweight="bold",
                fontsize=14,
            )

    fig.tight_layout()
    plt.savefig("distribution_matrix.svg", transparent=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
