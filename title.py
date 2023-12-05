import pygame
from pygame import mixer


def show_title_screen(screen):
    font = pygame.font.Font('assets/fonts/font.ttf', 120)
    title_text = font.render("Go On Lucky Fairway", True, (255, 255, 255))

    music_sfx = mixer.Sound('assets/sfx/music.mp3')
    music_sfx.play(-1)

    # 이미지 로드
    start_button_img = pygame.image.load("assets/images/start.png")
    club_button_img = pygame.image.load("assets/images/club.png")
    background = pygame.image.load("assets/images/background.png")
    background = pygame.transform.scale(background, (960, 960))

    # 버튼 위치 설정
    start_button_rect = start_button_img.get_rect(center=(480, 500))
    club_button_rect = club_button_img.get_rect(center=(480, 650))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return "game"
                elif club_button_rect.collidepoint(event.pos):
                    return "shop"

        screen.blit(background, (0, 0))
        screen.blit(title_text, (screen.get_width() / 2 - title_text.get_width() / 2, 100))
        screen.blit(start_button_img, start_button_rect)
        screen.blit(club_button_img, club_button_rect)

        pygame.display.update()
