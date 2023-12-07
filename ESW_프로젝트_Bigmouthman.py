from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import numpy as np

class Joystick:
    def __init__(self):
        self.cs_pin = DigitalInOut(board.CE0)
        self.dc_pin = DigitalInOut(board.D25)
        self.reset_pin = DigitalInOut(board.D24)
        self.BAUDRATE = 24000000

        self.spi = board.SPI()
        self.disp = st7789.ST7789(
                    self.spi,
                    height=240,
                    y_offset=80,
                    rotation=180,
                    cs=self.cs_pin,
                    dc=self.dc_pin,
                    rst=self.reset_pin,
                    baudrate=self.BAUDRATE,
                    )

        # Input pins:
        self.button_A = DigitalInOut(board.D5)
        self.button_A.direction = Direction.INPUT

        self.button_B = DigitalInOut(board.D6)
        self.button_B.direction = Direction.INPUT

        self.button_L = DigitalInOut(board.D27)
        self.button_L.direction = Direction.INPUT

        self.button_R = DigitalInOut(board.D23)
        self.button_R.direction = Direction.INPUT

        self.button_U = DigitalInOut(board.D17)
        self.button_U.direction = Direction.INPUT

        self.button_D = DigitalInOut(board.D22)
        self.button_D.direction = Direction.INPUT

        self.button_C = DigitalInOut(board.D4)
        self.button_C.direction = Direction.INPUT

        # Turn on the Backlight
        self.backlight = DigitalInOut(board.D26)
        self.backlight.switch_to_output()
        self.backlight.value = True

        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for color.
        self.width = self.disp.width
        self.height = self.disp.height

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # 맵을 2D 배열로 초기화, 일단은 모든 부분이 이동 가능한 것으로 초기화
        self.grid = [[1] * width for _ in range(height)]
         # 추가: 맵의 배경을 그리기 위한 Draw 객체 생성
        self.background_image = Image.new('RGBA', (width * 20, height * 20))
        self.background_draw = ImageDraw.Draw(self.background_image)

    def set_obstacle(self, x, y):
        # (x, y) 좌표에 장애물을 설정 (이동 불가능한 영역으로 변경)
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = 0

class Enemy:
    def __init__(self, spawn_position):
        self.appearance = 'circle'
        self.state = 'alive'
        self.position = np.array([spawn_position[0] - 25/5, spawn_position[1] - 25/5, spawn_position[0] + 25/5, spawn_position[1] + 25/5])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.outline = "#00FF00"

