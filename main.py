import pygame, sys, math, random
import pymunk
from pygame import mixer
import title
import shop

# Pygame 초기화 및 기본 설정
pygame.init()
screen = pygame.display.set_mode((960, 960))
clock = pygame.time.Clock()

# 사용자가 구매한 골프공 목록과 현재 장착된 골프공
gold = 1000  # 초기 골드
purchased_balls = ["ball.png"]  # 기본으로 구매된 골프공
equipped_ball = "ball.png"  # 현재 장착된 골프공

# 게임 상태
game_state = "title"

font = pygame.font.Font('assets/fonts/font.ttf', 64)

hit_sfx = mixer.Sound('assets/sfx/hit.mp3')
goal_sfx = mixer.Sound('assets/sfx/hole.mp3')
power_sfx = mixer.Sound('assets/sfx/power.mp3')

hole_img = pygame.image.load("assets/images/hole.png")
hole_img = pygame.transform.scale(hole_img, (42, 42))

stroke_ui_img = pygame.image.load("assets/images/stroke_ui.png")
stroke_ui_img = pygame.transform.scale(stroke_ui_img, (480, 80))
stroke_ui_img.set_alpha(100)

background = pygame.image.load("assets/images/background.png")
background = pygame.transform.scale(background, (960, 960))

tile_img = pygame.image.load("assets/images/tile.png")
tile_img = pygame.transform.scale(tile_img, (128, 128))

arrow_img = pygame.image.load("assets/images/arrow.png")
arrow_img = pygame.transform.scale(arrow_img, (42, 168))

# 텍스트 출력 함수
def text_print(font_render, text):
    text_render = font_render.render(text, True, (255, 255, 255))
    text_rect = text_render.get_rect(center = (960 / 2, 40))
    text_shadow_render = font_render.render(text, True, (0, 0, 0))
    text_shadow_rect = text_render.get_rect(center = (960 / 2, 44))
    screen.blit(text_shadow_render, text_shadow_rect)
    screen.blit(text_render, text_rect)

# 충돌 발생 시 효과음 재생 함수
def hit():
    hit_sfx.play()

# 충돌 시 동작 정의 함수
def hit_object(arbiter, space, _):
    global new_level, vel_x, vel_y
    shape_1, shape_2 = arbiter.shapes
    if shape_1.elasticity == 1 and shape_2.elasticity == 1:
        goal_sfx.play()
        new_level = True
    elif shape_1.elasticity == 1 and shape_2.elasticity == 1.1:
        if vel_y < 0 and shape_2.body.position[1] + 64 > shape_1.body.position[1] > shape_2.body.position[1] - 64:
            vel_x *= -1
            hit()
        elif vel_y < 0 and not shape_2.body.position[1] + 64 > shape_1.body.position[1] > shape_2.body.position[1] - 64:
            vel_y *= -1
            hit()
        elif vel_y > 0 and shape_2.body.position[1] + 64 > shape_1.body.position[1] > shape_2.body.position[1] - 64:
            vel_x *= -1
            hit()
        elif vel_y > 0 and not shape_2.body.position[1] + 64 > shape_1.body.position[1] > shape_2.body.position[1] - 64:
            vel_y *= -1
            hit()
    return True

# 파워 효과음 재생 함수
def power_sfx_play():
    power_sfx.play()

# 대형 타일 생성 함수
def create_tile_large(space, pos):
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = (pos[0] * 64, pos[1] * 64)
    shape = pymunk.Poly.create_box(body, (120, 120))
    shape.collision_type = 1
    shape.elasticity = 1.1
    space.add(body,shape)
    return shape

# 홀 생성 함수
def create_hole(space, pos):
    body = pymunk.Body(1, 100, body_type = pymunk.Body.KINEMATIC)
    body.position = pos
    shape = pymunk.Circle(body, 16)
    shape.collision_type = 1
    shape.elasticity = 1
    space.add(body, shape)
    return shape

