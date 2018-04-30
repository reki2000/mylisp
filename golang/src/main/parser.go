package main

import (
	"strconv"
)

type context struct {
	line   []rune
	pos    int  // current parsing position in the "line"
	result expr // latest matched result
}

// parse string as a LISP program
func parse(line string) expr {
	ctx := context{pos: 0, line: []rune(line)}
	ctx.isElement()
	return ctx.result
}

func (ctx *context) eol() bool {
	return ctx.pos >= len(ctx.line)
}

func (ctx *context) char() rune {
	return ctx.line[ctx.pos]
}

func (ctx *context) is(ch rune) bool {
	if ctx.char() == ch {
		//fmt.Println("is:", ch, ctx)
		ctx.pos++
		return true
	}
	return false
}

func (ctx *context) skip() {
	for !ctx.eol() && ctx.is(' ') {
	}
}

func (ctx *context) match(val expr) bool {
	ctx.result = val
	return true
}

func (ctx *context) fail(pos int) bool {
	ctx.pos = pos
	return false
}

func (ctx *context) isOneOf(chars string) bool {
	for _, char := range chars {
		if ctx.is(char) {
			return ctx.match(char)
		}
	}
	return false
}

func (ctx *context) isToken(chars string) bool {
	pos := ctx.pos
	token := []rune{}
	for !ctx.eol() && ctx.isOneOf(chars) {
		token = append(token, ctx.result.(rune))
	}
	if len(token) > 0 {
		return ctx.match(string(token))
	}
	return ctx.fail(pos)
}

func (ctx *context) isNumber() bool {
	if ctx.isToken("0123456789") {
		i, err := strconv.ParseInt(ctx.result.(string), 10, 32)
		if err == nil {
			return ctx.match(int(i))
		}
	}
	return false
}

func (ctx *context) isString() bool {
	const stringChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-!_?+*&#$"
	if ctx.isToken(stringChars) {
		return true
	}
	return false
}

func (ctx *context) isNil() bool {
	pos := ctx.pos
	if ctx.is('n') &&
		ctx.is('i') &&
		ctx.is('l') {
		return ctx.match(NIL)
	}
	return ctx.fail(pos)
}

func (ctx *context) isElement() bool {
	ctx.skip()
	if ctx.isNil() ||
		ctx.isList() ||
		ctx.isQList() ||
		ctx.isNumber() ||
		ctx.isString() {
		ctx.skip()
		return true
	}
	return false
}

func (ctx *context) isElements() bool {
	pos := ctx.pos
	result := []expr{}
	for !ctx.eol() && ctx.isElement() {
		result = append(result, ctx.result)
	}
	if len(result) > 0 {
		return ctx.match(result)
	}
	return ctx.fail(pos)
}

func (ctx *context) isList() bool {
	pos := ctx.pos
	if ctx.is('(') {
		if ctx.isElements() {
			result := ctx.result
			if ctx.is(')') {
				return ctx.match(result)
			}
		}
		if ctx.is(')') {
			return ctx.match(NIL)
		}
	}
	return ctx.fail(pos)
}

func (ctx *context) isQList() bool {
	pos := ctx.pos
	if ctx.is('\'') && ctx.isList() {
		return ctx.match([]expr{"quote", ctx.result})
	}
	return ctx.fail(pos)
}
