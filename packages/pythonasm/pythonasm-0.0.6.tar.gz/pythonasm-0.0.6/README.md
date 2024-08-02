# pythonasm Library
I. Overview
This is a Python library that contains a series of functions related to data processing, assembly virtual machines, conversion of machine codes, and operations. It can simulate the input and output of an assembler, convert machine codes and use virtual machines. The author is Lin Honghan, a sixth-grade primary school student in China. The pypi account is linhhanpy, and the gitee account is lin. It was made during the summer vacation out of boredom.
More functions will be updated in the future and use real assembly instructions.
II. Main Functions
- Defined basic mathematical operation functions: add (addition), sub (subtraction), mul (multiplication), div (division, handling the case where the divisor is 0).
- Handles instructions such as db, mov, etc.
- operation function: Matches and performs corresponding operation operations according to specific instruction patterns.
- check function: Used for checking specific conditions.
- asm function: Can read the specified file, parse the instructions in it, and perform corresponding processing.

III. Usage Method

After importing the relevant modules, you can call the functions within for usage.
IV. Dependent Libraries
 - `re`: Used for regular expression operations.
 - `os`: Used for file and directory-related operations.
 - `keystone`：Used for compilation
 - `capstone`：Used for compilation
 - `tkinter`:for window
 - `pynput`:for keyboard

V. Sample Code
```python
import pythonasm.main,pythonasm.VM.VMasm
from pythonasm.asm import*
pythonasm.VM.VMasm("asm_VM_file.asm")
mov("ax", 1)
add("ax", 2)
inc("ax")
db(0x90)  # NOP
int_(0x80)
jmp(0x90)
display()
pythonasm.main.asm('pyasm.asm')
```
```asm
#pyasm.asm
msg db "abc"
mov ax,3
mov bx,0
mov cx,msg
mov dx,3
int 80h
mov ax,4
mov bx,1
mov dx,3
int 80h
```
```asm_VM_file
#asm_VM_file.asm

[bits 16]
[org 0x7C00]

; 初始化段寄存器
mov ax, 0x07C0
mov ds, ax
mov es, ax
mov ss, ax
mov sp, 0x7C00

; 打印"Hello, MyOS!"
mov ah, 0x0E ; BIOS的Teletype功能
mov al, 'H'
int 0x10
mov al, 'e'
int 0x10
mov al, 'l'
int 0x10
mov al, 'l'
int 0x10
mov al, 'o'
int 0x10
mov al, ','
int 0x10
mov al, ' '
int 0x10
mov al, 'M'
int 0x10
mov al, 'y'
int 0x10
mov al, 'O'
int 0x10
mov al, 'S'
int 0x10
mov al, '!'
int 0x10
mov al, 0x0D ; 回车
int 0x10
mov al, 0x0A ; 换行
int 0x10
mov ah, 0x00 ; BIOS键盘服务 - 读取键盘状态
int 0x10 ; 调用BIOS中断
mov ah, 0x0E ; 准备输出字符
int 0x10 ; 输出字符（此时AL已由BIOS设为键值）
jmp keyboard_input ; 循环等待下一个按键


```






```input
#command_input
123
```
```command
#command_out
mov ax,1            ;0x66B80100
add ax, 2           ;0x6683C002
inc ax              ;0x66FFC0
db 144              ;0x90
int 128             ;0xCD80
jmp 144             ;0xE98B000000
123
```
VI. Copyright Statement

This library is open source, but the author and source must be indicated. The final interpretation right belongs to Lin Honghan.
# pythonasm 库

 一、概述
这是一个包含了一系列与数据处理和汇编虚拟机和转换机器码和操作相关功能的 Python 库，能模拟汇编器的输入输出，转换机器码，作者为中国六年级小学生林泓翰pypi账号linhhanpy，gitee账号lin，暑假无聊做的。
以后会更新更多功能，使用真正的汇编指令。

 二、主要功能（main）
 - 定义了基本的数学运算函数：`add`（加法）、`sub`（减法）、`mul`（乘法）、`div`（除法，处理除数为 0 的情况）。
 - 处理`db`，`mov`等指令。
 - `operation` 函数：根据特定的指令模式匹配并执行相应的运算操作。
 - `check` 函数：用于进行特定条件的检查。
 - `asm` 函数：能够读取指定文件，解析其中的指令并进行相应处理。
 - `display`函数：显示汇编和机器码
 - `VMasm`函数：识别汇编指令的虚拟机

 三、使用方法
导入相关模块后，即可调用其中的函数进行使用。

 四、依赖库
 - `re` ：用于正则表达式操作。
 - `os` ：用于文件和目录相关操作。
 - `keystone`：用于编译
 - `capstone`：用于编译
 -  - `tkinter`:显示窗口
 - `pynput`:键盘检测

 五、示例代码
```python
import pythonasm.main, pythonasm.VM.VMasm
from pythonasm.asm import*
pythonasm.VM.VMasm("asm_VM_file.asm")
mov("ax", 1)
add("ax", 2)
inc("ax")
db(0x90)  # NOP
int_(0x80)
jmp(0x90)
display()
pythonasm.main.asm('pyasm.asm')
```
```asm
#pyasm.asm
msg db "abc"
mov ax,3
mov bx,0
mov cx,msg
mov dx,3
int 80h
mov ax,4
mov bx,1
mov dx,3
int 80h
```
```asm_VM_file
#asm_VM_file.asm

[bits 16]
[org 0x7C00]

; 初始化段寄存器
mov ax, 0x07C0
mov ds, ax
mov es, ax
mov ss, ax
mov sp, 0x7C00

; 打印"Hello, MyOS!"
mov ah, 0x0E ; BIOS的Teletype功能
mov al, 'H'
int 0x10
mov al, 'e'
int 0x10
mov al, 'l'
int 0x10
mov al, 'l'
int 0x10
mov al, 'o'
int 0x10
mov al, ','
int 0x10
mov al, ' '
int 0x10
mov al, 'M'
int 0x10
mov al, 'y'
int 0x10
mov al, 'O'
int 0x10
mov al, 'S'
int 0x10
mov al, '!'
int 0x10
mov al, 0x0D ; 回车
int 0x10
mov al, 0x0A ; 换行
int 0x10
mov ah, 0x00 ; BIOS键盘服务 - 读取键盘状态
int 0x10 ; 调用BIOS中断
mov ah, 0x0E ; 准备输出字符
int 0x10 ; 输出字符（此时AL已由BIOS设为键值）
jmp keyboard_input ; 循环等待下一个按键


```
```input
#command_input
123
```
```command
#command_out
mov ax,1            ;0x66B80100
add ax, 2           ;0x6683C002
inc ax              ;0x66FFC0
db 144              ;0x90
int 128             ;0xCD80
jmp 144             ;0xE98B000000
123
```
六、版权声明
本库开源，但需标明作者和出处，最终解释权归林泓翰所有。

