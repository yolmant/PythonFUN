from opcua import Server, ua
from opcua.ua.uatypes import StringNodeId
from datetime import datetime
from tkinter import messagebox

import time, os
import random, json

class TagJSON:

    def __init__(self):

        PATH = os.getcwd()+'\configuration.json'
        if os.path.exists(PATH):
            with open(PATH, errors='ignore') as data:
                self.data = json.load(data)
        else:
            self.data={
                    "Metadata": {
                        "Server_IP": "127.0.0.1",
                        "Port":4840,
                        "Interval":1000,
                        "Tags":[]
                        }
                    }
            self.dump()
            
    def dump(self):

        directory = os.getcwd()

        with open(directory+'\configuration.json', mode='w', encoding='cp1252') as file:
              json.dump(self.data, file,ensure_ascii=False,indent=2)

    def tagData(self,nametag, datatype,sttvalue,endvalue,strvalue,binary):
        
        self.newtag={
                "nameTag": nametag,
                "datatype": datatype
                }

        if datatype == 'Integer' or datatype == 'Double':

            self.newtag.update({"start_value": str(sttvalue), "end_value": str(endvalue)})

        elif datatype == 'String':

            self.newtag.update({"string_value1": str(strvalue[0])})
            self.newtag.update({"string_value2": str(strvalue[1])})
            
        elif datatype == 'Binary':
                
            self.newtag.update({"binary_file": binary})
            
        tagging = self.data["Metadata"]["Tags"]
        tagging.append(self.newtag)

    def update_config(self,IP,port,interval):

        pass


class OPCUASim():

    def __init__(self,control,parent):

        self.status = False
        self.parent = parent
        self.control = control
        
        self.tag={}
        self.value={}
        self.images=[]
        
        self.toggle = {'1':'2','2':'1'}
        self.tog = '1'
        self.ind = 0

    def start_server(self,port,interval,ip):

    
        if not self.status:

            self.data = TagJSON()
            self.metadata = self.data.data
            self.server = Server()
            self.interval = interval
            self.status=True

            self.metadata['Metadata']['Server_IP'] = ip
            self.metadata['Metadata']['Port'] = port
            self.metadata['Metadata']['Interval'] = self.interval
            self.data.dump()

            url = "opc.tcp://"+ip+":"+port
            name = "OPC-UA iOPS Simulator"
            self.server.name = name
                                      
            self.server.set_endpoint(url)
            self.addspace = self.server.register_namespace(name)
            node = self.server.get_objects_node()
            self.param = node.add_object(StringNodeId('[JBT]',self.addspace), "[JBT]")

            self.start_time = datetime.utcnow()
            
            self.dataset = ua.DataValue('0')
            self.dataset.SourceTimestamp = self.start_time
            self.dataset.ServerTimestamp = self.start_time
              
            for index in range(len(self.metadata['Metadata']['Tags'])):
                key = self.metadata['Metadata']['Tags'][index]['nameTag']
                datatype = self.metadata['Metadata']['Tags'][index]['datatype']
                
                try:
                    sttvalue=int(self.metadata['Metadata']['Tags'][index]['start_value'])
                    self.value[key]=sttvalue
                except:
                    pass
                
                try:
                    img = self.metadata['Metadata']['Tags'][index]['binary_file']
                    for bi in img:
                        self.images.append(open(bi,'rb').read())
                except:
                    pass
                
                value = self.param.add_variable(StringNodeId('[JBT].'+key,self.addspace),key,'0')
                self.tag[key]=value
                
            for i in self.tag:
                self.server.set_attribute_value(self.tag[i].nodeid, self.dataset)

            try:    
                self.server.start()
            except OSError:

                messagebox.showerror("Error 91","the requested address is not valid in its context. Try another IP")
                self.stop_server()
                
            time.sleep(4)
            self.run_server()
            
        else:
            messagebox.showerror("Error 98","OPC-UA server has already started. You must stop the service first")    
                        
    def run_server(self):
        
        for index in range(len(self.metadata['Metadata']['Tags'])):
            self.index=index
            tagname = self.metadata['Metadata']['Tags'][index]['nameTag']
            datatype = self.metadata['Metadata']['Tags'][index]['datatype']

            try:
                
                value=int(self.metadata['Metadata']['Tags'][index]['start_value'])
                endvalue=int(self.metadata['Metadata']['Tags'][index]['end_value'])
                
            except:
                pass

            if datatype == "Integer":

                
                self.pushing(value, tagname)           
                if value >= endvalue:
                    self.metadata['Metadata']['Tags'][index]['start_value']=self.value[tagname]
                else:
                    self.metadata['Metadata']['Tags'][index]['start_value']=str(int(self.metadata['Metadata']['Tags'][index]['start_value'])+1)

            if datatype == "Double":
                
                value = round(random.uniform(value, endvalue),2)
                self.pushing(value, tagname)

            if datatype == "String":

                self.tog = self.toggle[self.tog]
##                print(self.tog)
                value = self.metadata['Metadata']['Tags'][index]['string_value'+self.tog]   
                self.pushing(value, tagname)

            if datatype == "Binary":

                if self.ind >= len(self.images): self.ind = 0

                value = self.images[self.ind]
                self.ind+=1
                self.pushing(value, tagname)

        self.scanning()

    def pushing(self,value,variable):

        self.dataset = ua.DataValue(value)
        self.dataset.SourceTimestamp = datetime.utcnow()
        self.dataset.ServerTimestamp= self.start_time
        self.server.set_attribute_value(self.tag[variable].nodeid, self.dataset)

    def stop_server(self):

        try:
            self.server.stop()
            self.status=False
            return True
        except:
            messagebox.showinfo("Info","OPC-UA server hasn't been started")
        
    def scanning(self):

        if self.status:
            #print(self.date)
            self.parent.after(self.interval,self.run_server)
        #print(self.status)
