"""
행소박물관 디지털 아카이브

주요 기능:
- 메인화면 / 게임 시작 / 종료
- 1층, 2층, 전시관 이동
- 유물 배치 및 설명창 출력
- 유물 복원 직소 퍼즐 미니게임
"""


# 라이브러리 불러오기
import pygame
import sys
import os
import random


# 기본 설정
pygame.init()

WIDTH = 640
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("행소박물관 디지털 아카이브")

clock = pygame.time.Clock()
BASE_DIR = os.path.dirname(__file__)


# 이미지 로드
map_1f = pygame.image.load(os.path.join(BASE_DIR, "1fmap.png")).convert()
map_2f = pygame.image.load(os.path.join(BASE_DIR, "2fmap.png")).convert()
map_1 = pygame.image.load(os.path.join(BASE_DIR, "1map.png")).convert()
map_2 = pygame.image.load(os.path.join(BASE_DIR, "2map.png")).convert()
map_special = pygame.image.load(os.path.join(BASE_DIR, "specialmap.png")).convert()

title_bg = pygame.image.load(os.path.join(BASE_DIR, "hangso.png")).convert()
title_bg = pygame.transform.scale(title_bg, (WIDTH, HEIGHT))


# 플레이어 스프라이트 설정
player_sheet = pygame.image.load(os.path.join(BASE_DIR, "player-Sheet.png")).convert_alpha()

PLAYER_FRAME_SIZE = 16
PLAYER_DRAW_SIZE = 32

player_frames = []

for i in range(4):
    frame = player_sheet.subsurface(
        i * PLAYER_FRAME_SIZE,
        0,
        PLAYER_FRAME_SIZE,
        PLAYER_FRAME_SIZE
    )
    frame = pygame.transform.scale(frame, (PLAYER_DRAW_SIZE, PLAYER_DRAW_SIZE))
    player_frames.append(frame)

player_frame_index = 0
animation_timer = 0
animation_speed = 8
facing_right = True


# 유물 이미지 로드 함수
def load_artifact(filename, size):
    img = pygame.image.load(os.path.join(BASE_DIR, filename)).convert_alpha()
    return pygame.transform.scale(img, size)


# 유물 이미지 목록
artifact_images = {
    1: load_artifact("artifact_1.png", (70, 70)),
    2: load_artifact("artifact_2.png", (70, 70)),
    3: load_artifact("artifact_3.png", (70, 70)),
    4: load_artifact("artifact_4.png", (70, 70)),
    5: load_artifact("artifact_5.png", (70, 70)),
    6: load_artifact("artifact_6.png", (70, 70)),

    7: load_artifact("artifact_7.png", (70, 70)),
    8: load_artifact("artifact_8.png", (70, 70)),
    9: load_artifact("artifact_9.png", (70, 70)),
    10: load_artifact("artifact_10.png", (70, 70)),

    11: load_artifact("artifact_11.png", (70, 70)),
    12: load_artifact("artifact_12.png", (70, 70)),
    13: load_artifact("artifact_13.png", (70, 70)),
    14: load_artifact("artifact_14.png", (70, 70)),
}


# 충돌 영역 설정
# 1층 충돌 영역
walls_1f = [
    pygame.Rect(0, 0, 640, 90),
    pygame.Rect(0, 90, 510, 50),
    pygame.Rect(0, 140, 210, 50),
    pygame.Rect(545, 90, 640, 80),
    pygame.Rect(0, 355, 175, 130),
    pygame.Rect(173, 385, 150, 105),
    pygame.Rect(435, 383, 210, 100),
    pygame.Rect(495, 290, 220, 60),
    pygame.Rect(590, 350, 6350, 50),
    pygame.Rect(0, 190, 1, 170),
    pygame.Rect(639, 140, 640, 170),
    pygame.Rect(0, 479, 640, 480),
    pygame.Rect(320, 145, 48, 63)
]

# 2층 충돌 영역
walls_2f = [
    pygame.Rect(270, 210, 100, 95),
    pygame.Rect(0, 0, 225, 480),
    pygame.Rect(415, 0, 225, 480),
    pygame.Rect(0, 0, 640, 1),
    pygame.Rect(0, 479, 640, 480)
]

