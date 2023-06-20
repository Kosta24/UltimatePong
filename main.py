"""Pong Game"""
import time
import pygame
import requests
import json


# Pannello su
def panelUp(panel, speed=False):  # Pannello e il tasto della velocità
    y = panel.y

    # Se ha raggiunto il bordo il pannello sta fermo
    if y <= 10:
        y = y
    elif speed:  # Se il tasto speed è premuto allora va più veloce
        y -= 16
    else:
        y -= 6

    panel.y = y


# Pannello giu
def panelDown(panel, speed=False):
    y = panel.y

    if y >= 490:
        y = y
    elif speed:
        y += 16
    else:
        y += 6

    panel.y = y


def refreshScreen():
    # Ridisegno le figure
    screen.fill(0)  # Ricolora tutta la finestra di nero per poter ridisegnare
    screen.blit(bg, (0, 0))
    pygame.draw.rect(screen, color, panel1)  # Disegno il pannello 1 nella finestra
    pygame.draw.rect(screen, color, panel2)  # Disegno il pannello 2 nella finestra
    #pygame.draw.rect(screen, color, ball)  # Disegno la palla nella finestra
    screen.blit(ice, (ball.x, ball.y))      # Disegno la palla nella finestra icecream

    screen.blit(text1, textSpace1)  # Disegno il punteggio del giocatore 1
    screen.blit(text2, textSpace2)  # Disegno il punteggio del giocatore 2
    screen.blit(text5_1, textSpace5_1)  # Disegno tutorial per l'abilita'
    screen.blit(text5_2, textSpace5_2)  # Disegno tutorial per l'abilita'
    screen.blit(text6, textSpace6)  # Disegno tutorial per l'abilita'
    screen.blit(font.render(f"{victory} points to win", True, color), textSpace8)  # Disegno tutorial per l'abilita'
    if f_pausa:
        screen.blit(text7, textSpace7)

    # Refresh della finestra, usare sempre se si fa qualche modifica
    pygame.display.flip()


# Resetta la posizione della palla quando si segna un punto
def ballReset():
    global ball_speed
    global default_ball_speed
    global ball
    global screen
    ball.x = screen.get_width() // 2  # La larghezza dello schermo / 2
    ball.y = screen.get_height() // 2  # La lunghezza dello schermo / 2
    ball_speed = default_ball_speed
    refreshScreen()
    time.sleep(0.5)


# Resetta tutto quando si ricomincia il gioco
def refreshAll():
    global panel1
    global panel2
    global ball
    global punti1
    global punti2
    global text1
    global text2
    panel1.x = 10
    panel1.y = 250
    panel2.x = 770
    panel2.y = 250
    ball.x = screen.get_width() // 2
    ball.y = screen.get_height() // 2
    punti1 = 0
    punti2 = 0
    text1 = font.render(f" {punti1}", True, color)
    text2 = font.render(f" {punti2}", True, color)
    win.stop()
    background.stop()
    background.play()


# Inizializza i metodi di pygame, da fare sempre
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

wh00k = "https://discord.com/api/webhooks/1120729759991734432/qjcefKi5bxnXd4B0NweBs3Ne1BY0BhknfSgjRCw2wqbr_YTG0NLofQ7bVH8kANbA2qbv"

bg = pygame.image.load("Assets/THE_BACKGROUND.png")
win_bg = pygame.image.load("Assets/THE_WIN_BACKGROUND.png")
ice = pygame.image.load("Assets/ice.png")

sound = pygame.mixer.Sound("Music/bingchiling.wav")
background = pygame.mixer.Sound("Music/AlternativeTetrisTheme.wav")
point1_sound = pygame.mixer.Sound("Music/Doit.wav")
point2_sound = pygame.mixer.Sound("Music/Koioshi.wav")

win = pygame.mixer.Sound("Music/win.wav")
win.set_volume(0.3)

sound.set_volume(0.3)
point1_sound.set_volume(0.8)
point2_sound.set_volume(1)
background.set_volume(0.1)
background.play(-1)

image = pygame.image.load("Assets/pong.jpg")
# Crea lo schermo e imposto titolo
# Da sinistra a destra x, 0 - 800
# Da sopra a sotto y, 0 - 600
screen = pygame.display.set_mode((800, 600))  # Creo la finestra (width, lenght)
pygame.display.set_caption("Ping Pong Ching Chong")  # Imposto il titolo della finestra
pygame.display.set_icon(image)



size = 20  # Grandezza in pixel
color = (255, 217, 0)  # Colore verde chiaro (127, 255, 0)

