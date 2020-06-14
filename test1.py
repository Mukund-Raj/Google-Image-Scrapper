import json

class user:
    def __init__(self):
        print('object created')
        self.arr = [1,2,3]

    def prints(self):
        print(self.arr)


if __name__ == "__main__":
    u=user()
    print(u.__dict__)
    print(json.dumps(u.__dict__))