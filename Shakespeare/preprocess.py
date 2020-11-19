from tqdm import tqdm
import os
import sys
import re

def apostophes(word):

    if "'s" in word:
        return word.replace("'s", " is")
    
    if "'ve" in word:
        return word.replace("'ve", " have")

    if "n't" in word:
        return word.replace("n't", " not")
    
    return word





if __name__ == "__main__":

    text = ""

    with open("./DATA/shakespeare.txt", "r") as f:

        text = f.read() 

    # Get rid of unecessary text 😎, Works like a charm
    text = text[text.index("THE SONNETS") : text.index("FINIS")]

    text = text.lower()
    text = text.strip()
    print("Preprocessing the data ... 👨‍💻")

    preprocessed_data = ""
    with tqdm(total=len(text.split("\n"))) as pbar:
        for sents in text.split("\n"):

            sents = sents.strip()
            sents = sents.split()
            sents = list(map(lambda x: apostophes(x).strip(), sents))
            sents = " ".join(sents)

            sents = re.findall(r"[a-z]+", sents)
            sents = list(filter(lambda x: x not in ['', ' '], sents))
            sents = " ".join(sents)

            preprocessed_data += sents + " "

            pbar.update(1)

    
    preprocessed_data = preprocessed_data.strip()


    print("Saving the file ... 🗒")

    with open("./DATA/preprocessed-shakespeare.txt", "w") as f:
        f.write(preprocessed_data)