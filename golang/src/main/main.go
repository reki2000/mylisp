package main

import (
	"bufio"
	"fmt"
	"os"
)

// Predefined constants
var (
	NIL = []int{}
)

type env map[expr]string

// expr should be one of string, int, NIL, TRUE, FALSE and array of expr
type expr interface{}

var globalEnv env

// repl - interactive interpreter for console
func repl(line string) expr {
	if len(line) > 0 && line[0] != ';' {
		return eval(globalEnv, parse(line))
	}
	return nil
}

func main() {
	// file, err := os.Open("rc.lisp")
	// if err != nil {
	// 	log.Fatal(err)
	// }
	// defer file.Close()

	// scanner := bufio.NewScanner(file)
	// for scanner.Scan() {
	// 	fmt.Println(repl(scanner.Text()))
	// }

	// if err := scanner.Err(); err != nil {
	// 	log.Fatal("scanner error")
	// }

	fmt.Print("lisp>")
	console := bufio.NewScanner(os.Stdin)
	for console.Scan() {
		fmt.Println(repl(console.Text()))
		fmt.Print("lisp> ")
	}
}
