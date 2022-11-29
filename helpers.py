import os
import pathlib
import shutil
import argparse
import requests

import html2text

YEAR = "2022"
BASE_URL = f"https://adventofcode.com/"

NEIGHBORS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
NEIGHBORS_ORTH = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def parse_input(filename):
    with open(filename) as file:
        input_list = file.read().splitlines()
    return input_list


def nested_list_to_int(input_data):
    return [[int(x) for x in lst] for lst in input_data]


def create_folder_structure():
    cwd = pathlib.Path().resolve()
    for i in range(1,26):
        day_number = str(i).zfill(2)
        newdir_path = os.path.join(cwd, day_number)

        try:
            os.mkdir(newdir_path)
        except FileExistsError:
            pass

        for filename in ["inputtest.txt", "input.txt"]:
            pathlib.Path(os.path.join(newdir_path, filename)).touch()

        exercise_filename = f"exercise_{day_number}.py"
        shutil.copy((os.path.join(cwd, "template.py")), os.path.join(newdir_path, exercise_filename))

def download_problem_for_day(day, year=YEAR):

    year = year if year else YEAR
    day_url = BASE_URL + f"{year}/day/{str(day)}"
    gh_cookie = os.environ.get("GH_COOKIE")
    day_number = str(day).zfill(2)
    cwd = pathlib.Path().resolve()

    response = requests.get(day_url, headers={"cookie":gh_cookie})
    parsed_response = html2text.html2text(response.text)

    # drop header nonsense
    parsed_response = parsed_response.split("## \\")[1]

    # extract example
    example = parsed_response.split("\n\n    \n    \n    ")[1].split("\n\n")[0]
    example = "\n".join([item.strip() for item in example.split("\n")[:-1]])
    example_path = os.path.join(cwd, day_number, f"inputtest.txt")
    with open(example_path, "w+") as file:
        file.write(example)

    # get problem text
    parsed_response = parsed_response.split("To play, please")[0].strip("\n")
    txt_path = os.path.join(cwd, day_number, f"{day_number}.txt")
    with open(txt_path, "w+") as file:
        file.write(parsed_response)

    # get puzzle input
    if gh_cookie:
        response = requests.get(day_url + "/input", headers={"cookie": gh_cookie})
        parsed_response = str(response.text).strip("\n")
        input_path = example_path = os.path.join(cwd, day_number, f"input.txt")
        with open(input_path, "w+") as file:
            file.write(parsed_response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--init', action='store_true')
    parser.add_argument('-d', '--day', type=int, help="Day to pull down")
    parser.add_argument('-y', '--year', type=int, help="AoC year to target")
    args = parser.parse_args()
    if args.init:
        create_folder_structure()
    if args.day:
        download_problem_for_day(args.day, year=args.year)
