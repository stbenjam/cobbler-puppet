#!/usr/bin/env python

class InvalidSystemDefinition(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class EncParameterNotFound(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
       return repr(self.value)
