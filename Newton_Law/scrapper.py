from bs4 import BeautifulSoup
import requests
import json
import os
import sys


url = r"https://www.thoughtco.com/what-are-newtons-laws-of-motion-608324"
resp = requests.get(url)

soup = BeautifulSoup(resp.text, "html.parser")

data = soup.find(name="div", class_="comp structured-content expert-content mntl-sc-page mntl-block").text.strip()

if not os.path.exists("./DATA"):
    os.mkdir("./DATA")

with open("./DATA/laws.txt", "w") as f:
    f.write(data)