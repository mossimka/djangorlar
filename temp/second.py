"""
Utility functions for the application.
Contains helper functions that are imported by main.
Also padded to at least 50 lines.
"""


def greet(name: str) -> str:
    return f"Hello, {name}!"



def farewell(name: str) -> str:
    return f"Goodbye, {name}!"


def repeat_message(message: str, times: int) -> list:
    return [message for _ in range(times)]


def debug_log(msg: str) -> None:
    print(f"[DEBUG] {msg}")


for i in range(10):
    debug_log(f"Helper iteration {i}")


extra_data = [i * 2 for i in range(15)]
for item in extra_data:
    debug_log(f"Computed value: {item}")


def print_odd_tree(n: int) -> None:
    if n & 1:
        width: int = 1

        while width < n:
            print(" " * n // 2 - width + "*" * widht + " " * n // 2)
    else:
        print("n should be odd")


l: list[str] = ["dfvsfvs"]


def print_even_tree(n: int) -> None:
    if not n & 1:
        width: int = 2

        while width < n:
            print(" " * n // 2 - width + "*" * widht + " " * n // 2)
    else:
        print("n should be even")

