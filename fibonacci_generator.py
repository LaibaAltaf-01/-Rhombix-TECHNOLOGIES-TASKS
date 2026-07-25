"""
Task 1: Fibonacci Generator
----------------------------
The Fibonacci series is a sequence where each number is the sum of the
two preceding numbers, defined by a mathematical recurrence relationship.

F(0) = 0
F(1) = 1
F(n) = F(n-1) + F(n-2), for n > 1
"""


def fibonacci_generator(n):
    """
    Generator function that yields the first n numbers
    of the Fibonacci sequence.
    """
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1


def fibonacci_infinite():
    """
    Generator function that yields Fibonacci numbers
    indefinitely (no fixed limit).
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def main():
    print("=" * 40)
    print("FIBONACCI GENERATOR")
    print("=" * 40)

    try:
        n = int(input("Enter how many Fibonacci numbers to generate: "))
    except ValueError:
        print("Please enter a valid integer.")
        return

    if n <= 0:
        print("Please enter a positive integer.")
        return

    print(f"\nFirst {n} Fibonacci numbers:")
    result = list(fibonacci_generator(n))
    print(result)


if __name__ == "__main__":
    main()
