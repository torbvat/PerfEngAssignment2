import re

input_str = "1. f4 {+0.00/1 0s} d5 {+0.00/1 0s} 2. b3 {+0.00/1 0s} Bg4 {+0.00/1 0s} 3. Bb2 {+0.00/1 0s} Nc6 {+0.00/1 0s} 4. h3 {+0.00/1 0s} Bh5 {+0.00/1 0s} 5. g4 {+0.00/1 0s} Bg6 {+0.00/1 0s} 6. Nf3 {+0.00/1 0s} h5 {+0.00/1 0s} 7. g5 {+0.00/1 0s} e6 {+0.00/1 0s} 8. e3 {+0.00/1 0s} Nge7 {+0.00/1 0s} 9. Bb5 {-0.36/32 45s} a6 {(h4) +0.59/28 20s} 10. Bxc6+ {(Bxc6) -0.24/30 10s} Nxc6 {(Nxc6) +0.62/28 18s} 0-1 "

result = re.findall(r'\S+', re.sub(r'{.*?}', '', input_str))

print(result)
print(input_str.endswith("1-0") or input_str.endswith("0-1") or input_str.endswith("1/2-1/2"))
liste = [""]
print(liste)