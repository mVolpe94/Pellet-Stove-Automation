import os, re

temp_file = open("TestingEnvironment/temptest.txt")
lines = temp_file.readlines()
temp_line = lines[1]
p = re.compile(r"[t][=](\d*)")
result = p.search(lines[1])
temp = result.group(1)
temp = int(temp) / 1000
temp = 9/5 * temp + 32
print(temp)



