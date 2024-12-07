import sys
from pathlib import Path
from typing import List, Set, Iterable, Tuple, Generator

FOLDER: Path = Path("leipzig")

# In order of importance; similarity checking will prioritize the first 3
CORPORA: List[Path] = list(map(
    lambda name: FOLDER / name,
    [
        # Main sources
        "vie_news_2022_1M",
        "vie_wikipedia_2021_1M",
        "vie-vn_web_2015_1M",
        "vie_mixed_2014_1M",
        "vie_newscrwal_2011_1M",

        # Secondary sources (only take sentences if they are unique)
        "vie_news_2020_1M",
        "vie_news_2019_300K",
        "vie_wikipedia_2016_1M",
    ]
))


def _is_duplicate(sentence: str, sentence_set: Set[str]) -> bool:
    if sentence in sentence_set:
        return True
    # TODO: similarity hashing
    return False


def _process_corpus(
        source_iter: Iterable[str],
        sentence_iter: Iterable[str],
        source_set: Set[str],
        sentence_set: Set[str]
) -> Generator[
    str,  # yield type
    None,  # send type
    Tuple[Set[str], Set[str]]  # return type
]:
    new_source_set: Set[str] = set()
    new_sentence_set: Set[str] = set()

    for source, sentence in zip(source_iter, sentence_iter):
        sentence_number: int = int(source.strip().split("\t", 1)[0])
        source: str = source.strip().split("\t", 1)[1]
        sentence: str = sentence.strip().split("\t", 1)[1].lower()

        # Progress indicator
        print(end=f"\r\t{sentence_number:,} processed", flush=True, file=sys.stderr)

        # Duplicate checking
        if source in source_set:
            # `\r`: Write over any progress indicator
            print("\r\t[Source Duplicate]", source, file=sys.stderr)
            continue
        if _is_duplicate(sentence, sentence_set):
            # `\r`: Write over any progress indicator
            print("\r\t[Duplicate]", sentence, file=sys.stderr)
            continue

        yield sentence
        new_source_set.add(source)
        new_sentence_set.add(sentence)

    return new_source_set, new_sentence_set


def get_sentences_iter() -> Iterable[str]:
    sentence_count: int = 0
    source_set: Set[str] = set()
    sentence_set: Set[str] = set()

    for corpus_file in CORPORA:
        sources_file = corpus_file / f"{corpus_file.name}-sources.txt"
        sentences_file = corpus_file / f"{corpus_file.name}-sentences.txt"

        print(f"Processing corpus {corpus_file.name}...", file=sys.stderr)

        with sources_file.open("r") as sources_file, sentences_file.open("r") as sentences_file:
            # `yield from` returns the StopIteration value
            new_source_set, new_sentence_set = yield from _process_corpus(
                sources_file,
                sentences_file,
                source_set,
                sentence_set,
            )

            source_set.update(new_source_set)
            sentence_set.update(new_sentence_set)

            # `\r`: Write over any progress indicator
            print(f"\rFetched {len(new_sentence_set):,} sentences from {corpus_file.name}", file=sys.stderr)
            sentence_count += len(new_sentence_set)

    print(f"Total: {sentence_count:,} sentences", file=sys.stderr)


def get_sentences() -> List[str]:
    sentences: List[str] = list(get_sentences_iter())
    return sentences


def main(_args: List[str]) -> int:
    if input("This will overwrite sentences.txt. Proceed? (y/N) ") != "y":
        return 1

    with Path("sentences.txt").open("w") as file:
        for sentence in get_sentences_iter():
            print(sentence, file=file)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
