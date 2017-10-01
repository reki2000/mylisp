#!/usr/bin/env python
# encoding:utf-8

#
# Delimiter := ' '*
# QList := ''' '(' Elements ')'
# List := '(' Elements ')'
# Elements := (Delimiter Element)* Delimiter
# Element := QList | List | Nil | Token
# Token := Number | Symbol | String
# Nil := 'n' 'i' 'l'
# Number := '0'..'9' ('0'..'9')*
# Symbol := ( 'a'..'z' | '-' | '_' | '0'..'9' )*
# String := '"' Char* '"'
# Char := 'a..z' | 'A'..'Z' | ' ' | '\' '\n' | '\' '\'  | '\' '"'

from core import Symbol, NIL, _s

line = ""

def parse(_line):
    global line
    line = _line
    ctx = Context()
    is_element(ctx.child())
    return ctx.result

def is_nil(ctx):
    if ctx.is_oneof('n') and ctx.is_oneof('i') and ctx.is_oneof('l'):
        return ctx.matched(NIL)

def is_number(ctx):
    token = ""
    while ctx.is_oneof('1234567890'):
        token += ctx.result
    if len(token) > 0:
        return ctx.matched(int(token))

def is_string(ctx):
    if ctx.is_oneof('"'):
        token = ""
        while True:
            if ctx.is_oneof('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvexyz#$%\'()[]{}<>.,/;:@^~|-_+*1234567890!?&= '):
                token += ctx.result
            elif ctx.is_oneof('\\'):
                if ctx.is_oneof('n"\\'):
                    if ctx.result == 'n':
                        token += "\n"
                    else:
                        token += ctx.result
                else:
                    # Invalid char after backslash
                    return
            else:
                break
        if ctx.is_oneof('"'):
            return ctx.matched(token)

def is_symbol(ctx):
    token = ""
    while ctx.is_oneof('abcdefghijklmnopqrstuvexyz-_+*1234567890!?&='):
        token += ctx.result
    if len(token) > 0:
        return ctx.matched(_s(token))

def is_token(ctx):
    if is_number(ctx.child()) or is_symbol(ctx.child()) or is_string(ctx.child()):
        return ctx.matched()

def is_element(ctx):
    if is_nil(ctx.child()) \
        or is_token(ctx.child()) \
        or is_list(ctx.child()) \
        or is_qlist(ctx.child()):
        return ctx.matched()

def is_elements(ctx):
    result = []
    ctx.skip_delimiter()
    while is_element(ctx.child()):
        result.append(ctx.result)
        ctx.skip_delimiter()
    ctx.skip_delimiter()
    return ctx.matched(result)

def is_qlist(ctx):
    if ctx.is_oneof("'") and ctx.is_oneof('(') and is_elements(ctx.child()):
        result = ctx.result
        if ctx.is_oneof(')'):
            return ctx.matched([_s('quote'), result])

def is_list(ctx):
    if ctx.is_oneof('(') and is_elements(ctx.child()):
        result = ctx.result
        if ctx.is_oneof(')'):
            return ctx.matched(result)

class Context:
    def __init__(self, parent=None):
        self.pos = 0 if parent is None else parent.pos
        self.parent = parent
        self.result = None

    def is_oneof(self, str):
        if self.pos < len(line):
            ch = line[self.pos]
            if ch in str:
                self.pos += 1
                self.result = ch
                return True

    def skip_delimiter(self):
        while self.is_oneof(' '):
            pass

    def child(self):
        return Context(self)

    def matched(self, result=None):
        self.parent.pos = self.pos
        self.parent.result = self.result if result is None else result
        return True

if __name__ == '__main__':
    import unittest
    class Test(unittest.TestCase):
        def test_simple(self):
            global line
            line = '(abc () nil (abc abc))'
            ctx = Context()
            matched = is_list(ctx.child())
            self.assertEqual(matched, True)
            self.assertEqual(ctx.result, [_s('abc'), [], [], [_s('abc'), _s('abc')]])

        def test_string_escape(self):
            global line
            line = '("ab\\\\\\n\\"c{}")'
            ctx = Context()
            matched = is_list(ctx.child())
            self.assertEqual(matched, True)
            self.assertEqual(ctx.result, ['ab\\\n\"c{}'])
    unittest.main()
