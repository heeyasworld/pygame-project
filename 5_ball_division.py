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
ball_images = [
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
    "pos_y": 50,  # y좌표
    "img_idx": 0,  # 제일 큰 공(이미지 중에서 0번째 공 사용)
    "to_x": 3,  # 공의 x축 이동방향, -3이면 왼쪽으로 3이면 오른쪽으로 이동
    "to_y": -6,  # y축 이동방향
    "init_spd_y": ball_speed_y[0]  # y 최초 속도 (init_speed_y)
})  # {} 딕셔너리 형태로 키값 : 밸류로 저장

# 사라질 무기와 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1


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

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        # balls 리스트에서 가져와서 하나씩 index값이랑 value를 출력해주는 역할 : enumerate(balls)
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 가로벽에 닿았을 때 공 이동 위치를 반대 방향으로 변경해주는 역할 (튕겨져 나오는 효과)
        if ball_pos_x <= 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        # 세로 위치 : 스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else:  # 그외에는 속도를 증가 -18, -17.5, -17.0 .... 0, +0.5, +1....
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

        # It's too difficult now, what the heck!!!!!!
        # salaveme chiquillos, super dificl python tambien T-T
        # 살ㄹㅕ주세요 갑자기 어려워져서 내 머리 터지게 해요
        #　むずかしすぎる！うちはプログラマー👩‍💻になれるのか？？？？？？？？？？

        # 4. 충돌 처리

        # character rect information update
        character_rect = character.get_rect()  # size
        character_rect.left = character_x_pos
        character_rect.top = character_y_pos

        for ball_idx, ball_val in enumerate(balls):
            ball_pos_x = ball_val["pos_x"]
            ball_pos_y = ball_val["pos_y"]
            ball_img_idx = ball_val["img_idx"]

            # 공 렉트 정보 업데이트
            ball_rect = ball_images[ball_img_idx].get_rect()
            ball_rect.left = ball_pos_x
            ball_rect.top = ball_pos_y

            # ball 충돌 character
            if character_rect.colliderect(ball_rect):
                running = False  # game over
                break

            # 공과 무기들 충돌 처리
            for weapon_idx, weapon_val in enumerate(weapons):
                weapon_pos_x = weapon_val[0]
                weapon_pos_y = weapon_val[1]

            # rect 무기 정보 업데이트
                weapon_rect = weapon.get_rect()
                weapon_rect.left = weapon_pos_x
                weapon_rect.top = weapon_pos_y

                # 충돌 체크
                if weapon_rect.colliderect(ball_rect):
                    weapon_to_remove = weapon_idx  # 해당 무기 없애기 위한 값 설정
                    ball_to_remove = ball_idx
                    break

        # 충돌된 공 혹은 무기 없애기
        if ball_to_remove > -1:
            del balls[ball_to_remove]
            ball_to_remove = -1

        if weapon_to_remove > -1:
            del weapons[weapon_to_remove]
            weapon_to_remove = -1

            # 5. 화면 그리기
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, (screen_height - stage_height)))
    screen.blit(character, (character_x_pos, character_y_pos))

    pygame.display.update()

# pygame 종료
pygame.quit()
