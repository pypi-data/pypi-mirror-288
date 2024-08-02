from keystone import *
from capstone import *

assembly_instructions = []

def mov(reg1,reg2):
    assembly_instructions.append(f"mov {reg1},{reg2}")

def db(value):
    assembly_instructions.append(str(value))

def add(reg1, reg2):
    assembly_instructions.append(f"add {reg1}, {reg2}")

def inc(reg):
    assembly_instructions.append(f"inc {reg}")

def int_(vector):
    assembly_instructions.append(f"int {vector}")

def jmp(label):
    assembly_instructions.append(f"jmp {label}")

def jne(label):
    assembly_instructions.append(f"jne {label}")

def je(label):
    assembly_instructions.append(f"je {label}")

def label(label):
    assembly_instructions.append(f"{label}:")

# 创建汇编器和反汇编器引擎
ks = Ks(KS_ARCH_X86, KS_MODE_64)
engine = Cs(CS_ARCH_X86, CS_MODE_64)


def display():
    for instruction in assembly_instructions:
        try:
            # 汇编指令，获取机器码
            encoding, count = ks.asm(instruction)
            # 反汇编机器码
            for asm in engine.disasm(bytes(encoding), 0x1000):

                print(f"{instruction:20};0x{bytes(asm.bytes).hex().upper()}")

        except KsError:
            print(f"db {instruction:17};{hex(int(instruction))}")

