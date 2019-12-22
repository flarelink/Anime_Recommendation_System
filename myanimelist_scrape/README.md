# How to use

This script can be used to download anime dataset from [**Myanimelist**](https://myanimelist.net/) using an unofficial MyAnimeList REST API, [**Jikan**](https://jikan.me/docs).

#### Column metadata:

* animeID: id of anime as in anime url [https://myanimelist.net/anime/<span style="color:red">**1**</span>](https://myanimelist.net/anime/1)
* name: title of anime
* premiered: premiered on. default format (season year) 
* genre: list of genre
* type: type of anime (example TV, Movie etc) 
* episodes: number of episodes
* studios: list of studio
* source: source of anime (example original, manga, game etc) 
* scored: score of anime
* scoredBy: number of member scored the anime
* members: number of member added anime to their list

#### Syntax
```
python getAnime.py starting_index ending_index [output_file.csv]
```

# Slightly Modified Web Scraping Script from: https://github.com/Dibakarroy1997/myanimelist-data-set-creator