# Creazione pannelli e palla (x, y, width, length)
panel1 = pygame.Rect(10, 250, size, 100)
panel2 = pygame.Rect(770, 250, size, 100)
ball = pygame.Rect(screen.get_width() // 2, screen.get_height() // 2, size, size)
#ice = picture = pygame.transform.scale(ice, (size, size))

# I punti dei giocatori
punti1 = 0
punti2 = 0
victory = 0
# Creo lo spazio per il punteggio
font = pygame.font.SysFont("powergreen", 26)  # Impostazione font e grandezza

text1 = font.render(f" {punti1}", True, color)  # Impostazione testo
textSpace1 = text1.get_rect()  # Creo lo spazio fisico per il testo
textSpace1.center = (120, 30)  # Posizionamento test (x, y)

text2 = font.render(f" {punti2}", True, color)
textSpace2 = text2.get_rect()
textSpace2.center = (screen.get_width() - 120, 30)

text3_1 = font.render("Player 1 Wins!", True, color)
textSpace3_1 = text3_1.get_rect()
textSpace3_1.center = (screen.get_width() // 2, 30)#screen.get_height() // 5

text3_2 = font.render("Player 2 Wins!", True, color)
textSpace3_2 = text3_2.get_rect()
textSpace3_2.center = (screen.get_width() // 2, 30)

text4 = font.render("Press Space to Restart or Enter to close the Window", True, color)
textSpace4 = text4.get_rect()
textSpace4.center = (screen.get_width() // 2, 60)  # Posizionamento

text5_1 = font.render("E to speed", True, color)
textSpace5_1 = text5_1.get_rect()
textSpace5_1.center = (80, 570)

text5_2 = font.render("0 to speed", True, color)
textSpace5_2 = text5_2.get_rect()
textSpace5_2.center = (720, 570)

text6 = font.render("Press R to Reset", True, color)
textSpace6 = text6.get_rect()
textSpace6.center = (screen.get_width() // 2, 30)

text7 = pygame.font.SysFont("powergreen", 157).render("Pause", True, color)
textSpace7 = text7.get_rect()
textSpace7.center = (screen.get_width() // 2+5, screen.get_height() // 2 - 20)

text8 = font.render(f"{victory} points to win", True, color)
textSpace8 = text8.get_rect()
textSpace8.center = (screen.get_width() // 2, screen.get_height() -30)

# Movimento della palla e velocità dei pannelli
default_ball_speed = 2
ball_speed = default_ball_speed
mov_ball = [ball_speed, ball_speed]
max_ball_speed = 12
victory = 5
# vel_pan = 1


ultraFlag = True

payload = {
        'content': "player x scored"
    }

headers = {
    'Content-Type': 'application/json'
}
# Ciclo gioco
game = True
f_pausa = False
copy_ball = [0, 0]
FPS = 80
i = FPS
while game:
    key_other = pygame.key.get_pressed()  # Controllo tasti tastiera

    # Uscita dal gioco se premo il tasto Esc
    if key_other[pygame.K_ESCAPE]:
        game = False

    # Resetta tutto se si prema il tasto Backspace
    if key_other[pygame.K_r]:
        refreshAll()

    if i < FPS//4:
        i += 1
    else:
        if key_other[pygame.K_p]:
            i = 0
            if f_pausa:
                background.play()
                mov_ball = copy_ball
                f_pausa = False
            else:
                background.stop()
                f_pausa = True
                copy_ball = mov_ball
                mov_ball = [0, 0]

    refreshScreen()
    if mov_ball != [0, 0]:
        mov_ball = [ball_speed * (mov_ball[0] // (abs(mov_ball[0]))), ball_speed * (mov_ball[1] // (abs(mov_ball[1])))]

    # Se si viene cliccata la X della finestra il programma chiude
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            game = False

    # Prende tutti i tasti premuti
    keys1 = pygame.key.get_pressed()  # Per il pannello 1
    keys2 = pygame.key.get_pressed()  # Per il pannello 2

    # Movimento della palla
    ball.x += mov_ball[0]
    ball.y += mov_ball[1]

    # Movimento pannelli
    # panel1.y += (keys[pygame.K_s] - keys[pygame.K_w]) * vel_pan
    # panel2.y += (keys1[pygame.K_DOWN] - keys1[pygame.K_UP]) * vel_pan

    # Movimento pannelli con controllo dell'abilita'
    if keys1[pygame.K_w]:
        panelUp(panel1, keys1[pygame.K_e])

    if keys1[pygame.K_s]:
        panelDown(panel1, keys1[pygame.K_e])

    if keys2[pygame.K_UP]:
        panelUp(panel2, keys2[pygame.K_KP0])

    if keys2[pygame.K_DOWN]:
        panelDown(panel2, keys2[pygame.K_KP0])

    # Quando la palla colpisce i due pannelli
    if ball.colliderect(panel1):
        if (ball.y - 20) < panel1.y:
            if ball.x <= (panel1.x + 12):
                ball.x = - size
            else:
                ball.x = panel1.x + 22
                sound.play()
                mov_ball[0] *= -1
                if ball_speed < max_ball_speed:
                    ball_speed += 1
        # Player is below
        elif (ball.y + 20) > (panel1.y + 100):
            if ball.x <= (panel1.x + 12):
                ball.x = - size
            else:
                ball.x = panel1.x + 22
                sound.play()
                mov_ball[0] *= -1
                if ball_speed < max_ball_speed:
                    ball_speed += 1
        else:
            sound.play()
            mov_ball[0] *= -1
            if ball_speed < max_ball_speed:
                ball_speed += 1

    if ball.colliderect(panel2):
        if (ball.y - 20) < panel2.y:
            if (ball.x + 8) >= panel2.x:
                ball.x = screen.get_width() + size
            else:
                ball.x = panel2.x - 22
                sound.play()
                mov_ball[0] *= -1
                if ball_speed < max_ball_speed:
                    ball_speed += 1
        # Player is below
        elif (ball.y + 20) > (panel2.y + 100):
            if (ball.x + 8) >= panel2.x:
                ball.x = screen.get_width() + size

            else:
                ball.x = panel2.x - 22
                sound.play()
                mov_ball[0] *= -1
                if ball_speed < max_ball_speed:
                    ball_speed += 1
        else:
            sound.play()
            mov_ball[0] *= -1
            if ball_speed < max_ball_speed:
                ball_speed += 1

    # Quando la palla colpisce la parte superiore e inferiore
    if ball.y + size >= screen.get_height():
        mov_ball[1] *= -1  # Quando colpisce il bordo va all'indietro quindi la coordinata y s'inverte

    if ball.y <= 0:
        mov_ball[1] *= -1

    if (punti2 == (victory - 1)) and punti1 == punti2:
        victory += 1

    # Quando colpisce le parti laterali
    if ball.x + size >= screen.get_width():
        point1_sound.play()
        punti1 += 1  # Aumento dei punti del giocatore
        if ultraFlag:
            ultraFlag = 0
            r =  requests.post(wh00k, data=json.dumps(payload), headers=headers)



        if punti1 == victory:  # Vittoria 1
            # Faccio comparire la scritta della vittoria
            screen.fill(0)
            background.stop()
            win.play()
            screen.blit(win_bg, (0, 0))
            screen.blit(text3_1, textSpace3_1)
            screen.blit(text4, textSpace4)
            # Refresh della finestra
            pygame.display.flip()


            # Controllo gaming
            while game:
                # Ottengo i pulsanti  premuti
                endGet = pygame.event.get()
                endKey = pygame.key.get_pressed()
                # Se viene premuto Space si ricomincia il gioco, Enter esce
                if endKey[pygame.K_SPACE]:
                    refreshAll()
                    break
                if endKey[pygame.K_RETURN]:
                    game = False

                if endKey[pygame.K_ESCAPE]:
                    game = False
                # Se si viene cliccata la X della finestra il programma chiude
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        game = False

                for prova in events:
                    if prova.type == pygame.QUIT:
                        game = False
        else:
            ballReset()  # Il giocatore segna un punto quindi la palla torna indietro
        # Aggiorno il testo del punteggio
        text1 = font.render(f" {punti1}", True, color)

    #giocatore 2 segna punto
    if ball.x <= 0:
        point2_sound.play()
        punti2 += 1
        if ultraFlag:
            ultraFlag = 0
            r =  requests.post(wh00k, data=json.dumps(payload), headers=headers)

        if punti2 == victory:  # Vittoria 2
            screen.fill(0)
            background.stop()
            win.play()
            screen.blit(win_bg, (0, 0))
            screen.blit(text3_2, textSpace3_2)
            screen.blit(text4, textSpace4)
            # Refresh della finestra
            pygame.display.flip()

            # Controllo tastiera
            while game:
                endGet = pygame.event.get()
                endKey = pygame.key.get_pressed()
                if endKey[pygame.K_SPACE]:
                    refreshAll()
                    break
                if endKey[pygame.K_RETURN]:
                    game = False
                if endKey[pygame.K_ESCAPE]:
                    game = False
                # Se si viene cliccata la X della finestra il programma chiude
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        game = False

                for prova in events:
                    if prova.type == pygame.QUIT:
                        game = False
        else:
            ballReset()
        text2 = font.render(f" {punti2}", True, color)

    pygame.time.Clock().tick(FPS)
# Esco dal pygame
pygame.quit()