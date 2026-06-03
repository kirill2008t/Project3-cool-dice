import pygame
import random
import sys
import math

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cooldice - Бросай кубик!")

icon_surface = pygame.Surface((32, 32))
icon_surface.fill((255, 255, 255))
pygame.draw.rect(icon_surface, (50, 50, 50), (4, 4, 24, 24), 2)
dot_positions = [(16, 16)]
for pos in dot_positions:
    pygame.draw.circle(icon_surface, (0, 0, 0), pos, 3)
pygame.display.set_icon(icon_surface)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (76, 175, 80)
DARK_GREEN = (56, 135, 60)
BLUE = (33, 150, 243)
PURPLE = (156, 39, 176)
ORANGE = (255, 152, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GOLD = (255, 215, 0)
YELLOW = (255, 235, 59)
PINK = (233, 30, 99)

font_title = pygame.font.Font(None, 72)
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

animation_progress = 0
is_rolling = False
roll_start_time = 0
ROLL_ANIMATION_DURATION = 500
dice_value = None
result_text = "Нажми кнопку, чтобы бросить кубик!"
rolling_values = []

DICE_SIZE = 150
DICE_X = WIDTH // 2 - DICE_SIZE // 2
DICE_Y = HEIGHT // 2 - DICE_SIZE // 2 - 30

button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 120, 200, 60)
button_hover = False

def draw_gradient():
    for y in range(HEIGHT):
        color_value = 100 + int(155 * (y / HEIGHT))
        color = (color_value, 180, 230)
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

