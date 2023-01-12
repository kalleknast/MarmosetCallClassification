"""
Utilities for MarmosetCallClassification
"""
def convert_annotation_codes():
    """
    The original annotation codes are as follows:
    49 phee
    50 twitter
    51 trill
    52 cry
    53 subharmonic phee
    54 and 55 cry-phee.
    31, 56 and 57 are unknown.
    """
    converter = {31: ('unknown', 'u', 'tab:blue'),
                 49: ('phee', 'p', 'tab:orange'),
                 50: ('twitter', 't', 'tab:green'),
                 51: ('trill', 'r', 'tab:red'),
                 52: ('cry', 'c', 'tab:purple'),
                 53: ('subharmonic phee', 's', 'tab:brown'),
                 54: ('cry-phee', 'y', 'tab:pink'),
                 55: ('cry-phee', 'y', 'tab:pink'),
                 56: ('unknown', 'u', 'tab:blue'),
                 57: ('unknown', 'u', 'tab:blue'),
                 'u': ('unknown', 31, 'tab:blue'),
                 'p': ('phee', 49, 'tab:orange'),
                 't': ('twitter', 50, 'tab:green'),
                 'r': ('trill', 51, 'tab:red'),
                 'c': ('cry', 52, 'tab:purple'),
                 's': ('subharmonic phee', 53, 'tab:brown'),
                 'y': ('cry-phee', 54, 'tab:pink')}

    return converter
