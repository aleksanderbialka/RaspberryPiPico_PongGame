from machine import Pin, SPI, ADC
import st7735
import utime
import urandom


# Konfiguracja SPI
spi = SPI(0, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))
dc = Pin(20, Pin.OUT)
rst = Pin(21, Pin.OUT)
cs = Pin(17, Pin.OUT)
bl = Pin(22, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_UP)  # Przycisk podłączony do GP14]
LED_single_player = Pin(13,Pin.OUT)

# Włączenie podświetlenia
bl.value(1)

# Inicjalizacja wyświetlacza
display = st7735.ST7735(spi, 130, 161, cs, dc, rst)
display.init()

# Wyczyszczenie ekranu na czarno
display.fill(0)

# Inicjalizacja potencjometrów
pot1 = ADC(Pin(26))  # GP26
pot2 = ADC(Pin(27))  # GP27

# Parametry gry
paddle_width = 5
paddle_height = 30
ball_size = 5
screen_width = 130
screen_height = 161
score_area_height = 10  # Wysokość obszaru wyświetlania punktów
game_area_height = screen_height - score_area_height  # Wysokość obszaru gry

# Pozycje startowe
paddle1_y = game_area_height // 2 - paddle_height // 2 + score_area_height
paddle2_y = game_area_height // 2 - paddle_height // 2 + score_area_height
ball_x = screen_width // 2
ball_y = game_area_height // 2 + score_area_height
ball_dx = urandom.choice([-2, 2])  # Losowy kierunek (-2 lub 2) dla osi x
ball_dy = urandom.choice([-2, 2])  # Losowy kierunek (-2 lub 2) dla osi y

# Punkty graczy
score1 = 0
score2 = 0
winning_score = 10

# Funkcja do rysowania prostokąta
def draw_rect(x, y, w, h, color):
    display.framebuf.fill_rect(x, y, w, h, color)

# Funkcja do czyszczenia prostokąta
def clear_rect(x, y, w, h):
    draw_rect(x, y, w, h, 0)
    
def draw_circle(x_center, y_center, radius, color):
    x = radius
    y = 0
    decision_over_2 = 1 - x  # Decision criterion divided by 2 evaluated at x=r, y=0

    while y <= x:
        display.framebuf.pixel(x_center + x, y_center + y, color)
        display.framebuf.pixel(x_center + y, y_center + x, color)
        display.framebuf.pixel(x_center - x, y_center + y, color)
        display.framebuf.pixel(x_center - y, y_center + x, color)
        display.framebuf.pixel(x_center - x, y_center - y, color)
        display.framebuf.pixel(x_center - y, y_center - x, color)
        display.framebuf.pixel(x_center + x, y_center - y, color)
        display.framebuf.pixel(x_center + y, y_center - x, color)
        y += 1
        if decision_over_2 <= 0:
            decision_over_2 += 2 * y + 1  # Change in decision criterion for y -> y+1
        else:
            x -= 1
            decision_over_2 += 2 * (y - x) + 1  # Change for y -> y+1, x -> x-1

# Funkcja do czyszczenia okręgu
def clear_circle(x_center, y_center, radius):
    draw_circle(x_center, y_center, radius, 0)

# Funkcja do wyświetlania tekstu
def show_text(text, x, y, color):
    display.framebuf.text(text, x, y, color)
    display.show()

# Funkcja sprawdzająca, czy ktoś wygrał
def check_winner():
    global score1, score2
    if score1 >= winning_score:
        display.fill(0)
        show_text("Gracz 1 wygrywa!", 10, 70, st7735.ST7735.color565(255, 255, 255))
        utime.sleep(2)
        return True
    elif score2 >= winning_score:
        display.fill(0)
        show_text("Gracz 2 wygrywa!", 10, 70, st7735.ST7735.color565(255, 255, 255))
        utime.sleep(2)
        return True
    return False

# Funkcja do resetowania gry
def reset_game():
    global paddle1_y, paddle2_y, ball_x, ball_y, ball_dx, ball_dy, score1, score2, game_started
    paddle1_y = game_area_height // 2 - paddle_height // 2 + score_area_height
    paddle2_y = game_area_height // 2 - paddle_height // 2 + score_area_height
    ball_x = screen_width // 2
    ball_y = game_area_height // 2 + score_area_height
    ball_dx = urandom.choice([-4, 6])  # Losowy kierunek (-2 lub 2) dla osi x
    ball_dy = urandom.choice([-4, 6])  # Losowy kierunek (-2 lub 2) dla osi y
    score1 = 0
    score2 = 0
    game_started = False


game_started = False

# Pozycje poprzednie
prev_paddle1_y = paddle1_y
prev_paddle2_y = paddle2_y
prev_ball_x = ball_x
prev_ball_y = ball_y


    

