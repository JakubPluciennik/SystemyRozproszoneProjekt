import pygame, sys
import json
#from rabbitmq_client import client_loop
from button import Button
from random import randint
from pika import BlockingConnection, ConnectionParameters
from rabbitmq_client_game import client_loop

ROW_COUNT = 6
COLUMN_COUNT = 7

# kolory
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

SQUARE_SIZE = 100

# dane do wyznaczenia rozmiaru okna
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT+1) * SQUARE_SIZE
size = (width, height) # okno 700x700


RADIUS = int(SQUARE_SIZE/2 - 5)

pygame.init()
SCREEN = pygame.display.set_mode(size)
pygame.display.set_caption("Menu")

def get_font(size): 
    return pygame.font.SysFont('Comic Sans MS', size)


def wynikGry_menu(ktoWygral : str, ktoGraNaTymKompie : str): 
    pygame.display.set_caption("Menu - Utwórz sesję")
    
    while True: 
        SCREEN.fill("blue") # czarne tło    
        # potencjalne napisy do wyświetlenia -> wyświetlony zostanie tylko jeden zależnie od wyniku gry
        WYGRANA_TEXT = get_font(80).render("Wygrałeś!", True, "#00ff00") # na zielono
        WYGRANA_RECT = WYGRANA_TEXT.get_rect(center=(350, 100))

        PRZEGRANA_TEXT = get_font(80).render("Przegrałeś!", True, "#ff0000") # na czerwono
        PRZEGRANA_RECT = PRZEGRANA_TEXT.get_rect(center=(350, 100))
        
        REMIS_TEXT = get_font(80).render("Remis!", True, "#ffff00") # na żółto
        REMIS_RECT = REMIS_TEXT.get_rect(center=(350, 100))

        # przycisk powrotu do menu
        WROCDOMENU_BUTTON = Button(image=None, pos=(350, 650), text_input="Wróć do menu", font=get_font(50),
                                    base_color="#d7fcd4", hovering_color="White")

        if ktoWygral == "Wygrał gracz X":
            # wygrał gracz 1 a gracz 2 przegrał
            if ktoGraNaTymKompie == '1':
                SCREEN.blit(WYGRANA_TEXT, WYGRANA_RECT)
            else: 
                SCREEN.blit(PRZEGRANA_TEXT, PRZEGRANA_RECT)
        elif ktoWygral == "Wygrał gracz O":
            if ktoGraNaTymKompie =='2': 
                SCREEN.blit(WYGRANA_TEXT, WYGRANA_RECT)
            else: 
                SCREEN.blit(PRZEGRANA_TEXT, PRZEGRANA_RECT)
            # wygrał gracz 2 a gracz 1 przegrał
        else: 
            # remis
            SCREEN.blit(REMIS_TEXT, REMIS_RECT)
        
        pygame.display.update()
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        for button in [WROCDOMENU_BUTTON]: 
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if WROCDOMENU_BUTTON.chechForInput(MENU_MOUSE_POS):
                    main_menu()
        
        pygame.display.update()
    

