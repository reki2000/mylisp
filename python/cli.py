#!/usr/bin/env pt\ython
# encoding:utf-8

import parser3 as p
import runner2 as r
import sys

def _prompt(str, console):
    if console:
        print(str, flush=True, end='')

def load(f, console=False, env=r.global_env):
    buf = ""
    _prompt('lisp>', console)
    for l in f:
        #print("loaded:" + l)
        if len(l) == 0 or l[0] == ';':
            buf = ''
        else:
            buf += l.rstrip('\n')
            if buf.count('(') - buf.count(')') > 0:
                _prompt('    >', console)
                continue

        if buf:
            expr = p.parse(buf)
            if expr is None:
                print('Syntax error in:' + buf)
            else:
                try:
                    result = r._eval(env, expr)
                    _prompt('=>' + str(result) + '\n', console)
                except Exception as e:
                    print(e)

            buf = ''

        _prompt('lisp>', console)

with open('rc.lisp', 'r') as f:
    load(f)

load(sys.stdin, console=True)