def draw_dice_face(value, x, y, size=150, rotation_angle=0, scale=1.0):
    actual_size = int(size * scale)
    
    dice_surface = pygame.Surface((actual_size, actual_size), pygame.SRCALPHA)
    
    shadow_offset = max(3, int(5 * scale))
    shadow_alpha = int(80 * scale)
    shadow_surface = pygame.Surface((actual_size, actual_size), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surface, (0, 0, 0, shadow_alpha), 
                    (shadow_offset, shadow_offset, actual_size, actual_size), 
                    border_radius=int(20 * scale))
    
    pygame.draw.rect(dice_surface, WHITE, (0, 0, actual_size, actual_size), 
                    border_radius=int(20 * scale))
    pygame.draw.rect(dice_surface, DARK_GRAY, (0, 0, actual_size, actual_size), 
                    max(2, int(3 * scale)), border_radius=int(20 * scale))
    
    dot_radius = max(5, actual_size // 12)
    dot_color = BLACK
    positions = {
        1: [(actual_size//2, actual_size//2)],
        2: [(actual_size//4, actual_size//4), (3*actual_size//4, 3*actual_size//4)],
        3: [(actual_size//4, actual_size//4), (actual_size//2, actual_size//2), 
            (3*actual_size//4, 3*actual_size//4)],
        4: [(actual_size//4, actual_size//4), (3*actual_size//4, actual_size//4), 
            (actual_size//4, 3*actual_size//4), (3*actual_size//4, 3*actual_size//4)],
        5: [(actual_size//4, actual_size//4), (3*actual_size//4, actual_size//4), 
            (actual_size//2, actual_size//2),
            (actual_size//4, 3*actual_size//4), (3*actual_size//4, 3*actual_size//4)],
        6: [(actual_size//4, actual_size//4), (3*actual_size//4, actual_size//4),
            (actual_size//4, actual_size//2), (3*actual_size//4, actual_size//2),
            (actual_size//4, 3*actual_size//4), (3*actual_size//4, 3*actual_size//4)]
    }
    
    for pos in positions.get(value, []):
        pygame.draw.circle(dice_surface, dot_color, pos, dot_radius)
        if dot_radius > 3:
            pygame.draw.circle(dice_surface, (220, 220, 220), 
                              (pos[0]-dot_radius//3, pos[1]-dot_radius//3), 
                              max(2, dot_radius//3))
    
    screen.blit(shadow_surface, (x, y))
    
    if rotation_angle != 0:
        rotated_surface = pygame.transform.rotate(dice_surface, rotation_angle)
        rect = rotated_surface.get_rect(center=(x + actual_size//2, y + actual_size//2))
        screen.blit(rotated_surface, rect.topleft)
    else:
        screen.blit(dice_surface, (x, y))

def draw_button():
    global button_hover
    
    mouse_pos = pygame.mouse.get_pos()
    button_hover = button_rect.collidepoint(mouse_pos)
    
    if button_hover:
        btn_color = DARK_GREEN
        shadow_offset = 2
        pulse = math.sin(pygame.time.get_ticks() * 0.008) * 0.1 + 0.9
    else:
        btn_color = GREEN
        shadow_offset = 4
        pulse = 1.0
    
    pygame.draw.rect(screen, DARK_GRAY, 
                    (button_rect.x + shadow_offset, button_rect.y + shadow_offset, 
                     button_rect.width, button_rect.height), 
                    border_radius=15)
    
    if pulse != 1.0:
        btn_color = tuple(int(c * pulse) for c in btn_color)
    
    pygame.draw.rect(screen, btn_color, button_rect, border_radius=15)
    pygame.draw.rect(screen, GOLD, button_rect, 2, border_radius=15)
    
    button_text = font_medium.render("Бросить кубик!", True, WHITE)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

def draw_particles():
    if is_rolling:
        center_x = WIDTH // 2
        center_y = HEIGHT // 2 - 30
        for i in range(30):
            angle = random.randint(0, 360)
            radius = 120 + int(math.sin(animation_progress * math.pi * 4 + i) * 30)
            x = center_x + math.cos(math.radians(angle + animation_progress * 20)) * radius
            y = center_y + math.sin(math.radians(angle + animation_progress * 20)) * radius
            colors = [GOLD, ORANGE, YELLOW, PINK]
            color = colors[i % len(colors)]
            size = random.randint(2, 5)
            pygame.draw.circle(screen, color, (int(x), int(y)), size)
            
            tail_x = int(x - math.cos(math.radians(angle + animation_progress * 20)) * 10)
            tail_y = int(y - math.sin(math.radians(angle + animation_progress * 20)) * 10)
            pygame.draw.line(screen, color, (int(x), int(y)), (tail_x, tail_y), 2)

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60)
    
    if is_rolling:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - roll_start_time
        
        if elapsed >= ROLL_ANIMATION_DURATION:
            is_rolling = False
            dice_value = rolling_values[-1] if rolling_values else random.randint(1, 6)
            result_text = f"Выпало {dice_value}!"
            
            flash_surface = pygame.Surface((WIDTH, HEIGHT))
            flash_surface.fill(WHITE)
            flash_surface.set_alpha(180)
            screen.blit(flash_surface, (0, 0))
            pygame.display.flip()
            pygame.time.wait(50)
        else:
            animation_progress = elapsed / ROLL_ANIMATION_DURATION
            if elapsed % 50 < 16:
                rolling_values.append(random.randint(1, 6))
                if len(rolling_values) > 10:
                    rolling_values.pop(0)
    
    draw_gradient()
    
    title_shadow = font_title.render("COOLDICE", True, DARK_GRAY)
    title_text = font_title.render("COOLDICE", True, PURPLE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 60))
    screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
    screen.blit(title_text, title_rect)
    
    if is_rolling:
        scale = 1 + math.sin(animation_progress * math.pi) * 0.15
        angle = animation_progress * 360 * 1.5
        current_dice = rolling_values[-1] if rolling_values else random.randint(1, 6)
        
        draw_dice_face(current_dice, DICE_X, DICE_Y, DICE_SIZE, angle, scale)
        draw_particles()
        
        anim_text = font_medium.render("Бросаем!", True, ORANGE)
        anim_rect = anim_text.get_rect(center=(WIDTH // 2, DICE_Y + DICE_SIZE + 40))
        screen.blit(anim_text, anim_rect)
        
    elif dice_value:
        draw_dice_face(dice_value, DICE_X, DICE_Y, DICE_SIZE)
        
        pulse = math.sin(pygame.time.get_ticks() * 0.005) * 0.15 + 0.85
        
        if dice_value == 6:
            result_color = GOLD
        elif dice_value == 1:
            result_color = ORANGE
        else:
            result_color = BLUE
        
        result_surface = font_large.render(result_text, True, result_color)
        result_rect = result_surface.get_rect(center=(WIDTH // 2, DICE_Y + DICE_SIZE + 40))
        screen.blit(result_surface, result_rect)
        
        glow_surface = font_large.render(result_text, True, GOLD)
        glow_surface.set_alpha(40)
        glow_rect = glow_surface.get_rect(center=(WIDTH // 2 + 2, DICE_Y + DICE_SIZE + 42))
        screen.blit(glow_surface, glow_rect)
        
        if dice_value == 1:
            tip_text = "Новая попытка? Удача на твоей стороне!"
            tip_color = DARK_GRAY
        elif dice_value == 6:
            tip_text = "Отлично! Максимальный результат!"
            tip_color = GOLD
        elif dice_value >= 4:
            tip_text = "Хороший результат! Так держать!"
            tip_color = ORANGE
        else:
            tip_text = "Попробуй ещё раз!"
            tip_color = DARK_GRAY
        
        tip_surface = font_small.render(tip_text, True, tip_color)
        tip_rect = tip_surface.get_rect(center=(WIDTH // 2, DICE_Y + DICE_SIZE + 85))
        screen.blit(tip_surface, tip_rect)
    else:
        draw_dice_face(1, DICE_X, DICE_Y, DICE_SIZE)
        start_text = font_medium.render(result_text, True, DARK_GRAY)
        start_rect = start_text.get_rect(center=(WIDTH // 2, DICE_Y + DICE_SIZE + 40))
        screen.blit(start_text, start_rect)
    
    draw_button()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect.collidepoint(event.pos) and not is_rolling:
                is_rolling = True
                roll_start_time = pygame.time.get_ticks()
                rolling_values = []
                result_text = "Бросаем кубик..."
    
    pygame.display.flip()

pygame.quit()
sys.exit()