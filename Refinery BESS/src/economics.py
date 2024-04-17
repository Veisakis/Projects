'''Economic functions'''

import config


def euro(money):
    '''Nice format for printing money'''
    return format(round(money, 2), ",") + " €"

