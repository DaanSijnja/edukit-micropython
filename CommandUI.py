import subprocess
import PySimpleGUI as sg


setterList = ["Kp1","Ki1","Kd1","Kp2","Ki2","Kd2"]

##generate sidebar
sidebartop = [
           [sg.Push(),sg.Text("EDUKIT SETUP",justification='c'),sg.Push()],
           [sg.HSeparator()],
           [sg.Button('Find COM',key="-rshellread-"),],
           [sg.Button('Flash to',key="-flash-"), sg.Combo(["COM0","COM1","COM2","COM3","COM4","COM5","COM6","COM7","COM8"],"COM0",s=(15,2),enable_events=True,readonly=True,key="-flashinput-")],
           [sg.Button('Open Edukit',key="-openedukit-"),],
           [sg.HSeparator()],
           [sg.Push(),sg.Text("CONTROL SETTINGS",justification='c'),sg.Push()],
           [sg.HSeparator()],    

           ]

for item in setterList:
    st = [
        sg.Text(item),
        sg.Push(),
        sg.InputText(key=item+"input",size=(10,2),default_text="0.0"),
        sg.Button("set",key=item+"button")
        ]
    
    sidebartop.append(st)

sidebarbottom = [
    [sg.HSeparator()],
    [sg.Push(),sg.Text("OTHER SETTINGS",justification='c'),sg.Push()],
    [sg.HSeparator()],  
]



sidebar = []
for item in sidebartop:
    sidebar.append(item)

for item in sidebarbottom:
    sidebar.append(item)

commandLayout = [
    [sg.Push(),sg.Text("COMMAND OUTPUT",justification='c'),sg.Push()],
    [sg.HSeparator()],
    [sg.Multiline(size=(50,30),key="-cmdoutput-",default_text="opened command viewer",autoscroll=True,background_color='#000000',text_color='#ffffff')],
    [sg.InputText(),sg.Button("Send")]
]

mainLayout = [[sg.Push(),sg.Text("COMMAND UI EDUKIT HHS",justification='c'),sg.Push()],
              [sg.HSeparator()],
              [sg.vtop(sg.Column(sidebar,justification='')),sg.VSeparator(), sg.Column(commandLayout)],
          ]

window = sg.Window('Command UI EDUKIT HHS', mainLayout,size=(700, 600))

def SendCommand(args):
    _input = ''

    for arg in args:
        _input += arg + " "
    print(_input)
    try:
        _output = subprocess.run(args,text=True,capture_output=True)
    except:
        _output = "Something went wrong with this command"
        return (_input, _output)
    return (_input, _output.stdout)

def SetToOutput(text,_window):
    t = _window['-cmdoutput-']
    t.update(t.get()+'\n'+ text )
    



while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    if event in ("-rshellread-"):
        a = SendCommand(['rshell','-l'])
        SetToOutput(a[0],window)
        SetToOutput(a[1],window)
        
    
    if event in ("-flash-"):
        a = SendCommand(['rshell','-p',values["-flashinput-"],'cp','*.mpy','/flash/'])
        SetToOutput(a[0],window)
        SetToOutput(a[1],window)

    if event in ("-openedukit-"):
        a = SendCommand(['python','.\edukit_pc.py '])
        SetToOutput(a[0],window)
        SetToOutput(a[1],window)

    for item in setterList:
        if(item+"button" == event):
            a = SendCommand(["mp",f'pid.{item}','=',values[item+"input"]])
            SetToOutput(a[0],window)
            SetToOutput(a[1],window)

    

window.close()



