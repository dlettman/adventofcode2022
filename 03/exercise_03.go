package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

const LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

func make_map(string) map[rune]int {
	score_map := make(map[rune]int)
	for idx, char := range LETTERS {
		score_map[char] = idx + 1
	}
	fmt.Println(score_map)
	return score_map
}

var LETTER_SCORES = make_map(LETTERS)

func part1(input_filename string) string {

	score := 0
	file, _ := os.Open(input_filename)
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		text := scanner.Text()
		midpoint := len(text) / 2
		part1, part2 := text[0:midpoint], text[midpoint:]
		for _, char := range part1 {
			if strings.ContainsRune(part2, char) {
				score += LETTER_SCORES[char]
				break
			}
		}
	}
	return strconv.Itoa(score)
}

func part2(input_filename string) string {

	score, ticker := 0, 0
	working_string := ""
	file, _ := os.Open(input_filename)
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		text := scanner.Text()
		ticker += 1
		newstring := ""
		if working_string == "" {
			working_string = text
		} else {
			for _, char := range working_string {
				if strings.ContainsRune(text, char) {
					newstring += string(char)
				}
			}
			working_string = newstring
		}
		if ticker%3 == 0 {
			score += LETTER_SCORES[rune(working_string[0])]
			working_string = ""
		}
	}
	return strconv.Itoa(score)
}

func main() {

	fmt.Println(part1("inputtest.txt"))
	fmt.Println(part1("input.txt"))
	fmt.Println(part2("inputtest.txt"))
	fmt.Println(part2("input.txt"))
}
