# coding:utf-8

# 程序名称:     计算机票价格
# 程序功能:     通过月份,仓位计算机票价格
# 开发者:       20258672刘志刚

price = 1000
discount_price = 0
print("请输入您出行的月份: ")
month = int(input())
print("请输入您选择头等舱还是经济仓, 头等舱输入1, 经济仓输入2")
cabin_class = int(input())
if month >= 4 and month <= 10:
    if cabin_class == 1:
        discount_price = price * 0.9
    else:
        discount_price = price * 0.6
else:
    if cabin_class == 1:
        discount_price = price * 0.5
    else:
        discount_price = price * 0.4
print(f"您的机票价格为: {discount_price}")















def main():
    price: int = 1000
    discount_price: int = 0
    month = int(input("请输入您出行的月份: "))
    cabin_class = input("请输入您选择头等舱还是经济仓, 头等舱输入1, 经济仓输入2")
    if month >= 4 and month <= 10:
        if cabin_class == 1:
            discount_price = price * 0.9
        else:
            discount_price = price * 0.6
    else:
        if cabin_class == 1:
            discount_price = price * 0.5
        else:
            discount_price = price * 0.4
    print(f"您的机票价格为: {discount_price}")
