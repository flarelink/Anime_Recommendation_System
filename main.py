##############################################################################
# main.py - Music generation program using a recurrent neural network. The
#           file takes an input folder with .mp3 files and trains on these
#           files to create new .mp3 files filled with new music.
#
# Copyright (C) 2019   Humza Syed
#
# This is free software so please use it however you'd like! :)
##############################################################################

from __future__ import print_function, division
import argparse
import os
import pandas as pd
from utils import scrape_genres, user_xml_to_pandas_df

"""
##############################################################################
# Parser
##############################################################################
"""


def create_parser():
    """
    return: parser inputs
    """

    class NiceFormatter(argparse.ArgumentDefaultsHelpFormatter,
                        argparse.RawDescriptionHelpFormatter):
        """Nice-looking formatter for argparse parsers. Prints defaults in help
        messages and allows for newlines in description/epilog."""
        pass

    parser = argparse.ArgumentParser(
        description='Anime Recommender System.',
        formatter_class=NiceFormatter
    )

    # function to allow parsing of true/false boolean
    def str2bool(v):
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    # arguments for dataset
    parser.add_argument('-d', '--dataset_path', type=str, default=os.path.join(os.getcwd(), 'Anime.csv'),
                        help='Specify dataset path')
    parser.add_argument('-g', '--genres', type=str2bool, default=False,
                        help='Specify if we want to grab genres off web page')

    # arguments for user data
    # extract gz from: https://myanimelist.net/panel.php?go=export
    parser.add_argument('-u', '--user_gz', type=str, default=os.path.join(os.getcwd(),
                                                                          'animelist_1576887385_-_3451891.xml.gz'),
                        help='Specify path to user profile gz')

    args = parser.parse_args()

    return args


"""
##############################################################################
# Main, where all the magic starts~
##############################################################################
"""


def main():
    """
      Runs through two images iteratively to make neural artwork~
    """

    # parsing input arguments
    args = create_parser()

    # load data into Dataframe
    anime_df = pd.read_csv(args.dataset_path)

    # all genres
    genres = scrape_genres(args.genres)

    # user anime list extracted using:
    user_df = user_xml_to_pandas_df(args.user_gz)



"""
##############################################################################
# Main call
##############################################################################
"""
if __name__ == '__main__':
    main()
