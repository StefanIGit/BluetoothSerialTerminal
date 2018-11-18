#!/usr/bin/python

import tkinter as tk
import serial.tools.list_ports
import io



top = tk.Tk()
# Code to add widgets will go here...

layoutCnf = {'column': 0,
            'row': 0,
}

def getComProts():
    ports = list(serial.tools.list_ports.comports())
    #print(ports)
    if ports: return [x.device for x in ports]
    else: return['No COM Port']




selectedCOMPort = tk.StringVar(top)
lComPorts = getComProts()
selectedCOMPort.set(lComPorts[0])
ComPortListDropDown = tk.OptionMenu(top, selectedCOMPort, *lComPorts)

selectedBaud = tk.StringVar(top)
lBaud = ['9600', '19200', '38400', '115200', '230400', '250000']
selectedBaud.set(lBaud[2])
BaudListDropDown = tk.OptionMenu(top, selectedBaud, *lBaud)



def refrehComProts():
    ports = getComProts()

    # Reset selectedCOMPort and delete all old options
    selectedCOMPort.set('')
    ComPortListDropDown['menu'].delete(0, 'end')

    # Insert list of new options (tk._setit hooks them up to selectedCOMPort)
    for choice in ports:
        ComPortListDropDown['menu'].add_command(label=choice, command=tk._setit(selectedCOMPort, choice))
    
    selectedCOMPort.set(ports[0])
    
    

reFreshButton = tk.Button(text='Refresh', command=refrehComProts)
reFreshButton.grid(cnf=layoutCnf)

layoutCnf['column'] = 1
ComPortListDropDown.grid(cnf=layoutCnf)
layoutCnf['column'] += 1
BaudListDropDown.grid(cnf=layoutCnf)
layoutCnf['row'] +=1
layoutCnf['column'] = 0

def runScript(text = 'AT', row=None):
    entries = entries_by_row[row] if row is not None else ['AT']
    print ('runScript {}. Contents of entries: {}'.format(text, [entry.get() for entry in entries]))
    

    with serial.Serial(selectedCOMPort.get(), selectedBaud.get(), timeout=1) as ser:
        #x = ser.read()          # read one byte
        #s = ser.read(10)        # read up to ten bytes (timeout)
        #ser.write(bytes('\n\r','utf-8'))
        #ser.write(bytes(entries[0].get(),'utf-8'))
        #ser.write(bytes('\n\r','utf-8'))
        
        #ser = serial.serial_for_url('loop://', timeout=1)
        sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

        sio.write(str(entries[0].get() +"\n\r"))
        sio.flush() # it is buffering. required to get the data out *now*
        line = sio.readline()
        
        
        #line = ser.readlines()   # read a '\n' terminated line
        print (line)
        '''line = ''
        while True:
            
            char = ser.read()
            line += str(char)
            print(char)
            if char  == b'\n': break
        print(line)
        '''

rowOffset = 5
row = 0
column = 0
entries_by_row = []
lCmds = ['at', 'at+pswd', '']
for command in range(3):
    entries_by_row.append([])
    button = tk.Button(top, text='name%s'%command, command=lambda row=row: runScript('nondefault text', row))
    button.grid(row=rowOffset+row, column=column, sticky='w')
    column +=1
    entry = tk.Entry(top)
    entry.insert(0,lCmds[command])#text %s'%command)
    entry.grid(row=rowOffset+row, column=column)
    column +=1
    entries_by_row[-1].append(entry)
    row +=1
    column = 0


layoutCnf['row'] = rowOffset + row + 1
# scrolled text box used to display the serial data
frame = tk.Frame(top, bg='cyan')
frame.grid(cnf=layoutCnf)
#layoutCnf['row'] +=1
#layoutCnf['column'] = 0
#pack(side="bottom", fill='both', expand='no')
import tkinter.scrolledtext as tkscrolledtext

textbox = tkscrolledtext.ScrolledText(master=frame, wrap='word', width=180, height=28) #width=characters, height=lines
textbox.grid(cnf=layoutCnf)
#layoutCnf['row'] +=1
#layoutCnf['column'] = 0
#pack(side='bottom', fill='y', expand=True, padx=0, pady=0)
textbox.config(font="bold")

top.mainloop()