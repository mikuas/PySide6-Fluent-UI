# coding:utf-8

# 程序名称:     判断成绩是否及格
# 程序功能:     判断输入的成绩是否及格,如未及格,计算差多少分
# 开发者:       20258672刘志刚


score = eval(input("请输入张山的Python分数: "))
if score > 60:
    print("张山的Python成绩及格")
else:
    print(f"张山的Python成绩不及格\n还差{60 - score}分及格")
