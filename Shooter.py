'''
Projeto: Shooter Game
Professor: Fabrício Henrrique
Matéria: Computação gráfica
Criado por: Wesley Santos
RA: N3855J-3
Turma: CC5P18
'''
import turtle
import math
import random
import os
import tkinter as tk

path = os.getcwd()
os.chdir(path)
print("O caminho é: " + path)

# Configurando a Screen
window = turtle.Screen()
window.title("shooter Game")
window.setup(width=800, height=600)
window.tracer(0)
window.bgpic("pele.gif")

#Inserindo o sprite
turtle.register_shape("shooterUP.gif")
turtle.register_shape("shooterDW.gif")
turtle.register_shape("shooterRT.gif")
turtle.register_shape("shooterLT.gif")
turtle.register_shape("explosion.gif")
turtle.register_shape("corona.gif")
turtle.register_shape("bolha.gif")

enemy_vertices = ((0,15),(-15,0),(-18,5),(-18,-5),(0,0),(18,-5),(18, 5),(15, 0))
window.register_shape("enemy", enemy_vertices)

#Score do game
class Score(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.penup()

# Classe shooter
class shooter(turtle.Turtle):
    def __init__(self, goto):
        turtle.Turtle.__init__(self)
        self.shape("shooterUP.gif")
        self.penup()
        self.left(90)
        self.goto(goto, 0)
        self.shapesize(3, 3)
        self.dx = 10
        self.dy = 10

    # Configurações de comandos do shooter
    def walkForward(self):
        y=self.ycor()
        if y < 260:
            self.sety(y+10)
        self.degrees(360)
        self.shape("shooterUP.gif")

    def walkBackward(self):
        y=self.ycor()
        if y > -250:
            self.sety(y-10)
        self.degrees(-360)
        self.shape("shooterDW.gif")

    def turnRight(self):
        x=self.xcor()
        if x < 350:
            self.setx(x+10)
        self.degrees(0.00001)
        self.shape("shooterRT.gif")

    def turnLeft(self):
        x=self.xcor()
        if x > -355:
            self.setx(x-10)
        self.degrees(-720)
        self.shape("shooterLT.gif")


# Classe Shoot
class Shoot(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("bolha.gif")
        self.speed(0)
        self.penup()

# Class Enemy
class Enemy(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("corona.gif")
        self.speed(0)
        self.penup()

# Método para atrair dois pontos
def get_heading_to(t1, t2):
    x1 = t1.xcor()
    y1 = t1.ycor()
    
    x2 = t2.xcor()
    y2 = t2.ycor()
    
    heading = math.atan2(y1 - y2, x1 - x2)
    heading = heading * 180.0 / 3.14159
    
    return heading

score = Score()
score.color("white")
score.hideturtle()
score.goto(0, 250)
score.write("Score: 0", False, align = "center", font = ("Arial", 24, "normal"))

#Instâncias de inimigos
enemys = []
for _ in range(10):
    enemy = Enemy()
    enemy.speed = 0.005
    enemy.state = "spawn"
    enemy.hideturtle()
    enemy.shapesize(0.5, 0.5)
    enemys.append(enemy)

#Instâncias de tiros
shoots = []
for _ in range(5):
    shoot = Shoot()
    shoot.shapesize(0.5, 0.5)
    shoot.speed = 0.5
    shoot.state = "ready"
    shoot.hideturtle()
    shoots.append(shoot)

# Instância da classe jogador
shooter = shooter(0)
shooter.score = 0

#Atualizar sprites de shooter
def sprite_player(shooter):
    if shooter.heading() == shooter.xcor():
        shooter.shape("shooterRT.gif")

#Nascer inimigos
def enemy_spawn():
    for enemy in enemys:
        if enemy.state == "spawn":
            enemy.goto(shooter.xcor(), shooter.ycor())
            enemy.showturtle()
            enemy.state = "live"
            heading = random.randint(0, 260)
            distance = random.randint(300, 400)
            enemy.setheading(heading)
            enemy.fd(distance)
            enemy.setheading(get_heading_to(shooter, enemy))
            enemys.append(enemy)

#Atualiza o destino dos inimigos
def enemy_update(enemys):
    for enemy in enemys:
        enemy.setheading(get_heading_to(shooter, enemy))
        if enemy.speed > 10:
            enemy.speed += 0.0000001

#Atirar
def fire_shoot():
    for shoot in shoots:
        if shoot.state == "ready":
            shoot.goto(shooter.xcor(), shooter.ycor())
            shoot.showturtle()
            shoot.state = "fire"
            shoot.setheading(shooter.heading())
            break

# Configurações de Teclado
window.listen()
window.onkeypress(shooter.walkForward, "Up")
window.onkeypress(shooter.turnRight, "Right")
window.onkeypress(shooter.walkBackward, "Down")
window.onkeypress(shooter.turnLeft, "Left")
window.onkeypress(fire_shoot, "space")

# Loop de inicialização de jogo
while True:

    #Variável para definir o fim do jogo
    Game_Over = False

    window.update()
    enemy_spawn()
    enemy_update(enemys)

    # Trejeto do tiro
    for shoot in shoots:
        if shoot.state == "fire":
            shoot.fd(shoot.speed)

        # Verificar disponibilidade de tiros na screen
        if shoot.xcor() > 500 or shoot.xcor() < -500 or shoot.ycor() > 300 or shoot.ycor() < -300:
            shoot.hideturtle()
            shoot.state = "ready"

    # Spawn dos inimigos
    for enemy in enemys:
        enemy.state == "spawn"
        enemy.fd(enemy.speed)

        # Verificar colisões
        # Enemy e shoot
        for shoot in shoots:
            if enemy.distance(shoot) < 35:

                # Resetar einimigos
                heading = random.randint(0, 260)
                distance = random.randint(600, 800)
                enemy.setheading(heading)
                enemy.fd(distance)
                enemy.setheading(get_heading_to(shooter, enemy))

                # Mecânica que aumenta a velocidade dos inimigos ao passar as waves
                enemy.speed += 0.01
                
                # Reset tiro
                shoot.goto(600, 600)
                shoot.hideturtle()
                shoot.state = "ready"

                # Aumentar pontuação
                shooter.score += 10
                score.clear()
                score.write("Score: {}".format(shooter.score), False, align = "center", font = ("Arial", 24, "normal"))

            # Enemy e Shooter
            if enemy.distance(shooter) < 40:
                # Resetar enemy
                heading = random.randint(0, 260)
                distance = random.randint(600, 800)
                enemy.setheading(heading)
                enemy.fd(distance)
                enemy.setheading(get_heading_to(shooter, enemy))
                enemy.speed += 0.005
                Game_Over = True
                score.clear()
                score.write("Score: {}".format(shooter.score), False, align = "center", font = ("Arial", 24, "normal"))

        if Game_Over == True:
            shooter.hideturtle()
            shoot.hideturtle()
            for a in enemys:
                a.hideturtle()
            score.clear()
            window.bgpic("game_over.gif")
            score.goto(0, -100)
            score.write("Score: {}".format(shooter.score), False, align = "center", font = ("Arial", 24, "normal"))
            break

    
