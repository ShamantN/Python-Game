import pygame
import os 
from time import sleep
import math
import random
import tkinter as tk
from tkinter import *
from tkinter import Button
from tkinter import messagebox
from PIL import Image, ImageTk
from PIL import *
import csv
import pygame_menu
from pygame_menu import themes
from tkinter import ttk
from os.path import abspath
import calendar

root=tk.Tk()
root.title('Zapocalypse')
root.geometry('350x100')
menubar = Menu(root)
optionsmenu = Menu(menubar, tearoff=0)
helpmenu = Menu(menubar, tearoff=0)

PLAYER_YELLOW = ""
PLAYER_RED = ""
pie=math.pi

INPUT = os.path.abspath("C:\\Users\\shama\\GameProject\\Tally.csv")
FILES_ = open(INPUT, "r+")
READER_ = csv.reader(FILES_)
DATA_ = list(READER_)

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500                     #DEFINE CONSTANT VALUES WITH ALL CAPS( GOOD PRACTICE)
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("BATTLE GALACTICA")

BORDER=pygame.Rect(WIDTH//2 - 10, 0, 10, HEIGHT)
YELLOW_HEALTH_BORDER=(0,0, 137, 27)
RED_HEALTH_BORDER=(763,0, 137, 27)

HEALTH_FONT=pygame.font.SysFont('impact', 30)
WINNER_FONT=pygame.font.SysFont('impact', 50)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
WINNER_SOUND= pygame.mixer.Sound(os.path.join('Assets', 'vid_game_win.wav'))

COLOUR=(0,0,0)
YELLOW=(255,255,0)
RED=(255,0,0)
CYAN=(0,255,255)
GREEN=(0,255,0)
PURPLE=(255,0,255)

FPS=165
VEL=4
BULLET_VEL=8
MAX_BULLETS=4

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55,40

RED_HIT=pygame.USEREVENT +1
YELLOW_HIT=pygame.USEREVENT + 2

BACKGROUND_IMAGE=pygame.image.load(os.path.join('Assets','new_space_image.jpg'))
BACKGROUND=pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT) )

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))  #GET THE IMAGE YOU WANT TO BLIT ONTO THE SCREEN
YELLOW_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)     #NEW SCALED DOWN IMAGE TO BE USED IN BLIT FUNCTION 


RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)


surface = pygame.display.set_mode((900, 500))
mainmenu = pygame_menu.Menu('ZAPOCALYPSE', 900, 500, theme=themes.THEME_DARK)
loading = pygame_menu.Menu('Loading the Game...', 900, 500, theme=themes.THEME_DARK)
update_loading = pygame.USEREVENT + 0

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, COLOUR, BORDER)
    pygame.draw.rect(WIN, CYAN, YELLOW_HEALTH_BORDER)
    pygame.draw.rect(WIN, CYAN, RED_HEALTH_BORDER)
    red_health_font = HEALTH_FONT.render("HEALTH = " + str(red_health), 1, RED)
    yellow_health_font = HEALTH_FONT.render("HEALTH = " + str(yellow_health), 1, YELLOW)
    WIN.blit(yellow_health_font, (0, -6))
    WIN.blit(red_health_font, (763, -6))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()


def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x < 400:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y < HEIGHT - 56:  # DOWN
        yellow.y += VEL


def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x > 450:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x < WIDTH - 40:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y < HEIGHT - 56:
        red.y += VEL


def handle_bullets(yellow, red, yellow_bullets, red_bullets):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            BULLET_HIT_SOUND.play()
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            BULLET_HIT_SOUND.play()
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)



def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def about():
   messagebox.showinfo("About the Game", "Zapocalypse thrusts players into an electrifying space odyssey, a Python-crafted 2-player spacecraft shooter. Amidst the cosmic expanse, pilots engage in intense dogfights, unleashing laser salvos to conquer celestial adversaries. Navigating through radiant nebulae and treacherous asteroid fields, players vie for interstellar dominance. With sleek graphics and responsive controls, Zapocalypse delivers an immersive, action-packed gaming experience. Brace for an epic duel in the cosmos, where only the most skilled pilots will emerge victorious in this riveting, Python-powered space showdown.")
   Q1=messagebox.askquestion("Continue", "Do you want to continue?")
   if Q1 == "yes":
      pass
   else:
      root.destroy()

