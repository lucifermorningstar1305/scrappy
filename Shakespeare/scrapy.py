from bs4 import BeautifulSoup
import requests
import os
import sys



if __name__ == "__main__":

    base_url = r"https://www.gutenberg.org/files/100/100-h/100-h.htm#link2HCH0001"
    resp = requests.get(base_url)

    print("Parsing...... 🛠️")
    soup = BeautifulSoup(resp.text, "html.parser")

    text = soup.text

    if not os.path.exists("./DATA"):
        os.mkdir("./DATA/")


    with open("./DATA/shakespeare.txt","w") as f:
        f.writelines(text)

    print("Complete... 😉")