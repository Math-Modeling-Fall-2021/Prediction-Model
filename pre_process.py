import spacy
import csv
import typer
from spacy.tokens import DocBin

def main():
    output_path = "./eval.spacy"

    data_read = []
    with open("Critic Reviews Data Sample.csv") as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        # next(reader, None)  # skip the headers
        train_len = 320
        for i, row in enumerate(reader):
            if i < 1:
                continue
            data_read.append(row)
            if i > train_len:
                break
            # if i < 10000:
            #    continue
    print(len(data_read))
    # Data starts at row 1, content is at index 4, score is at index 8

    nlp = spacy.blank("en")
    db = DocBin()
    data_tuples = ((eg[4], eg) for eg in data_read) 
    num = 0
    for doc, eg in nlp.pipe(data_tuples, as_tuples=True):
        if eg[8] == "-1":
            num += 1
            print(num)
            continue
        score = float(eg[8])
        if score < 0.7:
            doc.cats["bad"] = 0
        elif score > 0.7:
            doc.cats["good"] = 1
        db.add(doc)
    db.to_disk(output_path)
    print(f"Processed {len(db)} documents: {output_path}")

if __name__ == "__main__":
    typer.run(main)
