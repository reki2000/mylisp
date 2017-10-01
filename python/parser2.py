#!/usr/bin/env python
# encoding:utf-8

#
# Delimiter := ' '*
# QList := ''' '(' Elements ')'
# List := '(' Elements ')'
# Elements := (Delimiter Element)* Delimiter
# Element := QList | List | Token
# Token := ( 'a'..'z' | '-' | '_' )*
#

def parse(line):
    ctx = Context(line, None)
    parse_element(ctx.child())
    return ctx.result

def parse_token(ctx):
    token = ""
    while ctx.is_match('abcdefghijklmnopqrstuvexyz-_+*1234567890!?'):
        token += ctx.result
    if len(token) > 0:
        if token.isdigit():
            ctx.matched(int(token))
        else:
            ctx.matched(token)
        return True
    return False

def parse_element(ctx):
    if parse_token(ctx.child()) \
            or parse_list(ctx.child()) \
            or parse_qlist(ctx.child()):
        ctx.matched(ctx.result)
        return True
    return False

def parse_elements(ctx):
    result = []
    while True:
        ctx.skip_delimiter()
        if not parse_element(ctx.child()):
            break
        result.append(ctx.result)
    ctx.skip_delimiter()
    ctx.matched(result)
    return True

def parse_qlist(ctx):
    if ctx.is_match("'") and ctx.is_match('('):
        if parse_elements(ctx.child()):
            result = ctx.result
            if ctx.is_match(')'):
                ctx.matched(['quote', result])
                return True
    return False

def parse_list(ctx):
    if ctx.is_match('('):
        if parse_elements(ctx.child()):
            result = ctx.result
            if ctx.is_match(')'):
                ctx.matched(result)
                return True
    return False

class Context:
    def __init__(self, line, parent):
        self.line = line
        self.pos = 0
        self.parent = parent
        self.result = None

    def is_match(self, str):
        if self.pos < len(self.line):
            ch = self.line[self.pos]
            if ch in str:
                self.pos += 1
                self.result = ch
                return True
        return False

    def skip_delimiter(self):
        while self.is_match(' '):
            pass

    def child(self):
        return Context(self.line[self.pos:], self)

    def matched(self, result):
        self.parent.pos += self.pos
        self.parent.result = result

if __name__ == '__main__':
    import unittest
    class Test(unittest.TestCase):
        def test_simple(self):
            ctx = Context('(abc ()  (abc abc))', None)
            matched = parse_list(ctx.child())
            self.assertEqual(matched, True)
            self.assertEqual(ctx.result, ['abc', [], ['abc', 'abc']])
    unittest.main()
