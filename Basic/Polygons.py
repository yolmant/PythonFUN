import turtle

def polygon(t,sz,n):
    for i in range(n):
        t.forward(sz)
        angle=360/n
        t.left(angle)

side=int(input('introduce how many sides your polygon will have: '))
size=100
wn=turtle.Screen()
dw=turtle.Turtle()
polygon(dw,size,side)

wn.mainloop()
