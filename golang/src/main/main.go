package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

// Predefined constants
var (
	NIL   = []expr{}
	TRUE  = 1
	FALSE = 0
)

// expr should be one of string, int, NIL, TRUE, FALSE and array of expr
type expr interface{}

// Var contains defined variables
type Var struct {
	name string
	body expr
}

// GlobalEnv have global variables
var GlobalEnv = []Var{}

// repl - interactive interpreter for console
func repl(line string) expr {
	if len(line) > 0 && line[0] != ';' {
		return eval(GlobalEnv, parse(line))
	}
	return nil
}

func main() {
	GlobalEnv = append(GlobalEnv, Var{"car", func(env []Var, a ...expr) expr {
		return a[0].([]expr)[0]
	}})
	GlobalEnv = append(GlobalEnv, Var{"cdr", func(env []Var, a ...expr) expr {
		return a[0].([]expr)[1:]
	}})
	GlobalEnv = append(GlobalEnv, Var{"eq?", func(env []Var, a ...expr) expr {
		if a[0] == a[1] {
			return TRUE
		}
		return FALSE
	}})
	GlobalEnv = append(GlobalEnv, Var{"+", func(env []Var, a ...expr) expr {
		return a[0].(int) + a[1].(int)
	}})
	GlobalEnv = append(GlobalEnv, Var{"-", func(env []Var, a ...expr) expr {
		return a[0].(int) - a[1].(int)
	}})
	GlobalEnv = append(GlobalEnv, Var{"*", func(env []Var, a ...expr) expr {
		return a[0].(int) * a[1].(int)
	}})

	file, err := os.Open("rc.lisp")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		fmt.Println(repl(scanner.Text()))
	}

	if err := scanner.Err(); err != nil {
		log.Fatal("scanner error")
	}

	fmt.Print("lisp>")
	console := bufio.NewScanner(os.Stdin)
	for console.Scan() {
		fmt.Println(repl(console.Text()))
		fmt.Print("lisp> ")
	}
}