# 플레이어(공) 그리기 함수
def draw_player(shape, equipped_ball):
    ball_img = pygame.image.load(f"assets/images/{equipped_ball}")
    ball_img = pygame.transform.scale(ball_img, (42, 42))
    for ball in shape:
        ball_rect = ball_img.get_rect(center = (int(ball.body.position[0]), int(ball.body.position[1])))
        screen.blit(pygame.transform.scale(ball_img, (round(42 * (100 - size) / 100), round(42 * (100 - size) / 100))), ball_rect)

# 홀 그리기 함수
def draw_hole(shape):
    for ball in shape:
        ball_rect = hole_img.get_rect(center = (int(ball.body.position[0]), int(ball.body.position[1])))
        screen.blit(hole_img, ball_rect)

# 대형 타일 그리기 함수
def draw_tile_large(shape):
    for square in shape:
        ball_rect = tile_img.get_rect(center = (int(square.body.position[0]), int(square.body.position[1])))
        screen.blit(tile_img, ball_rect)

# 정적 객체 삭제 함수
def delete_static(shape):
    for square in shape:
        space.remove(square, square.body)

# 텍스트 출력 함수
def text_print(font_render, text):
    text_render = font_render.render(text, True, (255, 255, 255))
    text_rect = text_render.get_rect(center = (960 / 2, 40))
    text_shadow_render = font_render.render(text, True, (0, 0, 0))
    text_shadow_rect = text_render.get_rect(center = (960 / 2, 44))
    screen.blit(text_shadow_render, text_shadow_rect)
    screen.blit(text_render, text_rect)

