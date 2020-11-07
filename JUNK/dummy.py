from bs4 import BeautifulSoup
import bs4
from requests import get
import re
response = get("https://www.imdb.com/search/title/?genres=comedy")
html_soup = BeautifulSoup(response.text, "html.parser")
movie_container = html_soup.find_all(name="div", class_="lister-item mode-advanced")

print(movie_container[0])
print("------ 🦧 --------")
print(movie_container[0].div)
print("------ 🦧 --------")
print(movie_container[0].h3.a.text)
print(movie_container[0].strong.text)
genre = movie_container[0].find('span', class_="genre").text 
print(genre.strip())

# print(movie_container[0].find(name="p", class_="").contents)
cast_container = movie_container[0].find(name="p", class_="").text
pattern = re.compile(r"[,|\t\n]")
# print(cast_container.strip().split("\n"))
data = pattern.split(cast_container.strip()) 
data = list(filter(lambda x : x not in ['', ' '], data))
data = list(map(lambda x: x.strip(), data))
print(data)
if "Director:" in data:
    ds = data.index("Director:")
    de = data.index("Stars:")
    print("Director")
    print(data[ds+1:de])


elif "Directors:" in data:
    ds = data.index("Directors:")
    de = data.index("Stars:")
    print("Directors")
    print(data[ds+1:de])


print("Cast")
print(data[data.index("Stars:")+1:])

print(movie_container[0].find(name="span", class_="lister-item-year text-muted unbold").text.replace("(","").replace(")", ""))

print(movie_container[0].find(name="span", class_="metascore favorable").text)

# print(movie_container[21].find(name="span", class_="runtime").text.strip())

html_soup.select("lister-page-next next-page")
print(html_soup.find(name="a", class_="lister-page-next next-page", href=True)['href'])

