import pandas as pd
import os
from pathlib import Path

def main():

    # Read CSV file
    doc = pd.read_csv("metadata.csv", dtype=str)


    Path("./Extracted_abstracts").mkdir(parents=True, exist_ok=True)

    # Save each abstracts to a .txt file
    for index, row in doc.iterrows():
        abs = str(row['abstract'])
        index_str = str(index + 1)
        path = "./Extracted_abstracts/" + "abs_" + index_str +".txt"
        exist = os.path.isfile(path)
        if exist == False:
            with open(path, "w") as text_file:
                text_file.write(abs)
            print("saving file n° " + index_str)
        else:
            print("File already exists.")

if __name__ == "__main__":
    main()





