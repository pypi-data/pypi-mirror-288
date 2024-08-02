

from staq.stack import Stack, StackFrame, StackCell 
from staq.function import Function, FunctionArgument
from staq.conventions import CallingConvention, Register
from typing import List

import re

class CdeclConvention(CallingConvention):
    def __init__(self, session = None, stack = None):
        super().__init__('cdecl', session=session, stack=stack)
        self.endian = 'little'


        self.registers = {
            'eax': Register('eax', 4, 'Return Value'),
            'ecx': Register('ecx', 4, 'Arg 1'),
            'edx': Register('edx', 4, 'Arg 2'),
            'ebx': Register('ebx', 4, 'Arg 3'),
            'esp': Register('esp', 4, 'Stack Pointer'),
            'ebp': Register('ebp', 4, 'Base Pointer'),
            'esi': Register('esi', 4, 'Source Index'),
            'edi': Register('edi', 4, 'Destination Index'),
            'eip': Register('eip', 4, 'Instruction Pointer')
        }

        self.setReg('esp', hex(self.stack.pointer))
        self.setReg('eip', '???')
        self.setReg('ebp', hex(self.stack.baseAddress))

    def clear(self):

        for key in self.registers:
            self.registers[key].value = None
        
        self.setReg('esp', hex(self.stack.pointer))
        self.setReg('eip', '???')
        self.setReg('ebp', hex(self.stack.baseAddress))

    # def leave(self):

    #     if self.registers['ebp'].value and self.stack:
            
    #         esp = self.stack.pointer
    #         ebp = self.getReg('ebp')

    #         #pop everything until the prev ebp
    #         while esp < ebp:
    #             self.stack.pop()
    #             esp = self.stack.pointer

    #         prev_ebp = self.stack.pop()
    #         self.setReg("ebp",prev_ebp.value)
    #         self.setReg("esp",esp)




    def setInstructionPointer(self, val):

        self.setReg("eip", val)
    
    


        