# 메인 게임 루프 함수
def main_game_loop(screen, font, equipped_ball):
    global space, size, vel_x, vel_y, shapes, balls, goals, hold, stroke, power, new_level, level, hole_max_timer, hole_timer

    # 게임에 필요한 초기 설정
    space = pymunk.Space()
    space.gravity = (0, 0)

    ball_position = ()

    shapes = []
    body = pymunk.Body(5, 100, body_type=pymunk.Body.DYNAMIC)
    body.position = (480, 160)
    shape = pymunk.Circle(body, 24)
    shape.collision_type = 1
    shape.elasticity = 1
    shape.friction = 1.785
    space.add(body, shape)
    shapes.append(shape)

    balls = []
    balls.append(create_tile_large(space, (640, 384)))
    balls.append(create_tile_large(space, (320, 320)))

    goals = []
    goals.append(create_hole(space, (480, 480)))

    h = space.add_collision_handler(1, 1)
    h.begin = hit_object

    hold = False
    stroke = 0
    power = 0
    vel_x = 0
    vel_y = 0
    new_level = True
    level = 0
    hole_max_timer = 240
    hole_timer = 240
    size = 0

    # 게임 루프
    running = True
    while running:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if (-0.00001 < vel_x < 0.12225 and -0.00001 < vel_y < 0.12225) or (
                        0.00001 > vel_x > -0.12225 and 0.00001 > vel_y > -0.12225):
                    hold = True
            if event.type == pygame.MOUSEBUTTONUP:
                if hold:
                    hold = False
                    stroke += 1
                    vel_x = (mouse_position[0] - ball_position[0]) * 1.675773 / 100
                    vel_y = (mouse_position[1] - ball_position[1]) * 1.675773 / 100
                    power_sfx_play()

        body.position = [body.position[0] - vel_x, body.position[1] - vel_y]

        vel_x = vel_x * 98.87 / 100
        vel_y = vel_y * 98.87 / 100

        fps = 2400
        space.step(1 / 2400)

        draw_tile_large(balls)
        draw_hole(goals)

        if new_level == False:
            pass
        else:
            if hole_timer >= hole_max_timer:
                delete_static(balls)
                balls = []
                if level == 0:
                    balls.append(create_tile_large(space, (10, 6)))
                    balls.append(create_tile_large(space, (5, 5)))
                elif level == 1:
                    balls.append(create_tile_large(space, (8, 10)))
                    balls.append(create_tile_large(space, (7, 5)))
                elif level == 2:
                    balls.append(create_tile_large(space, (12, 6)))
                    balls.append(create_tile_large(space, (3, 6)))
                stroke = 0
                level += 1
                new_level = False
                body.position = (480, 96)
                vel_x, vel_y = 0, 0
                hole_timer = 1
                size = 0
                win_pos = 0
            else:
                if hole_max_timer / hole_timer >= 3:
                    body.position = (
                    480 + (hole_timer / 9) + random.randint(-3, 3), 480 + (hole_timer / 9) + random.randint(-3, 3))
                elif 3 > hole_max_timer / hole_timer >= 2:
                    body.position = (
                    480 + (hole_timer / 10) + random.randint(-2, 2), 480 + (hole_timer / 10) + random.randint(-2, 2))
                elif 2 > hole_max_timer / hole_timer >= 1:
                    body.position = (
                    480 + (hole_timer / 11) + random.randint(-1, 1), 480 + (hole_timer / 11) + random.randint(-1, 1))
                if size <= 86:
                    size = hole_timer / hole_max_timer * 100
                else:
                    size = 100

                if hole_timer > 80:
                    if abs(vel_x) + abs(vel_y) >= 4.5:
                        if random.randint(1, 8) == 1:
                            new_level = False
                            body.position = (480, 480)
                            vel_x, vel_y = random.randint(-4, 4), random.randint(-4, 4)
                            hole_timer = 1
                            size = 0
                    elif 4.5 > abs(vel_x) + abs(vel_y) >= 2:
                        if random.randint(1, 15) == 1:
                            new_level = False
                            body.position = (480, 480)
                            vel_x, vel_y = random.uniform(-4.85, 4.85), random.randint(-4, 4)
                            hole_timer = 1
                            size = 0
                    elif 2 > abs(vel_x) + abs(vel_y) >= 1.25:
                        if random.randint(1, 30) == 1:
                            new_level = False
                            body.position = (480, 480)
                            vel_x, vel_y = random.uniform(-4.85, 4.85), random.randint(-4, 4)
                            hole_timer = 1
                            size = 0
                    elif 1.25 > abs(vel_x) + abs(vel_y) >= 0.75:
                        if random.randint(1, 60) == 1:
                            new_level = False
                            body.position = (480, 480)
                            vel_x, vel_y = random.randint(-4, 4), random.randint(-4, 4)
                            hole_timer = 1
                            size = 0
                hole_timer += 1

        draw_tile_large(balls)
        draw_hole(goals)

        if hold == True:
            ball_position = body.position
            mouse_position = pygame.mouse.get_pos()

            x_distance = ball_position[0] - mouse_position[0]
            y_distance = ball_position[1] - mouse_position[1]

            angle = math.degrees(math.atan2(y_distance, x_distance)) + 90

            rotate_image = pygame.transform.rotate(arrow_img, -angle)
            arrow_rect = rotate_image.get_rect(center=ball_position)
            screen.blit(rotate_image, arrow_rect)

        draw_player(shapes, equipped_ball)
        ui_rect = stroke_ui_img.get_rect(center=(480, 40))
        screen.blit(stroke_ui_img, ui_rect)
        text_print(font, f"Strokes: {str(stroke)}")

        ball_position = body.position

        if ball_position[0] > 942:
            body.position = [942, body.position[1]]
            vel_x = -vel_x
            hit()
        elif ball_position[0] < 18:
            body.position = [18, body.position[1]]
            vel_x = -vel_x
            hit()
        elif ball_position[1] > 942:
            body.position = [body.position[0], 942]
            vel_y = -vel_y
            hit()
        elif ball_position[1] < 18:
            body.position = [body.position[0], 18]
            vel_y = -vel_y
            hit()

        pygame.display.update()
        clock.tick(fps)

    return "title"

# 메인 루프
while True:
    if game_state == "title":
        game_state = title.show_title_screen(screen)
    elif game_state == "open_shop":
        equipped_ball, gold, shop_state = shop.show_shop_screen(screen, purchased_balls, equipped_ball, gold)
        if shop_state == "quit":
            break
        elif shop_state == "exit":
            game_state = "title"
    elif game_state == "start_game":
        game_state = main_game_loop(screen, font, equipped_ball)


# 게임 종료 시 음악 정지
pygame.mixer.music.stop()

# 게임 종료 시 처리
pygame.quit()
sys.exit()
