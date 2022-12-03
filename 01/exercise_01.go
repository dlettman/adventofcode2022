package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
)

func part1(input_filename string) string {
	elves := make([]int, 0)
	curr_tot := 0
	file, _ := os.Open(input_filename)
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		text := scanner.Text()
		if text == "" {
			elves = append(elves, curr_tot)
			curr_tot = 0
		} else {
			cals, _ := strconv.Atoi(text)
			curr_tot += cals
		}
	}
	elves = append(elves, curr_tot)
	sort.Ints(elves)
	return strconv.Itoa(elves[len(elves)-1])
}

func part2(input_filename string) string {
	elves := make([]int, 0)
	curr_tot := 0
	file, _ := os.Open(input_filename)
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		text := scanner.Text()
		if text == "" {
			elves = append(elves, curr_tot)
			curr_tot = 0
		} else {
			cals, _ := strconv.Atoi(text)
			curr_tot += cals
		}
	}
	elves = append(elves, curr_tot)
	sort.Ints(elves)
	total := 0
	for _, elf := range elves[len(elves)-3:] {
		total += elf
	}
	return strconv.Itoa(total)
}

func main() {
	fmt.Println(part1("input.txt"))
	fmt.Println(part2("input.txt"))
}
