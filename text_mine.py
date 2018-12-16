import argparse
import atexit
import csv
from datetime import datetime
from functools import reduce
import logging
from time import clock
import re
import sys

import nltk
from nltk.corpus import PlaintextCorpusReader, words as nltkwords, stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

# download words, stopwords
nltk.download("words")
nltk.download("stopwords")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("text_mine")

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", default=sys.stdout, help="output path")
args = parser.parse_args()

target = "big_output_05--payload1.txt"
dest_csv = args.output


def main():
    logger.info(f"starting now: {datetime.utcnow()}")

    # read target and tokenize
    with open(target, "r") as f:
        tokens = word_tokenize(f.read())

    logger.info(f"Tokenized {len(tokens)} words")

    # filter english-only words
    # most of should be cleaned in preprocessing but just in case
    filtered = set(
        t.lower()
        for t in tokens
        if re.search(r"[\/+=<>0-9_:;,'@!()$|i\{\}\[\]?&*#%]", t.lower()) is None
    )

    # no stopwords
    less_stopwords = [
        x.lower() for x in filtered if x not in stopwords.words("english")
    ]

    logger.info(f"Filtered {len(filtered)} english only words")

    # build a freq dist
    fdist = FreqDist(w.lower() for w in tokens)

    # sort by top most common words
    common = sorted(
        [(word, fdist.freq(word)) for word in less_stopwords],
        key=lambda x: x[1],
        reverse=True,
    )[0:500]

    # write to a file
    with open(dest_csv, "w") as dest:
        writer = csv.writer(dest)
        for word in common:
            writer.writerow([word[0], word[1]])

    return 0


def seconds_to_str(t):
    time_str = reduce(
        lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60]
    )
    return "%d:%02d:%02d.%03d" % time_str


def endlog():
    end = clock()
    passed_time = end - start
    logger.info("done: ")
    logger.info(seconds_to_str(passed_time))


if __name__ == "__main__":
    start = clock()
    atexit.register(endlog)
    main()