# 제1전시관 충돌 영역
walls_room1 = [
    pygame.Rect(0, 0, 640, 1),
    pygame.Rect(0, 480, 640, 479),
    pygame.Rect(0, 0, 79, 480),
    pygame.Rect(590, 0, 50, 480),
]

# 제2전시관 충돌 영역
walls_room2 = [
    pygame.Rect(0, 0, 640, 1),
    pygame.Rect(0, 480, 640, 479),
    pygame.Rect(0, 0, 50, 480),
    pygame.Rect(561, 0, 79, 480),
]

# 특별전시관 충돌 영역
walls_special = [
    pygame.Rect(0, 0, 640, 1),
    pygame.Rect(0, 480, 640, 479),
    pygame.Rect(0, 0, 50, 480),
    pygame.Rect(561, 0, 79, 480),
]


# 전시 유물 데이터
# 특별전시관 유물
artifacts_special = [
    {"id": 1, "rect": pygame.Rect(380, 410, 70, 70), "name": "청화 백자에 그려진 봉황", "desc": "청화 백자 항아리로 구름 속을 날고 있는 봉황을 그려 넣었다.\n봉황은 민화 속의 봉황과 비교할 때 간략하지만 봉황의 특징인 닭의 머리와 가늘고 긴눈, 원앙의 날개, 길게 휘날리는 꼬리의 특징을 잘 살려 대범하게 그렸다.\n봉황은 왕실의 문양으로 사용되어 왕의 어진 정치와 나라의 평안함을 바라는 소망이 담겨 있다."},
    {"id": 2, "rect": pygame.Rect(180, 405, 70, 70), "name": "봉황도", "desc": "봉황도는 해와 구름, 소나무 사이를 거니는 봉황을 그려 넣은 그림이다.\n 봉황은 닭의 머리와 길게 뻗은 꼬리, 화려한 날개의 특징을 잘 살려 표현하였으며, 붉은 해와 푸른 구름을 함께 배치하여 신성하고 길상적인 분위기를 나타냈다.\n 봉황은 예로부터 태평성대와 왕실의 권위를 상징하는 상서로운 새로 여겨졌으며, 나라의 평안과 백성의 행복을 바라는 소망이 담겨 있다."},
    {"id": 3, "rect": pygame.Rect(50, 270, 70, 70), "name": "장수의 상징 사슴 등을 그려 넣은 청화 백자", "desc": "정화 백자 대접으로 오래 살기를 바라는 소망을 담아 해, 구름, 사슴, 거북, 소나무, 학, 바위, 대나무, 불로초를 청화 안료로 그려 넣었다. 대접의 안쪽 바닥에는 변형된 목숨 '수'자를 그려 넣어 질병 없이 오래 살기를 바라는 소망을 더욱 강조하고있다."},
    {"id": 4, "rect": pygame.Rect(50, 100, 70, 70), "name": "용이 새겨진 자수용 판과 용보", "desc": "용보수판은 용무늬 자수를 놓기 위한 밑그림을 새긴 나무판이다. 원형의 용무늬는 왕과 왕세자의 곤룡포에 장식되는 '보'로 사용되었다. 수판의 용은 몸을 둥글게 말고 다섯 발톱을 지녔으며, 실제 용보는 금실로 수놓아 왕권과 권위를 상징한다."},
    {"id": 5, "rect": pygame.Rect(180, 20, 50, 50), "name": "오래 사는 열 가지를 그려 넣은 청화 백자", "desc": "청화 백자 병으로 몸통에는 오래 산다고 믿어왔던 동물 등 상징물인 해, 구름, 사슴, 거북, 소나무, 학, 바위, 대나무, 불로초, 산을 청화 안료로 그려 넣었다. 술 등 음료를 담았던 병으로 음료를 마시면서도 옛사람들은 오래오래 건강하게 사는 삶은 소망하였다."},
    {"id": 6, "rect": pygame.Rect(380, 20, 70, 70), "name": "청화 백자에 그려진 구름 속 용", "desc": "청화백자 표면에 구름 사이를 날아오르는 용을 그려 넣은 작품이다. 용은 길게 뻗은 몸체와 힘찬 발톱, 역동적인 움직임을 간결하면서도 대담하게 표현하였다. 용은 예로부터 왕권과 권위를 상징하는 상서로운 동물로 여겨졌으며, 나라의 평안과 번영, 백성의 안녕을 바라는 소망이 담겨 있다."},
]

