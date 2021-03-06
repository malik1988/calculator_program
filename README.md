# calculator_program 程序员计算器
A easy calculator for programmers.

## 设计初衷
windows 10 自带的计算器超级难用，特别是“程序员模式”，简直是不能使用。只能简单的多进制数值转换，无法进行 十进制与十六进制数值加减乘除等运算。

因此，自己利用Python做了个简易的“程序员计算器”。

## 运行环境
- Python3 
- PyQt5

## 现有功能
- 十进/十六进制/八进制制数 基本算数运算
- 十进制/十六进制/八进制数混合运算
- 指数运算，移位运算

## 隐藏功能
- 支持键盘直接输入表达式进行计算
    示例： 0x123+123/3*(2<<2)+sin(10)
- 支持python math库中所有函数表达式运算：
    示例：sin(120) , log(121) , sqrt(12) , degrees(10)


## 打包
### 程序支持pyinstaller打包
```bash
pyinstaller  calculator.spec
```

### 已经打包好的文件在dist目录
直接运行 dist/calculator

## 截图
![1](./screenshot/screenshot.png)
![2](./screenshot/screenshot1.png)
![3](./screenshot/screenshot2.png)