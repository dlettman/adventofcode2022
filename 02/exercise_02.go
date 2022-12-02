package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

var idx_map_them = map[string]int{
	"A": 0,
	"B": 1,
	"C": 2,
}
var idx_map_me = map[string]int{
	"X": 0,
	"Y": 1,
	"Z": 2,
}
var diff_score_map = map[int]int{
	0:  3,
	-1: 0,
	-2: 6,
}
var diff_map = map[string]int{
	"X": -1,
	"Y": 0,
	"Z": -2,
}
var my_moves = []string{"X", "Y", "Z"}

func my_move_score(my_move string) int {
	return idx_map_me[my_move] + 1
}

func part1(input_filename string) string {

	file, _ := os.Open(input_filename)
	defer file.Close()
	scanner := bufio.NewScanner(file)
	total := 0
	for scanner.Scan() {
		text := scanner.Text()
		moves := strings.Split(text, " ")
		diff := -1 * (3 + idx_map_them[moves[0]] - idx_map_me[moves[1]]) % 3 // Find out the result based on where our move is relative to theirs
		score := diff_score_map[diff] + my_move_score(moves[1])
		total += score
	}
	return strconv.Itoa(total)
}

func part2(input_filename string) string {

	file, _ := os.Open(input_filename)
	defer file.Close()
	scanner := bufio.NewScanner(file)
	total := 0
	for scanner.Scan() {
		text := scanner.Text()
		move, result := strings.Split(text, " ")[0], strings.Split(text, " ")[1]
		my_move := my_moves[(3+idx_map_them[move]+diff_map[result])%3] // Find out our move based on their move and the result
		score := diff_score_map[diff_map[result]] + my_move_score(my_move)
		total += score
	}
	return strconv.Itoa(total)
}

func main() {

	fmt.Println(part1("inputtest.txt"))
	fmt.Println(part1("input.txt"))
	fmt.Println(part2("inputtest.txt"))
	fmt.Println(part2("input.txt"))
}