# ta funkcja odpowiada jakby funkcji graczX z client.py
def utworzSesje_menu(): 
    pygame.display.set_caption("Menu - Utwórz sesję")
    id = randint(1000, 9999) # numer sesji
    zmienna = True
    while zmienna: 

        SCREEN.fill("black") # czarne tło
        # zmienne potrzebne dalej
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(80).render("Tworzenie sesji", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(350, 100))

        # 1) tutaj trzeba wypisać losowo wygenerowany numer sesji
        # 2) Potem trzeba to będzie powiązać z systemem komunikatów
        # 
        # póki co będzie tu tylko wychodzenie z powrotem do menu gry oraz wypisywanie losowego numeru (1000,9999)
        

        SESJA_TEXT = get_font(60).render(f"Numer sesji: {id}", True, "#ff0505")
        SESJA_RECT = SESJA_TEXT.get_rect(center=(350, 350))
        WROCDOMENU_BUTTON = Button(image=None, pos=(350, 650), text_input="Wróć", font=get_font(50),
                                    base_color="#d7fcd4", hovering_color="White")

        OCZEKUJ_BUTTON = Button(image=None, pos=(350, 550), text_input="Oczekuj", font=get_font(50),
                                    base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(SESJA_TEXT, SESJA_RECT)
        for button in [OCZEKUJ_BUTTON, WROCDOMENU_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        # trzeba jeszcze wypisać nr. sesji
        # obsługa eventów pygame
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if OCZEKUJ_BUTTON.chechForInput(MENU_MOUSE_POS): 
                    zmienna = False
                if WROCDOMENU_BUTTON.chechForInput(MENU_MOUSE_POS):
                    main_menu()

        pygame.display.update()

    
    gracz = 1
    message = {
        "id": id,
        "gracz": gracz
    }
    id = str(id)
    # konwertowanie wiadomości do JSON
    message = json.dumps(message)
    # wysłanie wiadomości do kolejki
    channel.basic_publish(exchange="main_exchange",
                          routing_key="",
                          body=message)
    client_loop(id, gracz, SCREEN)


def dolaczDoSesji_menu(): 
    # przy wysyłaniu numeru sesji trzeba będzie przekonwertować inputID na int
    pygame.display.set_caption("Menu - Dołącz do sesji")
    zmienna = True


    textInput_font = pygame.font.Font(None, 32)
    inputID = ''
    input_rect = pygame.Rect(250, 250, 200, 32)
    inputColorActive = pygame.Color('lightskyblue3')
    inputColorPassive = pygame.Color('gray15')
    inputColor = inputColorPassive

    input_active = False
    while zmienna: 
        SCREEN.fill("black") # czarne tło
        # zmienne potrzebne dalej
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(60).render("Podaj numer sesji:", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(350, 100))

        TIP_TEXT = get_font(50).render("(1000 - 9999)", True, "#b68f40")
        TIP_RECT = MENU_TEXT.get_rect(center=(350, 160))
        
        # przyciski
        POLACZ_BUTTON = Button(image=None, pos=(350, 550), text_input="Połącz", font=get_font(50),
                                    base_color="#d7fcd4", hovering_color="White")

        WROCDOMENU_BUTTON = Button(image=None, pos=(350, 650), text_input="Wróć", font=get_font(50),
                                    base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(TIP_TEXT, TIP_RECT)

        input_surface = textInput_font.render(inputID, True, WHITE)
        SCREEN.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

        pygame.draw.rect(SCREEN, inputColor, input_rect, 2)
        for button in [POLACZ_BUTTON, WROCDOMENU_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # obsługa eventów pygame
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN: 
                if input_active == True: 
                    if event.key == pygame.K_BACKSPACE:
                        inputID = inputID[:-1] # odjęcie ostatniego znaku
                    else: 
                        inputID += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    input_active = True
                else: 
                    input_active = False

                if POLACZ_BUTTON.chechForInput(MENU_MOUSE_POS):
                    # tutaj trzeba łączyć gracza -> tak jakby graczO() i przechodzić do gry
                    zmienna = False
                
                if WROCDOMENU_BUTTON.chechForInput(MENU_MOUSE_POS):
                    main_menu()

        if input_active: 
            inputColor = inputColorActive
        else: 
            inputColor = inputColorPassive
        
        pygame.display.update()

    gracz = 2
    id = inputID
    message = {
        "id": int(id),
        "gracz": gracz
    }
    # konwertowanie wiadomości do JSON
    message = json.dumps(message)
    # wysłanie wiadomości do kolejki
    channel.basic_publish(exchange="main_exchange",
                          routing_key="",
                          body=message)
    
    client_loop(id, gracz, SCREEN)

        

def main_menu(): 
    pygame.display.set_caption("Menu")
    global channel
    while True: 

        # połączenie
        host = "localhost"    # Hostname
        connection = BlockingConnection(ConnectionParameters(host,heartbeat=0))
        channel = connection.channel()
        q_name = "main_queue"
        # --- konfiguracja kanału odbierającego ---
        channel.exchange_declare(exchange="main_exchange",
                             exchange_type="fanout")
        result = channel.queue_declare(queue=q_name,
                                   durable=True)
        channel.queue_bind(exchange="main_exchange", queue=q_name)

        # teraz elementy gry
        SCREEN.fill("black") # czarne tło
        # zmienne potrzebne dalej
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(80).render("Menu główne", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(350, 100))

        UTWORZSESJE_BUTTON = Button(image=None, pos=(350, 250), text_input="Utwórz sesję", font=get_font(50),
                                    base_color="#d7fcd4", hovering_color="White")

        DOLACZDOSESJI_BUTTON = Button(image=None, pos=(350, 450), text_input="Dołącz do sesji", font=get_font(50),
                                    base_color="#d7fcd4", hovering_color="White")
        
        WYJDZZGRY_BUTTON = Button(image=None, pos=(350, 650), text_input="Wyjdź z gry", font=get_font(50),
                                    base_color="#d7fcd4", hovering_color="White")

        # ustawienie napisu "Menu główne na ekranie"
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # aktualizowanie przycisków zależnie od tego czy kursor myszki znajduje się na nich czy nie
        for button in [UTWORZSESJE_BUTTON, DOLACZDOSESJI_BUTTON, WYJDZZGRY_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if UTWORZSESJE_BUTTON.chechForInput(MENU_MOUSE_POS):
                    utworzSesje_menu()

                if DOLACZDOSESJI_BUTTON.chechForInput(MENU_MOUSE_POS):
                    dolaczDoSesji_menu()

                if WYJDZZGRY_BUTTON.chechForInput(MENU_MOUSE_POS):
                    channel.close()
                    connection.close()
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()


main_menu()    