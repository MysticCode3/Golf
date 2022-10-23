import pygame
import sys
from pygame import mixer
import math


# Functions
def Get_Distance(current, initial):
    return math.sqrt(math.pow(abs(current[0] - initial[0]), 2) + math.pow(abs(current[1] - initial[1]), 2))


def Get_Change_X_Y(x, y, target_x, target_y):
    global Angle
    Angle = math.atan2(target_y - y, target_x - x)
    dx = math.cos(Angle)
    dy = math.sin(Angle)
    return dx, dy


def Load_Map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    level = []
    for row in data:
        level.append(list(row))
    return level


def Next_Level_Reset():
    global Current_Level
    global Ball_Pos
    global Strokes
    global Velocity
    global Vel_X
    global Vel_Y
    global Friction
    global Timer
    global Level_Index
    global Tile_Rect_List
    global Hole_List
    global Hazard_List

    Ball_Pos = [Dimensions[0] / 2, Dimensions[1] * (3 / 4)]
    Strokes = 0
    Velocity = 0
    Vel_X = 0
    Vel_Y = 0
    Friction = 1
    Timer = 1
    Tile_Rect_List = []
    Hole_List = []
    Hazard_List = []
    if Level_Index + 1 < len(Level_List):
        Level_Index += 1


def Fade(width, height):
    fade = pygame.Surface((width, height))
    fade.fill((0, 0, 0))
    for alpha in range(0, 150):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)


# Classes
class Circle_Animation():
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.radius)

    def update(self):
        self.radius -= 0.3


# Initializations
pygame.init()
mixer.init()

# Screen Dimensions
Dimensions = (512, 832)

# Background Color
Background_Color = (144, 238, 144)

# Load Images
Block = pygame.image.load("block.png")
Block = pygame.transform.scale2x(Block)
Background = pygame.image.load("background.png")
Background = pygame.transform.scale(Background, Dimensions)
Flag = pygame.image.load("flag.png")
Flag = pygame.transform.scale(Flag, (32, 64))
Power_Bar = pygame.image.load('power_bar.png')
Hazard = pygame.image.load("hazard.png")
Hazard = pygame.transform.scale2x(Hazard)

# FPS
FPS = 120

# Mouse Variables
cx, cy = (0, 0)
Initial_Pos = (0, 0)

# Ball Variables
Ball_Pos = [Dimensions[0] / 2, Dimensions[1] * (3 / 4)]
Ball_Size = 10
Ball_Rect = pygame.Rect(Ball_Pos[0] - Ball_Size / 2 - Ball_Size, Ball_Pos[1] - Ball_Size / 2 - Ball_Size, Ball_Size * 2, Ball_Size * 2)
Velocity = 0
Vel_X = 0
Vel_Y = 0
Friction = 1
Timer = 1
Velocity_Bar = 0
Circle_Animation_List = []
Angle = 0

# Read game map from txt
Level_1 = Load_Map('Level_1')
Level_2 = Load_Map('Level_2')
Level_3 = Load_Map('Level_3')
Level_4 = Load_Map('Level_4')
Level_List = [Level_1, Level_2, Level_3, Level_4]

# Tile Size
Tile_Size = 64

# Tile List
Tile_Rect_List = []

# Hole List
Hole_List = []

# Hazard List
Hazard_List = []

# Levels
Level_Index = 0
Current_Level = Level_List[Level_Index]

# Strokes
Strokes = 0

# Hazard
Did_Hit_Hazard = False

# Sound Effects
Hit_Sound = pygame.mixer.Sound("hit_golf_ball.wav")
pygame.mixer.Sound.set_volume(Hit_Sound, 1)

Hit_Hole_Sound = pygame.mixer.Sound("hit_hole.wav")
pygame.mixer.Sound.set_volume(Hit_Hole_Sound, 1)

Hit_Hazard_Sound = pygame.mixer.Sound("hit_hazard.wav")
pygame.mixer.Sound.set_volume(Hit_Hazard_Sound, 0.1)

