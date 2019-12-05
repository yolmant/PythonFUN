import  JReader

calling = []

if __name__ == "__main__":

    js = JReader.ReadJSON()

    uinput = input('Enter input: \n')

    function='js.'+uinput

    exec(function)
    
    
