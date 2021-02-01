import time

x = 0

start = time.time()
print(start)
while x < 10000000:
    x += 1

end = time.time()
print(end)
print(end-start)