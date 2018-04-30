package main

import (
	"fmt"
	"reflect"
)

func find(env []Var, name string) expr {
	for _, v := range env {
		if v.name == name {
			return v.body
		}
	}
	return name
}

func cond(env []Var, v ...expr) expr {
	for _, e := range v {
		e := e.([]expr)
		if eval(env, e[0]) == TRUE {
			return e[1]
		}
	}
	return NIL
}

func eval(env []Var, e expr) expr {
	switch e.(type) {
	case int:
		return e.(int)
	case string:
		return find(env, e.(string))
	case []expr:
		e := e.([]expr)
		if len(e) == 0 {
			return NIL
		}
		fn := e[0]
		switch fn {
		case "lambda", "fn":
			return func(_env []Var, _args ...expr) expr {
				argv := []Var{}
				for i, _e := range e[1].([]expr) {
					argv = append(argv, Var{_e.(string), _args[i]})
				}
				return eval(append(argv, _env...), e[2])
			}
		case "quote":
			return e[1]
		case "cond":
			return eval(env, cond(env, e[1:]...))
		case "define":
			GlobalEnv = append(GlobalEnv, Var{e[1].(string), eval(env, e[2])})
			return NIL
		default:
			args := []expr{}
			for _, e := range e {
				args = append(args, eval(env, e))
			}
			if reflect.TypeOf(args[0]).Kind() == reflect.Func {
				fn := args[0].(func([]Var, ...expr) expr)
				return fn(env, args[1:]...)
			}
			panic("Not function:" + fmt.Sprintf("%v", e))
		}
	}
	panic("Invalid expression:" + fmt.Sprintf("%v", e))
}
