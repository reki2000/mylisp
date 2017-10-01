#!/usr/bin/env pt\ython
# encoding:utf-8

NIL = []

TRUE = 1

class Symbol(object):
    def __init__(self, name):
      self.name = name

    def __repr__(self):
        return "Symbol(%s)" % self.name

_symbol_table = {}
def symbol(name):
    if not name in _symbol_table:
        _symbol_table[name] = Symbol(name)
    return _symbol_table[name]

_s = symbol
