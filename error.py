import sys
import csv

import spacy

def main(argv):
    if len(argv) != 1:
        print("Not enough command line arguments")
        return 1

    train_len = int(argv[0])

    data_read = []
    with open("all_data.csv") as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"', dialect="excel")
        # next(reader, None)  # skip the headers
        rover = next(reader)
        data_read.append(rover)
        skips = 0
        bad = 0
        good = 0
        i = 0

        while True:
            try:
                rover = next(reader)
                if i > train_len * 2 and len(rover) == 23:
                    data_read.append(rover)
                    score = float(rover[12])
                    if score >= 0 and score < 0.5:
                        bad += 1
                    elif score >= 0.5:
                        good += 1
            except UnicodeDecodeError:
                skips += 1
                continue
            except StopIteration:
                break
            i += 1
        print("num skipped due to invalid encoding:", skips)


    print(len(data_read))
    both = good + bad
    print("actual good:", good)
    print("actual bad:", bad)
    print("actual good percentange:", good / both)
    print("actual bad percentange:", bad / both)

    nlp = spacy.load("output/model-best")
    doc = nlp("")
    print(doc.cats)

if __name__ == "__main__":
    main(sys.argv[1:])
