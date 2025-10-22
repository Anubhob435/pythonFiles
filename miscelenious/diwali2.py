import turtle
import math
import random

# diwali2.py
# Draw a Diya (traditional oil lamp) with turtle graphics


# Configuration
WIDTH, HEIGHT = 800, 600
BG_COLOR = "#071428"  # deep night blue
BOWL_COLOR = "#8B4000"  # sienna-like
BOWL_HIGHLIGHT = "#C68642"
DECOR_COLOR = "#FFD700"  # gold
WICK_COLOR = "#2B1A0F"
FLAME_COLORS = ["#FF3D00", "#FF8C00", "#FFD700"]  # red -> orange -> yellow

turtle.colormode(255)
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor(BG_COLOR)
screen.title("Diya - Diwali")

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.pensize(2)


def goto(x, y):
   pen.penup()
   pen.goto(x, y)
   pen.pendown()


def draw_bowl(cx, cy, width, height):
   """Draw the diya bowl as an elliptical filled shape."""
   pen.color(BOWL_COLOR)
   pen.begin_fill()
   goto(cx - width // 2, cy)
   pen.setheading(0)
   # approximate ellipse by many short arcs
   steps = 120
   for i in range(steps + 1):
      theta = math.pi * i / steps  # top half
      x = cx + (width / 2) * math.cos(theta)
      y = cy - (height / 2) * math.sin(theta)
      pen.goto(x, y)
   # bottom curve
   for i in range(steps + 1):
      theta = math.pi * i / steps  # bottom half reversed
      x = cx - (width / 2) * math.cos(theta)
      y = cy - (height / 2) * math.sin(theta) - (height * 0.2)
      pen.goto(x, y)
   pen.end_fill()
   # highlight
   pen.color(BOWL_HIGHLIGHT)
   pen.width(1)
   goto(cx - width * 0.25, cy - height * 0.15)
   pen.setheading(60)
   pen.begin_fill()
   pen.circle(width * 0.18, 120)
   pen.left(120)
   pen.circle(width * 0.08, 120)
   pen.end_fill()


def draw_decorations(cx, cy, width, height):
   """Draw gold dots and scallop pattern on the bowl."""
   pen.color(DECOR_COLOR)
   pen.width(2)
   dots = 7
   spacing = width / (dots + 1)
   y = cy - height * 0.1
   for i in range(1, dots + 1):
      goto(cx - width / 2 + i * spacing, y + (math.sin(i) * 4))
      pen.begin_fill()
      pen.circle(6)
      pen.end_fill()
   # scallop edge
   goto(cx - width / 2, cy)
   pen.setheading(-60)
   scallops = 10
   for i in range(scallops):
      pen.penup()
      x = cx - width / 2 + (i + 0.5) * (width / scallops)
      y0 = cy + height * 0.02
      pen.goto(x, y0)
      pen.pendown()
      pen.begin_fill()
      pen.circle(width / (scallops * 6))
      pen.end_fill()


def draw_wick(cx, cy, wick_height):
   pen.color(WICK_COLOR)
   pen.width(4)
   goto(cx, cy)
   pen.setheading(90)
   pen.forward(wick_height)


def draw_flame(cx, cy, max_height):
   """Draw layered flame (three teardrop shapes)."""
   # layers from outside (red) to inside (yellow)
   offsets = [0, -6, -12]
   scales = [1.0, 0.68, 0.44]
   for color, off, scale in zip(FLAME_COLORS, offsets, scales):
      pen.color(color)
      pen.begin_fill()
      goto(cx + off, cy)
      pen.setheading(90)
      # draw a teardrop by two arcs
      r = max_height * scale
      pen.forward(r * 0.5)
      pen.right(40)
      pen.circle(-r, 180)
      pen.right(80)
      pen.circle(-r, 180)
      pen.end_fill()


def draw_glow(cx, cy, radius):
   """Subtle glow around the flame using translucent concentric circles."""
   # Turtle doesn't support alpha; approximate using lighter colors and thin rings
   rings = 6
   for i in range(rings):
      pen.width(2)
      shade = int(255 - (i * (255 / rings)))
      glow = (255, shade, 0)
      pen.color(glow)
      pen.penup()
      pen.goto(cx, cy + i * (radius * 0.08))
      pen.setheading(0)
      pen.forward(-radius * (1 + i * 0.08))
      pen.pendown()
      pen.circle(radius * (1 + i * 0.08))


def draw_plate(cx, cy, width):
   """Decorative plate under diya."""
   pen.color("#3B2F2F")
   pen.begin_fill()
   goto(cx - width / 2 - 20, cy - 18)
   pen.setheading(0)
   for _ in range(2):
      pen.forward(width + 40)
      pen.left(90)
      pen.forward(20)
      pen.left(90)
   pen.end_fill()
   # rim
   pen.color("#5C4A42")
   pen.width(3)
   goto(cx - width / 2 - 10, cy - 8)
   pen.setheading(0)
   pen.forward(width + 20)


def main():
   cx, cy = 0, -20
   bowl_w, bowl_h = 380, 130
   flame_height = 110
   # draw plate
   draw_plate(cx, cy - 35, bowl_w)
   # bowl
   draw_bowl(cx, cy, bowl_w, bowl_h)
   draw_decorations(cx, cy, bowl_w, bowl_h)
   # wick
   wick_top_y = cy + 10
   draw_wick(cx, wick_top_y, 18)
   # flame layers
   draw_flame(cx, wick_top_y + 20, flame_height)
   # glow
   draw_glow(cx, wick_top_y + 40, 60)
   # small animated sparkles around lamp
   sparkle = turtle.Turtle()
   sparkle.hideturtle()
   sparkle.speed(0)
   sparkle.penup()
   for _ in range(14):
      x = random.randint(-200, 200)
      y = random.randint(0, 220)
      size = random.randint(2, 6)
      sparkle.goto(x, y)
      sparkle.color(random.choice(["#FFD700", "#FFA500", "#FFDB58"]))
      sparkle.dot(size)
   pen.penup()
   pen.goto(0, -HEIGHT // 2 + 20)
   pen.color("white")
   pen.write("Happy Diwali", align="center", font=("Arial", 24, "bold"))
   pen.hideturtle()
   turtle.done()


if __name__ == "__main__":
   main()