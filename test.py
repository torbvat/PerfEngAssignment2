import re

string = "1. f4 {+0.00/1 0s} d5 {+0.00/1 0s}"
pattern = r"\s+(?=[^{}]*(?:\{|$))"

result = re.split(pattern, string)

print(result)