# Everything
pygame.display.set_caption('Golf')
screen = pygame.display.set_mode((Dimensions[0], Dimensions[1]))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            cx, cy = pygame.mouse.get_pos()
            print(cx, cy)
            if Velocity == 0:
                pygame.mixer.Sound.play(Hit_Sound)
                Change_X, Change_Y = 0, 0
                Strokes += 1
                Velocity = Get_Distance((cx, cy), Initial_Pos)
                Vel_X = (Get_Change_X_Y(int(Ball_Pos[0] - Ball_Size / 2), int(Ball_Pos[1] - Ball_Size / 2), cx, cy)[0])
                Vel_Y = (Get_Change_X_Y(int(Ball_Pos[0] - Ball_Size / 2), int(Ball_Pos[1] - Ball_Size / 2), cx, cy)[1])
        Velocity_Bar = Get_Distance(pygame.mouse.get_pos(), Initial_Pos)

    # Detects Key Presses
    keys = pygame.key.get_pressed()

    if keys[pygame.K_1]:
        pygame.quit()

    # Screen Color
    screen.fill(Background_Color)

    # Load Background
    screen.blit(Background, (0, 0))

    # Font
    font = pygame.font.SysFont("comicsansms", 50)

    # Main Calculations
    # Render all the tiles
    Tile_Rect_List = []
    y = 0
    for Row in Current_Level:
        x = 0
        for Tile in Row:
            if Tile == '1':
                screen.blit(Block, (x * Tile_Size, y * Tile_Size, Tile_Size, Tile_Size))
                Tile_Rect_List.append(pygame.Rect(x * Tile_Size, y * Tile_Size, Tile_Size, Tile_Size))
            if Tile == '2':
                pygame.draw.circle(screen, (0, 0, 0), (x * Tile_Size, y * Tile_Size), Tile_Size / 2)
                screen.blit(Flag, (x * Tile_Size - Tile_Size / 4 - 10, y * Tile_Size - Tile_Size))
                Hole_List.append(pygame.Rect(x * Tile_Size - Tile_Size / 2, y * Tile_Size - Tile_Size / 2, Tile_Size, Tile_Size))
            if Tile == '3':
                screen.blit(Hazard, (x * Tile_Size, y * Tile_Size, Tile_Size, Tile_Size))
                Hazard_List.append(pygame.Rect(x * Tile_Size, y * Tile_Size, Tile_Size, Tile_Size))
            x += 1
        y += 1

    # Draw Ball
    if Velocity == 0:
        pygame.draw.line(screen, (0, 0, 0), (int(Ball_Pos[0] - Ball_Size / 2), int(Ball_Pos[1] - Ball_Size / 2)), (pygame.mouse.get_pos()), 1)
    pygame.draw.circle(screen, (255, 255, 255), (int(Ball_Pos[0] - Ball_Size / 2), int(Ball_Pos[1] - Ball_Size / 2)), Ball_Size)
    pygame.draw.circle(screen, (0, 0, 0), (int(Ball_Pos[0] - Ball_Size / 2), int(Ball_Pos[1] - Ball_Size / 2)), Ball_Size, 3)

    # Circle Animation
    if Velocity != 0:
        Circle_Animation_List.append(Circle_Animation(int(Ball_Pos[0] - Ball_Size / 2), int(Ball_Pos[1] - Ball_Size / 2), Ball_Size))
    for Circle_Animation_Obj in Circle_Animation_List:
        Circle_Animation_Obj.draw(screen)
        Circle_Animation_Obj.update()
        if Circle_Animation_Obj.radius < 0.3:
            Circle_Animation_List.remove(Circle_Animation_Obj)

    # Power Bar
    screen.blit(Power_Bar, (int(Ball_Pos[0] - Ball_Size / 2) + 12, int(Ball_Pos[1] - Ball_Size / 2) - 20))
    if (Velocity_Bar / Power_Bar.get_height()) * 8 < Power_Bar.get_height():
        pygame.draw.rect(screen, (30, 30, 30), (int(Ball_Pos[0] - Ball_Size / 2) + 12, int(Ball_Pos[1] - Ball_Size / 2) + 24 - (Velocity_Bar / Power_Bar.get_height()) * 8, Power_Bar.get_width(), 3))
    else:
        pygame.draw.rect(screen, (30, 30, 30), (int(Ball_Pos[0] - Ball_Size / 2) + 12, int(Ball_Pos[1] - Ball_Size / 2) + 24 - Power_Bar.get_height() + 5, Power_Bar.get_width(), 3))

    # Update Ball
    Ball_Rect = pygame.Rect(Ball_Pos[0] - Ball_Size / 2 - Ball_Size, Ball_Pos[1] - Ball_Size / 2 - Ball_Size, Ball_Size * 2, Ball_Size * 2)
    if Velocity == 0:
        Initial_Pos = Ball_Pos
    if Velocity != 0:
        Ball_Pos[0] -= Vel_X * Velocity / 25
        Ball_Pos[1] -= Vel_Y * Velocity / 25
    if Velocity > 0:
        Velocity -= Friction
    if Velocity < 1:
        Velocity = 0
        Friction = 1
    if Velocity > 150:
        Velocity = 150

    # Collision With Tiles
    for Tile_Obj in Tile_Rect_List:
        if Timer == 1:
            if Tile_Obj.colliderect(Ball_Rect):
                if Tile_Obj.bottom > Ball_Rect.top & Tile_Obj.top < Ball_Rect.bottom:
                    pygame.mixer.Sound.play(Hit_Sound)
                    Timer -= 0.1
                    Vel_Y *= -1
                if Tile_Obj.right > Ball_Rect.left & Tile_Obj.left < Ball_Rect.right:
                    pygame.mixer.Sound.play(Hit_Sound)
                    Timer -= 0.1
                    Vel_X *= -1

    if Timer == 1:
        if Ball_Rect.right > Dimensions[0]:
            pygame.mixer.Sound.play(Hit_Sound)
            Timer -= 0.1
            Vel_X *= -1
        if Ball_Rect.left < 0:
            pygame.mixer.Sound.play(Hit_Sound)
            Timer -= 0.1
            Vel_X *= -1
        if Ball_Rect.bottom > Dimensions[1]:
            pygame.mixer.Sound.play(Hit_Sound)
            Timer -= 0.1
            Vel_Y *= -1
        if Ball_Rect.top < 0:
            pygame.mixer.Sound.play(Hit_Sound)
            Timer -= 0.1
            Vel_Y *= -1

    if Timer < 1:
        if Timer > 0:
            Timer -= 0.1
    if Timer < 0.15:
        Timer = 1

    # Collision With Hazard
    for Hazard_Obj in Hazard_List:
        if Hazard_Obj.colliderect(Ball_Rect):
            if not Did_Hit_Hazard:
                Did_Hit_Hazard = True
                pygame.mixer.Sound.play(Hit_Hazard_Sound)
            Friction = 3
    if Friction == 1:
        Did_Hit_Hazard = False

    # Check if the ball hit the hole
    for Hole in Hole_List:
        if Hole.colliderect(Ball_Rect):
            pygame.mixer.Sound.play(Hit_Hole_Sound)
            Next_Level_Reset()
            Current_Level = Level_List[Level_Index]
            Fade(Dimensions[0], Dimensions[1])
            Circle_Animation_List.clear()
            break

    # Draw Strokes
    Strokes_Shadow = font.render(f"Strokes: {Strokes}", True, (0, 0, 0))
    screen.blit(Strokes_Shadow, (Dimensions[0] / 2 - Strokes_Shadow.get_width() / 2, 22))
    Strokes_Text = font.render(f"Strokes: {Strokes}", True, (255, 255, 255))
    screen.blit(Strokes_Text, (Dimensions[0] / 2 - Strokes_Text.get_width() / 2, 20))

    # FPS and Update
    pygame.display.update()
    clock.tick(FPS)
