import string
from pprint import pprint

import string
import re
from copy import copy

def populate_dict(d, keys, value):
    """Populate 'dict' by nested 'keys'
    'value' will be a value of last key in 'keys'

    Example:
        dict = {}
        populate_dict(dict, ['py', 'ver'], '3.5')
        dict    # {'py': {'ver': '3.15'}}
    """
    reference_point = d
    for key in keys[:-1]:
        if not key in reference_point:
            reference_point[key] = {}
        reference_point = reference_point[key]
    reference_point[keys[-1]] = value

def trace_dict(d, keys):
    """Return a value of the last key of a nest of dicts
    
    Example:
        trace_dict({'py': {'ver': '3.5'}}, ['py', 'ver'])
        returns '3.5'
    """
    value = None
    reference_point = dict(d)
    for key in keys:
        #print(reference_point)
        reference_point = reference_point[key]
    return reference_point

def optimize_data(template, data):
    new_dict = {}

    pieces = string.Formatter().parse(template)
    pieces = filter(lambda piece: piece[1] != None, pieces)

    for piece in pieces:
        dict_repr = piece[1]             # Getting a string that represents
                                         # dictionary's nest structure
        #print(dict_repr)

        keys = re.split('\[|\]', dict_repr) # Split into keys by square brackets
        keys = filter(lambda s: s != '', keys)  # Filter out empty strings
                                            # (there must be a better way to
                                            # split by multiple delimiters)
        keys = list(keys)

        # Retrieving value of last key from dict
        #print(data, keys)
        value = trace_dict(data, keys)
    
        populate_dict(new_dict, keys, value)

    return new_dict


def main():
    template = 'Python version: {languages[python][latest_version]}'
    data = {
        'languages': {
            'python': {
                'latest_version': '3.6',
                'site': 'http://python.org',
            },
            'rust': {
                'latest_version': '1.17',
                'site': 'https://rust-lang.org',
            },
        },
    }
    print("Original data:")
    pprint(data)

    new_data = optimize_data(template, data)
    print("Optimized data:")
    pprint(new_data)


if __name__ == '__main__':
    main()
