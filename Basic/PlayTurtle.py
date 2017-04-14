import turtle

wn= turtle.Screen()
dw= turtle.Turtle()

wn.title('HELLO, TURTLE')

dw.color('blue')
dw.shape('blank')
dw.pensize(3)

for i in range(4):
    dw.fd(80)
    dw.left(90)
    
wn.mainloop()
