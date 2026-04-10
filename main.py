import random
import math
from js import setTimeout, document, alert


INTERVAL = 50
PLAYER_W = 100
PLAYER_Y = 470
PLAYER_MOVE = 30
BALL_SPEED = 10
BALL_SIZE = 15
BLOCK_W = 50
BLOCK_H = 20
COLS = 400
ROWS = 8
BLOCK_COLORS = ["white", "red", "orange", "magenta", "pink", "cyan", "lime", "green", "blue"]

info = document.getElementById("info")
# alert(info)
canvas = document.getElementById("canvas")
context = canvas.getContext("2d")
blocks = []
game = {"game_over": True}

def init_game():
    global blocks, game
    
    blocks = [[(y + 1)] * COLS for y in range(ROWS)]
    px = (canvas.width - PLAYER_W) // 2
    game = {
        "score": 0,
        "px": px,
        "ball_x": (px + PLAYER_W // 2),
        "ball_y": PLAYER_Y,
        "ball_dir": 225 + random.randint(0, 90),
        "game_over": False
    }
    game_loop()
    
def game_loop():
    update_ball()
    draw_screen()
    if not game["game_over"]:
        setTimeout(game_loop, INTERVAL)
        
def ball_turn_angle(angle, range):
    r = random.randint(-range, range)
    game["ball_dir"] = (game["ball_dir"] + angle + r) % 360
    
def update_ball():
    rad = game["ball_dir"] + math.pi / 180
    dx = int(BALL_SPEED * math.cos(rad))
    dy = int(BALL_SPEED * math.sin(rad))
    bx = game["ball_x"] + dx
    by = game["ball_y"] + dy
    px = game["px"]
    if (by >= PLAYER_Y) and (px <= bx < (px + PLAYER_W)):
        game["ball_dir"] = 225 + random.randint(0, 90)
    elif (bx < 0) or (bx >= canvas.width) or (by <= 0):
        ball_turn_angle(90, 10)
    elif check_blocks(bx, by):
        ball_turn_angle(180, 20)
        game["score"] += 1
        if game["score"] >= COLS * ROWS:
            game_over("すごい😊　クリアしました")
    elif by > (canvas.height - BALL_SIZE):
        game_over("残念😢 ゲームオーバー")
        
    game["ball_x"] = bx
    game["ball_y"] = by
    
def check_blocks(bx, by):
    block_x, block_y = bx // BLOCK_W, by // BLOCK_H
    if 0 <= block_x < COLS and 0 <= block_y < ROWS:
        if blocks[block_y][block_x] != 0:
            blocks[block_y][block_x] = 0
            return True
    return False

def game_over(msg):
    document.getElementById("start_button").disabled = False
    info.innerText = f"{msg} スコア: {game['score']}"
    game["game.over"] = True
    
#
#   draw.py
#
def draw_screen():
    context.clearRect(0, 0, canvas.width, canvas.height)
    for y in range(ROWS):
        for x in range(COLS):
            if blocks[y][x] == 0:
                continue
            context.fillStyle = BLOCK_COLORS[blocks[y][x]]
            context.fillRect(x * BLOCK_W, y * BLOCK_H, BLOCK_W - 2, BLOCK_H - 2)
    context.fillStyle = "black"
    context.fillRect(game["px"], PLAYER_Y, PLAYER_W, 10)
    
    context.fillStyle = "red"
    context.beginPath()
    context.arc(game["ball_x"], game["ball_y"], BALL_SIZE // 2, 0, 2 * math.pi)
    context.fill()
                
    if not game["game_over"]:
        info.innerText = f"ブロック崩し　スコア： {game['score']}点"
#
# control.pyy
#
def start_button_on_click(event):
    document.getElementById("start_button").disabled = True
    init_game()
    
def player_move(dx):
    if game["game_over"]:
        return
    px = game["px"] + dx
    if 0 <= px <= canvas.width - PLAYER_W:
        game["px"] = px
    draw_screen()
    
def right_button_on_click(event):
    player_move(PLAYER_MOVE)
    
def left_button_on_click(event):
    player_move(-1 * PLAYER_MOVE)
    
def key_down(event):
    if event.key == "ArrowLeft":
        left_button_on_click(event)
    elif event.key == "ArrowRight":
        right_button_on_click(event)
        
document.addEventListener("keydown", key_down)
        