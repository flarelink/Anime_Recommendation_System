# Anime_Recommendation_System
A fun content based anime recommendation system. The recommendation system is initially based on the similarity of genre, type (TV, OVA, etc.), and studio(s). It is then based off the shrinkage estimation of the scores and number of people that scored. 

Usage:
-------------

python3 main.py

By default the program will look for the Anime.csv file in the current working directory and then the default anime is currently set to Naruto with 5 recommendations and no username is specified to search their list.

An example output can be seen below:

![Output Image](anime_recs.png)

If you want to check out 10 recommendations for One Piece using my profile on myanimelist.net run:

python3 main.py --sel_anime 'One Piece' --num_recs 10 --username flarelink --watching_list True 

For additional options on the arguments used in the program run:

python3 main.py -h


Python Version and OS used:
--------------
- Python 3.7.4
- Ubuntu 18.04LTS 
