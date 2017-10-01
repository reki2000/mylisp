#!/usr/bin/env pt\ython
# encoding:utf-8

from runner2 import global_env, _eval, NIL, TRUE, _s

import unittest

class Test(unittest.TestCase):

    def test_eq(self):
        self.assertEqual(_eval(global_env, [_s('eq?'), 1, 2]), [])
        self.assertEqual(_eval(global_env, [_s('eq?'), 1, 1]), 1)

    def test_cond(self):
        self.assertEqual(_eval(global_env, [_s('cond'), [[], 1]]), [])
        self.assertEqual(_eval(global_env, [_s('cond'), [[], 2], [1, 1]]), 1)

    def test_eval(self):
        self.assertEqual(_eval(global_env, [_s('eval'), [_s('+'), 1, 2]]), 3)

    def test_quote(self):
        self.assertEqual(_eval(global_env, [_s('quote'), [1, 2]]), [1, 2])

    def test_set(self):
        user_env = [] + global_env
        _eval(user_env, [_s('define'), _s('a'), 2])
        self.assertEqual(_eval(user_env, _s('a')), 2)

    def test_plus(self):
        self.assertEqual(_eval(global_env, [_s('+'), [_s('+'), 1, 2], 3]), 6)

    def test_fn(self):
        self.assertEqual(_eval(global_env, [[_s('fn'), [_s('x'), _s('y')], [_s('+'), _s('x'), _s('y')]], [_s('+'), 1, 2], 2]), 5)

    def test_fn_quote(self):
        self.assertEqual(_eval(global_env, [[_s('fn'), [_s('x'), _s('y')], [_s('+'), [_s('eval'), _s('x')], _s('y')]], [_s('quote'), [_s('+'), 1, 2]], 2]), 5)

    def test_recursive(self):
        user_env = [] + global_env
        list = [_s('define'), _s('len'), [_s('fn'), [_s('x')], [_s('cond'), [[_s('eq?'), _s('x'), NIL], 0], [1, [_s('+'), 1, [_s('len'), [_s('cdr'), _s('x')]]]]]]]
        _eval(user_env, list)
        self.assertEqual(_eval(user_env, [_s('len'), [_s('quote'), [i for i in range(0,80)]]]), 80)

    def test_define_fn(self):
        user_env = [] + global_env
        _eval(user_env, [_s('define'), _s('plus'), [_s('fn'), [_s('x'), _s('y')], [_s('+'), _s('x'), _s('y')]]])
        self.assertEqual(_eval(user_env, [_s('plus'), 1, 3]), 4)

    def test_define_complex_fn(self):
        user_env = [] + global_env
        _eval(user_env, [_s('define'), _s('not'), [_s('fn'), [_s('x')], [_s('cond'), [_s('x'), []], [1, 1]]]])
        self.assertEqual(_eval(user_env, [_s('not'), []]), 1)

    def test_let_fn(self):
        line = [_s('let'), [_s('plus'), [_s('fn'), [_s('x'), _s('y')], [_s('+'), _s('x'), _s('y')]]], [_s('plus'), 1, 2]]
        self.assertEqual(_eval(global_env, line), 3)

    def test_let_car(self):
        self.assertEqual(_eval(global_env, [_s('car'), [_s('quote'), [1, 2]]]), 1)

    def test_let_car2(self):
        self.assertEqual(_eval(global_env, [_s('car'), [_s('quote'), [[1, 2], 3]]]), [1, 2])

    def test_let_car3(self):
        self.assertEqual(_eval(global_env, [_s('car'), [_s('car'), [_s('quote'), [[1,2], 3]]]]), 1)

    def test_define_setq(self):
        user_env = [] + global_env
        _eval(user_env, [_s('define'), _s('a'), 1])
        _eval(user_env, [_s('setq!'), _s('a'), 2])
        self.assertEqual(_eval(user_env, [_s('+'), 0, _s('a')]), 2)

if __name__ == '__main__':
    unittest.main()
