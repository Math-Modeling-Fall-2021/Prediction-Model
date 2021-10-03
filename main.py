import spacy
import csv


with open("Critic Reviews Data Sample.csv") as fp:
    reader = csv.reader(fp, delimiter=",", quotechar='"')
    # next(reader, None)  # skip the headers
    data_read = [row for row in reader]

# Data starts at row 1, content is at index 4
sent = data_read[1][4]
print(sent)


nlp = spacy.load("en_core_web_trf")
doc = nlp(sent)
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)