# 제1전시관 유물
artifacts_room1 = [
    {"id": 7, "rect": pygame.Rect(210, 110, 70, 70), "name": "무문토기 큰 항아리", "desc": "청동기시대의 무문토기(민무늬토기)로 곡식과 물 등을 저장하는 데 사용되었다. 청동기시대 사람들의 생활 모습을 보여주는 대표적인 유물로, 정착 생활과 농경 문화의 발달을 알 수 있다."},
    {"id": 8, "rect": pygame.Rect(370, 110, 70, 70), "name": "돌칼", "desc": "돌을 갈아 만든 청동기시대의 무기이다. 날카로운 칼날과 손잡이를 갖추고 있으며, 사냥과 방어에 사용되거나 권위를 상징하는 물건으로 활용되었다. 돌칼은 당시 사람들의 생활과 기술 발달 모습을 보여주는 대표적인 유물이다."},
    {"id": 9, "rect": pygame.Rect(370, 290, 70, 70), "name": "쇠투겁창", "desc": "쇠로 만든 쇠투겁창으로 초기철기시대의 철제 무기중 하나이다. 양날의 몸체와 자루를 끼우는 투겁으로 나누어진다. 길이에 따라 단봉식 중봉식, 장봉식으로 나누어진다."},
    {"id": 10, "rect": pygame.Rect(210, 290, 70, 70), "name": "경주 황성동 신라 거푸집", "desc": "경주 황성동에서 발굴된 원삼국시대 신라의 초기 거푸집이다. 철제 기구를 만들때 사용했다."},
]

# 제2전시관 유물
artifacts_room2 = [
    {"id": 11, "rect": pygame.Rect(350, 290, 70, 70), "name": "갑옷과 투구(삼국시대, 가야)", "desc": "전쟁에서 날카로운 칼과 화살을 막기위해 철로 만든 갑옷과 투구이다. 얇은 철판을 옷이나 가죽으로 고정하여 만든 횡장편갑 형식의 갑옷이다. 투구는 측현 4개의 가늘고 긴 철판을 상하로 연결하여 상부에 쌀주걱 모양의 철판을 덮어 만들었다. 이와 같은 철갑옷은 가야의 우수한 철 제작기술을 보여준다."},
    {"id": 12, "rect": pygame.Rect(190, 290, 70, 70), "name": "청자 상감 물가 풍경 무늬 대접(고려시대)", "desc": "청자 대접으로 안쪽 면에는 버드나무와 오리 등 물가 풍경 무늬가 흑력상감으로 표현되어 있다. 고려청자에 보이는 물가 풍경 무늬에 관해서는 중국 요대 액화의 명칭으로 보거나 불교 관련된 극락세계를 표현한 것으로 보는 의견이 있다."},
    {"id": 13, "rect": pygame.Rect(190, 110, 70, 70), "name": "고동이 담긴 항아리(성주 성산리, 5세기)", "desc": "고둥 담긴 항아리는 5세기 성주 성산리 제38호분에서 출토된 유물이다. 항아리 내부에는 고둥이 가득 담긴 채 발견되었으며, 같은 무덤에서는 벼 알맹이 흔적이 남은 유물도 함께 출토되었다. 이러한 유물은 당시 사람들의 먹거리 문화와 장례 풍습을 보여주는 중요한 자료이다."},
    {"id": 14, "rect": pygame.Rect(350, 110, 70, 70), "name": "나전 베갯모(조선후기)", "desc": "베개의 양쪽 끝을 장식하는 배겟모로 나전기법으로 만들어졌다. 나전 베갯모는 궁중이나 양반가에서 사용되던 것으로 특히 통영의 나전 베갯모가 유명했다."},
]


