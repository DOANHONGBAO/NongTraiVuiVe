import pygame

ROWS, COLS = 8, 8
BOARD_SIZE = 400  # Bàn cờ nhỏ hơn màn hình
SQUARE_SIZE = BOARD_SIZE // COLS

WHITE = (245, 245, 220)
BLACK = (139, 69, 19)

def load_images():
    pieces = ['wp', 'bp', 'wr', 'br', 'wn', 'bn', 'wb', 'bb', 'wq', 'bq', 'wk', 'bk']
    images = {}
    for piece in pieces:
        images[piece] = pygame.transform.scale(
            pygame.image.load(f'assets/chess/{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE)
        )
    return images

def create_board():
    return [
        ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
        ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
    ]

def draw_board(surface, top_left):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            rect = pygame.Rect(
                top_left[0] + col * SQUARE_SIZE,
                top_left[1] + row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE
            )
            pygame.draw.rect(surface, color, rect)

def draw_pieces(surface, board, images, top_left):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != '--':
                surface.blit(
                    images[piece],
                    (top_left[0] + col * SQUARE_SIZE, top_left[1] + row * SQUARE_SIZE)
                )

def check_game_over(board):
    flat_board = sum(board, [])
    if 'bk' not in flat_board:
        return 'white'
    if 'wk' not in flat_board:
        return 'black'
    return None

def start_chess_battle_overlay(screen):
    images = load_images()
    board = create_board()

    selected = None
    turn = 'w'  # Player: trắng

    clock = pygame.time.Clock()
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Màu đen mờ, alpha = 180

    screen_rect = screen.get_rect()
    board_top_left = (
        screen_rect.centerx - BOARD_SIZE // 2,
        screen_rect.centery - BOARD_SIZE // 2
    )

    running = True
    while running:
        clock.tick(30)

        # VẼ lớp gameplay bên dưới screen (không xóa gì hết)

        # VẼ lớp phủ mờ
        screen.blit(overlay, (0, 0))

        # VẼ bàn cờ
        draw_board(screen, board_top_left)
        draw_pieces(screen, board, images, board_top_left)

        pygame.display.update()

        result = check_game_over(board)
        if result:
            pygame.time.delay(500)
            return result == 'white'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos
                bx, by = board_top_left

                if bx <= x < bx + BOARD_SIZE and by <= y < by + BOARD_SIZE:
                    col = (x - bx) // SQUARE_SIZE
                    row = (y - by) // SQUARE_SIZE

                    if selected:
                        start_row, start_col = selected
                        piece = board[start_row][start_col]
                        if piece.startswith(turn):
                            board[row][col] = board[start_row][start_col]
                            board[start_row][start_col] = "--"
                            turn = 'b'
                        selected = None
                    else:
                        if board[row][col] != '--' and board[row][col][0] == turn:
                            selected = (row, col)

        if turn == 'b':
            # Bot: tìm quân đen và đi ngẫu nhiên
            move_made = False
            for r in range(ROWS):
                for c in range(COLS):
                    if board[r][c].startswith('b'):
                        directions = [(-1,0), (1,0), (0,-1), (0,1)]
                        for dr, dc in directions:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < ROWS and 0 <= nc < COLS:
                                if board[nr][nc] == '--' or board[nr][nc][0] == 'w':
                                    board[nr][nc] = board[r][c]
                                    board[r][c] = '--'
                                    turn = 'w'
                                    move_made = True
                                    break
                        if move_made:
                            break
