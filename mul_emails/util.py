import re
import ast

string_of_variables = """srajan = 'erh',
mayank = [145,2,3],
kutta = ['aman','rupesh']"""

pattern = r'(\w+)\s*=\s*(?:(?P<list>\[.*?\])|(?P<string>.*?))(?:,\s*|\Z)'
matches = re.findall(pattern, string_of_variables)

var = {'subject': ''}

print(matches)

for match in matches:
    variable_name = match[0]
    if match[1]:
        try:
            variable_value = ast.literal_eval(match[1])
        except (SyntaxError, ValueError):
            variable_value = match[1].strip("'")
    elif match[2]:  # Accessing the "string" group
        variable_value = match[2].strip("'")  # Extracting the string value
    else:
        variable_value = None

    var[variable_name] = variable_value

print(var)

