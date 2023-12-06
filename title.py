import pygame
from pygame import mixer

def show_title_screen(screen):
    font = pygame.font.Font('assets/fonts/font.ttf', 120)
    title_text = font.render("Go On Lucky Fairway", True, (255, 255, 255))

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load('assets/sfx/music.mp3')
        pygame.mixer.music.play(-1)  # 무한 반복 재생

    # 이미지 로드
    start_button_img = pygame.image.load("assets/images/start.png")
    club_button_img = pygame.image.load("assets/images/club.png")
    background = pygame.image.load("assets/images/background.png")
    background = pygame.transform.scale(background, (960, 960))

    # 버튼 위치 설정
    start_button_rect = start_button_img.get_rect(center=(480, 500))
    club_button_rect = club_button_img.get_rect(center=(480, 650))

    # 상점 화면을 표시하는 함수

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        # 마우스가 버튼 위에 있을 때 크기 변경
        if start_button_rect.collidepoint(mouse_pos):
            start_button_scaled = pygame.transform.scale(start_button_img, (
            int(start_button_rect.width * 1.2), int(start_button_rect.height * 1.2)))
            start_button_scaled_rect = start_button_scaled.get_rect(center=start_button_rect.center)
        else:
            start_button_scaled = start_button_img
            start_button_scaled_rect = start_button_rect

        if club_button_rect.collidepoint(mouse_pos):
            club_button_scaled = pygame.transform.scale(club_button_img, (
            int(club_button_rect.width * 1.5), int(club_button_rect.height * 1.5)))
            club_button_scaled_rect = club_button_scaled.get_rect(center=club_button_rect.center)
        else:
            club_button_scaled = club_button_img
            club_button_scaled_rect = club_button_rect

        # 버튼의 새로운 크기에 대한 rect를 계산하고 중심점을 유지
        start_button_scaled_rect = start_button_scaled.get_rect(center=start_button_rect.center)
        club_button_scaled_rect = club_button_scaled.get_rect(center=club_button_rect.center)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return "start_game"  # 게임 시작
                elif club_button_rect.collidepoint(event.pos):
                    return "open_shop"  # 상점 열기

        screen.blit(background, (0, 0))
        screen.blit(title_text, (screen.get_width() / 2 - title_text.get_width() / 2, 100))
        screen.blit(start_button_scaled, start_button_scaled_rect)
        screen.blit(club_button_scaled, club_button_scaled_rect)

        pygame.display.update()
