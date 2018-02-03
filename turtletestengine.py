import turtle
import math

wn = turtle.Screen()
wn.tracer(0, 0)
player_x = 0
player_y = 0
player_angle = 0


def drawLine(x1,y1, x2, y2):
    turtle.up()
    turtle.goto(x1, y1)
    turtle.down()
    turtle.goto(x2, y2)
    turtle.up()

#px = player x position
#py = player y position

def drawPlayer(px, py, angle):
    plength = 100
    drawLine(px, py, px + math.cos(angle) * plength, py + math.sin(angle) * plength)


def moveForward(player_x, player_y, player_angle):
    stepLength = 20 
    player_x += stepLength * math.cos(player_angle)
    player_y += stepLength * math.sin(player_angle)

def moveBackward(px, py, angle):
    stepLength = 20 
    px += stepLength * math.cos(angle)
    py += stepLength * math.sin(angle)

def transform(x, y):
    x = x - player_x
    y = y - player_y
    return [x, y]

def rotate(x, y):
    x = (x - player_x)*(math.cos(player_angle)) - (y - player_y)*(math.sin(player_angle))
    y = (x - player_x)*(math.sin(player_angle)) + (y - player_y)*(math.cos(player_angle))
    return [x, y]

turtle.listen()
while 1:
    drawPlayer(player_x, player_y, player_angle)
    turtle.update()
    turtle.clear()
    turtle.onkey(moveForward(player_x, player_y, player_angle), 'UP')


turtle.forward(1)

## while true():
##      Handle keys
##      update player data
##      draw player


