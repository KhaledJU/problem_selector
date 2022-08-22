import json
from time import sleep
from typing import List

import requests

from constants import PPU_TEST_HANDLES, CODEFORCES_BASE_URL, PROBLEM_SET_URL, SUBMISSIONS_URL, PPU_HANDLES
from models import GeneralResponse, Problem


def get_problems():
    response = requests.get(url=f'{CODEFORCES_BASE_URL}/{PROBLEM_SET_URL}')
    modeled = GeneralResponse(**response.json())
    return set(problem.json() for problem in modeled.result.problems if problem.rating)


def get_solved_by_handle(handle: str):
    response = requests.get(url=f'{CODEFORCES_BASE_URL}/{SUBMISSIONS_URL}', params={'handle': handle})
    modeled = GeneralResponse(**response.json())
    solved_problems = set()

    if not modeled.result:
        return solved_problems

    for submission in modeled.result:
        solved_problems.add(submission.problem.json())

    return solved_problems


def exclude_solved(problems):
    unsolved = problems
    for handle in PPU_HANDLES:
        solved = get_solved_by_handle(handle)
        unsolved = unsolved - solved
        print(len(unsolved))
        sleep(0.5)

    return unsolved


def format_problems(problems):
    tags_map = {}
    for problem in problems:
        modeled = Problem(**json.loads(problem))
        for tag in modeled.tags:
            if tag not in tags_map:
                tags_map[tag] = []
            tags_map[tag].append(modeled)

    for key in tags_map:
        tags_map[key].sort(key=lambda x: (x.rating, -int(x.contestId)))

    return tags_map


def print_html_results(tags_map):
    for tag, problems in tags_map.items():
        f = open(f'html_results/{tag}.html', "w")
        f.write(f'<h1>{tag}</h1>')
        f.write('''
            <table class="table">
              <thead>
                <tr>
                  <th scope="col">Name</th>
                  <th scope="col"></th>
                  <th scope="col">Link</th>
                  <th scope="col"></th>
                  <th scope="col">Rate</th>
                  <th scope="col"></th>
                  <th scope="col">Tags</th>
                </tr>
              </thead>
              <tbody>

            ''')
        for problem in problems:
            f.write(f'''
                    <tr>
                      <td>{problem.name}</td>
                      <td>  </td>
                      <td><a href="https://codeforces.com/contest/{problem.contestId}/problem/{problem.index}">{problem.contestId} - {problem.index}</a></td>
                      <td>  </td>
                      <td>{problem.rating}</td>
                      <td>  </td>
                      <td>{problem.tags}</td>
                    </tr>
    
                ''')

        f.write('''
              </tbody>
            </table>
            ''')
        f.close()


def print_results(tags_map):
    for tag, problems in tags_map.items():
        f = open(f'text_results/{tag}.txt', "w")
        for problem in problems:
            f.write(f'url: <https://codeforces.com/contest/{problem.contestId}/problem/{problem.index}>  |  rating={problem.rating}  |  tags={problem.tags}')
            f.write('\n')
        f.close()