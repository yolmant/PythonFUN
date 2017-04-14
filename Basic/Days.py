days_enter=int(input("Enter the number of days: "))

years= days_enter//365
days_left= days_enter%365
months= days_left//30
days_left= days_left%30
weeks= days_left//7
days= days_left%7

print(days_enter,"days equals",years,"years,",months,"months,",weeks,"weeks,",days,"days.")

total_days= (years*365)+(months*30)+(weeks*7)+days

print("Total days are",total_days,"which should be the same as",days_enter)
