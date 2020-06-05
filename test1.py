

def fun():
    for i in range(5):
        yield i
    yield None


f = fun()

while True:
    i = next(f)
    if i is None:
        break
    print(i)