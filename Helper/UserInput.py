import  JReader

calling = []
service = True
if __name__ == "__main__":

    js = JReader.ReadJSON()

    print('Enter Funcionts: \n\n')

    uinput = input('User>> ')
    
while service:

    inst = uinput.split()
    function='js.'+inst[0]
    
    try:
        exec(function)

    except:
        print("Error - Function doesn't exist")
            
    uinput = input('User>> ')

    if inst[0] == 'exit' or inst[0] == 'exit()':
        service = False

## HELLO WORLD
