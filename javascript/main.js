#!
require('console');

var NIL = [];
var FALSE = 0;
var TRUE = 1;

function _eval(env, expr) {
    while(true) {
        if (typeof expr === 'number') {
            return expr;
        } else if (typeof expr === 'string') {
            for (var i=0; i<env.length; i++) {
                if (expr === env[i].name) {
                    return env[i].body
                }
            }
            return expr;
        } else if (expr instanceof Array) {
            if (expr.length === 0) {
                return NIL;
            }
            func = expr[0];
            if (func === 'lambda' || func === 'fn') {
                return function() {
                    var argv = [];
                    for (var i=0; i<expr[1].length; i++) {
                        argv.push({name:expr[1][i], body:arguments[i+1]});
                    };
                    return _eval(argv.concat(arguments[0]), expr[2]);
                };
            } else if (func === 'quote') {
                return expr[1];
            } else if (func === 'cond') {
                expr = cond(env, expr.slice(1));
                continue;
            } else if (func === 'define') {
                global_env.unshift({name: expr[1], body: _eval(env, expr[2])});
                return NIL;
            } else {
                var args = []
                for (var i=0; i<expr.length; i++) {
                    args.push(_eval(env, expr[i]));
                }
                func = args.shift();
                if (typeof func === 'function') {
                    return func.apply(null, [env].concat(args));
                }
            }
            throw ('Not function:' + expr)
        }
        throw ('Unknown expression:' + expr);
    }
}

function cond(env, expr) {
    for (var i=0; i<expr.length; i++) {
        if (_eval(env, expr[i][0]) === TRUE) {
            return expr[i][1];
        }
    }
    return NIL;
}

function _parse(line) {
    function is_token(ctx, chars) {
        var token = '';
        while (!eol(ctx) && is_oneof(child(ctx), chars)) {
            token += ctx.result;
        }
        if (token.length > 0) {
            return matched(ctx, token);
        }
    }
    function is_number(ctx) {
        if (is_token(child(ctx), '0123456789')) {
            return matched(ctx, ctx.result - 0);
        };
    }
    function is_string(ctx) {
        if (is_token(child(ctx), 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-!_?+*&#')) {
            return matched(ctx, '' + ctx.result);
        }
    }
    function is_element(ctx) {
        skip(ctx);
        if (is_nil(child(ctx))
            || is_list(child(ctx))
            || is_qlist(child(ctx))
            || is_number(child(ctx))
            || is_string(child(ctx))) {
            skip(ctx);
            return matched(ctx, ctx.result);
        }
    }
    function is_elements(ctx) {
        var result = [];
        while (!eol(ctx) && is_element(child(ctx))) {
            result.push(ctx.result);
        }
        if (result.length > 0) {
            return matched(ctx, result);
        }
    }
    function is_nil(ctx) {
        if (is_oneof(child(ctx), 'n')
            && is_oneof(child(ctx), 'i')
            && is_oneof(child(ctx), 'l')) {
                return matched(ctx, NIL);
        }
    }
    function is_qlist(ctx) {
        if (is_oneof(child(ctx), "'") && is_list(child(ctx))) {
            return matched(ctx, ['quote', ctx.result]);
        }
    }
    function is_list(ctx) {
        var result = [];
        if (is_oneof(child(ctx), '(')) {
            if (is_elements(child(ctx))) {
                result = ctx.result;
                if (is_oneof(child(ctx), ')')) {
                    return matched(ctx, result);
                }
            }
        }
    }
    function is_oneof(ctx, chars) {
        for (var i=0; i<chars.length; i++) {
            if (line[ctx.pos] === chars[i]) {
                ctx.pos++;
                return matched(ctx, chars[i]);
            }
        }
    }
    function eol(ctx) {
        return ctx.pos >= line.length;
    }
    function skip(ctx) {
        while (!eol(ctx)) {
            if (line[ctx.pos] !== ' ') {
                return;
            }
            ctx.pos++;
        }
    }
    function child(ctx) {
        return {pos: ctx.pos, result: null, parent: ctx};
    }
    function matched(ctx, result) {
        ctx.parent.pos = ctx.pos;
        ctx.parent.result = result;
        return true;
    }

    ctx = { pos: 0, result: null, parent: null};
    if (is_element(child(ctx))) {
        return ctx.result;
    }
    return false;
}

var global_env = [
    {name: 'car', body: function(env, a) { return a[0]; }},
    {name: 'cdr', body: function(env, a) { return a[0]; }},
    {name: 'eq?', body: function(env, a,b) { return (a === b) ? TRUE : FALSE; }},
    {name: '+', body: function(env, a,b) { return a + b; }},
    {name: '-', body: function(env, a,b) { return a - b; }},
    {name: '*', body: function(env, a,b) { return a * b; }}
];

function _repl(line, isConsole) {
    if (line.length > 0 && line[0] != ';') {
        return _eval(global_env, _parse(line));
    }
}

var fs = require("fs");
var readline = require("readline"); 
var stream = fs.createReadStream("rc.lisp", "utf8");
var reader = readline.createInterface({ input: stream });
reader.on("line", (data) => {
    _repl(data, false);
});

process.stdout.write("lisp>");
process.stdin.setEncoding('utf-8');
process.stdin.on('data', function (data) {
    console.log(_repl(data, true));
    process.stdout.write("lisp>");
});
