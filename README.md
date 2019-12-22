# Anime_Recommender_System
A fun content based anime recommender system

Usage:
-------------

python3 main.py

By default the program will look for the Anime.csv file in the current working directory and then the default anime is currently set to Dr. Stone with 5 recommendations and no username is specified to search their list.

If you want to check out 10 recommendations for One Piece using my profile on myanimelist.net run:

python3 main.py --sel_anime 'One Piece' --num_recs 10 --username flarelink --watching_list True 

What you will find is that the anime recommendations won't include what I'm watching/what I have completed.

For additional options on the arguments used in the program run:

python3 main.py -h


Requirements + Libraries:
--------------
- Python 3.X
- Pandas
- NumPY
- OS
- Argparse
- requests
- requests_html
- BeautifulSoup
- Sci-kit learn

I'm using the following OS:
- Ubuntu 18.04LTS (I have not tested this program on Windows or Mac)
