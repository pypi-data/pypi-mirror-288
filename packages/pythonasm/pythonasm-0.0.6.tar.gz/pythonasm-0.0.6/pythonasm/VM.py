import tkinter as tk
import re
import os
from pynput import keyboard
from tkinter import scrolledtext

class CustomTerminal:
    def __init__(self):
        master = tk.Tk()

        self.master = master
        self.master.title("虚拟机VMHan1.0(Ctrl+Alt释放鼠标)")
        self.master.geometry("900x500+200+200")
        self.master.configure(bg='black')
        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=40, height=10, bg='black', fg='white', cursor="none")
        self.text_area.pack(expand=True, fill=tk.BOTH)




variables = {'ax': 0, 'bx': 0, 'cx': 0, 'dx': 0, 'ah': 0, 'al': 0, 'ds': 0, 'es': 0, 'ss': 0, 'sp': 0}

# 定义按键监听器
def on_press(key):
    try:
        # 获取按键的 ASCII 编码
        variables['al'] = ord(key.char)
    except AttributeError:
        if key == keyboard.Key.space:  # 空格
            variables['al'] = ord(' ')
        elif key == keyboard.Key.enter:  # 回车
            variables['al'] = ord('\n')
        elif key == keyboard.Key.shift:  # shift 键
            variables['al'] = ord('<Shift>')
        elif key == keyboard.Key.ctrl:  # ctrl 键
            variables['al'] = ord('<Ctrl>')
        elif key == keyboard.Key.alt:  # alt 键
            variables['al'] = ord('<Alt>')
        elif key == keyboard.Key.backspace:  # backspace 键
            variables['al'] = ord('\b')
        elif key == keyboard.Key.esc:  # esc 键
            variables['al'] = 27
        elif key == keyboard.Key.return_:  # return 键
            variables['al'] = ord('\r')
        else:
            variables['al'] = 0  # 其他非字符键设为 0
    # 停止监听
    return False

def add(a, b): return a + b


def subtract(a, b): return a - b


def multiply(a, b): return a * b


def divide(a, b): return a / b if b != 0 else (print("Error:Divisor cannot be 0."), a)[1]


def operation(line):
    add_pattern = re.compile(r'add\s+(\w+),\s*(\w+)')
    sub_pattern = re.compile(r'sub\s+(\w+),\s*(\w+)')
    mul_pattern = re.compile(r'mul\s+(\w+),\s*(\w+)')
    div_pattern = re.compile(r'div\s+(\w+),\s*(\w+)')

    for pattern, operation in [(add_pattern, add), (sub_pattern, subtract), (mul_pattern, multiply), (div_pattern, divide)]:
        match = pattern.match(line)
        if match:
            operand1, operand2 = match.groups()
            if operand1 in variables:
                operand2_value = variables.get(operand2, None)
                if operand2_value is not None:
                    variables[operand1] = operation(variables[operand1], operand2_value)
                else:
                    try:
                        operand2_value = int(operand2)
                        variables[operand1] = operation(variables[operand1], operand2_value)
                    except ValueError:
                        print(f"Error:Operand {operand2} is not defined.")
            else:
                print(f"Error:Operand {operand1} is not defined.")
            return


def check(app = CustomTerminal()):
    if variables['ah'] == 0x0E:
        if isinstance(variables['al'], int):
            if 0 <= variables['al'] <= 127:
                variables['al'] = chr(variables['al'])
        app.text_area.insert(tk.END, variables['al'])

    elif variables['ah'] == 0x00:
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        listener.join()



def VMasm(filename):
    if not os.path.exists(filename):
        print(f"Error:File {filename} does not exist.")
        return


    app = CustomTerminal()
    app.text_area.insert(tk.END, f"VMasm BIOS (PCI)\nThis VGA/VBE Bios is released under the GNU LGPL\nIt is {filename}\n")
    app.master.mainloop()

    with open(filename, 'r') as file:
        lines = file.readlines()

    mov_reg_to_const_pattern = re.compile(r'mov\s+(\w+),\s*(\d+)')
    mov_reg_to_reg_pattern = re.compile(r'mov\s+(\w+),\s*\[?(\w+)\]?\s*')
    db_pattern = re.compile(r'(\w+)\s+db\s+"([^"]*)"')

    for line in lines:
        line = line.strip()

        if "[bits 16]" in line and "[org 0x7C00]" in line:


            match = mov_reg_to_const_pattern.match(line)
            if match:
                reg, value = match.groups()
                try:
                    variables[reg] = int(value)
                except ValueError:
                    print(f"Error:Cannot convert {value} to an integer.")
                continue

            match = mov_reg_to_reg_pattern.match(line)
            if match:
                dest, src = match.groups()
                if src in variables:
                 variables[dest] = variables[src]
                else:
                    print(f"Warning: Source register {src} is not defined.")
                continue

            match = db_pattern.match(line)
            if match:
                label, value = match.groups()
                variables[label] = value.strip('"')
                continue

            operation(line)
            if re.search(r"nt .*(?:10h|0x10)", line):
                check()