class Character:
    def __init__(self, width, height, map_width, map_height, map_instance):
        self.appearance = 'mouthman'
        self.state = None
        self.map_width = map_width
        self.map_height = map_height
        self.map = map_instance
        self.position = np.array([0, 0, 20, 20])
        self.outline = "#FFFFFF"
        self.angle = 45  # 마우스맨이 향하는 각도

    def move(self, command = None):
        if command['move'] == False:
            self.state = None
            self.outline = "#FFFFFF"  # 검정색상 코드!
        else:
            self.state = 'move'
            self.outline = "#FF0000"  # 빨강색상 코드!


            if command['up_pressed']:
                # 위로 이동
                self.position[1] -= 5
                self.position[3] -= 5
                self.angle = 90  # 위쪽을 향하도록 설정
                if self.position[1] < 0:
                    # 경계에 닿았을 때 처리
                    self.position[1] = 0
                    self.position[3] = 20
                elif self.map.grid[int(self.position[1]//20)][int((self.position[0])//20)] == 0 or self.map.grid[int(self.position[1]//20)][int((self.position[2]-1)//20)] == 0:
                    # 이동하려는 위치에 장애물이 있으면 원래 위치로 되돌림
                    self.position[1] += 5
                    self.position[3] += 5
            

            if command['down_pressed']:
                # 아래로 이동
                self.position[1] += 5
                self.position[3] += 5
                self.angle = 270  # 아래쪽을 향하도록 설정
                if self.position[3] > self.map_height:
                    # 경계에 닿았을 때 처리
                    self.position[1] = self.map_height - 20
                    self.position[3] = self.map_height
                elif self.map.grid[int((self.position[3]-1)//20)][int((self.position[0]+1)//20)] == 0 or self.map.grid[int((self.position[3]-1)//20)][int((self.position[2]-1)//20)] == 0:
                    # 이동하려는 위치에 장애물이 있으면 원래 위치로 되돌림
                    self.position[1] -= 5
                    self.position[3] -= 5
                    if not joystick.button_A.value: #A누르면 필살기: 속도 상승 및 벽 뚫기용
                        self.position[1] += 10
                        self.position[3] += 10
                
            if command['left_pressed'] and not command['up_pressed'] and not command['down_pressed']:
                # 왼쪽으로 이동
                self.position[0] -= 5
                self.position[2] -= 5
                self.angle = 0  # 왼쪽을 향하도록 설정
                if self.position[0] < 0:
                    # 경계에 닿았을 때 처리
                    self.position[0] = 0
                    self.position[2] = 20
                elif self.map.grid[int((self.position[1]+1)//20)][int(self.position[0]//20)] == 0 or self.map.grid[int((self.position[3]-1)//20)][int(self.position[0]//20)] == 0:
                    # 이동하려는 위치에 장애물이 있으면 원래 위치로 되돌림
                    self.position[0] += 5
                    self.position[2] += 5
                
            if command['right_pressed'] and not command['up_pressed'] and not command['down_pressed']:
                # 오른쪽으로 이동
                self.position[0] += 5
                self.position[2] += 5
                self.angle = 180  # 오른쪽을 향하도록 설정
                if self.position[2] > self.map_width:
                    # 경계에 닿았을 때 처리
                    self.position[0] = self.map_width - 20
                    self.position[2] = self.map_width
                elif self.map.grid[int((self.position[1]+1)//20)][int((self.position[2]-1)//20)] == 0 or self.map.grid[int((self.position[3]-1)//20)][int((self.position[2]-1)//20)] == 0:
                    # 이동하려는 위치에 장애물이 있으면 원래 위치로 되돌림
                    self.position[0] -= 5
                    self.position[2] -= 5


    def collision_check(self, enemys):
        for enemy in enemys:
            collision = self.overlap(self.position, enemy.position)
            
            if collision:
                enemy.state = 'die'
                self.state = 'hit'

    def overlap(self, ego_position, other_position):

        return ego_position[0] < other_position[0] and ego_position[1] < other_position[1] \
                 and ego_position[2] > other_position[2] and ego_position[3] > other_position[3]

            
joystick = Joystick()
my_image = Image.new("RGB", (joystick.width, joystick.height)) #도화지!
my_draw = ImageDraw.Draw(my_image) #그리는 도구!

# 맵 크기 정의
map_width = joystick.width
map_height = joystick.height
# (2, 3) 좌표에 장애물을 설정 (이동 불가능한 영역으로 변경)
game_map = Map(map_width, map_height)
game_map.set_obstacle(1, 1)
game_map.set_obstacle(1, 2)
game_map.set_obstacle(1, 3)
game_map.set_obstacle(1, 4)
game_map.set_obstacle(1, 5)
game_map.set_obstacle(1, 7)
game_map.set_obstacle(1, 8)
game_map.set_obstacle(2, 5)
game_map.set_obstacle(3, 5)
game_map.set_obstacle(1, 10)
game_map.set_obstacle(3, 1)
game_map.set_obstacle(3, 2)
game_map.set_obstacle(3, 3)
game_map.set_obstacle(5, 1)
game_map.set_obstacle(5, 2)
game_map.set_obstacle(5, 3)
game_map.set_obstacle(5, 5)
game_map.set_obstacle(5, 6)
game_map.set_obstacle(5, 7)
game_map.set_obstacle(5, 8)
game_map.set_obstacle(3, 7)
game_map.set_obstacle(3, 8)
game_map.set_obstacle(3, 9)
game_map.set_obstacle(3, 10)
game_map.set_obstacle(4, 10)
game_map.set_obstacle(5, 10)
game_map.set_obstacle(6, 10)
game_map.set_obstacle(7, 0)
game_map.set_obstacle(7, 1)
game_map.set_obstacle(7, 3)
game_map.set_obstacle(7, 4)
game_map.set_obstacle(7, 5)
game_map.set_obstacle(7, 6)
game_map.set_obstacle(7, 8)
game_map.set_obstacle(7, 9)
game_map.set_obstacle(7, 10)
game_map.set_obstacle(9, 1)
game_map.set_obstacle(10, 1)
game_map.set_obstacle(8, 3)
game_map.set_obstacle(9, 3)
game_map.set_obstacle(10, 3)
game_map.set_obstacle(11, 3)
game_map.set_obstacle(9, 5)
game_map.set_obstacle(10, 5)
game_map.set_obstacle(9, 6)
game_map.set_obstacle(10, 6)
game_map.set_obstacle(9, 7)
game_map.set_obstacle(10, 7)
game_map.set_obstacle(9, 9)
game_map.set_obstacle(10, 9)
game_map.set_obstacle(9, 10)
game_map.set_obstacle(10, 10)

enemy_1 = Enemy((50, 50))
enemy_2 = Enemy((230, 230))
enemy_3 = Enemy((150, 50))

enemys_list = [enemy_1, enemy_2, enemy_3]


# Character 클래스 생성 시 맵 크기 전달
my_mouthman = Character(joystick.width, joystick.height, map_width, map_height, game_map)
my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))

while True:

    if not joystick.button_U.value:  # up pressed
        command = {'move': True, 'up_pressed': True , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}

    if not joystick.button_D.value:  # down pressed
        command = {'move': True, 'up_pressed': False , 'down_pressed': True, 'left_pressed': False, 'right_pressed': False}

    if not joystick.button_L.value:  # left pressed
        command = {'move': True, 'up_pressed': False , 'down_pressed': False, 'left_pressed': True, 'right_pressed': False}

    if not joystick.button_R.value:  # right pressed
        command = {'move': True, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': True}

    my_mouthman.move(command)
    my_mouthman.collision_check(enemys_list)

    
    #그리는 순서가 중요합니다. 배경을 먼저 깔고 위에 그림을 그리고 싶었는데 그림을 그려놓고 배경으로 덮는 결과로 될 수 있습니다.
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
    # Draw obstacles
    for y in range(map_height):
        for x in range(map_width):
            if game_map.grid[y][x] == 0:
                my_draw.rectangle((x * 20, y * 20, (x + 1) * 20, (y + 1) * 20), fill=(0, 0, 0))
    my_draw.pieslice(tuple(my_mouthman.position), my_mouthman.angle-135, my_mouthman.angle+135, outline=my_mouthman.outline, fill=(255, 255, 0))

    for enemy in enemys_list:
        if enemy.state != 'die':
            my_draw.ellipse(tuple(enemy.position), outline = enemy.outline, fill = (255, 0, 0))

    #좌표는 동그라미의 왼쪽 위, 오른쪽 아래 점 (x1, y1, x2, y2)
    joystick.disp.image(my_image)

