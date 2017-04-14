import turtle

def dashed_line_1(L,n_cycles):
    size=L/n_cycles
    for i in range(n_cycles):
        dw.pendown()
        dw.forward(size)
        dw.penup()
        dw.forward(size)

length=int(input('introdude the length of the line: '))
cycles=int(input('introduce the number of cycle: '))

wn=turtle.Screen()
dw=turtle.Turtle()

dashed_line_1(length,cycles)
wn.mainloop()
