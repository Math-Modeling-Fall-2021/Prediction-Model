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
        i = 0
        correct = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
        preds = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
        total = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
        valid = 0
        bad = 0
        nlp = spacy.load("output/model-last")
        while True:
            try:
                rover = next(reader)
                if i > train_len * 2 and len(rover) == 23 and rover[12] != "-1":
                    valid += 1
                    data_read.append(rover)
                    actual_score = round(float(rover[12]) * 5)
                    content = rover[8]
                    prediction = nlp(content)
                    pred = int(max(prediction.cats, key=prediction.cats.get))
                    if pred > 5:
                        bad += 1
                        print(prediction.cats)
                        continue
                    preds[str(pred)] += 1
                    if abs(actual_score - pred) <= 0:
                        correct[str(actual_score)] += 1
                    total[str(actual_score)] += 1
                    #print(f"valid: {valid}, correct: {correct}")
            except UnicodeDecodeError:
                skips += 1
                continue
            except StopIteration:
                break
            i += 1
        print("num skipped due to invalid encoding:", skips)

    print("bad", bad)
    print(len(data_read))
 
    num_correct = 0
    for label in correct:
        num_correct += correct[label]
    num_valid = 0
    for label in correct:
        num_valid += total[label]
    num_incorrect = num_valid - num_correct
    accuracy = (num_correct * 6 + num_incorrect * 4) / (num_valid * 6)
    precision = (num_correct * 6) / (num_correct * 6 + num_incorrect)
    recall = (num_correct * 6) / (num_correct * 6 + num_incorrect)
    f_score = (2 * precision * recall) / (precision + recall)

    print("correct:", correct)
    print("preds:", preds)
    print("total:", total)

    print(f"number of guesses correct: {num_correct} out of {num_valid} (frac={num_correct / num_valid}%)")
    print(f"accuracy={accuracy}")
    print(f"precision={precision}")
    print(f"recall={recall}")
    print(f"f_1 score={f_score}")

if __name__ == "__main__":
    main(sys.argv[1:])