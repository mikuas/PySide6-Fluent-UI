# coding:utf-8
import random
import sys


class Person:

    def __init__(self):
        super().__init__()
        self._name: str = "TEST"
        self._age: int = 0

    @property
    def name(self) -> str:
        print("name getter")

        return self._name

    @name.setter
    def name(self, name: str) -> None:
        print("name setter")
        if name.strip() == "":
            raise "Names cannot be empty"

        self._name = name

    @name.deleter
    def name(self) -> None:
        print("name deleter")
        del self._name

    def __getAge(self) -> int:
        print("age getter")
        return self._age

    def __setAge(self, value: int) -> None:
        print("age setter")
        if value < 0:
            raise "age lessThan zero"

        self._age = value

    def __deleteAge(self) -> None:
        print("delete age")

        del self._age

    age = property(__getAge, __setAge, __deleteAge, "this is age property")

def personDemo():
    person: Person = Person()
    person.name = "zhangsan"
    print(person.name)

    del person.name
    try:
        print(person.name)
    except Exception:
        print("CONTINUE")

    person.age = 114
    print(person.age)

    del person.age
    try:
        print(person.age)
    except Exception:
        ...


def main():
    personDemo()


if __name__ == '__main__':
    main()