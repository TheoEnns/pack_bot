"""
    pb_get_json.py
        Author: Theodore Enns
        Brief: A few helper functions for getting json data
            for the pack bot assignment.
"""
import os
import urllib2
import json


def http_fetch_json(http_path):
    """
    Grabs json string from URL
    :param http_path: string path of http fetch
    :return: None if fetch fails and a serialized json string otherwise
    """
    director = urllib2.build_opener()
    req = urllib2.Request(http_path, headers={'Accept': 'application/json'})
    result = director.open(req)
    if result is not None:
        return result.read()
    else:
        return None


def file_fetch_json(file_path):
    """
    Grabs json string from file path (used for testing)
    :param file_path: string path of file
    :return: None if open fails and a serialized json string otherwise
    """
    if not os.path.isfile(file_path):
        return None
    result = open(file_path, "r")
    data = result.read()
    result.close()
    if data is not None:
        return data
    else:
        return None


def grab_dict_from(source):
    """
    Gets deserialized dict from json source (file path loading for debug purposes)
    :param source: string path of file or http path for file
    :return: a dictionary with deserialized contents from source
    """
    if source.startswith("http://"):
        data = http_fetch_json(source)
    else:
        data = file_fetch_json(source)
    if data is None:
        raise Exception(["Failed to open source path: ", source])
    result = json.loads(data)
    return result