# 이동 포인트 설정
gate_to_special = pygame.Rect(190, 160, 21, 20)
gate_to_room1 = pygame.Rect(414, 65, 15, 30)
gate_to_room2 = pygame.Rect(211, 385, 15, 30)

exit_room1 = pygame.Rect(65, 370, 15, 30)
exit_room2 = pygame.Rect(560, 65, 15, 30)
exit_special = pygame.Rect(560, 65, 15, 30)

stairs_1f = pygame.Rect(320, 145, 48, 64)
stairs_2f = pygame.Rect(304, 209, 35, 65)

gate_to_minigame = pygame.Rect(128, 350, 17, 17)

gate_to_title = pygame.Rect(320, 478, 110, 1)


# 폰트 설정
font = pygame.font.SysFont("gulim", 24)
small_font = pygame.font.SysFont("gulim", 16)


# 게임 상태 변수
game_state = "title"

current_floor = 1
current_map = 0

player = pygame.Rect(365, 440, 32, 32)
speed = 4

show_info = False
selected_artifact = None


# 직소 퍼즐 미니게임 설정
PUZZLE_SIZE = 240
PUZZLE_GRID = 3
PIECE_SIZE = PUZZLE_SIZE // PUZZLE_GRID

# 왼쪽: 퍼즐을 맞추는 판 / 오른쪽: 조각이 랜덤으로 놓이는 구역
PUZZLE_BOARD_RECT = pygame.Rect(40, 120, PUZZLE_SIZE, PUZZLE_SIZE)
PIECE_AREA_RECT = pygame.Rect(340, 120, 240, 240)

puzzle_pieces = []
selected_piece = None
mouse_offset_x = 0
mouse_offset_y = 0
puzzle_clear = False


# 플레이어 이동 및 충돌 처리
def move_player(dx, dy, walls):
    player.x += dx

    for wall in walls:
        if player.colliderect(wall):
            if dx > 0:
                player.right = wall.left
            elif dx < 0:
                player.left = wall.right

    player.y += dy

    for wall in walls:
        if player.colliderect(wall):
            if dy > 0:
                player.bottom = wall.top
            elif dy < 0:
                player.top = wall.bottom


# 유물 관련 함수
def get_current_artifacts():
    if current_map == 1:
        return artifacts_room1
    elif current_map == 2:
        return artifacts_room2
    elif current_map == 3:
        return artifacts_special
    return []

def draw_artifacts(artifact_list):
    for artifact in artifact_list:
        img = artifact_images[artifact["id"]]
        screen.blit(img, artifact["rect"])

def get_artifact_walls():
    artifact_walls = []

    for artifact in get_current_artifacts():
        artifact_walls.append(artifact["rect"])

    return artifact_walls

def get_near_artifact():
    for artifact in get_current_artifacts():
        detect_rect = artifact["rect"].inflate(45, 45)

        if player.colliderect(detect_rect):
            return artifact

    return None


# 설명창 텍스트 줄바꿈 함수
def draw_text(surface, text, font, color, rect):

    lines = []

    for paragraph in text.split("\n"):

        words = paragraph.split(" ")
        current_line = ""

        for word in words:

            test_line = current_line + word + " "

            if font.size(test_line)[0] <= rect.width:
                current_line = test_line

            else:
                lines.append(current_line)
                current_line = word + " "

        lines.append(current_line)

    for i, line in enumerate(lines):

        text_surface = font.render(
            line,
            True,
            color
        )

        surface.blit(
            text_surface,
            (rect.x, rect.y + i * 22)
        )


