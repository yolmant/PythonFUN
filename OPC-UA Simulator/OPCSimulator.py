##################################################################
####
####    OPC-UA iOPS simmulator for Windows
####                                                        
##################################################################
####
####    Auntor: Yolman Torrez
####    Created: June, 2019
####
##################################################################
####
####    Version: 1.3
####    Last-Update: 9/23/2019 
####
##################################################################

from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import filedialog
from tkinter import messagebox

from os import path
from datetime import datetime
from PIL import Image, ImageTk

from OPCsys import TagJSON
from opcua import Server, ua
from opcua.ua.uatypes import StringNodeId
from OPCsys import OPCUASim

import time, os
import random, json

' Main Windows of the application '
class App(Tk):

    def __init__(self):

        Tk.__init__(self)
        
        
        self.resizable(False,False)
        self.iconbitmap(self,default="OPC-IOPS.ico")
        self.title('OPC-UA iOPS Simulator')

        menubar = MenuBar(self)
        self.config(menu=menubar)
        
        package = Frame(self)
        package.pack(side="top", fill="both", expand=True)
        package.grid_rowconfigure(0, weight=1)
        package.grid_columnconfigure(0, weight=1)

        page= OneFrame(parent=package,control=self)
        self.frames= (page,'670x480')
        page.grid(row=0, column=0, sticky="nsew")

        self.show_frame()

    #set the frame of the application on top
    def show_frame(self):
        '''Show a frame for the given page name'''
        frame,size = self.frames
        
        self.geometry(size)
        frame.tkraise()

' class to set the menu bar on the top of the application '
class MenuBar(Menu):

    def __init__(self,parent):

        Menu.__init__(self,parent)

        view = Menu(self, tearoff=False)
        Menu.add_cascade(self,label = 'View', menu = view)
        view.add_command(label ='Config.json', command = self.openConfig)

    # Open the configuration file
    def openConfig (self):

        configFile = "configuration.json"
        os.startfile(configFile)

