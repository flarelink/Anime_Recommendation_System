##############################################################################
# main.py - Anime recommendation system - updated with all animes up until
#           12/21/19
#
# Copyright (C) 2019   Humza Syed
#
# This is free software so please use it however you'd like! :)
##############################################################################

from __future__ import print_function, division
import argparse
import os
import pandas as pd
from recommender import content_based

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
                        help='Specify path to dataset')

    # arguments for recommender system
    parser.add_argument('-s', '--sel_anime', type=str, default="Dr. Stone",
                        help='The anime you want recommendations based off of')
    parser.add_argument('-n', '--num_recs', type=int, default=5,
                        help='Number of output recommendations')
    # parser.add_argument('-g', '--genres', type=str2bool, default=False,
    #                     help='Specify if we want to grab genres off web page or from local txt file')

    # arguments for user data
    parser.add_argument('-u', '--username', type=str, default=None,
                        help='Specify your myanimelist.net username to make sure the anime has not been seen by you')
    parser.add_argument('-w', '--watching_list', type=str2bool, default=False,
                        help='Specify if you want to account for animes you are currently watching')

    # extract gz from: https://myanimelist.net/panel.php?go=export
    # depreciated:
    # parser.add_argument('-gz', '--user_gz', type=str, default=os.path.join(os.getcwd(),
    #                                                                        'animelist_1576887385_-_3451891.xml.gz'),
    #                     help='Specify path to user profile gz')

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

    # run through anime recommender
    recommendations, scraped_images = content_based(args)

    print(recommendations)
    print(scraped_images)



"""
##############################################################################
# Main call
##############################################################################
"""
if __name__ == '__main__':
    main()
