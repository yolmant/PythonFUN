#define a fuction to get the square root of any value
def SquareRoot(i):
    x=i**(1/2)
    return x

#define a fuction that calculates the square of any value
def Square(i):
    x=i**2
    return x

#introduce a value 
value=float(input("introduce the value: "))

#assign the parameters to the functions
root=SquareRoot(value)
square=Square(value)

#display the value introduces and the result of the operation
print("the square root of ",value," is equal to ",root)
print("and its square is equal to: ",square)