' class for the First Frame '
class OneFrame(Frame):

    def __init__(self,parent,control):
        global click
        
        #validate that all char in the entry are numbers
        def valid_digit(num):

            if num.isdigit():
                return True
            elif num is "":
                return True
            else:
                return False

        def valid_port(num):

            if num.isdigit() and int(num) <= 65535:
                return True
            elif num is "":
                return True
            else:
                return False

        def valid_ip(num):
            
            if num.isdigit() and int(num) < 256:
                return True
            elif num is "":
                return True
            else:
                return False

        #Limit the entry up to 5 digits
        def limit(*args):
            value = self.port_entry.get()
            if len(value) > 5: self.var.set(value[:5])
            
        Frame.__init__(self,parent)
        
        self.meta = TagJSON()
        self.nameTag = []
        self.parent=parent
        click = False
        
        self.img_logo = ImageTk.PhotoImage(Image.open('OPC-iOPS.png'))
        self.onLed = ImageTk.PhotoImage(Image.open('On-led.png'))
        self.offLed = ImageTk.PhotoImage(Image.open('Off-led.png'))

        self.panel = Label(self, image= self.img_logo)
        self.led2 = Label(self, image= self.onLed)
        self.led1 = Label(self, image= self.offLed)

        port,interval,ip=self.get_metadata()

        octet= ip.split('.')
        
        host_label = Label(self, text= 'IP: ',font=('Arial', 15, 'bold'))
        dot_label1 = Label(self, text= '.',font=('Arial', 22))
        dot_label2 = Label(self, text= '.',font=('Arial', 22))
        dot_label3 = Label(self, text= '.',font=('Arial', 22))
        port_label = Label(self, text= 'Port: ',font=('Arial', 15, 'bold'))
        interval_label = Label(self, text= 'Interval (ms): ',font=('Arial', 15, 'bold'))

        vcmd= self.register(valid_digit)
        vcmd_ip = self.register(valid_ip)
        vcmd_port= self.register(valid_port)
        self.var = StringVar()
        self.var.trace('w',limit)

        self.ip_entry1 = ttk.Entry(self,validate='key',validatecommand=(vcmd_ip,'%P'),width=3,font=('Arial', 18),justify='right')
        self.ip_entry2 = ttk.Entry(self,validate='key',validatecommand=(vcmd_ip,'%P'),width=3,font=('Arial', 18),justify='right')
        self.ip_entry3 = ttk.Entry(self,validate='key',validatecommand=(vcmd_ip,'%P'),width=3,font=('Arial', 18),justify='right')
        self.ip_entry4 = ttk.Entry(self,validate='key',validatecommand=(vcmd_ip,'%P'),width=3,font=('Arial', 18),justify='right')
        self.ip_entry1.insert(END,octet[0])
        self.ip_entry2.insert(END,octet[1])
        self.ip_entry3.insert(END,octet[2])
        self.ip_entry4.insert(END,octet[3])
        
        self.port_entry = ttk.Entry(self,validate='key',validatecommand=(vcmd_port,'%P'),width=6,font=('Arial', 20),textvariable=self.var,justify='right')
        self.port_entry.insert(END,port)

        self.interval_entry = ttk.Entry(self,validate='key',validatecommand=(vcmd,'%P'),width=8,font=('Arial', 20),justify='right')
        self.interval_entry.insert(END,interval)

        self.opc = OPCUASim(control=self,parent=parent)
        control.protocol('WM_DELETE_WINDOW', lambda: self.set_destroy(control=control,server = self.opc))
        
        add_button = ttk.Button(self,text='Add Tag',command= self.tag_button,width=12,style='my.TButton')
        del_button = ttk.Button(self,text='Delete Tag',command=self.imageDel,width=12,style='my.TButton')
        start_button = ttk.Button(self,text='Start OPC',command= self.set_starting ,width=12,style='my.TButton')
        stop_button = ttk.Button(self,text='Stop OPC', command=self.stopped,width=12,style='my.TButton' )
        
        self.tag_list= Listbox(self,height=10,width=20,font=('Arial', 20))
        self.tag_list.configure(justify=CENTER)
        
        host_label.place(x=15,y=280)
        dot_label1.place(x=87,y=280)
        dot_label2.place(x=140,y=280)
        dot_label3.place(x=193,y=280)
        port_label.place(x=15,y=330)
        interval_label.place(x=15, y=375)
        
        self.panel.place(x=20,y=40)
        self.led1.place(x=250,y=60)

        add_button.place(x=340,y=15)
        del_button.place(x=500,y=15)
        start_button.place(x=340,y=430)
        stop_button.place(x=500,y=430)

        self.tag_list.place(x=340,y=70)

        self.ip_entry1.place(x=45,y=280)
        self.ip_entry2.place(x=98,y=280)
        self.ip_entry3.place(x=151,y=280)
        self.ip_entry4.place(x=204,y=280)
        self.port_entry.place(x=70,y=325)
        self.interval_entry.place(x=150,y=375)

        self.showConfig()

    def set_starting(self):

        if self.ip_entry1.get().isdigit() and self.ip_entry2.get().isdigit() and self.ip_entry3.get().isdigit() and self.ip_entry4.get().isdigit():

            self.serverip = self.ip_entry1.get()+'.'+self.ip_entry2.get()+'.'+self.ip_entry3.get()+'.'+self.ip_entry4.get()

            if self.port_entry.get() == "":
                messagebox.showerror("Error 95","No port in the entry")

            elif self.interval_entry.get() == "":
                messagebox.showerror("Error 94","No interval")

            else:
                self.opc.start_server(port=self.port_entry.get(),interval=self.interval_entry.get(),ip=self.serverip)
                self.led1.place_forget()
                self.led2.place(x=250,y=60)

        else:
            messagebox.showerror("Error 93","Wrong IP")

    def set_destroy(self,control,server):

        if  server.status:   
            server.stop_server()

        control.destroy()

    def get_metadata(self):

        PATH = os.getcwd()+'\configuration.json'
        
        with open(PATH, errors='ignore') as data:
            config = json.load(data)

        return config['Metadata']['Port'],config['Metadata']['Interval'],config['Metadata']['Server_IP']

    def tag_button(self):
        global click
        
        if not click:
            
            click = True
            check=AddTag(control=self, tags=self.nameTag,parent=self.parent)
            
    def showConfig(self):

        try:
            PATH = os.getcwd()+'\configuration.json'
            
            with open(PATH, errors='ignore') as data:
                config = json.load(data)

            for tag in config['Metadata']['Tags']:
                self.tag_list.insert(END,tag['nameTag'])
                self.nameTag.append(tag['nameTag'])

        except:
            pass
        
    def imageDel(self):

        try:
            selected = self.tag_list.get(self.tag_list.curselection())
            self.tag_list.delete(ANCHOR)
            self.nameTag.remove(selected)
            for i in range(len(self.meta.data['Metadata']['Tags'])):
                if self.meta.data['Metadata']['Tags'][i]['nameTag'] == selected:
                    del self.meta.data['Metadata']['Tags'][i]
                    self.meta.dump()
                    break
        except:
            messagebox.showinfo("Info","OPC Tag is not selected")

    def stopped(self):

        stop = self.opc.stop_server()

        if stop:

            self.led2.place_forget()
            self.led1.place(x=250,y=60)
        
        
