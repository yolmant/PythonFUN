import datetime
import random
import pyodbc

sql=pyodbc.connect('DSN=localdb;uid=JBT;pwd=password')
p=sql.cursor()

def Queries (n,t,xt):
    f='%Y-%m-%d %H:%M:%S'
    for i in range(n):
        t = t + datetime.timedelta(minutes=xt)
        timedata=t.strftime(f)
        temp=random.randint(50,90)
        p.execute("INSERT INTO Machine VALUES (?,?)",(temp,timedata))
        sql.commit()
        print(temp,t.strftime(f))



ciclo=n=m=x=0
time=datetime.datetime.now()

while ciclo!='e':
    while n==0:
        count=raw_input('How many rows do you want to insert? ')
        try:
            count=int(count)
            break
        except ValueError or NameError:
            print (count,'is not a number. Try again\n')

    while m==0:       
        extraTime=raw_input('Introduce the time increase in minutes: ')
        try:
            extraTime=int(extraTime)
            break
        except ValueError:
            print(extraTime,'is not a number. Try again\n')           
    
    while x==0:
        print('\nthere are %s with an interval of %s'%(count,extraTime))
        check=raw_input('Do you want to proceed (Y/N)? ').lower()
        if check== 'y' or check== 'n':
            if check=='y':
                Queries(count,time,extraTime)
                x=1
            elif check=='n':
                break
        else:
            print('Your answer is out the options. Try again\n')
            
    ciclo=raw_input('\nto exit, write e. Otherwise press enter\n')
    
p.close()
sql.close()
