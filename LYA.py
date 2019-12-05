import json

from tkinter import filedialog, Tk

class ReadJSON():

    def __init__(self):
        
        self.root = Tk()
        self.root.withdraw()

    def get_json(self):

        with open(self.path, errors='ignore') as data:
            jdata = json.load(data)

        return jdata

    def get_keys(self,data):

        for key,val in data.items():

            print(key)

    def get_json_loads(self,data,key):

        ddata = json.loads(data[key])

        return ddata

    def get_readable_json(self,data):

        readable_json = json.dumps(data, indent = 2)

        print(readable_json)

    def set_file(self):

        self.path = filedialog.askopenfilename(initialdir = "c:/", title = "Select File", filetypes = (("JSON File","*.json"),("No files","*.noexe")))