class AddTag(Tk):

    def __init__(self,control,tags,parent):

        def set_destroy():
            global click
            
            click = False
            self.destroy()
            
        Tk.__init__(self)

        #self.overrideredirect(1)
        self.resizable(False,False)
        self.iconbitmap(self,default="OPC-IOPS.ico")
        self.title('OPC-UA iOPS Simulator')
        self.geometry('355x180') #320x180
        self.protocol('WM_DELETE_WINDOW', set_destroy)
        centerApp(self,2/3)
        
        self.boldStyle = ttk.Style(self)
        self.boldStyle.configure("TBold.TButton", font = ('Arial','15'))
        
        self.control=control
        self.nameTag = tags
        self.path={}
        self.selection= ['Integer', 'Double', 'String', 'Binary' ]
        self.variable = StringVar()
        
        tag_label = Label(self, text= 'Tag name:',font=('Arial', 15,'bold'))
        data_label = Label(self,text= 'Data Type:',font=('Arial', 15,'bold'))

        self.tag_entry = ttk.Entry(self,width=15,font=('Arial', 15))

        choice_dd = ttk.OptionMenu(self,self.variable,self.selection[0],*self.selection,style='TBold.TButton')
        choice_dd.configure(width=10)

        self.cancel_button = ttk.Button(self,text='Cancel', command = self.cancel, style = 'TBold.TButton')
        
        tag_label.place(x=30, y=25)
        data_label.place(x=30, y=75)

        self.tag_entry.place(x=140,y=25)

        choice_dd.place(x=170, y=75)
        self.cancel_button.place(x=205,y=125)

        # link function to change dropdown
        self.variable.trace('w', self.change_dropdown)

    # on change dropdown value
    def change_dropdown(self,*args):

        def validation_int(num):
            if num.isdigit():
                return True
            elif num is "":
                return True
            else:
                return False
            
        def validation_float(num):
            try:
                float(num)
                return True
            except:
                if num is "":
                    return True
                else:
                    return False

        def set_widgets(label1='Start value:',label2='End value:',Xaxis=30,valid = None):
            
            self.widget = Label(self,text=label1,font=('Arial', 15,'bold'))
            self.widget2 = Label(self,text=label2,font=('Arial', 15,'bold'))
            self.widget3 = ttk.Entry(self,validate='key',validatecommand=valid,width=15,font=('Arial', 15))
            self.widget4 = ttk.Entry(self,validate='key',validatecommand=valid,width=15,font=('Arial', 15))

            self.widget.place(x=Xaxis,y=140)
            self.widget2.place(x=Xaxis, y=190)
            self.widget3.place(x=155, y=140)
            self.widget4.place(x=155, y=190)
        
        self.geometry('355x310')    
        self.binary = []
        
        try:
            self.widget.destroy()
            self.widget2.destroy()
            self.widget3.destroy()
            self.widget4.destroy()
        except:
            pass
            
        if self.variable.get() == 'Integer':

            vcmd= self.register(validation_int)
            set_widgets(valid =(vcmd,'%P'))
            
        if self.variable.get() == 'Double':

            vcmd= self.register(validation_float)
            set_widgets(valid =(vcmd,'%P'))
            
        if self.variable.get() == 'String':

            set_widgets(label1='String Value 1:',label2='String Value 2:',Xaxis=10)
            
        if self.variable.get() == 'Binary':

            self.widget = ttk.Button(self,text='Select Binary',command=self.imageAdd,style = 'TBold.TButton')

            self.widget.place(x=25,y=165)
        
        save_button = ttk.Button(self,text='Save',command=self.buttonSave, style = 'TBold.TButton')

        save_button.place(x=70,y=255)
        self.cancel_button.place(x=205,y=255)

    #get binary data   
    def imageAdd(self):

        img=filedialog.askopenfilename(initialdir='C:/',title='Select Image',filetypes=[('Images','.png .jpg')],parent=self)
        if img:
            self.binary.append(img)

        numb_image = str(len(self.binary))
        
        self.widget2 = Label(self,text=numb_image+' images selected',font=('Arial', 15))
        
        self.widget2.place(x=165,y=165)
        
    def buttonSave(self):
        global click
        
        err=0
        sttvalue = None
        endvalue = None
        strvalue = []
        if not (any(char.isdigit() for char in self.tag_entry.get()) or any(char.isalpha() for char in self.tag_entry.get())):

            messagebox.showerror("Error 101","Tag name is empty or not correct",parent=self)
            err+=1

        else:

            if self.tag_entry.get() in self.nameTag:

                messagebox.showerror("Error 99","Tag name was already created",parent=self)
                err+=1

            else:

                if self.variable.get() == 'Integer' or self.variable.get() == 'Double' :
                    if (any(char.isdigit() for char in self.widget3.get()) or any(char.isalpha() for char in self.widget3.get())) and (any(char.isdigit() for char in self.widget4.get()) or any(char.isalpha() for char in self.widget4.get())):
                        
                        sttvalue = self.widget3.get()
                        endvalue = self.widget4.get()
                    else:
                        messagebox.showerror("Error 102","Some values are empty",parent=self)
                        err+=1
                        
                if self.variable.get() == 'String':
                    if (any(char.isdigit() for char in self.widget3.get()) or any(char.isalpha() for char in self.widget3.get())) and (any(char.isdigit() for char in self.widget4.get()) or any(char.isalpha() for char in self.widget4.get())):
                            
                        strvalue.append(self.widget3.get())
                        strvalue.append(self.widget4.get())
                    else:
                        messagebox.showerror("Error 102","Some values are empty",parent=self)
                        err+=1
                        
                if self.variable.get() == 'Binary':

                    if len(self.binary) < 2:

                        messagebox.showerror("Error 103","There must be at least 2 images selected",parent=self)
                        err+=1

        if err == 0:

            self.nameTag.append(self.tag_entry.get())
            self.control.meta.tagData(self.tag_entry.get(),self.variable.get(),sttvalue,endvalue,strvalue,self.binary)
            self.control.tag_list.insert(END,self.tag_entry.get())
            self.control.meta.dump()
            click=False
            self.destroy()

    def cancel(self):
        global click
        
        click=False
        self.destroy()
        
        
if __name__=="__main__":

    ' This function will center the application into a close center-position '
    def centerApp(pos,div):

        # Gets the requested values of the height and widht.
        windowWidth = pos.winfo_reqwidth()
        windowHeight = pos.winfo_reqheight()
         
        # Gets both half the screen width/height and window width/height
        positionRight = int(pos.winfo_screenwidth()/2 - windowWidth/div)
        positionDown = int(pos.winfo_screenheight()/2 - windowHeight/div)
         
        # Positions the window in the center of the page.
        pos.geometry("+{}+{}".format(positionRight, positionDown))
        
    root=App()
    centerApp(root,2/4)
    style = ttk.Style()
    style.configure('my.TButton', font=('Arial',15))
    root.mainloop()
