#we import the library Random
import random

def talk():
    '''this fuction will print us each color in x variable'''
    x = ['red','green','blue']
    for i in x:
        print(i)

#call the fuction
talk()

#fuction that will retun us the value of ids after accumulate an alphanumeric element after the FOR loop
def random_id(length):
    number = '0123456789'
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    ids = ''
    for i in range(0,length,1):
        ids += random.choice(number)
        ids += random.choice(alpha)
    return ids

#display the return from the function random_id
print(random_id(3))

#Assing a list of string
number = ['hola','good','tree']

#Display a random string from the list number
print(random.choice(number))  
