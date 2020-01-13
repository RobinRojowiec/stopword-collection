"""

IDE: PyCharm
Project: corpus-analysis
Author: Robin
Filename: util
Date: 13.01.2020

"""
import json


def save_dict(filename, dict: {}, prettyprint=False):
    """
    Stores a dictionary in JSON format
    :param filename:
    :param dict:
    :param prettyprint:
    :return:
    """
    json.dump(dict, open(filename, 'w+', encoding='utf-8'), indent=2 if prettyprint else 0)


def load_dict(filename):
    """
    Loads a dictionary stored in JSON format
    :param filename:
    :return:
    """
    data = json.load(open(filename))
    return data
