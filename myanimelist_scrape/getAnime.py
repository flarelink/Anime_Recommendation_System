"""
Slightly modified script from: https://github.com/Dibakarroy1997/myanimelist-data-set-creator

This script can be used to download anime dataset from [**Myanimelist**](https://myanimelist.net/)
using an unofficial MyAnimeList REST API, [**Jikan**](https://jikan.moe/).
Column metadata:

animeID: id of anime as in anime url https://myanimelist.net/anime/ID
name: title of anime
genre: list of genre
type: type of anime (example TV, Movie etc)
episodes: number of episodes
studios: list of studio
source: source of anime (example original, manga, game etc)
scored: score of anime
scoredBy: number of member scored the anime
members: number of member added anime to their list
"""

# importing libraries
import requests
import json
import csv
import sys

count = 0  # keep count of anime for current session

try:
    start = int(sys.argv[1])  # starting index
    end = int(sys.argv[2]) + 1  # ending index
except IndexError:
    print('Please provide all arguments.\nSyntax:\npython getAnime.py starting_index ending_index [output_file.csv]')
    sys.exit()
except:
    print('Unexpected error.')

# setting name of output file
if len(sys.argv) == 4:
    outputFile = str(sys.argv[3])
else:
    outputFile = 'Anime.csv'

# opening output file for writing
w = open(outputFile, 'w')

# header
w.write('animeID,name,genre,type,episodes,studios,source,scored,scoredBy,members\n')

# create a filter to ensure we don't get NSFW recommendations (Hentai)
nsfw_flag = False

# creating csv writer object
writer = csv.writer(w)

for i in range(start, end):  # note: The index starts in 1 and ends in 37115 (as on Jan 15 2018)
    apiUrl = 'http://api.jikan.moe/v3/anime/' + str(i)  # base url for API
    # note: for SSL use 'https://api.jikan.me/'. For more go here 'https://jikan.me/docs'

    # API call
    page = requests.get(apiUrl)
    c = page.content

    # Decoding JSON
    try:
        print('Fetching JSON...')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        continue

    jsonData = json.loads(c)

    # if status code is 200 then write to file
    if page.status_code == 200:

        studio = []  # list to store studio (list cause it can be more then 1)
        genre = []  # list to store genre (list cuase it can be more then 1)

        # getting genre
        for j in range(0, len(jsonData['genres'])):
            genre.append(jsonData['genres'][j]['name'])
            if jsonData['genres'][j]['name'] == "Hentai":
                nsfw_flag = True

        # filter to make sure we're getting true animes
        if not nsfw_flag:
            # getting studio name
            for j in range(0, len(jsonData['studios'])):
                studio.append(jsonData['studios'][j]['name'])

            print('\nWriting to file...')  # Message

            l = []  # List to store the data to write

            name = jsonData['title']  # getting anime title

            print('Reading', name, 'animelist...')  # printing title to screen

            count = count + 1  # Increament anime count

            l.append(i)  # anime ID
            l.append(name)  # anime title
            # l.append(jsonData['premiered'])  # anime premiered on
            l.append(genre)  # anime genre
            l.append(jsonData['type'])  # anime type
            l.append(jsonData['episodes'])  # number of episodes
            l.append(studio)  # studio
            l.append(jsonData['source'])  # source of anime
            l.append(jsonData['score'])  # score
            l.append(jsonData['scored_by'])  # number of members scored
            l.append(jsonData['members'])  # number members added this anime in their list

            l = [l]  # help in writing using csv.writer.writerows

            print('Writing anime', name)
            print('Total Anime stored in  the session:', count)
            print('Index of anime to be written:', i)

            writer.writerows(l)  # writing one row in the CSV

        else:
            nsfw_flag = False

w.close()  # closing file

print('No more anime left. Done.\nOutput file:', outputFile)
