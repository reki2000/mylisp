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

func (ctx *context) oneOf(chars string) bool {
	for _, char := range chars {
		if ctx.is(char) {
			ctx.result = char
			return true
		}
	}
	return false
}

func (ctx *context) token(chars string) bool {
	pos := ctx.pos
	token := []rune{}
	for !ctx.eol() && ctx.oneOf(chars) {
		token = append(token, ctx.result.(rune))
	}
	if len(token) > 0 {
		ctx.result = string(token)
		return true
	}
	ctx.pos = pos
	return false
}

func (ctx *context) isNumber() bool {
	if ctx.token("0123456789") {
		i, err := strconv.ParseInt(ctx.result.(string), 10, 32)
		if err == nil {
			ctx.result = int(i)
			return true
		}
	}
	return false
}

func (ctx *context) isString() bool {
	const stringChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-!_?+*&#$"
	if ctx.token(stringChars) {
		return true
	}
	return false
}

func (ctx *context) isNil() bool {
	pos := ctx.pos
	if ctx.is('n') &&
		ctx.is('i') &&
		ctx.is('l') {
		ctx.result = NIL
		return true
	}
	ctx.pos = pos
	return false
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
		ctx.result = result
		return true
	}
	ctx.pos = pos
	return false
}

func (ctx *context) isList() bool {
	pos := ctx.pos
	if ctx.is('(') {
		if ctx.isElements() {
			result := ctx.result
			if ctx.is(')') {
				ctx.result = result
				return true
			}
		}
	}
	ctx.pos = pos
	return false
}

func (ctx *context) isQList() bool {
	if ctx.is('\'') &&
		ctx.isList() {
		ctx.result = []expr{"quote", ctx.result}
		return true
	}
	return false
}
