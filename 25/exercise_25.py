from helpers import helpers


def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    score = 0
    for line in input:
        thisnum = 0
        for idx, char in enumerate(line[::-1]):
            power = 5 ** idx
            if char in ["0", "1", "2"]:
                thisnum += power * int(char)
            elif char == "-":
                thisnum -= power * 1
            elif char == "=":
                thisnum -= power * 2
        score += thisnum
    return count(score)


def count(score):
    string = ""
    while score != 0:
        remainder = score % 5
        if remainder == 0:
            string = "0" + string
        elif remainder == 1:
            string = "1" + string
            score -= 1
        elif remainder == 2:
            string = "2" + string
            score -= 2
        elif remainder == 3:
            string = "=" + string
            score += 2
        elif remainder == 4:
            string = "-" + string
            score += 1
        score = score // 5
    return string


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    print("THERE AIN'T NO PART TWO, COWBOY")
