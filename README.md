# LSCI 109 — Reduplication of Tones in Vietnamese

## Project Overview

The goal of this project is to analyze tonal transfer in Vietnamese reduplicates at a surface-level. It explores pairs
with partial reduplication like "nho nhỏ" and full reduplication like "từ từ" in the Leipzig Vietnamese corpora in hopes
of uncovering patterns in how tones change in reduplicated words. The overarching goal of this project is to explore
corpus linguistics techniques and create visualizations data-driven analysis.

## Code Overview

The code for this project is used to parse the Leipzig corpus, search for reduplicative pairs (ignoring tone), and
generate heatmap graphs to represent common combinations. The scripts should be run in the following order:

```bash
# Remove any downloaded or generated files
sh cleanup.sh

# Download Leipzig Vietnamese corpora and JVnTextPro Java library
# Also create Python virtual environment and install requirements.txt
sh setup.sh
source venv/bin/activate

# Parse the Leipzig corpora into sentences.txt, deduplicating identical sentences
python3 leipzig.py

# Use JVnTextPro's tokenizer and word segmenter to generate sentences.txt.tkn 
# and sentences.txt.tkn.wseg, which contain the tokenized and word-segmented
# versions of the sentences in sentences.txt
python3 sentence_processing.py

# Parses sentences.txt.tkn.wseg and adds both inter- and intra-word reduplicates
# (ignoring tone) into reduplicates.csv 
python3 find_reduplicates.py

# MANUAL STEP: edit filter_reduplicates.py and add bigrams that are manually
# confirmed to be false positive reduplicates
# Running this script filters out the false positives and only keeps reduplicative
# pairs with 75+ occurrences, storing the results in reduplicates.filtered.csv
python3 filter_reduplicates.py

# Uses Matplotlib to plot a heatmap of tone pairs in reduplicates.filtered.csv
python3 plot_distribution_matrix.py
```
