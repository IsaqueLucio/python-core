from typing import Optional

def add(a: float, b: float) -> float:
    result_add = a + b
    print(f"{a} + {b} = {result_add}")
    return result_add

def subtract(a: float, b: float) -> float:
    result_subtract = a - b
    print(f"{a} - {b} = {result_subtract}")
    return result_subtract

def multiply(a: float, b: float) -> float:
    result_multiply = a * b
    print(f"{a} x {b} = {result_multiply}")
    return result_multiply

def divide(a: float, b: float) -> Optional[float]:
    if b == 0:
        print("Division by zero is undefined.")
        return
    result_div = a / b
    print(f"{a} / {b} = {result_div}")
    return result_div

def main():
    operation = ("+", "-", "x", "/", "out")

    while True:
        print("\n" + "=" * 30)
        print("        SIMPLE CALCULATOR")
        print("=" * 30)
        print("[ + ] Addition")
        print("[ - ] Subtraction")
        print("[ x ] Multiplication")
        print("[ / ] Division")
        print("[ out ] Exit")
        print("=" * 30)

        value_1 = input("Value 01: ")

        try:
            value_1 = float(value_1)
        except ValueError:
            print("[VALUE_01 ERROR] Float value only.")
            continue

        type_op = input("Enter the desired option: ")

        if type_op not in operation:
            print('Only [ + ; - ; x ; / ] or "out" are options available.')
            continue

        if type_op == "out":
            print("\nClosing program...")
            break

        value_2 = input("Value 02: ")

        try:
            value_2 = float(value_2)
        except ValueError:
            print("[VALUE_02 ERROR] Float value only.")
            continue

        print("-" * 30)

        match type_op:
            case "+":
                add(value_1, value_2)
            case "-":
                subtract(value_1, value_2)
            case "x":
                multiply(value_1, value_2)
            case "/":
                divide(value_1, value_2)

if __name__ == "__main__":
    main()