# 유물 설명창 그리기
def draw_info_box(artifact):
    pygame.draw.rect(screen, (245, 245, 235), (40, 40, 560, 400))
    pygame.draw.rect(screen, (20, 20, 20), (40, 40, 560, 400), 4)

    title = font.render(artifact["name"], True, (0, 0, 0))
    close_text = small_font.render("E : 닫기", True, (80, 80, 80))

    img = artifact_images[artifact["id"]]
    big_img = pygame.transform.scale(img, (250, 250))

    screen.blit(title, (70, 70))
    screen.blit(big_img, (40, 120))
    screen.blit(close_text, (500, 390))

    draw_text(screen, artifact["desc"], small_font, (0, 0, 0), pygame.Rect(300, 120, 260, 250))



# 직소 퍼즐 관련 함수
def start_puzzle():
    global puzzle_pieces, puzzle_clear, selected_piece

    puzzle_pieces = []
    selected_piece = None
    puzzle_clear = False

    artifact_id = random.randint(1, 14)

    puzzle_img = pygame.image.load(
        os.path.join(BASE_DIR, f"artifact_{artifact_id}.png")
    ).convert_alpha()

    puzzle_img = pygame.transform.scale(
        puzzle_img,
        (PUZZLE_SIZE, PUZZLE_SIZE)
    )

    start_x = PUZZLE_BOARD_RECT.x
    start_y = PUZZLE_BOARD_RECT.y

    correct_positions = []

    for row in range(PUZZLE_GRID):
        for col in range(PUZZLE_GRID):
            correct_positions.append((
                start_x + col * PIECE_SIZE,
                start_y + row * PIECE_SIZE
            ))

    index = 0

    for row in range(PUZZLE_GRID):
        for col in range(PUZZLE_GRID):
            piece_img = puzzle_img.subsurface(
                col * PIECE_SIZE,
                row * PIECE_SIZE,
                PIECE_SIZE,
                PIECE_SIZE
            ).copy()

            random_x = random.randint(
                PIECE_AREA_RECT.left,
                PIECE_AREA_RECT.right - PIECE_SIZE
            )

            random_y = random.randint(
                PIECE_AREA_RECT.top,
                PIECE_AREA_RECT.bottom - PIECE_SIZE
            )

            piece = {
                "image": piece_img,
                "rect": pygame.Rect(
                    random_x,
                    random_y,
                    PIECE_SIZE,
                    PIECE_SIZE
                ),
                "correct_pos": correct_positions[index],
                "fixed": False
            }

            puzzle_pieces.append(piece)
            index += 1

def check_puzzle_clear():
    for piece in puzzle_pieces:
        if not piece["fixed"]:
            return False
    return True


def draw_puzzle_game():
    screen.fill((110, 75, 45))

    for y in range(0, HEIGHT, 30):
        pygame.draw.line(
            screen,
            (130, 90, 55),
            (0, y),
            (WIDTH, y),
            2
        )

    title = font.render("유물 복원 퍼즐", True, (255, 255, 255))
    guide = small_font.render("오른쪽 조각을 왼쪽 퍼즐판에 맞추세요", True, (255, 255, 255))
    exit_text = small_font.render("ESC : 박물관으로 돌아가기 | R : 다시하기", True, (255, 255, 255))

    screen.blit(title, (230, 35))
    screen.blit(guide, (170, 70))
    screen.blit(exit_text, (170, 430))

    board_text = small_font.render("퍼즐판", True, (255, 255, 255))
    piece_text = small_font.render("조각 보관함", True, (255, 255, 255))

    screen.blit(board_text, (120, 95))
    screen.blit(piece_text, (415, 95))

    pygame.draw.rect(
        screen,
        (210, 210, 210),
        PUZZLE_BOARD_RECT
    )

    pygame.draw.rect(
        screen,
        (30, 30, 30),
        PUZZLE_BOARD_RECT,
        3
    )

    for i in range(1, PUZZLE_GRID):
        x = PUZZLE_BOARD_RECT.x + i * PIECE_SIZE
        y = PUZZLE_BOARD_RECT.y + i * PIECE_SIZE

        pygame.draw.line(
            screen,
            (160, 160, 160),
            (x, PUZZLE_BOARD_RECT.y),
            (x, PUZZLE_BOARD_RECT.bottom),
            1
        )

        pygame.draw.line(
            screen,
            (160, 160, 160),
            (PUZZLE_BOARD_RECT.x, y),
            (PUZZLE_BOARD_RECT.right, y),
            1
        )

    pygame.draw.rect(
        screen,
        (180, 180, 180),
        PIECE_AREA_RECT
    )

    pygame.draw.rect(
        screen,
        (30, 30, 30),
        PIECE_AREA_RECT,
        3
    )

    for piece in puzzle_pieces:
        screen.blit(piece["image"], piece["rect"])

        if not puzzle_clear:
            if piece["fixed"]:
                pygame.draw.rect(screen, (0, 255, 0), piece["rect"], 2)
            else:
                pygame.draw.rect(screen, (255, 255, 255), piece["rect"], 1)

    if puzzle_clear:
        clear_text = font.render("복원 성공!", True, (255, 255, 0))
        screen.blit(clear_text, (250, 385))



