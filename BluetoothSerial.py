#!/usr/bin/python
'''
Serial Terminal for those HC-05 HC-06 Bluetooth modules
Not nice but I have not found one I like so far.

Todo: add option for \n\r

'''

# here is the list of the prdefined commands
lCmds = ['at', 
         'at+pswd', 
         'at+name', 
         'at+role', 
         'at+cmode',
         'at+version',
         'at+reset',
         'at+addr',
         'at+orgl',
         'at+rname',
         'at+uart',
         'at+bind',
         'at+RMAAD',
         'AT+ADCN',
         'at+bind=',
         ''
         ]
version = '0.5'

import tkinter as tk
import tkinter.scrolledtext as tkscrolledtext
import serial.tools.list_ports
import io



# callback functions

def getComProts():
    ports = list(serial.tools.list_ports.comports())
    #print(ports)
    if ports: return [x.device for x in ports]
    else: return['No COM Port']

def refrehComProts():
    ports = getComProts()

    # Reset selectedCOMPort and delete all old options
    selectedCOMPort.set('')
    ComPortListDropDown['menu'].delete(0, 'end')

    # Insert list of new options (tk._setit hooks them up to selectedCOMPort)
    for choice in ports:
        ComPortListDropDown['menu'].add_command(label=choice, command=tk._setit(selectedCOMPort, choice))
    
    selectedCOMPort.set(ports[0])

def clearOutPut():
    textbox.delete('1.0',tk.END)
    
def runScript(text = 'AT', row=None):
    entries = entries_by_row[row] if row is not None else ['AT']
    cmd = str(entries[0].get())
    textbox.insert('1.0', 'CMD: ' + cmd +'\n')
    with serial.Serial(selectedCOMPort.get(), selectedBaud.get(), timeout=1) as ser:
        sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
        sio.write(cmd +"\n\r")
        sio.flush() # it is buffering. required to get the data out *now*
        #line = sio.readline()

        seq =[]
        count = 0
        while True:
            for c in sio.read():
                seq.append(c)
                joined_seq = ''.join(str(v) for v in seq) #Make a string from array
                print (ord(c))
                if c == '\n':
                    textbox.insert('1.0', "RESP " + str(count) + ': ' + joined_seq)
                    seq = []
                    count += 1
            break
        if 'c' not in dir(): textbox.insert('1.0', 'No Response!!! not in AT mode?!?!\n')

# Layout
top = tk.Tk()
layoutCnf = {'column': 0,
            'row': 0,
            #'ipadx': 5,
            'padx': 5,
            #'ipady': 5,
            'pady': 5,

            }



# Comport Bottons and settings
selectedCOMPort = tk.StringVar(top)
lComPorts = getComProts()
selectedCOMPort.set(lComPorts[0])
ComPortListDropDown = tk.OptionMenu(top, selectedCOMPort, *lComPorts)

selectedBaud = tk.StringVar(top)
lBaud = ['9600', '19200', '38400', '115200', '230400', '250000']
selectedBaud.set(lBaud[2])
BaudListDropDown = tk.OptionMenu(top, selectedBaud, *lBaud)

reFreshButton = tk.Button(text='Refresh', command=refrehComProts)
clearOutPutButton = tk.Button(text='Clear', command=clearOutPut)

## Layout

reFreshButton.grid(cnf=layoutCnf)
layoutCnf['column'] = 1
ComPortListDropDown.grid(cnf=layoutCnf)
layoutCnf['column'] += 1
BaudListDropDown.grid(cnf=layoutCnf)
layoutCnf['column'] += 1
clearOutPutButton.grid(cnf=layoutCnf)
layoutCnf['row'] +=1
layoutCnf['column'] = 0
# CMD buttons and entries


rowOffset = 0
row = 1
column = 0
entries_by_row = []

for command in range(len(lCmds)):
    entries_by_row.append([])
    button = tk.Button(top, text='Send', command=lambda row=row: runScript('nondefault text', row-1))
    button.grid(layoutCnf, row=rowOffset+row, column=column, sticky='w')
    column +=1
    entry = tk.Entry(top)
    entry.insert(0,lCmds[command])#text %s'%command)
    entry.grid(layoutCnf, row=rowOffset+row, column=column, sticky='w', columnspan=3)
    column +=1
    entries_by_row[-1].append(entry)
    row +=1
    column = 0


layoutCnf['row'] = rowOffset + row + 1
layoutCnf['row'] = 1
layoutCnf['column'] = 2
# scrolled text box used to display the serial data
frame = tk.Frame(top, bg='cyan')
frame.grid(cnf=layoutCnf, columnspan=3, rowspan=len(lCmds))

textbox = tkscrolledtext.ScrolledText(master=frame, wrap='word', width=80, height=30) #width=characters, height=lines
textbox.grid(cnf=layoutCnf)#, columnspan=3, rowspan=len(lCmds))
#layoutCnf['row'] +=1
#layoutCnf['column'] = 0
#pack(side='bottom', fill='y', expand=True, padx=0, pady=0)
textbox.config(font="bold")

top.mainloop()