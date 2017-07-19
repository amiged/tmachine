#!/usr/bin/env python3
#Time-stamp: <>
import fnmatch
import functools
import os
import re

def find(path, pattern):

    if isinstance(pattern, str): 
        match = functools.partial(fnmatch.fnmatch, pat=pattern)
    elif isinstance(pattern, re._pattern_type):
        match = pattern.match
    elif callable(pattern):
        match = pattern
    else:
        raise TypeError

    for root, dirs, files in os.walk(path):
        for file_ in files:
            if match(file_):
                yield os.path.join(root, file_)


if __name__ == '__main__':
    for i in find('../log/', '*.jpg'):
        print (i)

