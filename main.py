import pygame
import time
import random
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load('music.mp3')  
pygame.mixer.music.play(-1) 
pygame.mixer.music.set_volume(0.2) 

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maths en jeux 2024")

a = random.randint(1,15)
b = random.randint(1,15)
invulnerable_until = 0



BG = pygame.transform.scale(pygame.image.load("brick wall.jpeg"), (WIDTH, HEIGHT))
PLAYER_SPRITE = pygame.image.load("bigbigplayer.png")
MATH_SPRITE = pygame.image.load("star.png")
STAR_SPRITE = pygame.image.load("arrow.png")
PLAYERINV_SPRITE = pygame.image.load("playerinv.png")

PLAYER_WIDTH = PLAYER_SPRITE.get_width()
PLAYER_HEIGHT = PLAYER_SPRITE.get_height()
PLAYER_VEL = 12

STAR_WIDTH = 9
STAR_HEIGHT = 30
STAR_VEL = 17

MATH_RECT_WIDTH = MATH_SPRITE.get_width()
MATH_RECT_HEIGHT = MATH_SPRITE.get_height()
MATH_RECT_VEL = 8
MATH_RECT_ADD_INCREMENT = 10000

current_player_sprite = PLAYER_SPRITE

FONT = pygame.font.SysFont("comicsans", 30)

def draw_problem(problem_text):
    problem_surface = FONT.render(problem_text, True, "white")
    WIN.blit(problem_surface, (WIDTH/2, HEIGHT / 2.3))
    pygame.display.update()

def get_answer():
    a = random.randint(1,15)
    b = random.randint(1,15)
    answer = ""
    input_box = pygame.Rect(WIDTH/2, HEIGHT/2, 32, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_active
    active = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, a, b
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        try:
                            return int(answer), a, b
                        except ValueError:
                            return None, a, b
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        answer = answer[:-1]
                    else:
                        answer += event.unicode

        draw_problem(f"What is {a} * {b}?")
        char_surface = FONT.render(answer, True, color)
        width = max(200, char_surface.get_width()+10)
        input_box.w = width
        x_offset = 80
        for char in answer:
            char_surface = FONT.render(char, True, color)
            WIN.blit(char_surface, (input_box.x + x_offset, input_box.y + input_box.h/2 - char_surface.get_height()/2))
            x_offset += char_surface.get_width() + 2
            
        pygame.draw.rect(WIN, color, input_box, 2)
        pygame.display.flip()
        pygame.draw.rect(WIN, color, input_box, 2)
        pygame.display.flip()

def draw(player, elapsed_time, stars, math_rects, invulnerable_until):
    WIN.fill((0, 0, 0))  
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, (255, 255, 255))
    WIN.blit(time_text, (10, 10))
    
    if time.time() < invulnerable_until:
        WIN.blit(PLAYERINV_SPRITE, (player.x, player.y))
    else:
        WIN.blit(PLAYER_SPRITE, (player.x, player.y))
    
    for star in stars:
        WIN.blit(STAR_SPRITE, (star.x, star.y))

    for math_rect in math_rects:
        WIN.blit(MATH_SPRITE, (math_rect.x, math_rect.y))
    
    pygame.display.update()

def main():
    run = True
    math_rects = [pygame.Rect(200, 200, MATH_RECT_WIDTH, MATH_RECT_HEIGHT)]
    
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    invulnerable_until = 0
    star_add_increment = 2000
    star_count = 0

    math_rect_count = 0

    stars = []
    hit = False

    

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        math_rect_count += clock.tick(60)
        if math_rect_count > MATH_RECT_ADD_INCREMENT:
            math_rect_x = random.randint(0, WIDTH - MATH_RECT_WIDTH)
            math_rect = pygame.Rect(math_rect_x, -MATH_RECT_HEIGHT, MATH_RECT_WIDTH, MATH_RECT_HEIGHT)
            math_rects.append(math_rect) 
            math_rect_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif time.time() > invulnerable_until and star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break
       
        if hit and time.time() > invulnerable_until:
            lost_text = FONT.render("You lost!", 1, "white")
            score_text = FONT.render(f"You survived {int(elapsed_time)} seconds", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            WIN.blit(score_text, (WIDTH/1.65 - score_text.get_width()/1.3, HEIGHT/1.7 - score_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(3000)
            break

        for math_rect in math_rects.copy():
            WIN.blit(MATH_SPRITE, (math_rect.x, math_rect.y))
            math_rect.y += MATH_RECT_VEL
            if math_rect.y > HEIGHT:
                math_rects.remove(math_rect)
            elif time.time() > invulnerable_until and math_rect.y + math_rect.height >= player.y and math_rect.colliderect(player):
                math_rects.remove(math_rect)
                start_problem_time = time.time()  
                answer, a, b = get_answer()
                end_problem_time = time.time()  
                problem_duration = end_problem_time - start_problem_time  
                start_time += problem_duration  
                if answer == "QUIT":
                    break
                elif answer is None or answer != a * b:
                    font = pygame.font.Font(None, 36)
                    lost_text = FONT.render(f"Wrong! The answer was {a*b}", 1, "white")
                    score_text = FONT.render(f"You survived {int(elapsed_time)} seconds", 1, "white")
                    WIN.blit(lost_text, (WIDTH/1.65 - lost_text.get_width()/2, HEIGHT/1.7 - lost_text.get_height()/2))
                    WIN.blit(score_text, (WIDTH/1.65 - score_text.get_width()/2, HEIGHT/1.5 - score_text.get_height()/2))
                    pygame.display.update()
                    pygame.time.delay(3000)
                    run = False
                    break
                else : 
                    invulnerable_until = time.time() + 5
               
                
              
        draw(player, elapsed_time, stars, math_rects, invulnerable_until)
            
    pygame.quit()

if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
