
from staq.conventions import CdeclConvention
from staq.stack import Stack, StackFrame, StackCell
from staq.function import Function, FunctionArgument, parseCFile
from staq.helper import splitWithEscapes
import re
import yaml
import json
import argparse

import importlib.resources as pkg_resources
import builtins



sizeDict = {
    "void": 0,
    "char": 1,
    "unsigned char": 1,
    "signed char": 1,
    "short": 2,
    "unsigned short": 2,
    "int": 4,
    "unsigned int": 4,
    "long": 4,
    "unsigned long": 4,
    "long long": 8,
    "unsigned long long": 8,
    "float": 4,
    "double": 8,
    "long double": 16,  # This can vary, but 16 bytes is a common size
    "int8": 1,
    "uint8": 1,
    "int16": 2,
    "uint16": 2,
    "int32": 4,
    "uint32": 4,
    "int64": 8,
    "uint64": 8,
    "va_list": 4,
}

def nullPrint(*args, **kwargs):
    pass

builtins.print = nullPrint

class StackSession():
    def __init__(self):
        self.stack = Stack()
        self.conv = CdeclConvention(session=self, stack = self.stack)
        self.functions = {}
        self.parser = argparse.ArgumentParser(description='Stack Visualizer', add_help=False)
        self.subparsers = None
        self.init_args()
        self.loadLibcFuntions()
        self.commands = []
        self.update = False
        self.status = ""
        self.cmdIdx = 0

    def addHistory(self,cmd):

        if self.cmdIdx < len(self.commands):
            self.commands = self.commands[:self.cmdIdx]

        self.commands.append(cmd)
        self.cmdIdx+=1

    def stepForward(self):

        if self.cmdIdx < len(self.commands):
            self.parseCommand(self.commands[self.cmdIdx], addHistory=False)
            self.cmdIdx +=1

    def stepBack(self):

        if self.cmdIdx > 0:

            self.cmdIdx -= 1
            self.stack.clear()
            
            for i in range(0,self.cmdIdx):
                self.parseCommand(self.commands[i], addHistory=False)

    def print(self,text):
        print(text)

    def refreshOutput(self):

        ansi = self.stack.toAnsi( showAddress=True)
        print(ansi)

    def loadYaml(self, obj):


        if isinstance(obj, str):
            with open(obj) as f:
                obj = yaml.safe_load(f)


        order = 'normal'

        if 'stackBase' in obj:
            self.stack.baseAddress = obj['stackBase']
        
        if 'order' in obj:
            order = obj['order']

        if 'functions' in obj:
            for func in obj['functions']:
                self.addFunction(Function.fromString(func))
    

        if 'stack' in obj:

            nodes = []
            if order == 'normal':
                nodes = reversed(obj['stack'])
            else:
                nodes = obj['stack']

            for node in nodes:
                
               if isinstance(node, dict) and 'function' in node:
                   #Create a new frame 
                   frame = StackFrame.fromObj(node, order= order)
                   self.stack.pushFrame(frame)
                   self.stack.currentFrame = None
               else:
                    cell = StackCell.fromObj(node)
                    self.stack.push(cell)
        
        self.stack.applyAddresses()


    
    def getCurrentFunction(self):

        if self.stack.currentFrame:

            if self.stack.currentFrame.function:
                return self.stack.currentFrame.function
            
        
        return None

    def addFunction(self, function):
        self.functions[function.name] = function


    def loadLibcFuntions(self):
        
        data_path = pkg_resources.files('staq.data').joinpath('libc.c')

        with open(data_path) as f:
            functions = parseCFile(f.read())
            for f in functions:
                self.addFunction(f)

        # for f in libc_functions:
        #     newFunc = Function.fromString(f)

        #     self.addFunction(newFunc)

    def parseFrame(self,words):
        
        line = " ".join(words[1:])
        self.stack.pushFrame(StackFrame(line))

    def frameCmd(self, args):
        frame = StackFrame(args.name)
        if args.color:
            frame.color = args.color
        self.stack.pushFrame(frame)

    def popCmd(self, args):

    
        if args.count and isinstance(args.count,str):
            if args.count.lower() == 'frame':
                self.stack.popFrame()
            elif args.count.lower().replace("$","") in self.conv.registers:

                word = self.stack.pop()
                self.conv.setReg(args.count.lower().replace("$",""), word.value )
            else:
                count = int(args.count)
                self.stack.pop(count)
        else:
            self.stack.pop()

    def retCmd(self, args):

        self.conv.ret()

    def jmpCmd(self, args):

        self.conv.jmp(args.address)

    def pushCmd(self, args):
        cell = StackCell()

        if args.value:

            line = " ".join(args.value)

            parts = line.split(":")

            if len(parts) > 1:
                cell.label = parts[0]

                words = parts[1].strip().split(",")
                words = [x.strip() for x in words]

                cell.setWords(words)
            else:
                words = parts[0].split(",")
                words = [x.strip() for x in words]
                cell.setWords(parts[0].split(","))


        if args.size:
            cell.setSize(args.size)
        
        if args.label:
            cell.label = args.label

        if args.address:
            cell.address = args.address

        if args.note:

            note = " ".join(args.note)

            cell.setNote(note)



        self.stack.push(cell)


    def parseFunction(self, line):

        function = Function.fromString(line)
        self.addFunction(function)

   
    def callCmd(self, args):
            

            line = " ".join(args.function)
    
            self.conv.call(line)

    def leaveCmd(self, args):
        self.conv.leave()

    def functionCmd(self,args):
        line = " ".join(args.function)
        function = Function.fromString(line)
        self.addFunction(function)
    
    def tryParseLocalVar(self, line):
        
        parts = line.split("=")

        
        revar = re.compile(r"(\w[\w\s\*]*\w)\s+(\w+)(\[(\d*)\])?")

        ptr = False

        decl = parts[0]
        if "*" in decl:
            ptr = True
            decl = decl.replace("*","")

        match = revar.match(decl)
        val = []
        if len(parts) > 1:
            parts[1] = parts[1].split("--")[0]
            val = parts[1].replace(";","")
            val = yaml.safe_load(val)

        if match:
            varType = match.group(1).strip()

            varName = match.group(2)

            arraySize = match.group(4) if match.group(4) else None

            cell = StackCell(varName)

            if "_t" in varType:
                varType = varType.replace("_t","")

            if varType not in sizeDict:
                return None

            
            if ptr:
                sizeBytes = 4
            else:
                sizeBytes = sizeDict.get(varType, 4)

            if arraySize:
                sizeBytes = sizeBytes * int(arraySize)
            
            size = int((sizeBytes + 3) / 4)

            cell.setWords(val)
            cell.setSize(size)
            cell.label = varName


            line = line.replace(match.group(0), 'local')


            return cell

        else:
            return None
            
    def localCmd(self, cell, args):

        if args.note:
            cell.setNote(" ".join(args.note))

            if args.note_color:
                cell.words[0].noteColor = args.note_color

        if args.color:
            cell.color = args.color

        self.stack.push(cell)

    def saveCmd(self, args):

        filename = args.filename




        if filename.endswith('.html'):
            with open(filename, "w") as f:
                f.write(self.stack.toHtml())

        elif filename.endswith('.png'):

            try:
                self.stack.generatePng(filename)
            except Exception as e:
                self.print("Failed to generate image. This is likely due to not having 'chrome' installed which is required for html2image. Please install chrome and try again.")

        else:
            with open(filename, "w") as f:
                for cmd in self.commands:
                    if not cmd.startswith("save"):
                        if not cmd.endswith("\n"):
                            cmd += "\n"
                        f.write(cmd)


                
        


    def loadCmd(self, args):
        filename = args.filename
        self.update = False

        if filename.endswith('.c'):

            with open(filename) as f:
                functions = parseCFile(f.read())

            self.status = f"Loaded {len(functions)} functions from {filename}"

            for func in functions:
                self.addFunction(func)

    def writeCmd(self, args):
        """
        
        write data1,data,2,data3 --address &cell+4
        write &cell+16: data1,data2,data3
        write &cell+16: [data1,data2,data3] 
        
        """
        address  = None
        line = " ".join(args.values)
        valLine = line
        
        parts = splitWithEscapes(line,":")

        if len(parts) > 1:
            address = parts[0]
            valLine = parts[1]


        if not valLine.startswith("[") and not valLine.endswith("]"):
            valLine = f"[{valLine}]"

        values = yaml.safe_load(valLine) #use yaml to parse the list so we get the correct types/escapes


        if args.address:
            address = args.address

        self.stack.write(values, address)


    def noteCmd(self, args):

        address  = args.address
        line = " ".join(args.note)
        note = line
        
        parts = splitWithEscapes(line,":")

        if len(parts) > 1:
            address = parts[0]
            note = parts[1]



        self.stack.setNote(note, address, args.color)

    def run(self, callLine = None, limit = 20):

        called = True

        functionCall = None
        
        if callLine:
            callLine = callLine.strip()
            if callLine == "":
                callLine = None

        if callLine:
            functionCall = callLine
        elif self.stack.currentFrame and self.stack.currentFrame.function:
            function = self.stack.currentFrame.function

            if len(function.calls) > 0:
                functionCall  = function.calls[0]

        if not functionCall:
            functionCall = "main()"

        self.conv.call(functionCall)
        limit -= 1

        while  called and (limit > 0):
            
            if self.stack.currentFrame and self.stack.currentFrame.function: 
                function = self.stack.currentFrame.function

                if len(function.calls) > 0:
                    call = function.calls[0]
                    self.conv.call(call)
                    called = True

            limit -= 1

    def runCmd(self, args):

        call = None
        if args.function:
            call = " ".join(args.function)


        self.run(call, limit = args.limit)

    def clearCmd(self, args):
        self.stack.clear()

    def parseCommand(self, line, addHistory = True):

        
        
        plainCmd = line.split(" ")[0]
        if plainCmd in [''," ","\n"]:
            return

        if addHistory and plainCmd not in ['save','s', 'load','l']:
            self.addHistory(line)
        self.update = True
        self.status = ""

        commands = splitWithEscapes(line,";")

        for cmd in commands:

            local = self.tryParseLocalVar(cmd)

            if local:
                cmd = f"local {cmd}"
                args = self.parser.parse_args(cmd.split(" "))
                self.localCmd(local, args)
                self.refreshOutput()

            else:

                try:
                    args = self.parser.parse_args(cmd.split(" "))
                    #print(args)

                    if args.help:
                        self.showHelp(args.command)
                    else:
                        args.func(args)
                        self.refreshOutput()
                except:
                    pass
                    words = cmd.split(" ")
                    self.showHelp(words[0])


    def showHelp(self, command):
            
            if command in self.subparsers.choices:
                self.print(self.subparsers.choices[command].format_help() + "\n\n [Enter] to continue...")
            else:
                self.print(self.parser.format_help() + "\n\n [Enter] to continue...")

            #self.print("[Enterr] to continue...")



    # Initialize the argument parser
    def init_args(self):

        self.parser.add_argument('--help', '-h', action='store_true', help='show this help message and exit')

        subparsers = self.parser.add_subparsers(dest='command', help='sub-command help')

        self.parser.error = nullPrint
        #local command 
        local_parser = subparsers.add_parser('local', help='Declaure a local variable using c syntax')
        local_parser.add_argument('local', nargs='*', help='Local variable declaration')
        local_parser.add_argument('--note','-n', nargs='*', type=str, help='Note for the cell')
        local_parser.add_argument('--color', '-c', type=str, help="Color of the cell")
        local_parser.add_argument('--note-color', '-nc', type=str, help="Color of the note")
        local_parser.set_defaults(func=self.localCmd)

        # pop command
        pop_parser = subparsers.add_parser('pop', help='pop words from the stack')
        pop_parser.add_argument('count', type=str, nargs='?', help='Number of elements to pop', default=1)
        pop_parser.set_defaults(func=self.popCmd)

        #ret command
        ret_parser = subparsers.add_parser('ret', help='Return (pop, jmp to return address)')
        ret_parser.set_defaults(func=self.retCmd)

        #jmp command
        jmp_parser = subparsers.add_parser('jmp', help='Jump to an address')
        jmp_parser.add_argument('address',  help='Address to jump to')
        jmp_parser.set_defaults(func=self.jmpCmd)
        
        #push command
        push_parser = subparsers.add_parser('push', help='push words to the stack')
        push_parser.add_argument('value', nargs='*', help='Value to push', default='')
        push_parser.add_argument('--size', '-s', type=int, help='Type of value')
        push_parser.add_argument('--label','-l', help='Label for the value')
        push_parser.add_argument('--address','-a', help='Address for the value')
        push_parser.add_argument('--note','-n', nargs='*', help='Note for the value')

        push_parser.set_defaults(func=self.pushCmd)

        #frame command
        frame_parser = subparsers.add_parser('frame', help='Start a new Frame')
        frame_parser.add_argument('name', nargs="?",  help='Name of the frame [omit to close the current frame]')
        frame_parser.add_argument('--color', '-c', help='Color of the frame')
        frame_parser.add_argument('--address', '-a', help='address of the frame ')
        frame_parser.add_argument('--size', '-s', type=int, help='size of the frame')
        frame_parser.set_defaults(func=self.frameCmd)

        #call parser
        call_parser = subparsers.add_parser('call', help='Call a function')
        call_parser.add_argument('function', nargs="*", help='Function to call')
        call_parser.set_defaults(func=self.callCmd)

        #function 
        function_parser = subparsers.add_parser('function', help="Define a function using c syntax")
        function_parser.add_argument('function', nargs="*", help='Function signature')
        function_parser.set_defaults(func=self.functionCmd)

        #save 
        save_parser = subparsers.add_parser('save', help='Save the current stack')
        save_parser.add_argument('filename', nargs="?", type=str, help='Filename to save', default='.stackinit')
        save_parser.set_defaults(func=self.saveCmd)

        #load
        load_parser = subparsers.add_parser('load', help='load stack file')
        load_parser.add_argument('filename', type=str, help='Filename to load')
        load_parser.set_defaults(func=self.loadCmd)

        #run 
        run_parser = subparsers.add_parser('run', aliases=['r'], help='Run the a function calls the `call` within a function')
        run_parser.add_argument('function', nargs="*", help='Function call to start, if not provided will use the first call in the current function, or main if no function is active')
        run_parser.add_argument('--limit', '-l', type=int, help='Limit of calls to make', default=20)
        run_parser.set_defaults(func=self.runCmd)

        #write 
        write_parser = subparsers.add_parser('write', aliases=['w'], help='Write data to stack')
        write_parser.add_argument('values', nargs="*", help='Values to write')
        write_parser.add_argument('--address', '-a', type=str, help='Address to write to can be a reference to a cell &<cellName>+4')
        write_parser.add_argument('--count', '-c', type=int, help='Repeated writes', default=1)
        write_parser.add_argument('--file', '-f', type=str, help='binary file to write')
        write_parser.set_defaults(func=self.writeCmd)


        #note
        note_parser = subparsers.add_parser('note', help='Add a note to the stack')
        note_parser.add_argument('note', nargs="*", help='Note to add')
        note_parser.add_argument('--color', '-c', type=str, help='Color of the note', default='red')
        note_parser.add_argument('--address', '-a', type=str, help='Address of the note', default=None)
        note_parser.set_defaults(func=self.noteCmd)

        #leave 
        leave_parser = subparsers.add_parser('leave', help='Pops words from stack until the previous base pointer')
        leave_parser.set_defaults(func=self.leaveCmd)


        clear_parser = subparsers.add_parser('clear', help='Clears the stack')
        clear_parser.set_defaults(func=self.clearCmd)

        for sub in subparsers.choices:
            subparsers.choices[sub].print_help =  nullPrint
            subparsers.choices[sub].error = nullPrint


        self.subparsers = subparsers
