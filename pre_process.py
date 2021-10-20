import spacy
import csv
import sys
from spacy.tokens import DocBin

def main(argv):

    if len(argv) != 2:
        print("Not enough command line arguments")
        return 1

    output_path = "./" + argv[0] + ".spacy"
    train_len = int(argv[1])

    data_read = []
    with open("all_data.csv") as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"', dialect="excel")
        # next(reader, None)  # skip the headers
        rover = next(reader)
        data_read.append(rover)
        skips = 0
        while True:
            try:
                rover = next(reader)
                data_read.append(rover)
            except UnicodeDecodeError:
                skips += 1
                continue
            except StopIteration:
                break
        print("num skipped due to invalid encoding:", skips)
        if output_path == "./train.spacy":
            data_read = data_read[1:train_len]
        elif output_path == "./dev.spacy":
            data_read = data_read[train_len:train_len*2]
        elif output_path == "./eval.spacy":
            data_read = data_read[train_len*2:]
        else:
            print("bad input file")
            return 1


    print("amount of data to be processed:", len(data_read))

    # Data starts at row 1, content is at index 8, score is at index 12
    nlp = spacy.blank("en")
    db = DocBin()
    data_tuples = ((eg[8], eg) for eg in data_read if len(eg) == 23) 
    invalid = 0
    for doc, eg in nlp.pipe(data_tuples, as_tuples=True):
        score = float(eg[12])
        if score < 0:
            invalid += 1
            continue
        elif score <= 0.5:
            doc.cats["good"] = 0
            doc.cats["bad"] = 1
        elif score > 0.5:
            doc.cats["good"] = 1
            doc.cats["bad"] = 0
        db.add(doc)
    print("num invalid scores:", invalid)
    db.to_disk(output_path)
    print(f"Processed {len(db)} documents: {output_path}")
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])
