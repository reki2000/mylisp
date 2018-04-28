package main

import (
	"reflect"
	"testing"
)

func TestParse(t *testing.T) {
	actual := parse("01")
	expected := 1
	if actual != expected {
		t.Errorf("got %v(%v) but expected %v", actual, reflect.TypeOf(actual), expected)
	}
}

func TestParseList(t *testing.T) {
	actual := parse("(1 2 3)")
	expected := []expr{1, 2, 3}
	if !reflect.DeepEqual(actual, expected) {
		t.Errorf("got %v(%v) but expected %v", actual, reflect.TypeOf(actual), expected)
	}
}

func TestParseStringList(t *testing.T) {
	actual := parse("(a (b c))")
	expected := []expr{"a", []expr{"b", "c"}}
	if !reflect.DeepEqual(actual, expected) {
		t.Errorf("got %v(%v) but expected %v", actual, reflect.TypeOf(actual), expected)
	}
}

func TestParseStringQList(t *testing.T) {
	actual := parse("(a '(b c))")
	expected := []expr{"a", []expr{"quote", []expr{"b", "c"}}}
	if !reflect.DeepEqual(actual, expected) {
		t.Errorf("got %v(%v) but expected %v", actual, reflect.TypeOf(actual), expected)
	}
}
