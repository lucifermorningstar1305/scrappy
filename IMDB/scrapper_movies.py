import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import traceback
import re
import json

def get_content(url, max_pages = 800):

    counter = 0
    ret = list()
    with tqdm(total=max_pages) as pbar:
        while counter < max_pages:
            try : 
                resp = requests.get(url)
                html_soup = BeautifulSoup(resp.text, "html.parser")

                movie_container = html_soup.find_all(name="div", class_="lister-item mode-advanced")
                
                # 
                # Collect the data of the next page
                #

                for movies in movie_container:

                    if movies.strong is None or movies.find(name="div", class_="inline-block ratings-metascore") is None: # Skipping if there is no IMDB rating for the show or any meta score of the show
                        continue

                    _temp = {
                    "movie_name" : movies.h3.a.text,
                    "runtime" : None,
                    "genre" : movies.find(name="span", class_="genre").text.strip(),
                    "imdb_rating" : movies.strong.text,
                    "director" : None,
                    "cast" : None,
                    "year":None,
                    "audience" : None,
                    "metascore": None} 

                    

                    if movies.find(name="span", class_="runtime") is not None:
                        _temp["runtime"] = movies.find(name="span", class_="runtime").text.strip()

                    if movies.find(name="span", class_="certificate") is not None:
                        _temp["audience"] = movies.find(name="span", class_="certificate").text.strip()

                    pattern = re.compile(r"[,|\t\n]")
                    people_container = pattern.split(movies.find(name="p", class_="").text.strip())
                    people_container = list(filter(lambda x : x not in ['', ' '], people_container))
                    people_container = list(map(lambda x: x.strip(), people_container))
                    
                    if "Stars:" in people_container:
                        if "Director:" in people_container:
                            ds = people_container.index("Director:")
                            de = people_container.index("Stars:")

                            _temp["director"] = people_container[ds+1:de]

                        elif "Directors:" in people_container:
                            ds = people_container.index("Directors:")
                            de = people_container.index("Stars:")

                            _temp["director"] = people_container[ds+1:de]
                        

                        _temp["cast"] = people_container[people_container.index("Stars:") + 1:]
                    
                    elif "Star:" in people_container:
                        if "Director" in people_container:
                            ds = people_container.index("Director:")
                            de = people_container.index("Star:")
                            _temp["director"] = people_container[ds+1 : de]

                        elif "Directors" in people_container:
                            ds = people_container.index("Directors:")
                            de = people_container.index("Star:")
                            _temp["director"] = people_container[ds+1:de]

                        _temp["cast"] = people_container[people_container.index("Star:") + 1: ]
                    
                    else:
                        if "Director" in people_container:
                            _temp["director"] = people_container[people_container.index("Director:")+1 : ]

                        elif "Directors:" in people_container:
                            _temp["director"] = people_container[people_container.index("Directors:") + 1 : ]
                        

                    year = movies.find(name="span", class_="lister-item-year text-muted unbold").text.replace("(","").replace(")", "")
                    _temp["year"] = str(year)


                    if movies.find(name="span", class_="metascore favorable"):
                        _temp["metascore"] = movies.find(name="span", class_="metascore favorable").text

                    elif movies.find(name="span", class_="metascore mixed"):
                        _temp["metascore"] = movies.find(name="span", class_="metascore mixed").text

                    else:
                        _temp["metascore"] = movies.find(name="span", class_="metascore unfavorable").text

                    ret.append(_temp)

                # next_page_url = html_soup.find(name="a", class_="lister-page-next next-page", href=True)['href']
                # url = url.replace("/search/title/?genres=comedy",next_page_url)
                try:
                    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                    match = False
                    while not match:
                        lastCount = lenOfPage
                        time.sleep(1)
                        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                        if lastCount == lenOfPage:
                            match = True

                    ""
                    
                    next_page = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.LINK_TEXT, "Next »")))
                    # next_page = driver.find_element_by_class_name("lister-page-next next-page")
                    # next_page = driver.find_element_by_link_text("Next »")
                    # driver.execute_script("arguments[0].click();",next_page)
                    next_page.click()
                    url = driver.current_url
                except Exception as e:
                    print("Error Occured : 🚷")
                    print(traceback.print_exc())

    

            except Exception as e:
                print("Error Occured ⛔")
                print(traceback.print_exc())


            counter += 1

            pbar.update(1)

    

    return ret
    



if __name__ == "__main__":

    base_url = "https://www.imdb.com/search/title/?genres="

    genres = ["comedy", "action", "adventure", "thriller", "sci-fi", "horror", "romance", "mystery", \
         "crime", "animation", "fantasy"]

    genre_icons = ["🤡", "🥋", "🏍️", "😱", "🤖", "👻", "💕", "🕵️", "🔪", "🦊", "🧙"]


    data = []

    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    for i in range(len(genres)):

        new_url = base_url + genres[i]
        driver.get(new_url)
        print(f"Collecting data for {genres[i]} {genre_icons[i]}...")
        ret = get_content(new_url, max_pages=4)
        data.append(ret)

    with open('./DATA/data_movies.json', 'w') as json_file:
        json.dump(data, json_file)
        
    






