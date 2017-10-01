#!/usr/bin/env pt\ython
# encoding:utf-8

from runner2 import global_env, _eval, NIL, TRUE

import unittest

class Test(unittest.TestCase):

    def test_eq(self):
        self.assertEqual(_eval(global_env, ['eq?', 1, 2]), [])
        self.assertEqual(_eval(global_env, ['eq?', 1, 1]), 1)

    def test_cond(self):
        self.assertEqual(_eval(global_env, ['cond', [[], 1]]), [])
        self.assertEqual(_eval(global_env, ['cond', [[], 2], [1, 1]]), 1)

    def test_eval(self):
        self.assertEqual(_eval(global_env, ['eval', ['+', 1, 2]]), 3)

    def test_quote(self):
        self.assertEqual(_eval(global_env, ['quote', [1, 2]]), [1, 2])

    def test_set(self):
        user_env = [] + global_env
        _eval(user_env, ['define', 'a', 2])
        self.assertEqual(_eval(user_env, 'a'), 2)

    def test_plus(self):
        self.assertEqual(_eval(global_env, ['+', ['+', 1, 2], 3]), 6)

    def test_fn(self):
        self.assertEqual(_eval(global_env, [['fn', ['x', 'y'], ['+', 'x', 'y']], ['+', 1, 2], 2]), 5)

    def test_fn_quote(self):
        self.assertEqual(_eval(global_env, [['fn', ['x', 'y'], ['+', ['eval', 'x'], 'y']], ['quote', ['+', 1, 2]], 2]), 5)

    def test_recursive(self):
        user_env = [] + global_env
        list = ['define', 'len', ['fn', ['x'], ['cond', [['eq?', 'x', NIL], 0], [1, ['+', 1, ['len', ['cdr', 'x']]]]]]]
        _eval(user_env, list)
        self.assertEqual(_eval(user_env, ['len', ['quote', [i for i in range(0,80)]]]), 80)

    def test_define_fn(self):
        user_env = [] + global_env
        _eval(user_env, ['define', 'plus', ['fn', ['x', 'y'], ['+', 'x', 'y']]])
        self.assertEqual(_eval(user_env, ['plus', 1, 3]), 4)

    def test_define_complex_fn(self):
        user_env = [] + global_env
        _eval(user_env, ['define', 'not', ['fn', ['x'], ['cond', ['x', []], [1, 1]]]])
        self.assertEqual(_eval(user_env, ['not', []]), 1)

    def test_let_fn(self):
        line = ['let', ['plus', ['fn', ['x', 'y'], ['+', 'x', 'y']]], ['plus', 1, 2]]
        self.assertEqual(_eval(global_env, line), 3)

    def test_let_car(self):
        self.assertEqual(_eval(global_env, ['car', ['quote', [1, 2]]]), 1)

    def test_let_car2(self):
        self.assertEqual(_eval(global_env, ['car', ['quote', [[1, 2], 3]]]), [1, 2])

    def test_let_car3(self):
        self.assertEqual(_eval(global_env, ['car', ['car', ['quote', [[1,2], 3]]]]), 1)

    def test_define_setq(self):
        user_env = [] + global_env
        _eval(user_env, ['define', 'a', 1])
        _eval(user_env, ['setq!', 'a', 2])
        self.assertEqual(_eval(user_env, ['+', 0, 'a']), 2)

if __name__ == '__main__':
    unittest.main()
