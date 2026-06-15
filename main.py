import turtle
import math
import random

#turtles
screen = turtle.Screen()
screen.tracer(0)

writer = turtle.Turtle()
writer.hideturtle()
writer.speed(0)
writer.up()

timer = writer.clone()
scorer = writer.clone()

player = turtle.Turtle()
player.shape("turtle")
player.color("red")
player.speed(0)
player.up()
player.hideturtle()

projectile = turtle.Turtle()
projectile.hideturtle()
projectile.penup()
projectile.shape("arrow")
projectile.color("red")
projectile.speed(0)

blocks = turtle.Turtle()
blocks.hideturtle()
blocks.shape("square")
blocks.penup()
blocks.speed(0)

eps = turtle.Turtle()
eps.hideturtle()
eps.penup()
eps.shape("circle")
eps.color("blue")
eps.speed(0)
    
#variables
obstacles_list = []
enemy_projectiles = []
playing = False
invincible = False
score = 0
time_left = 30
loaded = True
keys = {"d": False, "a": False, "w": False, "s": False}

#status update
def update_score():
    scorer.clear()
    scorer.goto(160, 180)
    scorer.write("Score:"+ str(score), align="center", font=("Arial", 12, "bold"))

def update_timer():
    global time_left, playing
    if playing:
        timer.clear()
        timer.goto(-160,180)
        timer.write("Time: " + str(time_left), align="center", font=("Arial", 12, "bold"))
        if time_left > 0:
            time_left -= 1
            screen.ontimer(update_timer, 1000)
        else:
            playing = False
            player.hideturtle()
            timer.goto(0, 0)
            timer.write("Game Over! Score: " + str(score), align="center", font=("Arial", 14, "bold"))
        
def end_inv():
    global invincible
    invincible = False
    player.color("red")

#enemy
def spawn_obstacles():
    global invincible
    for i in range(6):
        block = blocks.clone()
        block.goto(random.randint(-180, 180), random.randint(-180, 180))
        block.showturtle()
        obstacles_list.append(block)
    invincible = True
    player.color("yellow")
    screen.ontimer(end_inv, 2000)
        
def spawn_ep(block):
    ep = eps.clone()
    ep.goto(block.position())
    ep.setheading(ep.towards(player.position()))
    ep.showturtle()
    enemy_projectiles.append(ep)
    
def launch_ep():
    global playing
    if playing:
        for ep in enemy_projectiles[:]:
            rad = math.radians(ep.heading())
            ep.setx(ep.xcor() + 1*math.cos(rad))
            ep.sety(ep.ycor() + 1*math.sin(rad))
            if abs(ep.xcor()) > 210 or abs(ep.ycor()) > 210:
                ep.hideturtle()
                enemy_projectiles.remove(ep)
            elif ep.distance(player) < 15 and not invincible:
                ep.hideturtle()
                enemy_projectiles.remove(ep)
                playing = False
                player.hideturtle()
                writer.goto(0,0)
                writer.write("Game Over! Score: " + str(score), align="center", font=("Arial", 14, "bold"))
                return
        screen.update()
        screen.ontimer(launch_ep, 50)
        
def enemy_shoot():
    if playing:
        for block in obstacles_list:
            spawn_ep(block)
        launch_ep()
    screen.ontimer(enemy_shoot, 4000)

#movement control
def keypress(key):
    keys[key] = True

def keyrelease(key):
    keys[key] = False

def move_loop():
    if playing:
        if keys["d"] and player.xcor() <= 190:
            player.setx(player.xcor() + 3)
        if keys["a"] and player.xcor() >= -190:
            player.setx(player.xcor() - 3)
        if keys["w"] and player.ycor() <= 190:
            player.sety(player.ycor() + 3)
        if keys["s"] and player.ycor() >= -190:
            player.sety(player.ycor() - 3)
    screen.ontimer(move_loop, 16)
        
def face_cursor(x, y):
    player.setheading(player.towards(x, y))

#player projectile
def launch():
    global loaded, score
    if loaded and playing:
        loaded = False
        player.color("grey")
        projectile.showturtle()
        projectile.goto(player.position())
        projectile.setheading(player.heading())
        move_projectile()

def move_projectile():
    global loaded, score
    if abs(projectile.xcor()) <= 210 and abs(projectile.ycor()) <= 210:
        rad = math.radians(projectile.heading())
        projectile.setx(projectile.xcor() + 5 * math.cos(rad))
        projectile.sety(projectile.ycor() + 5 * math.sin(rad))
        for block in obstacles_list[:]:
            if projectile.distance(block) < 15:
                block.hideturtle()
                obstacles_list.remove(block)
                projectile.hideturtle()
                score += 1
                update_score()
                if len(obstacles_list) == 0:
                    spawn_obstacles()
                loaded = True
                player.color("red")
                return
        screen.ontimer(move_projectile, 16)
    else:
        projectile.hideturtle()
        loaded = True
        player.color("red")
        
#game flow
def start():
    global playing, score, time_left, obstacles_list, enemy_projectiles
    if not playing:
        playing = True
        time_left = 30
        score = 0
        for block in obstacles_list[:]:
            block.hideturtle()
            obstacles_list.remove(block)
        for ep in enemy_projectiles[:]:
            ep.hideturtle()
            enemy_projectiles.remove(ep)
        writer.clear() 
        player.showturtle()
        update_score()
        update_timer()
        spawn_obstacles()
        enemy_shoot()
        launch_ep()
        move_loop()
        
#Initial Screen
writer.goto(0, 50)
writer.write("My Game", align="center", font=("Arial", 12, "bold")) 
writer.goto(0, 0)
writer.write("Press 'Enter' to start.", align="center", font=("Arial", 12, "normal")) 
   
#Input
screen.listen()

screen.onkey(start, "Return") 
screen.onkeypress(lambda: keypress("d"), "d")
screen.onkeypress(lambda: keypress("a"), "a")
screen.onkeypress(lambda: keypress("w"), "w")
screen.onkeypress(lambda: keypress("s"), "s")
screen.onkeyrelease(lambda: keyrelease("d"), "d")
screen.onkeyrelease(lambda: keyrelease("a"), "a")
screen.onkeyrelease(lambda: keyrelease("w"), "w")
screen.onkeyrelease(lambda: keyrelease("s"), "s")
screen.onscreenclick(face_cursor)
screen.onkey(launch, "space")

screen.mainloop()