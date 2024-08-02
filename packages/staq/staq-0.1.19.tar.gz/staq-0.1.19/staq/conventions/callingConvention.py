
from staq.stack import Stack, StackFrame, StackCell 
from staq.function import Function, FunctionArgument
from staq.helper import *
from termcolor import colored

import re

class Register():
    def __init__(self, name, size, description):
        self.name = name
        self.size = size
        self.type = type
        self.value = None
        self.description = None


class CallingConvention():
    """
        Base Class for calling conventions
    """
    def __init__(self, name, session = None, stack = None):
        self.name = name
        self.endian = 'little'
        self.registers = {}
        self.session = session
        self.stack : Stack = stack

    def clear(self):

        for key in self.registers:
            self.registers[key].value = None


    def setInstructionPointer(self, val):
        pass

    def pop(self):
       return self.stack.pop()

    def push(self,cell):
        self.stack.push(cell)
    
    def popFrame(self):
       return self.stack.popFrame()
    
    def pushFrame(self, frame):
        self.stack.pushFrame(frame)

    def getReg(self, key):
        if key in self.registers:
            return self.registers[key].value
        
        return None
    
    def setReg(self,key, value):

        if key in self.registers:
            self.registers[key].value = value

    def leave(self):

        if self.stack.currentFrame:
            while self.stack.currentFrame.length() > 1:
                self.stack.pop()
            
            while self.stack.currentFrame.cells[0].size > 1:
                self.stack.pop()


    def ret(self):
        word = self.stack.pop()


        if word and word.value:
            self.jmp( word.value)
        else:
            self.jmp('???')

    def markArgs(self): 

        self.stack.argMarks = {}

        if self.stack.currentFrame and self.stack.currentFrame.function:
            func = self.stack.currentFrame.function

            pointer = self.stack.currentFrame.basePointer
            pointer+= 1 #skip the return address
            for i in range(len(func.args)):
                
                self.stack.argMarks[pointer] = func.args[i].name
                pointer += func.args[i].size



    def jmp(self, val):
        self.setInstructionPointer(val)

        offset = 0

        if val.startswith('<') and val.endswith('>'):
            val = val[1:-1]

        val = val.strip()

        if '+' in val:
            
            val, offset = val.split('+')


        if self.stack.currentFrame and self.stack.currentFrame.function and self.stack.currentFrame.function.name == val:
            pass 
        else:
            lastWord = self.stack.pop()
            func = self.session.functions.get(val, Function(val))
            self.stack.pushFrame(StackFrame(val,func))
            cell = StackCell('ret', [lastWord])

            self.stack.push(cell)

        self.markArgs()

    def updateRegs(self):
        self.setReg('esp', self.stack.pointer)


    def registersToAnsi(self, width = 30, color='yellow'):

        #  ┌───────────────────────────────────┐
        #  │ esp: <value>                      │
        #  │ ebp: <value>                      │
        #  │ eax: <value>                      │
        #  │ ebx: <value>                      │
        #  └───────────────────────────────────┘

        self.updateRegs()

        #get the max length of the register names
        maxNameLength = 0
        for key in self.registers:
            if len(key) > maxNameLength:
                maxNameLength = len(key)
        
        maxValLength =  width - (maxNameLength + 5)

        out = colored(f"┌{'─' * maxNameLength}{'─' * (maxValLength +5)}┐\n", color)
        for key in self.registers:
            if self.registers[key].value:

                if isinstance(self.registers[key].value, int):
                    strVal = hex(self.registers[key].value)
                else:
                    strVal = str(self.registers[key].value)

                truncVal = strVal.ljust(maxValLength)[:maxValLength]
                out += colored(f"│ {key.rjust(maxNameLength)} : {truncVal} │\n", color)

        out += colored(f"└{'─' * maxNameLength}{'─' * (maxValLength + 5)}┘\n", color)

        return out


    def call(self, callLine):


        regex = re.compile(r"(\S.*?)\((.*?)\)")

        match = regex.match(callLine)

        func : Function = None

        if match:

            functionName = match.group(1)

            args = match.group(2)

        else:
            functionName = callLine
            args = ""

        if args.strip() == "":
            args = []
        else:
            argStr = match.group(2)
            args = splitWithEscapes(argStr,',')


        # If the function does not exist, create it and assume all args are ints
        if functionName not in self.session.functions:
            newFunction = Function(functionName)

            for i in range(len(args)):
                newFunction.addArgument(FunctionArgument('int',f'arg{i+1}'))

            self.session.functions[functionName] = newFunction

        func  = self.session.functions[functionName]
        
        for i in reversed(range(len(args))):
            label = f'arg{i+1}'
            if i < len(func.args) and func.args[i].name: 
                label = f"{func.args[i].name}"
            

            cell = StackCell(  label, [args[i].strip()])
            self.stack.push(cell)

        currentFunction = self.session.getCurrentFunction()

        
        retCell = StackCell('ret', ['<???>'])
        if currentFunction:

            if isinstance(currentFunction, Function):
                
                retCell.setWords(f'<{currentFunction.name}+??>')
            else:
                retCell.setWords(f'<{currentFunction}+??>')

        self.stack.push(retCell)

        self.jmp(functionName)

        if func:
            for local in func.locals:
                cell = self.session.tryParseLocalVar(local)
                if cell:
                    self.stack.push(cell)


        

    