while True:
    if check_winner():
        display.fill(0)
        reset_game()

    # Sprawdzenie, czy przycisk został naciśnięty, aby rozpocząć grę
    if not game_started:
        show_text("PONG SW 2024", 15, 20, st7735.ST7735.color565(255, 255, 255))
        show_text("Gra do 10 pkt", 10, 45, st7735.ST7735.color565(255, 255, 255))
        show_text("LED ON - 1 os.", 5, 60, st7735.ST7735.color565(255, 255, 255))
        show_text("LED OFF - 2 os.", 5, 75, st7735.ST7735.color565(255, 255, 255))
        show_text("Przycisk start", 10, 110, st7735.ST7735.color565(255, 255, 255))
        show_text("--------->", 30, 125, st7735.ST7735.color565(255, 255, 255))
        # Sprawdzenie trybu gry na podstawie potencjometru
        single_player_mode = int(pot2.read_u16())<1000

        if single_player_mode:
            LED_single_player.value(1)
        else:
            LED_single_player.value(0)
        
    
        if button.value() == 0:  # Naciśnięty przycisk (przycisk wciśnięty do pinu)
            game_started = True
            display.fill(0)
            utime.sleep(0.2)  # Odczekaj krótki czas na uniknięcie przypadkowych naciśnięć

    if game_started:
        # Odczyt wartości potencjometrów
        paddle1_y = int(pot1.read_u16() / 65536 * (game_area_height - paddle_height)) + score_area_height
        if single_player_mode:
            # Aktualizacja pozycji paletki komputera
            if ball_y > paddle2_y + paddle_height // 2:
                paddle2_y = min(paddle2_y + 2, game_area_height - paddle_height + score_area_height)
            else:
                paddle2_y = max(paddle2_y - 2, score_area_height)
        else:
            # Odczyt wartości potencjometru dla drugiego gracza
            paddle2_y = int(pot2.read_u16() / 65536 * (game_area_height - paddle_height)) + score_area_height        
        
        
        ball_x += ball_dx
        ball_y += ball_dy


        # Odbicie piłki od ścian
        if ball_y <= score_area_height:
            ball_y = score_area_height
            ball_dy = -ball_dy
        elif ball_y >= screen_height - ball_size:
            ball_y = screen_height - ball_size
            ball_dy = -ball_dy

        if ball_x <= 0:
            score2 += 1
            ball_x = screen_width // 2
            ball_y = game_area_height // 2 + score_area_height
            ball_dx = urandom.choice([4, 6])  # Losowy kierunek (2 lub 3) dla osi x
            ball_dy = urandom.choice([4, 6])  # Losowy kierunek (2 lub 3) dla osi y
        elif ball_x >= screen_width - ball_size:
            score1 += 1
            ball_x = screen_width // 2
            ball_y = game_area_height // 2 + score_area_height
            ball_dx = urandom.choice([-4, -6])  # Losowy kierunek (-2 lub -3) dla osi x
            ball_dy = urandom.choice([-4, -6])  # Losowy kierunek (-2 lub -3) dla osi y
            
        # Odbicie piłki od paletek
        if (ball_x <= paddle_width+2 and paddle1_y <= ball_y <= paddle1_y + paddle_height) or \
           (ball_x >= screen_width - paddle_width - ball_size and paddle2_y <= ball_y <= paddle2_y + paddle_height):
            ball_dx = -ball_dx
            
        

        # Czyszczenie poprzednich pozycji
        clear_rect(2, prev_paddle1_y, paddle_width, paddle_height)
        clear_rect(screen_width - paddle_width, prev_paddle2_y, paddle_width, paddle_height)
        clear_circle(prev_ball_x, prev_ball_y, ball_size // 2)

        # Rysowanie nowych pozycji
        draw_rect(2, paddle1_y, paddle_width, paddle_height, st7735.ST7735.color565(255, 255, 255))
        draw_rect(screen_width - paddle_width, paddle2_y, paddle_width, paddle_height, st7735.ST7735.color565(255, 255, 255))
        draw_circle(ball_x, ball_y, ball_size // 2, st7735.ST7735.color565(255, 255, 255))
        
        display.framebuf.fill_rect(0, 0, screen_width, score_area_height, 0)  # Czyszczenie obszaru punktów
        display.framebuf.text("P1  "+str(score1)+ " : ", 15, 3, st7735.ST7735.color565(255, 255, 255))
        display.framebuf.text(str(score2)+"   P2", 75, 3, st7735.ST7735.color565(255, 255, 255))
        
        # Aktualizacja pozycji poprzednich
        prev_paddle1_y = paddle1_y
        prev_paddle2_y = paddle2_y
        prev_ball_x = ball_x
        prev_ball_y = ball_y

        # Wyświetlanie na ekranie
        display.show()

        # Opóźnienie
        utime.sleep(0.01)
