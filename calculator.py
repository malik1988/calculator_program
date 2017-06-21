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
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QLineEdit
from PyQt5 import QtCore
from PyQt5 import uic

uifile = os.path.split(os.path.realpath(__file__))[0] + '/calculator.ui'

Ui_MainWindow, QtBaseClass = uic.loadUiType(uifile)


class Calculator(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(u'程序员计算器')
        self._addButtons()

    def _addButtons(self):
        '''
        '''
        # 生成0~F字符
        symbol_hex = [hex(x).replace('0x', '').upper() for x in range(0, 16)]

        # 运算符号
        # symbol_opt=('x','+','-','*','/','^','<<','>>','(',')','DEL','=')
        symbol_dict = {
            'x': u'十六进制标志，0x',
            'b': u'二进制标志，0b',
            'o': u'八进制标志,0o',
            '+': u'加',
            '-': u'减',
            '*': u'乘',
            '/': u'除',
            '^': u'幂',
            '<<': u'左移',
            '>>': u'右移',
            '(': u'左括号',
            ')': u'右括号',
            'DEL': u'删除',
            '=': u'结果'
        }

        # 所有的符号集合
        symbols = tuple(symbol_hex) + tuple(symbol_dict.keys())

        for i, name in enumerate(symbols):
            button = QPushButton(name)
            button.clicked.connect(self._onButton)
            if name in symbol_hex:
                # 十进制/十六进制数值
                symbol_dict[name] = u'十进制/十六进制数'

            button.setToolTip(symbol_dict[name])
            # if name >='A' and name <='F':
            #     button.setEnabled(False)

            COL_NUM = 6  # 每行的列数
            row = i / COL_NUM  # 行
            col = i % COL_NUM  # 列
            self.gridLayout.addWidget(button, row, col)

    def _onButton(self):
        '''按键动作'''
        isResult=False #结果标志

        sender = self.sender()

        # 记录该按键的符号
        symbol = sender.text()
        editText = self.lineEdit.text()
        if symbol == 'DEL':
            #删除
            editText = editText[:-1]
        elif symbol == '=':
            isResult=True
            #更新表达式

            #计算结果
            if editText:
                result_num,result_str = self.cal(editText)    
                self.label.setText(u'结果：'+editText+'='+result_str)

                result=int(result_num)   
                label=u'十进制：'+str(result)+u' 二进制: '+bin(result)+u' 十六进制: '+hex(result)+u' 八进制: '+oct(result)
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
        #指数运算，替换为python识别的模式
        strExp=strExp.replace('^','**')
        #函数运算，替换为math.xxx
                
        for f in dir(math):
            if f+'(' in strExp: #f+'('确保f为一个函数
                strExp=strExp.replace(f,'math.'+f)
        
        try:
            result = eval(strExp.replace('^','**'))
            ret=(result,str(result))
        except ZeroDivisionError:
            QMessageBox.information(self, u'错误', u'除零！')
            ret=(0,'Error')
        except:
            QMessageBox.information(self, u'错误', u'表达式错误！')
            ret=(0,'Error')
        return ret 



def main():
    app = QApplication(sys.argv)
    mainwindow = Calculator()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
