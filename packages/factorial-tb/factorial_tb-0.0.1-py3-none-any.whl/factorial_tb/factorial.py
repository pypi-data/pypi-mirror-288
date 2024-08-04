def factorial(i: int) -> int:
    if type(i) == int:
        if 0 <= i:
            if i == 0:
                return 1
            else:
                return i * factorial(i - 1)
        else:
            raise ValueError()
    else:
        raise TypeError()

if __name__ == "__main__":
    print(factorial(3))