def help_index():
   messagebox.showinfo("Help", "If any errors with game, contact developers")
   Q2=messagebox.askyesnocancel("Trouble-Shooting", 'Do you have any questions or problems with the game?')
   if Q2==True:
      messagebox.showinfo("Contact Developers", " Satwik Kulkarni [Team Representative] : PES1UG23CS528 \n Kovid Ghiya : PES1UG23ME027 \n Shamant Nagabhushana : PES1UG23CS536 \n Samarth H : PES1UG23AM261")
   elif Q2==False:
      messagebox.showinfo("Thank You", "Thank you for playing and testing our game.")
   else:
      pass

def input_name_yellow():
    global PLAYER_YELLOW
    PLAYER_YELLOW = ENTRY_YELLOW.get()
    PLAYER_YELLOW = PLAYER_YELLOW.upper().strip()


def input_name_red():
    global PLAYER_RED
    PLAYER_RED = ENTRY_RED.get()
    PLAYER_RED = PLAYER_RED.upper().strip()

# Yellow Input
def yellow_input():
    LABEL1 = tk.Label(root, text="Yellow Player Name")
    LABEL1.grid(row=0, column=0, pady=5, padx=10)
    global ENTRY_YELLOW
    ENTRY_YELLOW = tk.Entry(root, width=20)
    ENTRY_YELLOW.grid(row=0, column=1, pady=5, padx=10)
    READY_YELLOW = tk.Button(root, text="Ready!", command=input_name_yellow)
    READY_YELLOW.grid(row=0, column=2, pady=5, padx=10)
    READY_YELLOW.bind('<Button-1>', red_input)
    menu_bar()
    root.mainloop()

# After name inputs have been taken
def contd(event):
    Q3=messagebox.askquestion("CONTINUE",'ARE YOU SURE YOU WANT TO CONTINUE?')
    if Q3=='yes':
        root.destroy()
        start_the_game()
    else:
        yellow_input()
    root.mainloop()

# Red Input
def red_input(event):
    LABEL2 = tk.Label(root, text="Red Player Name")
    LABEL2.grid(row=1, column=0, pady=5, padx=10)
    global ENTRY_RED
    ENTRY_RED = tk.Entry(root, width=20)
    ENTRY_RED.grid(row=1, column=1, pady=5, padx=10)
    READY_RED = tk.Button(root, text="Ready!", command=input_name_red)
    READY_RED.grid(row=1, column=2, pady=5, padx=10)
    READY_RED.bind('<Button-1>', lambda event: contd(event))
    root.mainloop()

def menu_bar():
    optionsmenu.add_command(label="New", command=donothing)
    optionsmenu.add_command(label="Open", command=donothing)
    optionsmenu.add_separator()
    optionsmenu.add_command(label="Exit", command=root.quit)
    
    menubar.add_cascade(label="Options", menu=optionsmenu)

    helpmenu.add_command(label="Help Index", command=help_index)
    helpmenu.add_command(label="About...", command=about)
    
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)
    root.mainloop()

def update_tally(winner, loser):
    player_found = False

    for row in DATA_:
        if row[0] == winner:
            player_found = True
            row[1] = str(int(row[1]) + 1)
            row[2] = loser
            break

    if not player_found:
        DATA_.append([winner, "1", loser])

    FILES_.seek(0)
    writer = csv.writer(FILES_)
    writer.writerows(DATA_)
    FILES_.truncate()

def yellow_winner_screen():
    update_tally(PLAYER_YELLOW, PLAYER_RED)
    WIN.blit(BACKGROUND, (0,0))
    winner_text=WINNER_FONT.render("THE YELLOW PLAYER IS THE WINNER!", 1, PURPLE)
    WINNER_SOUND.play()
    WIN.blit(winner_text, (100,210))
    pygame.display.update()

def red_winner_screen():
    update_tally(PLAYER_RED, PLAYER_YELLOW)
    WIN.blit(BACKGROUND, (0,0))
    winner_text=WINNER_FONT.render("THE RED PLAYER IS THE WINNER!", 1, PURPLE)
    WINNER_SOUND.play()
    WIN.blit(winner_text, (135, 210))
    pygame.display.update()

