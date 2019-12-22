from bs4 import BeautifulSoup
import requests
import pandas as pd
import gzip
from requests_html import HTMLSession


def scrape_genres(genres_flag=True):
    """
    TODO - You can ignore this function -> it was a great learning exercise for me
    Scrapes anime genres from myanimelist.net.
    I didn't end up using this function but it was a good learning experience for web scraping.

    Parameters:
    genres_flag (Boolean): Determines if we scrape genres from the web or reference the generated txt file

    Returns:
    genres (list of str): All of the genres in a list of strings
    """

    # extract genres from online and break once we've reached the last genre
    genres = []
    if genres_flag:
        file = open('genres.txt', 'w')

        source = requests.get('https://myanimelist.net/anime.php')

        if source.status_code == 200:
            soup = BeautifulSoup(source.text, "html.parser")
            for match in soup.find_all('a', class_='genre-name-link'):
                one_genre = match.text.split(' ')[0]
                file.write(one_genre + '\n')
                genres.append(one_genre)
                if one_genre == "Yuri":
                    break

        file.close()

    # if we've already created a txt file of the list of genres then just read that file
    else:
        try:
            file = open('genres.txt', 'r')
            genres = file.read().splitlines()
            file.close()
        except IOError:
            print('File could not be read')

    return genres


def user_xml_to_pandas_df(gz_file_path=None):
    """
    Depreciated due to: scrape_user_data_from_username
    Creates a dataframe from user's xml file. The dataframe contains the completed animes with their user scores.

    Parameters:
    gz_file_path (str): Path to the user gz file that was downloaded

    Returns:
    user_df (Dataframe): Dataframe with 2 columns; animeId and scored
    """
    if gz_file_path:
        with gzip.open(gz_file_path) as xml_file:
            data = BeautifulSoup(xml_file, 'xml')
            all_anime = data.find_all('anime')
            vals = []
            user_df = pd.DataFrame(columns=['animeID', 'scored'])
            pos = 0
            for anime in all_anime:
                if anime.find('my_status').text == 'Completed':
                    vals.append(int(anime.find('series_animedb_id').text))
                    vals.append(int(anime.find('my_score').text))

                    # all anime details
                    user_df.loc[pos] = vals
                    vals = []
                    pos += 1
    else:
        user_df = pd.DataFrame()

    return user_df


def scrape_user_data_from_username(username=None, inc_watching=False):
    # reference: http://theautomatic.net/2019/01/19/scraping-data-from-javascript-webpage-python/
    df = pd.DataFrame(columns=['animeID', 'scored', 'status'])
    pos = 0
    if username:
        session = HTMLSession()
        source = session.get('https://myanimelist.net/animelist/' + username)

        if source.status_code == 200:
            vals = []

            source.html.render(scrolldown=3000)  # run the javascript on the page and obtain the html
            source.html.html

            soup = BeautifulSoup(source.html.html, "html.parser")
            for anime_row in soup.find_all('tbody', class_='list-item'):

                if anime_row.find('td', class_='data status watching') and inc_watching:
                    anime_id = anime_row.find('a', class_='link sort')['href'].split('/')[-2]

                    bad_chars = str.maketrans(dict.fromkeys("\n[]', "))
                    anime_scored = anime_row.find('td', class_='data score').text
                    anime_scored = anime_scored.translate(bad_chars)
                    if anime_scored == '-':
                        anime_scored = 0

                    vals.append(int(anime_id))
                    vals.append(int(anime_scored))
                    vals.append('watching')

                    # anime_id and anime_scored
                    df.loc[pos] = vals
                    vals = []
                    pos += 1

                elif anime_row.find('td', class_='data status completed'):
                    anime_id = anime_row.find('a', class_='link sort')['href'].split('/')[-2]

                    bad_chars = str.maketrans(dict.fromkeys("\n[]', "))
                    anime_scored = anime_row.find('td', class_='data score').text
                    anime_scored = anime_scored.translate(bad_chars)
                    if anime_scored == '-':
                        anime_scored = 0

                    vals.append(int(anime_id))
                    vals.append(int(anime_scored))
                    vals.append('completed')

                    # anime_id and anime_scored
                    df.loc[pos] = vals
                    vals = []
                    pos += 1
            print(pos)
        else:
            print('The url was: ', 'https://myanimelist.net/animelist/' + username + '?status=2')
            print('Unable to scrape user data', source.status_code)

    return df


def scrape_image_url(anime_id):
    """
    Scrapes anime url from myanimelist.net using the anime_id

    Parameters:
    anime_id (str): anime id to scrape image from

    Returns:
    anime_img_url (str): the url to the image of the anime
    """
    anime_img_url = ''
    source = requests.get('https://myanimelist.net/anime/' + str(anime_id))
    if source.status_code == 200:
        soup = BeautifulSoup(source.text, "html.parser")
        anime_img_url = soup.find('img', class_='ac')['src']
    else:
        anime_img_url = str(source.status_code)

    return anime_img_url

