import turtle
import math
import time

screen = turtle.Screen()
screen.title("Happy Diwali: Animated Diya 🪔")
screen.bgcolor("black")
t = turtle.Turtle(visible=False)
t.speed(0)

def draw_diya():
    # Draw base
    t.penup()
    t.goto(0, -120)
    t.pendown()
    t.color('#d2691e')
    t.begin_fill()
    t.circle(120, 180)
    t.left(90)
    t.forward(50)
    t.left(90)
    t.circle(170, 180)
    t.left(90)
    t.forward(50)
    t.end_fill()
    t.right(270)

    # Inner part
    t.penup()
    t.goto(0, -100)
    t.pendown()
    t.color('#ffbc8a')
    t.begin_fill()
    t.circle(100, 180)
    t.left(90)
    t.forward(30)
    t.left(90)
    t.circle(140, 180)
    t.left(90)
    t.forward(30)
    t.end_fill()
    t.right(270)
    
def draw_flame(radius, flicker):
    t.penup()
    t.goto(0, -30)
    t.pendown()
    t.seth(90)
    t.color('#ffd700')
    t.begin_fill()
    for angle in range(0, 361, 20):
        r = radius + flicker * math.sin(math.radians(angle*3))
        x = r * math.cos(math.radians(angle))
        y = r * math.sin(math.radians(angle))
        t.goto(0 + x, -30 + y)
    t.end_fill()

def write_message():
    t.penup()
    t.goto(0, 130)
    t.color('yellow')
    t.hideturtle()
    t.write("Happy Diwali!", align="center", font=("Arial", 28, "bold"))
    t.goto(0, 100)
    t.color('orange')
    t.write("May your life shine as bright as the Diya!", align="center", font=("Arial", 17, "bold"))

def animate_flame():
    draw_diya()
    write_message()
    n = 0
    while True:
        t.penup()
        t.goto(0, -30)
        t.pendown()
        t.color(screen.bgcolor())
        t.begin_fill()
        t.circle(35)
        t.end_fill()
        draw_flame(35, 10 * math.sin(n))
        n += 0.1
        screen.update()
        time.sleep(0.04)

turtle.tracer(0, 0)
animate_flame()
