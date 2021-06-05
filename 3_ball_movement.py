import os
import pygame
import random
#########################################################################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()

# 화면 크기 설정
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Heeya Pang")

# FPS
clock = pygame.time.Clock()
#########################################################################################################

# 1. 사용자 게임 초기화 (배경화면, 게임이미지, 좌표, 속도, 폰트 등 설정)
current_path = os.path.dirname(__file__)  # 현재 파일의 위치 변환
image_path = os.path.join(current_path, "images")  # image folder 위치 반환

# background
background = pygame.image.load(os.path.join(image_path, "background.png"))

# stage
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]  # 스테이지의 높이 위에 캐릭터를 두기 위해서 사용함

# character
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - stage_height - character_height

# 캐릭터의 이동 방향 / 좌우로만 움직이므로 x만 만들면 됨
character_to_x = 0

# speed
character_speed = 5

# weapon
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러 발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 10

# balloon (4개 크기에 대해 따로 처리)
ball_imagaes = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))]

# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9]  # index 0,1,2,3에 해당하는 값

# 공들의 정보
balls = []

# 최초 발생하는 큰 공 추가
balls.append({
    "pos_x": 50,  # 공의 x 좌표
    "pox_y": 50,  # y좌표
    "img_idx": 0,  # 제일 큰 공
    "to_x": 3,  # 공의 x축 이동방햐, -3이면 왼쪽으로 3이면 오른쪽으로 이동
    "to_y": -6,  # y축 이동방향,
    "init_spe_y": ball_speed_y[0]  # y 최초 속도
})

running = True
while running:
    dt = clock.tick(30)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + \
                    (character_width / 2) - \
                    (weapon_width / 2)  # 현재 캐릭터 위치 정중앙에서 발사됨
                weapon_y_pos = character_y_pos  # 캐릭터 머리에서 발사됨
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x

    # 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    # 100, 200 -> x 좌표는 그대로(100), y좌표는 스피드만큼 190, 180, 170 ... 줄어듦
    weapons = [[w[0], w[1] - weapon_speed]
               for w in weapons]  # 무기 위치를 위로 / 한줄 for문 사용
    # weapons list 속 값을 하나씩 불러와서 그걸 w 라고 하고
    # w를 통해서 앞쪽 처리를 한다
    # 그 처리를 한 것들은 맨앞 weapons 리스트에 다시 집어 넣는다

    # 천장에 닿은 무기 없애기
    # if문처럼 y 좌표가 0보다 크다, 즉 천장에 닿지 않았을 경우에만 보이고 그렇지 않다면 화면에서 사라짐
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # 4. 충돌 처리

    # 5. 화면 그리기
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    screen.blit(stage, (0, (screen_height - stage_height)))
    screen.blit(character, (character_x_pos, character_y_pos))

    pygame.display.update()

# pygame 종료
pygame.quit()
