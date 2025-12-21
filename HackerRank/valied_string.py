n = int(input())
strings_list = []

for i in range(n):
    strings_list.append(input())

first_bracket_open = "("
first_bracket_close = ")"
second_bracket_open = "{"
second_bracket_close = "}"
third_bracket_open = "["
third_bracket_close = "]"

open_brackets = [first_bracket_open, second_bracket_open, third_bracket_open]
close_brackets = [first_bracket_close, second_bracket_close, third_bracket_close]

bracket_map = {
    first_bracket_open: first_bracket_close,
    second_bracket_open: second_bracket_close,
    third_bracket_open: third_bracket_close
}
def valid_bracket_string(s):
    stack = []

    for char in s:
        if char == '(' or char == '{' or char == '[':
            stack.append(char)
        else:
            if not stack:
                return "NO"

            last = stack.pop()

            if (char == ')' and last != '(') or \
               (char == '}' and last != '{') or \
               (char == ']' and last != '['):
                return "NO"

    if not stack:
        return "YES"
    else:
        return "NO"
            

for s in strings_list:
    print(valid_bracket_string(s))