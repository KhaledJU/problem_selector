from logic import get_problems, exclude_solved, format_problems, print_results, print_html_results

problems = get_problems()
unsolved = exclude_solved(problems)
tags_map = format_problems(unsolved)
print_html_results(tags_map)
print_results(tags_map)

