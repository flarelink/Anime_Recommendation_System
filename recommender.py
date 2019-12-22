import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import user_xml_to_pandas_df, scrape_image_url, scrape_user_data_from_username

# Helper functions
def get_name_from_id(df, id):
    return df[df.animeID == id]["name"].values[0]
def get_id_from_name(df, name):
    return df[df.name == name]["animeID"].values[0]
def combine_features(row, features, bad_chars):
    features_string = ''
    for f in features:
        features_string += row[f] + ' '
    features_string = features_string.translate(bad_chars)
    return features_string[:-1]  # don't want the last space

def content_based(args):
    # load data into Dataframe
    anime_df = pd.read_csv(args.dataset_path)
    anime_df.columns = anime_df.columns.str.lstrip()  # there was a space in the anime csv column header

    # single user anime list extracted
    # user_df = user_xml_to_pandas_df(args.user_gz)  # replacing with just referencing username and scraping from web
    user_df = scrape_user_data_from_username(args.username)
    user_animes_seen = {}
    if not user_df.empty:
        user_animes_seen = user_df.set_index('animeID').to_dict()['scored']

    # anime to recommend based off of
    sel_anime = args.sel_anime
    sel_anime_id = get_id_from_name(anime_df, sel_anime)
    sel_anime_index = anime_df.loc[(anime_df['animeID'] == sel_anime_id)].index[0]

    # combine features to utilize in count/similarity matrices
    features = ['genre', 'type', 'studios']
    bad_chars = str.maketrans(dict.fromkeys("[]',"))
    anime_df['sim_features'] = anime_df.apply(combine_features, args=(features, bad_chars, ), axis=1)

    # Let's grab a count matrix of animes that have similar features and then use cosine similarity on that matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(anime_df['sim_features'])
    sim_matrix = cosine_similarity(count_matrix)

    # Now we sort the similar animes; ignore the first entry because it'll be the same anime specified
    similar_animes = list(enumerate(sim_matrix[sel_anime_index]))
    similar_animes_sorted = sorted(similar_animes, key=lambda x: x[1])

    # Instead of just taking the most similar anime recommendation, let's instead sort them by the
    # animes that score the best relative to the number of people that scored
    anime_df.fillna(0)
    anime_df['norm_score'] = anime_df['scored'] / anime_df['scoredBy']
    anime_df.fillna(0)
    similar_animes_norm_score = sorted(similar_animes, key=lambda x: anime_df['norm_score'][x[0]])


    # Loop through to collect the anime ids from the recommendations
    # If the anime id is already in the user's completed animes, then ignore it and get a different recommendation
    recommendations = []
    rec_img_urls = []
    i = 0

    # for anime in similar_animes_sorted:  # sort only based on similarity
    for anime in similar_animes_norm_score:  # sort based off similarity and normalized score

        anime_id = anime_df.iloc[anime[0], 0]

        if anime_id not in user_animes_seen and anime_id != sel_anime_id:
            anime_name = get_name_from_id(anime_df, anime_id)
            recommendations.append(anime_name)
            rec_img_urls.append(scrape_image_url(anime_id))
            i += 1
        if i > args.num_recs-1:
            break

    return recommendations, rec_img_urls
