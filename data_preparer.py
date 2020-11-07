import numpy as np
import pandas as pd
import json
from datetime import datetime
from tqdm import tqdm
import re


if __name__ == "__main__":

    myfile = open("./DATA/data_movies.json", "r")
    fullData = json.load(myfile)
    myfile.close()

    csvData = {"showName" : [], "runtime" : [], "genre" : [], "imdbRating" : [], "director" : [], "cast" : [], \
        "releaseYear" : [], "targetAudience" : [], "metascore": []}

    print("Preparing the Data 🛠️ .....")

    with tqdm(total=len(fullData)) as pbar:
        for data in fullData:
            for datum in data:

                csvData["showName"].append(datum["movie_name"].strip())

                if datum["runtime"] is not None:
                    runtime = datum["runtime"].split()[0]

                    csvData["runtime"].append(int(runtime))

                else:
                    csvData["runtime"].append(None)
                
                csvData["genre"].append(datum["genre"])

                if datum["imdb_rating"] is not None:
                    csvData["imdbRating"].append(float(datum["imdb_rating"]))
                else:
                    csvData["imdbRating"].append(None)

                
                if type(datum["director"]) == list:
                    if len(datum["director"]) < 2:
                        csvData["director"].append(datum["director"][0])

                    else:
                        csvData["director"].append( ", ".join(datum["director"]))
                else:
                    csvData["director"].append(None)


                if type(datum["cast"]) == list:
                    if len(datum["cast"]) < 2:
                        csvData["cast"].append(datum["cast"][0])
                    else:
                        csvData["cast"].append(", ".join(datum["cast"]))

                else:
                    csvData["cast"].append(None)


                year = re.findall(r"[0-9]+", datum["year"])[0]

                csvData["releaseYear"].append(int(year))

                
                csvData["targetAudience"].append(datum["audience"])

                csvData["metascore"].append(datum["metascore"].strip())

            
            pbar.update(1)


    for k, v in csvData.items():
        print(k, len(v))
    df = pd.DataFrame(csvData)

    df = df.drop_duplicates()
    
    df.to_csv("./DATA/imdbData_movies.csv", index=False)

    print("Done! ✅")



            



