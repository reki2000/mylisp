
class Atom:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def eval(self, env):
        return self

class Symbol(Atom):
    def eval(self, env):
        print("search var %s in %s" % (self.value, env))
        for name, value in env:
            if self.value == name:
                return value
        if self.value in specials.keys():
            return self
        raise Exception("Unknown symbol %s" % self.value)

class Number(Atom):
    pass

class Nil(Atom):
    def __init__(self):
        pass

    def __str__(self):
        return "nil"

NIL = Nil()

class Cons:
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

    def __str__(self):
        return "(%s %s)" % (self.head, self.tail)

    def eval(self, env):
        print("eval cons %s with env %s" % (self.head, env))
        head = self.head.eval(env)
        if isinstance(head, Symbol):
            if head.value in specials.keys():
                return specials[head.value](env, self.tail)
        return head

class Func():
    def __init__(self, defs, body):
        self.defs = defs
        self.body = body

class Quote(Cons):
    def __init__(self, body):
        self.head = body
        self.tail = NIL

    def eval(env):
        return self.head

def plus(env, arg):
    if isinstance(arg, Nil):
        return Number(0)
    obj = arg.head.eval(env)
    if isinstance(obj, Number):
        return Number(obj.value + plus(env, arg.tail).value)
    raise Exception("invalid argument type: %s for %s" % (type(arg.head), arg.head))

def car(env, obj):
    if isinstance(obj, Cons):
        return obj.head
    raise Exception("invalid argument type: %s: %s" % (type(obj), obj))

def cdr(env, obj):
    if isinstance(obj, Cons):
        return obj.tail
    raise Exception("invalid argument type: %s: %s" % (type(obj), obj))

def quote(env, obj):
    return Quote(obj)

def fn(env, arg):
    if isinstance(arg, Cons):
        defs = arg.head
        body = arg.tail

    raise Exception("invalid argument type: %s: %s" % (type(arg), arg))

def let(env, arg):
    if isinstance(arg, Cons):
        defs = arg.head
        body = arg.tail
        if isinstance(defs, Cons):
            print("defining %s" % defs)
            var_name = defs.head
            if isinstance(var_name, Symbol):
                var_value = defs.tail.head.eval(env)
                return body.eval(env + [(var_name.value, var_value)])
    raise Exception("invalid argument type: %s: %s" % (type(arg), arg))

specials = {
    '+': plus,
    'car': car,
    'cdr': cdr,
    'let': let,
    'q' : quote
}

prog = [
    # (let (x 1) (+ x 1))
    Cons(Symbol('let'),
        Cons(
            Cons(Symbol('x'),
                Cons(Number(1), NIL)),
            Cons(
                Cons(Symbol('+'),
                    Cons(Symbol('x'),
                        Cons(Number(1),
                            NIL))),
                NIL)))
]

for line in prog:
    result = line.eval([])
    print(result)
