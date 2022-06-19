"""
File: datLista.py
Author: 
Class for list of data.
"""

import numpy as np
class DList(object):
    def __init__(self, name, unit=''):
        self._name = name
        self._unit = unit #defite the mesure unit of the list of data
        self._valueList = np.array([])
        self._errorList = np.array([])
        
#methods to get class' parameters
    def get_Name(self):
        return self._name

    def get_Unit(self):
        return self._unit
