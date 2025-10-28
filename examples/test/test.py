# coding:utf-8


def main():
    while True:
        try:
            score: float = float(input("Enter your score: "))
            if 100 < score < 0:
                print("Null")
            else:
                print(score)
        except ValueError:
            print("请输入数字!!!")
            continue

    return
    while True:
        try:
            print(eval(input("Enter a Number:")), end="\n")
        except Exception as e:
            print(e, end="\n")
        ...


if __name__ == '__main__':
    main()
