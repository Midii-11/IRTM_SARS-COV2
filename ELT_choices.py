# ---------------------------------------------------------------------------------------------------------------------
# 1) Extracts text from CSV and saves it to a Txt file.
# 2) Read from Txt | put words to lower case, remove stopwords and ponctuation | lemmatize | save output to Txt file.
# 3) Read from Txt file and calculate Tfidf (outputs the results)
# ---------------------------------------------------------------------------------------------------------------------
# code by Arthur Dorzee.

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import math
import string
import pandas as pd
import os
from pathlib import Path


class Lemmatize():
    def __init__(self, directory, safe_dir):
        self.directory = directory
        self.safe_dir = safe_dir

    def load_data(self):
        file_count = 0
        stopwords = nltk.corpus.stopwords.words('english')

        directory = self.directory
        for filename in os.listdir(directory):
            with open(os.path.join(directory, filename)) as f:
                lemmatizer = WordNetLemmatizer()
                sentence = f.read()
                sentence_low = sentence.lower()  # convert abstract to lower-cases
                sentence_Npon = "".join([w for w in sentence_low if w not in string.punctuation])  # remove punctuation

                tokens = nltk.word_tokenize(sentence_Npon)
                sentence_Npon = [w for w in tokens if w not in stopwords]
                sentence_Npon = " ".join(sentence_Npon)
                lem = Lemmatize

                sentence_up = ([lemmatizer.lemmatize(w, lem.get_wordnet_pos(w)) for w in
                                nltk.word_tokenize(sentence_Npon)])  # lemmatize in list
                sentence_up = [x for x in sentence_up if x != "abstract"]  # remove "abstract" from list
                sentence_fin = " ".join(sentence_up)  # string the list
                file_count = file_count + 1

                dir = self.safe_dir
                file = "abs_" + str(file_count) + "stem2.txt"
                path = (dir + file)
                with open(path, "w") as text_file:
                    text_file.write(sentence_fin)
                    print("File saved in: " + dir + " as: " + file)

    def get_wordnet_pos(word):
        """Map POS tag to first character lemmatize() accepts"""
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)


class Text_extraction():

    def __init__(self, safe_dir):
        self.safe_dir = safe_dir

    def extract(self):
        # Read CSV file
        doc = pd.read_csv("metadata.csv", dtype=str)
        Path(self.safe_dir).mkdir(parents=True, exist_ok=True)

        # Save each abstracts to a .txt file
        for index, row in doc.iterrows():
            abs = str(row['abstract'])
            index_str = str(index + 1)
            path = self.safe_dir + "abs_" + index_str + ".txt"
            exist = os.path.isfile(path)
            if not exist:
                with open(path, "w") as text_file:
                    text_file.write(abs)
                    print("saving file n° " + index_str)
            else:
                print("File already exists.")


class TFIDF():

    def __init__(self, directory, interest):
        self.directory = directory
        self.interest = interest

    def tfidf(self):

        print("Loading data...")

        obj_tfidf = TFIDF
        corpus = obj_tfidf.load_data(self)

        # Get all words in corpus
        print("Extracting words from corpus...")
        words = set()
        for filename in corpus:
            words.update(corpus[filename])

        # Calculate IDFs
        print("Calculating inverse document frequencies...")
        idfs = dict()
        for word in words:
            f = sum(word in corpus[filename] for filename in corpus)
            idf = math.log(len(corpus) / f)
            idfs[word] = idf

        # Calculate TF-IDFs
        print("Calculating term frequencies...")
        tfidfs = dict()
        for filename in corpus:
            tfidfs[filename] = []
            for word in corpus[filename]:
                tf = corpus[filename][word]
                tfidfs[filename].append((word, tf * idfs[word]))

        # Sort and get top 5 TF-IDFs for each file
        print("Computing top terms...")
        for filename in corpus:
            tfidfs[filename].sort(key=lambda tfidf: tfidf[1], reverse=True)
            tfidfs[filename] = tfidfs[filename][:self.interest]

        # Print results
        print()
        for filename in corpus:
            print(filename)
            for term, score in tfidfs[filename]:
                print(f"    {term}: {score:.4f}")

    def load_data(self):
        files = dict()
        for filename in os.listdir(self.directory):
            with open(os.path.join(self.directory, filename)) as f:

                # Extract words
                contents = [
                    word.lower() for word in
                    nltk.word_tokenize(f.read())
                    if word.isalpha()
                ]

                # Count frequencies
                frequencies = dict()
                for word in contents:
                    if word not in frequencies:
                        frequencies[word] = 1
                    else:
                        frequencies[word] += 1
                files[filename] = frequencies
        return files


if __name__ == "__main__":

    goal = input("Extract from CSV to TxT: \t (1) \n"
                 "Lemmatization: \t\t\t\t (2) \n"
                 "TfIdf: \t\t\t\t\t\t (3) \n"
                 "Answer: ")

    if goal == "1":
        # Copy abstracts from CSV to Txt file
        tx = Text_extraction("./Extracted_abstracts/")
        tx.extract()

    elif goal == "2":
        # Read Txt file lemmatize it and save result to other Txt file
        lem = Lemmatize("./Extracted_abstracts_sample", "./Extracted_abstracts_sample_test/")  # (input, output)
        lem.load_data()

        # Execute tfidf and print the result
    else:
        tfidf = TFIDF("./Extracted_abstracts_sample/", 15)
        tfidf.tfidf()
