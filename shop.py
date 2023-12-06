import pygame

def show_shop_screen(screen, purchased_balls, equipped_ball):
    font = pygame.font.Font('assets/fonts/font.ttf', 30)

    # 배경 이미지 로드
    background = pygame.image.load("assets/images/background.png")
    background = pygame.transform.scale(background, (960, 960))

    # 골프공 이미지 로드 및 크기 조정
    ball_images = [pygame.image.load(f"assets/images/ball{i}.png") for i in range(1, 7)]
    ball_images_scaled = [pygame.transform.scale(img, (100, 100)) for img in ball_images]  # 크기 조정
    ball_rects = [img.get_rect(center=(100 + i * 100, 300)) for i, img in enumerate(ball_images_scaled)]

    # 골프공 위치 설정 (두 줄로 배열)
    ball_rects = []
    for i, img in enumerate(ball_images_scaled):
        x = 280 + (i % 3) * 200  # 각 줄에 3개씩 배치
        y = 200 if i < 3 else 400  # 첫 번째 줄과 두 번째 줄
        ball_rects.append(img.get_rect(center=(x, y)))

    running = True
    while running:
        screen.blit(background, (0, 0))  # 배경화면 설정

        for i, ball_img in enumerate(ball_images_scaled):
            screen.blit(ball_img, ball_rects[i])
            ball_name = f"ball{i+1}.png"
            if ball_name in purchased_balls:
                status_text = "Purchased" if ball_name != equipped_ball else "Equipped"
                status_render = font.render(status_text, True, (255, 255, 255))
                screen.blit(status_render, (ball_rects[i].x, ball_rects[i].y + 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return equipped_ball
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(ball_rects):
                    if rect.collidepoint(event.pos):
                        ball_name = f"ball{i+1}.png"
                        if ball_name not in purchased_balls:
                            purchased_balls.append(ball_name)
                        equipped_ball = ball_name

        pygame.display.update()

    return equipped_ball