# 메인 게임 루프
running = True

while running:
    clock.tick(60)

    near_artifact = get_near_artifact()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == "title":
                if event.key == pygame.K_RETURN:
                    game_state = "game"
                    current_map = 0
                    current_floor = 1
                    player.x = 365
                    player.y = 440
                    show_info = False
                    selected_artifact = None
                elif event.key == pygame.K_ESCAPE:
                    running = False

            elif current_map == 4 and event.key == pygame.K_ESCAPE:
                current_map = 0
                current_floor = 1
                player.x = 120
                player.y = 310
            if current_map == 4 and event.key == pygame.K_r:
                start_puzzle()
            if event.key == pygame.K_e:
                if show_info:
                    show_info = False
                    selected_artifact = None
                else:
                    if near_artifact is not None:
                        selected_artifact = near_artifact
                        show_info = True

        if current_map == 4:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()

                    for piece in reversed(puzzle_pieces):
                        if piece["rect"].collidepoint(mx, my) and not piece["fixed"]:
                            selected_piece = piece
                            mouse_offset_x = mx - piece["rect"].x
                            mouse_offset_y = my - piece["rect"].y
                            break

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and selected_piece is not None:
                    correct_x, correct_y = selected_piece["correct_pos"]

                    if abs(selected_piece["rect"].x - correct_x) < 20 and abs(selected_piece["rect"].y - correct_y) < 20:
                        selected_piece["rect"].x = correct_x
                        selected_piece["rect"].y = correct_y
                        selected_piece["fixed"] = True

                    selected_piece = None
                    puzzle_clear = check_puzzle_clear()

            elif event.type == pygame.MOUSEMOTION:
                if selected_piece is not None:
                    mx, my = pygame.mouse.get_pos()
                    selected_piece["rect"].x = mx - mouse_offset_x
                    selected_piece["rect"].y = my - mouse_offset_y

    if game_state == "title":
        screen.blit(title_bg, (0, 0))

        # 어두운 반투명 박스
        title_panel = pygame.Surface((500, 190))
        title_panel.set_alpha(170)
        title_panel.fill((0, 0, 0))
        screen.blit(title_panel, (70, 145))

        title_text = font.render("행소박물관 디지털 아카이브", True, (255, 255, 255))
        start_text = small_font.render("ENTER : 박물관에 입장하기 | ESC : 떠나기", True, (255, 255, 255))
        guide_text = small_font.render("유물을 관람하고 복원 퍼즐을 체험해보세요", True, (230, 230, 230))

        screen.blit(title_text, (170, 190))
        screen.blit(guide_text, (170, 240))
        screen.blit(start_text, (170, 285))

        pygame.display.update()
        continue

    keys = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if not show_info:
        if keys[pygame.K_a]:
            dx = -speed
            facing_right = False

        if keys[pygame.K_d]:
            dx = speed
            facing_right = True

        if keys[pygame.K_w]:
            dy = -speed

        if keys[pygame.K_s]:
            dy = speed

    is_moving = dx != 0 or dy != 0

    if is_moving:
        animation_timer += 1

        if animation_timer >= animation_speed:
            animation_timer = 0
            player_frame_index += 1

            if player_frame_index >= len(player_frames):
                player_frame_index = 0
    else:
        player_frame_index = 0

    if current_map == 0:
        if current_floor == 1:
            walls = walls_1f
            stairs = stairs_1f
        else:
            walls = walls_2f
            stairs = stairs_2f

    elif current_map == 1:
        walls = walls_room1
        stairs = None

    elif current_map == 2:
        walls = walls_room2
        stairs = None

    elif current_map == 3:
        walls = walls_special
        stairs = None

    elif current_map == 4:
        walls = []
        stairs = None

    if not show_info:
        artifact_walls = get_artifact_walls()
        all_walls = walls + artifact_walls
        move_player(dx, dy, all_walls)

    if not show_info:
        if current_map == 0:

            if current_floor == 1 and player.colliderect(gate_to_title):
                game_state = "title"
                current_map = 0
                current_floor = 1
                player.x = 365
                player.y = 440
                show_info = False
                selected_artifact = None

            elif player.colliderect(stairs):
                if current_floor == 1:
                    current_floor = 2
                    player.x = 305
                    player.y = 160
                else:
                    current_floor = 1
                    player.x = 330
                    player.y = 230

            elif current_floor == 1 and player.colliderect(gate_to_special):
                current_map = 3
                player.x = 525
                player.y = 400

            elif current_floor == 1 and player.colliderect(gate_to_minigame):
                current_map = 4
                start_puzzle()
                player.x = 320
                player.y = 240

            elif current_floor == 2 and player.colliderect(gate_to_room1):
                current_map = 1
                player.x = 90
                player.y = 40

            elif current_floor == 2 and player.colliderect(gate_to_room2):
                current_map = 2
                player.x = 525
                player.y = 400

        else:
            if current_map == 1 and player.colliderect(exit_room1):
                current_map = 0
                current_floor = 2
                player.x = 380
                player.y = 380

            elif current_map == 2 and player.colliderect(exit_room2):
                current_map = 0
                current_floor = 2
                player.x = 230
                player.y = 50

            elif current_map == 3 and player.colliderect(exit_special):
                current_map = 0
                current_floor = 1
                player.x = 270
                player.y = 155

    if current_map == 0:
        if current_floor == 1:
            screen.blit(map_1f, (0, 0))

            room_text = font.render("특별전시관", True, (0, 0, 0))
            screen.blit(room_text, (100, 90))

            room_text = font.render("미니게임", True, (0, 0, 0))
            screen.blit(room_text, (45, 400))

            room_text = small_font.render("나가는 길", True, (0, 0, 0))
            screen.blit(room_text, (345, 440))

        else:
            screen.blit(map_2f, (0, 0))

            room_text = font.render("제1전시관", True, (0, 0, 0))
            screen.blit(room_text, (480, 230))

            room_text = font.render("제2전시관", True, (0, 0, 0))
            screen.blit(room_text, (70, 230))

    elif current_map == 1:
        screen.blit(map_1, (0, 0))
        draw_artifacts(artifacts_room1)

    elif current_map == 2:
        screen.blit(map_2, (0, 0))
        draw_artifacts(artifacts_room2)

    elif current_map == 3:
        screen.blit(map_special, (0, 0))
        draw_artifacts(artifacts_special)

    elif current_map == 4:
        draw_puzzle_game()

    near_artifact = get_near_artifact()

    if near_artifact is not None and not show_info:
        guide_text = small_font.render("E : 조사하기", True, (0, 0, 0))
        screen.blit(
            guide_text,
            (near_artifact["rect"].x, near_artifact["rect"].y - 25)
        )

    if current_map != 4:
        current_sprite = player_frames[player_frame_index]

        if not facing_right:
            current_sprite = pygame.transform.flip(current_sprite, True, False)

        screen.blit(current_sprite, player)

        floor_text = font.render(f"{current_floor}F", True, (0, 0, 0))
        screen.blit(floor_text, (10, 10))

    if show_info and selected_artifact is not None:
        draw_info_box(selected_artifact)

    pygame.display.update()



pygame.quit()
sys.exit()