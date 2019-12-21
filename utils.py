from bs4 import BeautifulSoup
import requests
import pandas as pd
import gzip


def scrape_genres(genres_flag=True):
    """
    Scrapes anime genres from myanimelist.net

    Parameters:
    genres_flag (Boolean): Determines if we scrape genres from the web or reference the generated txt file

    Returns:
    genres (list of str): All of the genres in a list of strings
    """

    # extract genres from online and break once we've reached the last genre
    genres = []
    if genres_flag:
        file = open('genres.txt', 'w')

        source = requests.get('https://myanimelist.net/anime.php').text
        soup = BeautifulSoup(source, "html.parser")
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


def user_xml_to_pandas_df(gz_file_path):
    """
    Creates a dataframe from user's xml file. The dataframe contains the completed animes with their user scores.

    Parameters:
    gz_file_path (str): Path to the user gz file that was downloaded

    Returns:
    user_df (Dataframe): Dataframe with 2 columns; animeId and scored
    """
    gz_file_path = '/home/flarelink/Documents/Github_Projects/Anime_Recommender_System/animelist_1576887385_-_3451891.xml.gz'
    with gzip.open(gz_file_path) as xml_file:
        data = BeautifulSoup(xml_file, 'xml')
        all_anime = data.find_all('anime')
        vals = []
        user_df = pd.DataFrame(columns=['animeID', 'scored'])
        pos = 0
        for anime in all_anime:
            if anime.find('my_status').text == 'Completed':
                vals.append(anime.find('series_animedb_id').text)
                vals.append(anime.find('my_score').text)

                # all anime details
                user_df.loc[pos] = vals
                vals = []
                pos += 1
    return user_df