def play_again_screen():
    play_again_menu = pygame_menu.Menu('Play Again?', 900, 500, theme=themes.THEME_DARK)
    play_again_menu.add.button('Yes', start_the_game)
    play_again_menu.add.button('No', pygame_menu.events.EXIT)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        play_again_menu.update(events)
        play_again_menu.draw(WIN)
        pygame.display.update()

def start_the_game():
    winner = None
    red = pygame.Rect(750, 220, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 220, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_health = 10
    yellow_health = 10
    red_bullets = []
    yellow_bullets = []
    keys_pressed = pygame.key.get_pressed()

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LALT and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width - 11, yellow.y + yellow.height // 2 + 3, 20, 6)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x - 15, red.y + red.height // 2 + 4, 10, 6)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                if red_health == 0:
                    winner = "YELLOW"

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                if yellow_health == 0:
                    winner = "RED"

        if winner is not None:
            if winner == "YELLOW":
                yellow_winner_screen()
            elif winner == "RED":
                red_winner_screen()
            pygame.display.update()
            pygame.time.delay(3000)  # Winner screen time

            play_again_screen()

            # Reset game variables if the user chooses to play again
            winner = None
            red_health = 10
            yellow_health = 10
            red_bullets = []
            yellow_bullets = []

        else:
            draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
            yellow_movement(keys_pressed, yellow)
            red_movement(keys_pressed, red)
            handle_bullets(yellow, red, yellow_bullets, red_bullets)

    pygame.quit()

def stats():
    def read_csv(INPUT):
        data = []
        with open(INPUT, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        return data

    def display_csv_table(data, root):
        table = ttk.Treeview(root, show="headings", height=10)
        
        # Set up columns
        columns = data[0]
        table['columns'] = columns
        for col in columns:
            table.column(col, anchor='center', width=100)  # Adjust width as needed
            table.heading(col, text=col, anchor='center')

        # Insert data
        for row in data[1:]:
            table.insert("", "end", values=row)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))

        table.pack(padx=10, pady=10)

    if __name__ == "__main__":
        INPUT = abspath("C:\\Users\\shama\\GameProject\\Tally.csv")
        csv_data = read_csv(INPUT)
        display_csv_table(csv_data, root)

        root.mainloop()

def credits():
    credits_menu = pygame_menu.Menu('Credit Screen', 900, 500, theme=pygame_menu.themes.THEME_DARK)

    credits_text = [
        "PES  Python Project",
        "",
        "Developer-1: SHAMANT NAGABHUSHANA",
        "Developer-2: KOVID GHIYA",
        "Graphics & Game: SHAMANT NAGABHUSHANA",
        "Start Menu & Game Tally : KOVID GHIYA",
        "End Screen Menu : Co-Developed by SHAMANT AND KOVID"
        "",
        "BG Image, Spaceship Images : SELF DESIGNED",
        "",
        "Music : AUDIO FILES FROM INTERNET",
        "",
        "Special Thanks:",
        "    - Pygame Developers",
        "    - SHAMANT",
        "    - KOVID",
        "    - SATWIK",
        "    - SAMARTH",

    ]

    for line in credits_text:
        credits_menu.add.label(line, font_size=20, align=pygame_menu.locals.ALIGN_LEFT)

    credits_menu.add.button('Back', lambda: game_setup())

    credits_menu.mainloop(WIN)

def loading_screen():
    mainmenu._open(loading)
    pygame.time.set_timer(update_loading, 30) #Change loading screen time

def game_setup():
    mainmenu.add.button('Play', loading_screen)
    mainmenu.add.button('Player Stats', stats)
    mainmenu.add.button('Credits', credits)
    mainmenu.add.button('Quit', pygame_menu.events.EXIT)
    loading.add.progress_bar("Progress", progressbar_id = "1", default=0, width = 200, )

    arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == update_loading:
                progress = loading.get_widget("1")
                progress.set_value(progress.get_value() + 1)
                if progress.get_value() == 100:
                    pygame.time.set_timer(update_loading, 0)
                    mainmenu.disable()
                    yellow_input()
            if event.type == pygame.QUIT:
                exit()

        if mainmenu.is_enabled():
            mainmenu.update(events)
            mainmenu.draw(surface)
            if (mainmenu.get_current().get_selected_widget()):
                arrow.draw(surface, mainmenu.get_current().get_selected_widget())

        pygame.display.update()

if __name__ == "__main__":
    game_setup()