#main function of the time and alarm set
def main():
    
    #calculate the hours left in a day from the amount of hours introduced by the user
    hours_left=set_alarm%24

    #sum the time set up and the hours left to determine the the time and meridiem
    hours=time_set+hours_left

    #time of the alarm
    final_time=alarm(hours)

    setting(final_time,hours_left)

#function that calculate the hour when the alarm will go off
def alarm(i):
    if (i > 12)and(i <= 24):
        i=i-12

    elif (i > 24):
        i=i-24

    return i

#function that will set the meridiem of the alarm
def meridiem(i):
    if (set_meridiem == x[0]):
        print("the time is",time,"and the alarm is set up to",str(i)+x[1])
    else:
        print("the time is",time,"and the alarm is set up to",str(i)+x[0])

#fuction that set the range of the time morning or afternoon
def setting(i,hours):
    lid=12-time_set
    liu=24-time_set
    if (lid != 0):
        if (hours >= lid) and (hours < liu):
            meridiem(i)
        else:
            print("the time is",time,"and the alarm is set up to",str(i)+set_meridiem)

    elif (lid == 0) and (liu == 0):
        meridiem(i)

    else:
        print("the time is",time,"and the alarm is set up to",str(i)+set_meridiem)
        
#ask to the user the current time 
time=input("introduce the current time(example 2pm or 12am): ")

#ask to the user to introduce the hours to set the alarm
set_alarm=int(input("introduce the amount of hours to set the alarm: "))

#list the two meridiem existed 
x=['am','pm']

#verifying that the variable time is in the range 1-9
if (len(time) == 3):
    
    #introduce the time to a variable 
    time_set=int(time[0])

    #introduce the meridiem into a variable, serparated from the time
    set_meridiem=time[1]+time[2]

    #excecute the main function
    main()

#verifying that the variable time is in the range 10-12
elif (len(time) == 4):

    #introduce the time to a variable 
    time_set=int(time[0]+time[1])

    #introduce the meridiem into a variable, serparated from the time
    set_meridiem=time[2]+time[3]

    #excecute the main function
    main()
