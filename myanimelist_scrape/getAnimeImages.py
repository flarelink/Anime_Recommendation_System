##############################################################################
# getAnimeImages.py - Gathers anime images for each anime id
#
# Copyright (C) 2019   Humza Syed
#
# This is free software so please use it however you'd like! :)
##############################################################################
import json
import requests
import urllib
import os
import time
import pandas as pd


def scrape_images(dataset_path):
    """
    Scrapes the images online using the anime ids

    :param dataset_path: path to Anime.csv
    :return: folder filled with anime images
    """
    if not (os.path.exists(os.path.join(os.getcwd(), 'anime_imgs'))):
        os.mkdir('anime_imgs')

    anime_df = pd.read_csv(dataset_path)

    for index, row in anime_df.iterrows():
        anime_id = row['animeID']
        print(anime_id)

        apiUrl = 'http://api.jikan.moe/v3/anime/' + str(anime_id)


        # API call
        page = requests.get(apiUrl)
        c = page.content

        # Decoding JSON
        try:
            print('Fetching JSON...')
        except:
            print("Unexpected error:")
            continue

        jsonData = json.loads(c)

        # if status code is 200 then write to file
        if page.status_code == 200:
            img_url = jsonData['image_url']

            f = open(os.path.join(os.getcwd(), 'anime_imgs', str(anime_id) + '.jpg'), 'wb')
            f.write(urllib.request.urlopen(img_url).read())
            f.close()

            time.sleep(3)


os.chdir('..')
path = os.path.join(os.getcwd(), 'Anime.csv')
scrape_images(path)
