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

        # 나가기 버튼 그리기 (마우스 오버 효과 포함)
        if exit_button_rect.collidepoint(mouse_pos):
            scaled_exit_button = pygame.transform.scale(exit_button_img, (220, 110))
            scaled_exit_button_rect = scaled_exit_button.get_rect(center=exit_button_rect.center)
            screen.blit(scaled_exit_button, scaled_exit_button_rect)
        else:
            screen.blit(exit_button_img, exit_button_rect)

        # 골프공 그리기 및 마우스 오버 효과
        for i, ball_img in enumerate(ball_images_scaled):
            ball_rect = ball_rects[i + 1]  # 첫 번째 골프공은 기본 골프공이므로 인덱스를 1부터 시작
            ball_name = f"ball{i + 1}.png"

            # 마우스 오버 효과 적용
            if ball_rect.collidepoint(mouse_pos):
                scaled_ball_img = pygame.transform.scale(ball_img, (120, 120))
                scaled_ball_rect = scaled_ball_img.get_rect(center=ball_rect.center)
                screen.blit(scaled_ball_img, scaled_ball_rect)
            else:
                screen.blit(ball_img, ball_rect)

            # 상태 텍스트 설정
            if ball_name == equipped_ball:
                status_text = "Equipped"
            elif ball_name in purchased_balls:
                status_text = "Available"
            else:
                status_text = f"{ball_prices[ball_name]} Gold"

            # 상태 텍스트 그리기
            status_render = font.render(status_text, True, (255, 255, 255))
            screen.blit(status_render, (ball_rect.x, ball_rect.y + 110))

        # 기본 골프공 그리기 및 마우스 오버 효과
        current_ball_rect = ball_rects[0]
        if current_ball_rect.collidepoint(mouse_pos):
            scaled_current_ball = pygame.transform.scale(current_ball_img, (120, 120))
            scaled_current_ball_rect = scaled_current_ball.get_rect(center=current_ball_rect.center)
            screen.blit(scaled_current_ball, scaled_current_ball_rect)
        else:
            screen.blit(current_ball_scaled, current_ball_rect)

        # 기본 골프공 상태 텍스트 설정 및 그리기
        current_ball_status_text = "Equipped" if "ball.png" == equipped_ball else "Available"
        current_ball_status_render = font.render(current_ball_status_text, True, (255, 255, 255))
        screen.blit(current_ball_status_render, (current_ball_rect.x, current_ball_rect.y + 110))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return equipped_ball, gold, "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):
                    return equipped_ball, gold, "exit"
                for i, rect in enumerate(ball_rects):
                    if rect.collidepoint(event.pos):
                        ball_name = f"ball{i}.png" if i > 0 else "ball.png"
                        if ball_name in purchased_balls:
                            equipped_ball = ball_name  # 골프공 장착
                        elif gold >= ball_prices[ball_name]:
                            purchased_balls.append(ball_name)
                            gold -= ball_prices[ball_name]
                            equipped_ball = ball_name  # 골프공 구매 및 장착

        pygame.display.update()

    return equipped_ball, gold, "continue"
