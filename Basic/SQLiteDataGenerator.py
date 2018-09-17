import sqlite3
import datetime
import random

def table_creator ():
     try:
          p.execute('create table '+tableName+'(Id integer primary key, Temperture integer, Date datetime);')
          db.commit()
     
     except:
          print dbName,'has been already created with the table %s \n'%(tableName)
          
def Queries (n,t,xt):
     f='%Y-%m-%d %H:%M:%S'
     for i in range(n):
          t = t + datetime.timedelta(minutes=xt)
          timedata=t.strftime(f)
          temp=random.randint(50,90)
          p.execute("INSERT INTO "+tableName+" (temperture,date) VALUES (?,?)",(temp,timedata))
          db.commit()
          print(temp,t.strftime(f))
                
dbName='Ravenna.db'
tableName='Machine'
db = sqlite3.connect(dbName)
p = db.cursor()

ciclo=n=m=x=0
time=datetime.datetime.now()
table_creator()

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
        print('\nthere are %s with an interval of %s minute'%(count,extraTime))
        check=raw_input('Do you want to proceed (Y/N)? ').lower()
        if check== 'y' or check== 'n':
            if check=='y':
                Queries(count,time,extraTime)
                break
            elif check=='n':
                break
        else:
            print('Your answer is out the options. Try again\n')
            
    ciclo=raw_input('\nto exit, write e. Otherwise press enter\n')
    
p.close()
db.close()
