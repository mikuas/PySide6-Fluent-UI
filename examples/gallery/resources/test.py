# coding:utf-8
import os


def main():
    with open("./test.txt", "w", encoding="utf-8") as f:
        for item in os.listdir("./controls"):
            f.write(f"<file>controls/{item}</file>\n")


if __name__ == '__main__':
    main()