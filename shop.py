import pygame

def show_shop_screen(screen, purchased_balls, equipped_ball, gold):
    font = pygame.font.Font('assets/fonts/font.ttf', 30)

    # 골프공 가격 설정
    ball_prices = {
        "ball1.png": 100,
        "ball2.png": 200,
        "ball3.png": 300,
        "ball4.png": 400,
        "ball5.png": 500,
        "ball6.png": 600
    }

    # 배경 이미지 로드
    background = pygame.image.load("assets/images/background.png")
    background = pygame.transform.scale(background, (960, 960))

    # 나가기 버튼 이미지 로드
    exit_button_img = pygame.image.load("assets/images/next.png")
    exit_button_img = pygame.transform.scale(exit_button_img, (200, 100))
    exit_button_rect = exit_button_img.get_rect(topright=(910, 100))

    # 골프공 이미지 로드 및 크기 조정
    ball_images = [pygame.image.load(f"assets/images/ball{i}.png") for i in range(1, 7)]
    ball_images_scaled = [pygame.transform.scale(img, (100, 100)) for img in ball_images]

    # 현재 장착 중인 골프공 추가
    current_ball_img = pygame.image.load("assets/images/ball.png")
    current_ball_scaled = pygame.transform.scale(current_ball_img, (100, 100))

    # 골프공 위치 설정 (두 줄로 배열)
    ball_rects = [current_ball_scaled.get_rect(center=(250, 200))]  # 현재 장착 중인 골프공 위치
    for i, img in enumerate(ball_images_scaled):
        x = 250 + (i % 3) * 250  # 각 줄에 3개씩 배치, x축 간격 증가
        y = 400 if i < 3 else 600  # 첫 번째 줄과 두 번째 줄, y축 위치 조정
        ball_rects.append(img.get_rect(center=(x, y)))

    running = True
    while running:
        screen.blit(background, (0, 0))  # 배경화면 설정
        mouse_pos = pygame.mouse.get_pos()

        # 현재 남은 골드 표시
        gold_text = f"Gold: {gold}"
        gold_render = font.render(gold_text, True, (255, 255, 255))
        screen.blit(gold_render, (800, 250))

        # 나가기 버튼 그리기
        screen.blit(exit_button_img, exit_button_rect)

        # 현재 장착 중인 골프공 그리기
        screen.blit(current_ball_scaled, ball_rects[0])
        status_render = font.render("Currently Equipped", True, (255, 255, 255))
        screen.blit(status_render, (ball_rects[0].x, ball_rects[0].y + 110))

        for i, ball_img in enumerate(ball_images_scaled):
            screen.blit(ball_img, ball_rects[i+1])
            ball_name = f"ball{i+1}.png"
            status_text = "Purchased" if ball_name in purchased_balls else f"Price: {ball_prices[ball_name]} Gold"
            status_render = font.render(status_text, True, (255, 255, 255))
            screen.blit(status_render, (ball_rects[i+1].x, ball_rects[i+1].y + 110))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return equipped_ball, gold, "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):
                    return equipped_ball, gold, "exit"
                for i, rect in enumerate(ball_rects[1:]):  # 첫 번째 골프공은 제외
                    if rect.collidepoint(event.pos):
                        ball_name = f"ball{i+1}.png"
                        if ball_name not in purchased_balls and gold >= ball_prices[ball_name]:
                            purchased_balls.append(ball_name)
                            gold -= ball_prices[ball_name]
                        equipped_ball = ball_name

        pygame.display.update()

    return equipped_ball, gold, "continue"
