#!/usr/bin/env python3
# coding: utf-8
# Author: lxm
# Created on 2017.06.21

'''程序员计算器程序
    Windows10自带的计算器太弱爆了，尤其是程序员模式，简直无法使用。
    为此利用Python自己开发一个简易的计算器。
'''

import os
import sys
import math
from math import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QMenu, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt5 import QtCore
from PyQt5 import uic
from collections import OrderedDict

if getattr(sys, 'frozen', False):
    APP_DIR = sys._MEIPASS
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
uifile = APP_DIR + '/calculator.ui'

Ui_MainWindow, QtBaseClass = uic.loadUiType(uifile)


class Calculator(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(u'程序员计算器')
        self._addButtons()
        # lineEdit回车事件响应
        self.lineEdit.returnPressed.connect(self._lineEdit_enterPressed)
        self._lineEdit_enter_mark = False  # 回车标志

        # 菜单栏-about点击事件响应
        self.actionabout.triggered.connect(self._about)
        # 菜单栏-help点击事件响应
        self.actionhelp.triggered.connect(self._help)

    def _addButtons(self):
        '''添加按键
        '''
        # 生成0~F字符
        symbol_hex = [hex(x).replace('0x', '').upper() for x in range(0, 16)]

        # 运算符号
        # symbol_opt=('x','+','-','*','/','^','<<','>>','(',')','DEL','=')
        symbol_dict=OrderedDict()
        symbol_dict['x']= u'十六进制标志，0x'
        symbol_dict['b']= u'二进制标志，0b'
        symbol_dict['o']= u'八进制标志,0o'
        symbol_dict['+']= u'加'
        symbol_dict['-']= u'减'
        symbol_dict['*']= u'乘'
        symbol_dict['/']= u'除'
        symbol_dict['^']= u'幂'
        symbol_dict['<<']= u'左移'
        symbol_dict['>>']= u'右移'
        symbol_dict['(']= u'左括号'
        symbol_dict[')']= u'右括号'
        symbol_dict['DEL']= u'删除'
        symbol_dict['=']= u'结果'

        # 所有的符号集合
        symbols = tuple(symbol_hex) + tuple(symbol_dict.keys())

        # 按键颜色样式
        qss_dict = {
            'normal': '''QPushButton{background-color:#00688B;border:none;color:#eff0f1;font-size:24px;} 
                        QPushButton:hover{background-color:#333333;}''',
            'red': '''QPushButton{background-color:#D35400;border:none;color:#ffffff;font-size:24px;} 
                        QPushButton:hover{background-color:#333333;}''',
            'green': '''QPushButton{background-color:#16A085;border:none;color:#ffffff;font-size:24px;} 
                        QPushButton:hover{background-color:#333333;}''',
        }

        for i, name in enumerate(symbols):
            button = QPushButton(name)
            if name == 'DEL':
                button.setStyleSheet(qss_dict['red'])
            elif name == '=':
                button.setStyleSheet(qss_dict['green'])
            else:
                button.setStyleSheet(qss_dict['normal'])

            button.clicked.connect(self._onButton)
            if name in symbol_hex:
                # 十进制/十六进制数值
                symbol_dict[name] = u'十进制/十六进制数'

            button.setToolTip(symbol_dict[name])
            # if name >='A' and name <='F':
            #     button.setEnabled(False)

            COL_NUM = 5  # 每行的列数
            row = i / COL_NUM  # 行
            col = i % COL_NUM  # 列
            self.gridLayout.addWidget(button, row, col)

    def _onButton(self):
        '''按键动作'''
        isResult = False  # 结果标志

        if self._lineEdit_enter_mark:
            self._lineEdit_enter_mark = False  # 清除回车标志
            symbol = '='
        else:
            sender = self.sender()
            # 记录该按键的符号
            symbol = sender.text()
        editText = self.lineEdit.text()
        if symbol == 'DEL':
            # 删除
            editText = editText[:-1]
        elif symbol == '=':
            isResult = True
            # 更新表达式

            # 计算结果
            if editText:
                result_num, result_str = self.cal(editText)
                self.label.setText(u'结果：' + editText + '=' + result_str)

                result = int(result_num)
                label = u'十进制：' + str(result) + u' 二进制: ' + bin(result) + \
                    u' 十六进制: ' + hex(result) + u' 八进制: ' + oct(result)
                self.lineEdit_convert.setText(label)
                self.lineEdit_convert.setToolTip(label)

        elif symbol in ('x', 'b', 'o'):
            # 进制标志，自动补充0
            editText = editText + '0' + symbol
        else:
            editText = editText + symbol

        self.lineEdit.setText(editText)

    def cal(self, strExp):
        '''计算
        @strExp:
            需要计算的字符表达式，string类型
        @return:
            计算的结果，Tuple类型 (number,str)
        '''
        # 删除无效的空格
        strExp = strExp.replace(' ', '')
        # 指数运算，替换为python识别的模式
        strExp = strExp.replace('^', '**')

        try:
            result = eval(strExp)
            ret = (result, str(result))
        except ZeroDivisionError:
            QMessageBox.critical(self, u'错误', u'除零！')
            ret = (0, 'Error')
        except:
            QMessageBox.critical(self, u'错误', u'表达式错误！')
            ret = (0, 'Error')
        return ret

    def _lineEdit_enterPressed(self):
        '''输入框中回车键按下事件'''
        self._lineEdit_enter_mark = True  # 标志回车键按下
        self._onButton()

    def _about(self):
        '''关于信息单击事件'''
        QMessageBox.about(
            self, u'关于', u'<h3><font color="blue">程序员计算器 v 0.5.1 <br> By lxm</font></h3>')

    def _help(self):
        '''帮助信息点击事件'''
        h = Help(self)
        
        h.show()

        # QMessageBox.about(self,'帮助',text)


class Help(QDialog):
    '''自定义帮助弹出窗'''

    def __init__(self, parent=None):
        super(Help, self).__init__(parent)
        self.setWindowTitle(u'帮助信息，详细请查看Python.math帮助文件')
        # self.setWindowFlags(QtCore.Qt.WindowTitleHint)
        d = {
            'acos': u'acos(x),反余弦',
            'acosh': u'acosh(x),反双曲余弦',
            'asin': u'asin(x),反正弦',
            'asinh': u'asinh(x),反双曲正弦',
            'atan': u'atan(x),反正切',
            'atan2': u'atan2(x)，反正切',
            'atanh': u'atanh(x),反双曲正切',
            'ceil': u'ceil(x),取大于等于x的最小整數',
            'copysign': u'copysign(x,y),返回与 y 同号的 x 值',
            'cos': u'cos(x),余弦',
            'cosh': u'cosh(x),双曲余弦',
            'degrees': u'degrees(x),ｘ(弧长) 转成角度',
            'e': u'%s' % e ,
            # 'erf': u' e^x',
            # 'erfc': u'',
            'exp': u'exp(x),等价于e^x',
            'expm1': u'expm1(x)，等价于e^x-1',
            'fabs': u'fabs(x),取x的绝对值',
            'factorial': u'factorial(x),取x的阶乘',
            'floor': u'≦ x 的最大整数，floor(5.6)=5',
            'fmod': u'fmod(x,y),x对y取模的余数',
            # 'frexp': u'',
            'fsum': u'fsum((x1,x2,x3,x4,x5,...,Xn)),取所有元素（X1～Xn）的和',
            # 'gamma': u'',
            'gcd': u'gcd(x,y)，取x和ｙ的最大公约数',
            'hypot': u'hypot(x,y)，返回sqrt(x^2+y^2',
            # 'inf': u'',
            # 'ldexp': u'',
            # 'lgamma': u'',
            'log': u'log(x,a)，以a为底的对数，默认a=e',
            'log10': u'log(x,10)',
            # 'log1p': u'',
            'log2': u'以２为底的对数值',
            # 'modf': u'',
            # 'nan': u'',
            'pi': u'%s' % pi,
            'pow': u'pow(x,y)，x的y次方，等价于x^y',
            'radians': 'radians(x)，将角度x转换成弧长',
            'sin': u'sin(x)，取ｘ的正弦值',
            'sinh': u'sinh(x)，取x的双曲正玄值',
            'sqrt': u'sqrt(x)，对ｘ开根号，x>=0',
            'tan': u'tan(x)，取ｘ的正切值',
            'tanh': u'tanh(x),双曲正切',
            # 'tau': u'%s'%(tau if tau else "不支持"),
            'trunc': u'trunc(x)，对ｘ取整'
        }
        self.table = QTableWidget(len(d), 2)  # 行，列数目,行数必须>=实际行数
        self.table.setHorizontalHeaderLabels([u'名称', u'说明'])
        self.table.horizontalHeader().setStretchLastSection(True)

        i = 0
        for name,value in d.items():
            # 设置第一列
            item_name = QTableWidgetItem(name)
            self.table.setItem(i, 0, item_name)
            # 设置第二列
            item_value = QTableWidgetItem(value)
            self.table.setItem(i, 1, item_value)
            i += 1
            

        self.table.setRowCount(i)

        layout = QHBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    mainwindow = Calculator()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
