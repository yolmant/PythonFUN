import turtle

wn=turtle.Screen()
dw=turtle.Turtle()

dw.left(90)

clock=[12,1,2,3,4,5,6,7,8,9,10,11]

for i in clock:
    dw.penup()
    dw.forward(100)
    dw.pendown()
    dw.forward(20)
    dw.penup()
    dw.forward(20)
    dw.pendown()
    dw.write(i,font=('harrington',14,'normal'))
    dw.penup()
    dw.setpos(0,0)
    dw.right(30)

dw.pendown()
dw.forward(80)
wn.mainloop()
