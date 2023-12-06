import pygame
from pygame import mixer

def show_shop_screen(screen, purchased_balls, equipped_ball):
    # 상점에서 사용할 폰트
    font = pygame.font.Font('assets/fonts/font.ttf', 30)

    # 골프공 이미지 로드
    ball_images = [pygame.image.load(f"assets/images/ball{i}.png") for i in range(1, 7)]
    ball_rects = [ball_img.get_rect(center=(100 + i * 100, 300)) for i, ball_img in enumerate(ball_images)]

    running = True
    while running:
        screen.fill((0, 0, 0))  # 상점 배경을 검은색으로 설정

        # 골프공 이미지와 구매 상태 표시
        for i, ball_img in enumerate(ball_images):
            screen.blit(ball_img, ball_rects[i])
            ball_name = f"ball{i + 1}.png"
            if ball_name in purchased_balls:
                status_text = "Purchased" if ball_name != equipped_ball else "Equipped"
                status_render = font.render(status_text, True, (255, 255, 255))
                screen.blit(status_render, (ball_rects[i].x, ball_rects[i].y + 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(ball_rects):
                    if rect.collidepoint(event.pos):
                        ball_name = f"ball{i + 1}.png"
                        if ball_name not in purchased_balls:
                            purchased_balls.append(ball_name)
                        equipped_ball = ball_name

        pygame.display.update()

    return equipped_ball