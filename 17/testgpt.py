import itertools

def generate_sequence():
  x = 1
  k = 1
  while True:
    yield x
    x += k
    if x % 7 == 0:
      k += 1

print([next(generate_sequence()) for _ in range(2023)])