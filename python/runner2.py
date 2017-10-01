#!/usr/bin/env pt\ython
# encoding:utf-8

from core import TRUE, NIL

def _eval_debug(env, expr):
    print("** evaluating %s with :" % expr)
    for k,v in [(k,v) for k,v in env if isinstance(v, (int, str, list))]:
        print("  %s=%s" % (k,v))
    v = _eval_core(env, expr)
    if v != expr:
        print("** result = %s for %s" % (v, expr))
    return v

def _eval_core(env, expr):
    while True:
        if isinstance(expr, int) or expr == []:
            return expr
        elif isinstance(expr, str):
            for body in [v for k,v in env if k == expr]:
                return body
        elif isinstance(expr, list):
            f = expr[0]
            if f == 'quote':
                return expr[1]
            elif f == 'cond':
                expr = cond(env, *expr[1:])
                continue
            elif f == 'lambda' or f == 'fn':
                var, body, *_ = expr[1:]
                return lambda env, *args: _eval([(k,v) for k,v in zip(var, args)] + env, body)
            elif f == 'define':
                name, body, *_ = expr[1:]
                return env.insert(0, (name, _eval(env, body)))
            elif f == 'setq!':
                for i, e in enumerate(env):
                    if e[0] == expr[1]:
                        env[i] = (expr[1], expr[2])
                        return NIL
            elif f == 'let':
                (var, val), body, *_ = expr[1:]
                env, expr = ([(var, _eval(env, val))] + env), body
                continue
            else:
                func, *args = [_eval(env, v) for v in expr]
                if callable(func):
                    return func(env, *args)
            raise Exception("%s is not a function in %s" % (expr[0], expr))
        raise Exception("unknown identifier: %s" % expr)

_eval = _eval_core

def cond(env, *v):
    return [] if not v \
        else v[0][1] if _eval(env, v[0][0]) != NIL \
        else cond(env, *v[1:])

global_env = [
    ('car', lambda env, x: x[0]),
    ('cdr', lambda env, x: x[1:]),
    ('cons', lambda env, x,y: [x] + y),
    ('eval', lambda env, x: _eval(env, x)),
    ('eq?', lambda env, x,y: TRUE if x == y else NIL),
    ('+', lambda env, x,y: x + y),
    ('-', lambda env, x,y: x - y),
    ('*', lambda env, x,y: x * y),
    ('echo', lambda env, x: print(x))
]
